import os
import sys
import hashlib
from datetime import datetime
from collections import namedtuple

import pandas as pd

Row = namedtuple('Row', 'path filename date_created date_modified byte_size hash')

def get_directory_info(starting_directory=None, hash_flag=False):
    results = []
    if not starting_directory:
        starting_directory = os.path.abspath(os.path.curdir)

    for root, dirs, files in os.walk(starting_directory):
        try:
            for filename in files:
                row = get_info_from_file_path(root, filename, hash_flag)
                results.append(row)
        except Exception as e:
            print(f'Error: {e}')
                
    df = pd.DataFrame(results)
    return df      


def get_info_from_file_path(root, filename, hash_flag=False):
    path = os.path.join(root, filename)
    info = os.stat(path)
    created = datetime.fromtimestamp(info.st_ctime)
    modified = datetime.fromtimestamp(info.st_mtime)
    size = info.st_size
    if hash_flag:
        try:
            hsh = hash_file(path)
        except Exception as e:
            hsh = f'Error: {e}'
    else:
        hsh = 'NA'
    
    return Row(root, filename, created, modified, size, hsh)


def hash_file(file_path):
    BUF_SIZE = 65536

    md5 = hashlib.md5()

    with open(file_path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
            
    return md5.hexdigest()
