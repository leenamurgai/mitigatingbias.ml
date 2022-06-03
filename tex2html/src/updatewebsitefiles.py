import os
import yaml
from yaml import load

def update_website_files():

    def replace_oldfile_w_newfile(old_file, new_file):
        print('Replace: ', new_file)
        os.system('rm '+old_file)
        os.system('cp '+new_file+' '+old_file)

    # 1. load the list of online book files, folders and fileTypes
    with open('tex2html/config/website.yml') as file:
        vars = load(file, Loader=yaml.FullLoader)

    # 2. Iterate over files and replace old files with new ones 
    for file in vars['files']:
        destination_file = os.path.join(vars['onlineBookFolder'],file)
        replace_oldfile_w_newfile(destination_file, file)

    # 3. Iterate over figures 
    for chapter in vars['chapters']:
        fig_folder = os.path.join(chapter, 'figures')
        destination_folder = os.path.join(vars['onlineBookFolder'],fig_folder)
        files = []
        for ext in vars['figureFileTypes']:
            fig_files = [f for f in os.listdir(fig_folder) if (os.path.isfile(os.path.join(fig_folder, f)) and f.endswith(ext))]
            files.extend(fig_files)
        for file in files:
            replace_oldfile_w_newfile(
                os.path.join(destination_folder, file),
                os.path.join(fig_folder, file))

    # 3. Iterate over tex2html 
    for folder, ext in vars['tex2htmlFolderFileType'].items():
        tex2html_folder = os.path.join('tex2html', folder)
        destination_folder = os.path.join(vars['onlineBookFolder'],
                                          tex2html_folder)
        # Make a list of files in the folder that end with the file ext
        files = [f for f in os.listdir(tex2html_folder)
        if (os.path.isfile(os.path.join(tex2html_folder, f)) and f.endswith(ext))]
        for file in files:
            replace_oldfile_w_newfile(
                os.path.join(destination_folder, file),
                os.path.join(tex2html_folder, file))

if __name__ == '__main__':
    update_website_files()