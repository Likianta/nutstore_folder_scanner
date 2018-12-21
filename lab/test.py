import os
from common_utils import read_and_write_basic

a = r'D:\likianta\lk_workspace\com_qwings_data\cnas\cnas_instr_spider\data\ability_baseinfo.json'
b = os.path.getsize(a)
print(b/1024/1024)
