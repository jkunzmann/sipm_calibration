# ///////////////////////////////////////////////////////////////// //
#                                                                   //
# Last modifications: 10.05.2024 by Jan Kunzmann, University of Bern//
#                                                                   //
# ///////////////////////////////////////////////////////////////// //

from run_calibration_conv_and_combining import calib
from compare_gains import compare_gains
import concurrent.futures
from functools import partial
import os
import shutil

def create_folder(folder_name):
    """
    Creates a folder with the specified name.
    
    Args:
    folder_name (str): The name of the folder to be created.
    
    Returns:
    str: The path of the created folder.
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def remove_folder(folder_path):
    """
    Removes the specified folder and all its contents.
    
    Args:
    folder_path (str): The path of the folder to be removed.
    
    Returns:
    bool: True if the folder was successfully removed, False if the folder does not exist.
    """
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

def copy_file_to_folder(file_path, folder_path):
    """
    Copies the specified file to the specified folder.
    
    Args:
    file_path (str): The path of the file to be copied.
    folder_path (str): The path of the folder where the file will be copied.
    
    Returns:
    str: The path of the copied file in the folder.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    if not os.path.exists(folder_path):
        raise NotADirectoryError(f"The folder {folder_path} does not exist.")
    
    file_name = os.path.basename(file_path)
    destination_path = os.path.join(folder_path, file_name)
    shutil.copy(file_path, destination_path)



def process_entry(entry, calib_name, AFI_viewer, calib_path, output_file_name, json_data):

    #data_path = entry.get("calib_run").rsplit('/',1)[:-1][0]+"/" #path to the *.data file
    data_path = "/home/jan/Universitat_Bern/Doktor/ADC_Viewer/" #path to the *.data file
    data_name = entry.get("calib_run").rsplit('/')[-1] #name of the *.data file

    create_folder(data_path+data_name[:-5])
    copy_file_to_folder(data_path+data_name, data_path+data_name[:-5])

    data_path = data_path+data_name[:-5]+"/"

    fitlog_path = data_path+"/fitlog"

    folder_path = "/home/jan/Universitat_Bern/Doktor/ADC_Viewer/2x2/sipm_calibration/"+calib_name+"/"
    ascii_file_name = calib_name+"_"+data_name[:-5]+"_ascii_fitlog"

    #print(data_path)
    print(data_name)

    
    # Run the calibration function
    calib.run_ADC_viewer(AFI_viewer, data_path+data_name)
    calib.move_folder(fitlog_path, calib_path, calib_name)
    calib.rename_folder_and_files(calib_path+calib_name+"/fitlog", calib_path+calib_name, calib_name+"_"+data_name[:-5])

    # Work on the file
    existing_data = compare_gains.process_files(calib_path+calib_name+"/", ascii_file_name, output_file_name, json_data, data_name)

    print("The generated file is called: " + output_file_name)
    # Save the data
    compare_gains.save_data(existing_data, calib_path+calib_name+"/"+output_file_name)
    
    print("REMOVE: "+ data_path)
    #remove_folder(data_path)
    


if __name__ == "__main__":
    AFI_viewer = "/home/jan/Universitat_Bern/Doktor/ADC_Viewer/AFIViewer_Bern/AFIViewer/build/ADC64Viewer"
    #fitlog_path = "/home/jan/Universitat_Bern/Doktor/ADC_Viewer/fitlog"
    
    #####only input needed: json file!!
    #json_path = "/home/jan/Universitat_Bern/Doktor/ADC_Viewer/2x2/sipm_calibration/2024.05.08.14.59.25.json"
    json_path = "/home/jan/Universitat_Bern/Doktor/ADC_Viewer/2x2/sipm_calibration/"
    
    js = input("Give it the json file name only (inc. .json): ")
    json_path = json_path + js

    json_data = compare_gains.read_json_file(json_path)

    #select where to safe the calibrated data
    calib_path = "/home/jan/Universitat_Bern/Doktor/ADC_Viewer/2x2/sipm_calibration/"
    calib_name= json_path.split('/')[-1][:-5] #takes the same name as the json file
    print("Calibration run: "+calib_name)
    output_file_name = calib_name+"_calibration"

    """
    for entry in json_data:
        process_entry(entry, calib_name, AFI_viewer, calib_path, output_file_name, json_data)
    """

    # Create a partial function with the fixed arguments
    partial_process_entry = partial(process_entry, calib_name=calib_name, AFI_viewer=AFI_viewer, calib_path=calib_path, 
                                    output_file_name=output_file_name, json_data=json_data)

    #with concurrent.futures.ThreadPoolExecutor() as executor:
    #    futures = [executor.submit(partial_process_entry, entry) for entry in json_data]
    #    for future in concurrent.futures.as_completed(futures):
    #        try:
    #            future.result()
    #        except Exception as exc:
    #            print(f'Generated an exception: {exc}')

    # If the tasks are CPU-bound, use ProcessPoolExecutor instead
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(partial_process_entry, entry) for entry in json_data]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                print(f'Generated an exception: {exc}')
