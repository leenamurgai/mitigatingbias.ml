import os
import yaml
from yaml import load
from tex2html import tex2html
from updatewebsitefiles import update_website_files

def update_website():
    tex2html()
    update_website_files()

if __name__ == '__main__':
    update_website()