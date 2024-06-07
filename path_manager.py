# Import the os module
import os

# Define the file path

def get_path(file_name):
    current_folder = os.getcwd()
    sub_folder_out = 'out'
    sub_folder_out_path = os.path.join(current_folder, sub_folder_out)

    if not os.path.exists(sub_folder_out_path):
        os.makedirs(sub_folder_out_path)

    return os.path.join(sub_folder_out_path, file_name)