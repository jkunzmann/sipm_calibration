import json
import shutil
import os
import csv

class collect_plots:    
    def select_channel_by_JSON_file(channel_name, json_data, data_name):
        for entry in json_data:
            if (data_name == entry.get("calib_run").rsplit('/')[-1]): #name of the *.data file
                json_adc = entry.get("adc_serials")
                #print(json_adc)
                local_json_ch = entry.get("local_channels")
                for i in range(len(json_adc)):
                    #print(json_adc[i][1:].lower())
                    if(channel_name == 'ChargeLight_'+json_adc[i][1:].lower()+'_ch'+local_json_ch[i] or channel_name == 'ChargeLight_'+json_adc[i][4:].lower()+'_ch'+local_json_ch[i]):
                        #print("TRUE")
                        return True
                    #else:
                    #    print("FALSE: CH_name" +channel_name +" json name: "+'ChargeLight_'+json_adc[i][1:].lower()+'_ch'+local_json_ch[i])
            
        return False

    def file_exists(filepath):
        """
        Check if a file exists at the specified filepath.

        :param filepath: The path to the file
        :return: True if the file exists, False otherwise
        """
        return os.path.isfile(filepath)


    
    def copy_file(source, destination):
        """
        Copy a file from the source location to the destination.

        :param source: The path to the source file
        :param destination: The path to the destination
        """
        try:
            shutil.copy2(source, destination)
            print(f"File '{source}' copied to '{destination}' successfully.")
        except FileNotFoundError:
            print(f"Source file '{source}' not found.")
        except PermissionError:
            print(f"Permission denied while copying '{source}' to '{destination}'.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def create_directory(directory_name):
        """
        Create a directory with the given name.

        :param directory_name: The name of the directory to be created
        """
        try:
            os.makedirs(directory_name)
            print(f"Directory '{directory_name}' created successfully.")
        except FileExistsError:
            print(f"Directory '{directory_name}' already exists.")
        except Exception as e:
            print(f"An error occurred: {e}")



    def read_json_file(file_path):
        """
        Read data from a JSON file.
        
        Args:
        - file_path (str): The path to the JSON file.
        
        Returns:
        - data (dict): The data read from the JSON file.
        """
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error: File '{file_path}' is not a valid JSON file.")
            return None

class gains_collection:
    def read_calib_file(filename):
        """
        Read the contents of the file and return it as a list of lines.
        """
        with open(filename, 'r') as file:
            lines = file.readlines()
        return lines

    def write_rows(lines, csv_filename):
        """
        Print each row from the list of lines.
        """
        with open(csv_filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            # Write a header
            csv_writer.writerow(['sn','ch','gain','sigma'])
        
            for line in lines:
                parts = line.strip().split(', ')
                csv_writer.writerow([parts[3], parts[5], parts[23], parts[25]])


if __name__ == "__main__":
    #give the json file path with the file name
    json_path = "/home/jan/Universitat_Bern/Doktor/ADC_Viewer/2x2/"

    js = input("Give it the json file name only (inc. .json): ")
    json_path = json_path + js

    json_data = collect_plots.read_json_file(json_path)

    calib_name= json_path.split('/')[-1][:-5] #takes the same name as the json file

    #location of the plots
    plot_path = "/home/jan/Universitat_Bern/Doktor/ADC_Viewer/2x2/"

    #print(calib_name)
    plot_collection_path = plot_path+calib_name+"/plot_collection"
    collect_plots.create_directory(plot_collection_path)
    
    for entry in json_data:
        calib_run_name = entry.get("calib_run").split("/")[-1][:-5]

        json_adc = entry.get("adc_serials")

        local_json_ch = entry.get("local_channels")
        for i in range(len(json_adc)):
            #print(json_adc[i][1:].lower())
            #print(local_json_ch[i])
            file_name1 = plot_path+calib_name+"/"+calib_name+"_"+calib_run_name+"/FIT_ChargeLight_"+json_adc[i][1:].lower()+"_ch"+local_json_ch[i].zfill(2)+"_"+calib_run_name+".data.png"
            file_name2 = plot_path+calib_name+"/"+calib_name+"_"+calib_run_name+"/FIT_ChargeLight_"+json_adc[i][4:].lower()+"_ch"+local_json_ch[i].zfill(2)+"_"+calib_run_name+".data.png"

            if(collect_plots.file_exists(file_name1)):
                collect_plots.copy_file(file_name1,plot_collection_path)
            elif(collect_plots.file_exists(file_name2)):
                collect_plots.copy_file(file_name2,plot_collection_path)
            else:
                print("This figure does not exist!!")
    

    calib_file_path = plot_path+calib_name+"/"+calib_name+"_calibration"
    rows= gains_collection.read_calib_file(calib_file_path)
    gains_collection.write_rows(rows, plot_path+calib_name+"/"+calib_name+"_calibration.csv")
    print("Calibration csv file was created here: "+plot_path+calib_name+"/"+calib_name+"_calibration.csv")
    
    
