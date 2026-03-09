import os
import hashlib
import config

def check_md5(md5_str):
    if not os.path.exists(config.md5_data_path):
        return False
    
    for line in open(config.md5_data_path,'r',encoding='utf-8').readlines():
        line=line.strip()
        if md5_str==line:
            return True
    return False
def save_md5(md5_str):
    if not os.path.exists(config.md5_data_path):
        open(config.md5_data_path,'w',encoding='utf-8').close()
    with open(config.md5_data_path,'a',encoding='utf-8') as f:
        f.write(md5_str+'\n')
def get_md5(input_str:str,encoding='utf-8'):
    str_bytes=input_str.encode(encoding=encoding)
    
    md5_obj=hashlib.md5()
    md5_obj.update(str_bytes)
    md5_hex=md5_obj.hexdigest()
    
    return md5_hex