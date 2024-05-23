# ///////////////////////////////////////////////////////////////// //
#                                                                   //
# Last modifications: 10.05.2024 by Jan Kunzmann, University of Bern//
#                                                                   //
# ///////////////////////////////////////////////////////////////// //

from run_calibration_conv_and_combining import calib
from compare_gains import compare_gains


if __name__ == "__main__":
    AFI_viewer = "/home/jan/Universitat_Bern/Doktor/ADC_Viewer/AFIViewer/build/ADC64Viewer"
    fitlog_path = "/home/jan/Universitat_Bern/Doktor/ADC_Viewer/fitlog"
    
    #####only input needed: json file!!
    json_path = "/home/jan/Universitat_Bern/Doktor/ADC_Viewer/2x2/sipm_calibration/2024.05.08.14.59.25.json"
    
    json_data = compare_gains.read_json_file(json_path)

    #select where to safe the calibrated data
    calib_path = "/home/jan/Universitat_Bern/Doktor/ADC_Viewer/2x2/sipm_calibration/"
    calib_name= json_path.split('/')[-1][:-5] #takes the same name as the json file
    print("Calibration run: "+calib_name)
    output_file_name = calib_name+"_calibration"

    for entry in json_data:
        data_path = entry.get("calib_run").rsplit('/',1)[:-1][0]+"/" #path to the *.data file
        data_name = entry.get("calib_run").rsplit('/')[-1] #name of the *.data file
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