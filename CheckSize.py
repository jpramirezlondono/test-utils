import os

# STEP 1: checking size of files:
class CheckSize(object):
    def __init__(self, file_name_v1: str, file_name_v2: str):
        self.file_name_v1 = file_name_v1
        self.file_name_v2 = file_name_v2

    def execute(self):
        size_v1 = os.path.getsize(self.file_name_v1)
        size_v2 = os.path.getsize(self.file_name_v2)
        self.compare_size(size_v1, size_v2)

    def get_bigger_file(self, size_v1, size_v2):
        if size_v1 > size_v2:
            return self.file_name_v1, "Nemo"
        elif size_v1 < size_v2:
            return self.file_name_v2, "RPC"
        else:
            return ''

    def get_difference_in_bytes(self, s1, s2):
        return s1 - s2 if s1 > s2 else s2 - s1

    def compare_size(self, size_v1, size_v2):
        bigger_file = self.get_bigger_file(size_v1, size_v2)
        if bigger_file[0] == '':
            print("Files have the same size")

        print(" The file version from ", bigger_file[1], " is greater for: ", self.get_difference_in_bytes( size_v1, size_v2), " bytes")

        print(" nemo EP file: ", self.file_name_v1, " measured: ", size_v1)
        print(" grpc EP file: ", self.file_name_v2, " measured: ", size_v2)