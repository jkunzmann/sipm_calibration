import os


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

def update_existing_data(existing_data, new_data):
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


def process_files(folder_path, file_name, output_file_name):
    existing_data = {}
    file_path = os.path.join(folder_path, file_name)
    existing_file_path = os.path.join(folder_path, output_file_name)
    new_data = read_data(file_path)
    existing_data = read_data_existing(existing_file_path)
    existing_data = update_existing_data(existing_data, new_data)
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


if __name__ == "__main__":
    # File information
    #folder_path = input("Please put the folder path here: ")
    #file_name = input("Please put the file name here: ")


    folder_path = "/home/jan/Universitat_Bern/Doktor/ADC_Viewer/fitlog"
    file_name = "ascii_fitlog"

    # Final file
    output_file_name = input("Please announce the final file name: ")

    # Work on the file
    existing_data = process_files(folder_path, file_name, output_file_name)

    print("The generated file is called: " + output_file_name)
    # Save the data
    save_data(existing_data, output_file_name)
