from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

file_root = 'E:\\Python\\Projects\\Ludum Dare\\23\\'

origIsSystemDLL = py2exe.build_exe.isSystemDLL
def isSystemDLL(pathname):
	if os.path.basename(pathname).lower() in ("libogg-0.dll", "sdl_ttf.dll"):
		return 0
	return origIsSystemDLL(pathname)
py2exe.build_exe.isSystemDLL = isSystemDLL

'''
Mydata_files = []
for files in os.listdir(file_root + 'sprites\\'):
    f1 = file_root + 'sprites\\' + files
    if os.path.isfile(f1): # skip directories
        f2 = 'sprites', [f1]
        Mydata_files.append(f2)
        
for files in os.listdir(file_root + 'fonts\\'):
    f1 = file_root + 'fonts\\' + files
    if os.path.isfile(f1): # skip directories
        f2 = 'fonts', [f1]
        Mydata_files.append(f2)
'''

setup(
    options = {'py2exe': {'bundle_files': 1}},
    windows = [{'script': "main.py"}],
    zipfile = None
)

#data_files = Mydata_files