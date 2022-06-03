import os
import yaml
from yaml import load

from fullwidthfigures import make_figures_fullwidth
from marginfigures import move_figures_to_margin
from tablenotes import put_tablenotes_in_divs
from linebreaks import insert_linebreaks
from appendices import letter_appendices
from marginrefs import move_refs_to_margin
from equations import remove_math_mode_from_eqn_labels
from equations import replace_eqref_in_eqns

def tex2html():

    def replace_oldfile_w_newfile(old_file, new_file):
        os.system('rm '+old_file)
        os.system('cp '+new_file+' '+old_file)

    # 1. load tex2html variables
    with open('tex2html/config/tex2html.yml') as file:
        vars = load(file, Loader=yaml.FullLoader)

    # 2. load pandoc's output html file as our input file for post-processing
    with open(vars['pandocYaml']) as file:
        temp_file = load(file, Loader=yaml.FullLoader)['output-file']

    # 3. run pandoc to create html file from tex file
    os.system("pandoc --defaults "+vars['pandocYaml'])

    # 4. Post-process pandoc output html file
    # 4.1. Make figures from list full width
    make_figures_fullwidth(temp_file,                  # In => Out
                           vars['html_file_out'],      # Out => In
                           vars['fullwidthfigures'])   # Params
    # 4.2. Move figures from a list to the margin
    move_figures_to_margin(vars['html_file_out'],      # In => Out
                           temp_file,                  # Out => In
                           vars['marginfigures'])   # Params
    # 4.3. Put tablenotes in divs
    put_tablenotes_in_divs(temp_file,                  # In => Out
                           vars['html_file_out'])      # Out => In
    # 4.4. Insert linebreaks in table cells as specified in the list
    insert_linebreaks(vars['html_file_out'],           # In => Out
                      temp_file,                       # Out => In
                      vars['linebreak_lines'])         # Params
    # 4.5 Replace numbering with letting for appendices
    letter_appendices(temp_file,                       # In
                      vars['html_file_out'],           # Out => In
                      vars['appendix_lettermap'],      # Params
                      vars['labels_pre_post'],         # Params
                      vars['appendix_label_prefixes']) # Params
    # 4.6 Move references to margin
    move_refs_to_margin(vars['html_file_out'],         # In
                        temp_file,                     # Out => In
                        vars['n_lines_per_ref'])       # Params
    # 4.7 Remove encapsulating math mode from equation labels
    remove_math_mode_from_eqn_labels(temp_file,             # In
                                     vars['html_file_out']) # Out => In

    # 4.8 Replace equation refs in equations with the corresponding number
    replace_eqref_in_eqns(vars['html_file_out'],       # In
                          temp_file,                   # Out
                          vars['refs_in_math'])

    # 5. Save
    replace_oldfile_w_newfile(vars['html_file_out'],temp_file)

if __name__ == '__main__':
    tex2html()