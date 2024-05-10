# ///////////////////////////////////////////////////////////////// //
#                                                                   //
# Last modifications: 10.05.2024 by Jan Kunzmann, University of Bern//
#                                                                   //
# ///////////////////////////////////////////////////////////////// //

import os
import json


class compare_gains:
    def read_data(file_name):
        data = []
        if not os.path.exists(file_name):
            # if data does not exist, create an empty one
            with open(file_name, 'w') as new_file:
                pass  # empty object created
        with open(file_name, 'r') as file:
            lines = file.readlines()
            # jump the first line
            for line in lines[1:]:
                values = line.strip().split(', ')
                # for value in values:
                #     print(value)
                data.append(values)
        return data

    def read_data_spreadsheet(file_name):
        data = []
        if not os.path.exists(file_name):
            # if data does not exist, create an empty one
            with open(file_name, 'w') as new_file:
                pass  # empty object created
        with open(file_name, 'r') as file:
            lines = file.readlines()
            # jump the first line
            for line in lines[1:]:
                values = line.strip().split(',')
                # for value in values:
                #     print(value)
                data.append(values)
        return data

    def read_data_existing(file_name):
        data = []
        if not os.path.exists(file_name):
            # if data does not exist, create an empty one
            with open(file_name, 'w') as new_file:
                pass  # empty object created
        with open(file_name, 'r') as file:
            lines = file.readlines()
            # jump the first line
            for line in lines[:]:
                values = line.strip().split(', ')
                # for value in values:
                #     print(value)
                data.append(values)
        return data

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


    def select_channel_by_Mother_of_Spreadsheet(calib_ID_number, channel_name, Mother_of_Spreadsheet_name):
        spreadsheet = read_data_spreadsheet(Mother_of_Spreadsheet_name)
        
        for sublist in spreadsheet:
            spreadsheet_calib_ID = sublist[-1]
            spreadsheet_adc = sublist[3][1:].lower()
            spreadsheet_ch = sublist[5]
            if int(spreadsheet_ch) < 10:
                spreadsheet_ch = str(spreadsheet_ch).zfill(2)

            if(calib_ID_number == spreadsheet_calib_ID and channel_name == 'ChargeLight_'+spreadsheet_adc+'_ch'+spreadsheet_ch):
                return True
            else:
                return False

    def select_channel_by_JSON_file(channel_name, json_data):
        for entry in json_data:
            json_adc = entry.get("adc_serials")
            #print(json_adc)
            local_json_ch = entry.get("local_channels")
            for i in range(len(json_adc)):
                #print(json_adc[i][1:].lower())
                if(channel_name == 'ChargeLight_'+json_adc[i][1:].lower()+'_ch'+local_json_ch[i]):
                    #print("TRUE")
                    return True
                #else:
                #    print("FALSE: CH_name" +channel_name +" json name: "+'ChargeLight_'+json_adc[i][1:].lower()+'_ch'+local_json_ch[i])
            
        return False

    def update_existing_data_w_chi(existing_data, new_data):
        #appended = False  # Variable to track if a line has been appended
        # Convert existing_data to a dictionary where the name is the key
        existing_data_dict = {item[1]: (item, item[-1].split(' ')[0]) for item in existing_data}
        
        for values in new_data:
            name = values[1]  # The name is on the second position of the line
            chi = float(values[-1].split(' ')[0])
            #print("chi: ", chi)
            #print("name: ", name)
            if 0.9 <= chi <= 1.1:
                if name in existing_data_dict and abs(float(existing_data_dict[name][-1]) - 1) > abs(float(chi) - 1):
                    print("Value better than existing, old value: ", existing_data_dict[name][-1],"new value: ", chi)
                    existing_data_dict[name] = (values, chi)
                elif name not in existing_data_dict:
                    print("Name doesn't exist yet and chi is good, appended to the end")
                    existing_data_dict[name] = (values, chi)
            else:
                if name not in existing_data_dict:
                    print("Name not present yet, chi not good, appending line to end")
                    existing_data_dict[name] = (values, -1)  # Set chi value to -1 as it's out of the acceptable range
                    #appended = True  # Mark that a line has been appended
                else:
                    print("Line existis or is better in chi")
                
        return existing_data_dict

    def update_existing_data_w_Mother_of_spreadsheet(existing_data, new_data):
        #appended = False  # Variable to track if a line has been appended
        # Convert existing_data to a dictionary where the name is the key
        existing_data_dict = {item[1]: (item, item[-1].split(' ')[0]) for item in existing_data}
        
        for values in new_data:
            name = values[1]  # The name is on the second position of the line
            chi = float(values[-1].split(' ')[0])
            
            #print("name: ", name)
            if compare_gains.select_channel_by_Mother_of_Spreadsheet(calib_ID_number, channel_name, Mother_of_Spreadsheet_name) == True:
                if name in existing_data_dict and abs(float(existing_data_dict[name][-1]) - 1) > abs(float(chi) - 1):
                    print("Value better than existing, old value: ", existing_data_dict[name][-1],"new value: ", chi)
                    existing_data_dict[name] = (values, chi)
                elif name not in existing_data_dict:
                    print("Name doesn't exist yet and chi is good, appended to the end")
                    existing_data_dict[name] = (values, chi)
            else:
                print("Line is not needed from this fiel for this channel calibration (Channel Calib wrong)")
                
        return existing_data_dict

    def update_existing_data_w_json(existing_data, new_data, json_data):
        #appended = False  # Variable to track if a line has been appended
        # Convert existing_data to a dictionary where the name is the key
        existing_data_dict = {item[1]: (item, item[-1].split(' ')[0]) for item in existing_data}
        
        for values in new_data:
            name = values[1]  # The name is on the second position of the line
            chi = float(values[-1].split(' ')[0])

            #print("name: ", name)
            if compare_gains.select_channel_by_JSON_file(name, json_data) == True:
                if name in existing_data_dict and abs(float(existing_data_dict[name][-1]) - 1) > abs(float(chi) - 1):
                    print("Value better than existing, old value: ", existing_data_dict[name][-1],"new value: ", chi)
                    existing_data_dict[name] = (values, chi)
                elif name not in existing_data_dict:
                    print("Name doesn't exist yet and chi is good, appended to the end")
                    existing_data_dict[name] = (values, chi)
            else:
                print("Line is not needed from this fiel for this channel calibration (Channel Calib ID wrong)")
                
        return existing_data_dict


    def process_files(folder_path, file_name, output_file_name, json_data):
        existing_data = {}
        file_path = os.path.join(folder_path, file_name)
        existing_file_path = os.path.join(folder_path, output_file_name)
        new_data = compare_gains.read_data(file_path)
        existing_data = compare_gains.read_data_existing(existing_file_path)
        existing_data = compare_gains.update_existing_data_w_json(existing_data, new_data, json_data)
        return existing_data

    def save_data(data, output_file):
        with open(output_file, 'w') as file:
            #file.write("# Run: Wed, 20 Mar 2024 14:34:24 +0100 (CET) +219507000 nsec\n")
            #print(data.items())
            #print(name, (values, chi) in data.items())
            for name, (values, chi) in data.items():
                if chi != -1:
                    line = ', '.join(values)
                    file.write(f"{line}\n")
                else:
                    #print(name)
                    parts = values[:]
                    parts[-1] = "-1"
                    line = ', '.join(parts)
                    file.write(f"{line}\n")
