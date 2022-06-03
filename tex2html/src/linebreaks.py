import os

def insert_linebreaks(html_file_in, html_file_out, search_strs):
    """
    For each line in the file, iterate over the keys in the search_srts dict and replace them in the string with the corresponding value (which contains a line break).

    Note replacements only happen inside <table> environments. You should only need to do this inside a table.
    """
    fin = open(html_file_in, "r")       # input file 
    lines = fin.readlines()             # list of lines in the input file
    fin.close()
    
    if os.path.exists(html_file_out):   # if output file exists       
        os.remove(html_file_out)        # remove it
    fout = open(html_file_out, 'w')     # output file
    
    #for k, v in search_strs.items():
    #    print('line_break: ', k, v)
    # iterate over the lines in the html_file
    for line in lines:
        newline = line
        if newline.startswith('<td '):
            for k, v in search_strs.items():
                newline = newline.replace(k, v)
        fout.write(newline)
    fout.close()