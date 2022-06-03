import os

def put_tablenotes_in_divs(html_file_in, html_file_out):
    """
    Put tablenotes in <div class="tablenotes">
    """
    fin = open(html_file_in, "r")       # input file 
    lines = fin.readlines()             # list of lines in the input file
    fin.close()
    
    if os.path.exists(html_file_out):   # if output file exists       
        os.remove(html_file_out)        # remove it
    fout = open(html_file_out, 'w')     # output file
    
    search_str = '<p><sup>'             # each tablenote starts with this
    n = len(search_str)
    ntnotes = 0                         # tablenotes counter
    # iterate over the lines in the html_file
    for i_line, line in enumerate(lines):
        if line[:n] == search_str:
            #print("Found tablenotes")
            ntnotes += 1
        if line[:n] != search_str and ntnotes > 0: # If we are passed all the tablenotes in the table
            if '<div class="tablenotes">' in lines[i_line-1]:
                print("Warning: Looks like tablenote divs are already there")
            fout.write('<div class="tablenotes">\n')
            #print('number of tablenotes = ', ntnotes)
            while ntnotes > 0:
                fout.write(lines[i_line-ntnotes])
                ntnotes -= 1
            fout.write('</div>\n')
        if ntnotes == 0:
            fout.write(line)
    fout.close()