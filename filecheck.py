# !/usr/bin/python

# A friend had a raid 1 instance go down and this was used to sort through the wreckage
# once the drives had been restored to the point of being recognisable by linux via NTFS-3G
import os
from shutil import copy2 as filecopy

FILE_PATH_1 = ""
FILE_PATH_2 = ""
HEADER_1 = f"################################### NOT IN {FILE_PATH_1}###############################\n"
HEADER_2 = f"################################### NOT IN {FILE_PATH_2}###############################\n"
DUMP_PATH = ""

def run_check():
    drive1_fies, drive2_2files = compile_filenames(FILE_PATH_1, FILE_PATH_2)
    diff1, diff2 = compare(drive1_fies, drive2_2files)
    generate_diff_file(diff1, diff2)
    find_and_copy(diff2, FILE_PATH_1, DUMP_PATH)
    
def find_and_copy(file_list, drv_path, dump):
    for root, dirs, files in os.walk(drv_path):
        for name in files:
            if name in file_list:
                try:
                    filecopy(os.path.join(root, name), dump)
                except OSError:
                    print(f"Could not copy file: {os.path.join(root, name)}")

def generate_diff_file(not_in_1, not_in_2):
    with open("diff_file.txt", mode="w", encoding="utf-8") as output:
        output.writelines(HEADER_1)
        for item in not_in_1:
            output.write(item+'\n')
        output.writelines(HEADER_2)
        for item in not_in_2:
            output.write(item+'\n')

def compare(files1, files2):
    not_in_1 = []
    not_in_2 = []
    for item in files1:
        if(item not in files2):
            not_in_2.append(item)
    for item in files2:
        if(item not in files1):
            not_in_1.append(item)
    return not_in_1, not_in_2

def compile_filenames(path1, path2):
    files1 = []
    files2 = []
    for root, dirs, files in os.walk(path1):
        for name in files:
            files1.append(name)
    
    for root, dirs, files in os.walk(path2):
        for name in files:
            files2.append(name)
    
    return files1, files2

run_check()
    