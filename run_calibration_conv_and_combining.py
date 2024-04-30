import subprocess
import os
import shutil

def run_ADC_viewer(AFI_Viewer_path, data_path):
    """
    Run the ADC64Viewer script with specified arguments.

    AFI_Viewer_path (str): path to the AFI Viewer
    data_path (str): path to the data (*.data)

    """
    command = [AFI_Viewer_path,
               "-g", "0",
               "-f", data_path,
               "-m", "i",
               "-s"]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("Error: The ADC64Viewer script failed to run.")
        print(e)


def move_folder(fitlog_path, data_path, calib_name):
    """
    moves the fitlog folder (fitlog_path) to the folder calib_name at data_path
    """
    try:
        # Check if the folder to move exists
        if not os.path.exists(fitlog_path):
            print("Error: The folder to move does not exist.")
            return

        # Create the destination folder if it doesn't exist
        if not os.path.exists(data_path):
            os.makedirs(data_path)

        # Check if the calib_name folder already exists in the data_path
        calib_path = os.path.join(data_path, calib_name)
        if not os.path.exists(calib_path):
            os.makedirs(calib_path)  # Create the calib_name folder if it doesn't exist

        # Move the fitlog_path folder to the data_path with the calib_name
        shutil.move(fitlog_path, calib_path)
        print(f"Successfully moved '{fitlog_path}' to '{calib_path}'.")
    except Exception as e:
        print("Error:", e)
    
def rename_folder_and_files(folder_path, new_folder_path, new_folder_name):
    """
    Renames the fitlog folder full path (folder_path), to the name of the new_folder_name at the new_folder_path
    And then moves everything but png out of this folder to the new_folder_path
    Possibility: Remove png and folder
    """
    try:
        # Rename the folder to the new name
        os.rename(folder_path, new_folder_path+"/"+new_folder_name)

        # Rename each file inside the folder
        for filename in os.listdir(new_folder_path+"/"+new_folder_name):
            if os.path.isfile(os.path.join(new_folder_path+"/"+new_folder_name, filename)):
                if not filename.endswith(".png"):
                    new_filename = new_folder_name + "_" + filename  # Add new_folder_name to the beginning of the filename
                    os.rename(os.path.join(new_folder_path+"/"+new_folder_name, filename), os.path.join(new_folder_path+"/"+new_folder_name, new_filename))

        for filename2 in os.listdir(new_folder_path+"/"+new_folder_name):
            if not filename2.endswith(".png"):
                #print(new_folder_path+"/"+new_folder_name+"/"+filename2)
                # Move the file to the parent folder (new_folder_path)
                shutil.move(os.path.join(new_folder_path, new_folder_name, filename2), new_folder_path)
                print(f"Successfully moved '{filename2}' to '{new_folder_path}'.")
            
            """
            if filename2.endswith(".png"):
                print(new_folder_path+"/"+new_folder_name+"/"+filename2)
                os.remove(new_folder_path+"/"+new_folder_name+"/"+filename2)
            
        #print(new_folder_path+"/"+new_folder_name+"/")
        os.rmdir(new_folder_path+"/"+new_folder_name)
        """    

        print(f"Successfully renamed '{folder_path}' and its contents to '{new_folder_name}'.")
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    AFI_viewer = "/home/jan/Universitat_Bern/Doktor/ADC_Viewer/AFIViewer/build/ADC64Viewer"
    data_path = "/home/jan/Universitat_Bern/Doktor/ADC_Viewer/"
    data_name = "mpd_run_god_013.data"
    fitlog_path = "/home/jan/Universitat_Bern/Doktor/ADC_Viewer/fitlog"
    calib_path = "/home/jan/Universitat_Bern/Doktor/ADC_Viewer/2x2/sipm_calibration/"
    calib_name= "test1"

    # Run the function
    run_ADC_viewer(AFI_viewer, data_path+data_name)
    move_folder(fitlog_path, calib_path, calib_name)
    rename_folder_and_files(calib_path+calib_name+"/fitlog", calib_path+calib_name, data_name[:-5])

