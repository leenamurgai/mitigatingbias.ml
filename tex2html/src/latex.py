import os
import yaml
from yaml import load

def delete_intermediate_latex_files():

    # 1. load the list of online book files and folders
    with open('tex2html/config/latex.yml') as file:
        vars = load(file, Loader=yaml.FullLoader)

    # 2. Navigate the folders and remove files
    for ext in vars['file-extensions']:
        os.system('rm *.'+ext)
    for chap in vars['chapters']:
        for ext in vars['chapter-extensions']:
            os.system('rm '+chap+'/*.'+ext)
    for i in vars['inputs']:
        os.system('rm '+i+'/*.aux')

if __name__ == '__main__':
    delete_intermediate_latex_files()