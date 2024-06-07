

# Import the os module
import os

# Define the file path

def get_path(file_name):
    current_folder = os.getcwd()
    folder_out = 'out'
    folder_out_path = os.path.join(current_folder, folder_out)

    if not os.path.exists(folder_out_path):
        os.makedirs(folder_out_path)

    return os.path.join(folder_out_path, file_name)