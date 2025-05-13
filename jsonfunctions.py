import json
import os

# empty_data should be what data we want to put in there if the file doesn't exist
# either {} or [] as we are working with json files
def create_if_not_exist(filename, empty_data):
    if not os.path.exists(filename):
        write_json_file(filename, empty_data)

def write_json_file(filename, info_to_save):
    # write out to file
    my_file = open(filename, "w")
    json.dump(info_to_save, my_file)
    my_file.close()

def read_json_file(filename):
    my_file = open(filename, "r")
    information = json.load(my_file)
    my_file.close()
    return information
