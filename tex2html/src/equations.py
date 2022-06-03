import os

####

def remove_math_mode_from_eqn_labels(html_file_in, html_file_out):
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
    
    # iterate over the lines in the html_file
    for line in lines:
        newline = line
        if line.startswith('<td style="text-align: right;"><span class="math display">\[('):
            newline = newline.replace('<span class="math display">\[', '')
            newline = newline.replace('\]</span>', '')
        fout.write(newline)

    fout.close()

####

def replace_eqref_in_eqns(html_file_in, html_file_out, refs_in_math):
    """
    Iterate over the lines
      1. Set the label to the first item key in refs_in_math
      2. When we get to the corresponding div
      3. Find the equation number, corresponding to the label. Save them in label2numbermap.
      4. Iterate over labels in label2numbermap.
         4.1. Replace \ref{label} with label2numbermap[label] in the line
      5. When you have passed the eqn div, update label to be the next in the list of keys in refs_in_math

    Note: We only need to iterate over the lines once since references always come after labels for equations
    """
    fin = open(html_file_in, "r")       # input file 
    lines = fin.readlines()             # list of lines in the input file
    fin.close()
    
    if os.path.exists(html_file_out):   # if output file exists       
        os.remove(html_file_out)        # remove it
    fout = open(html_file_out, 'w')     # output file
    
    label2numbermap = {}
    in_labelled_eqn = False
    in_search_eqn = False
    eqno_prefix = '<td style="text-align: right;">('
    number_start_index = len(eqno_prefix)
    n_eqns_left = len(refs_in_math)
    n_eqns_found = 0

    # We only iterate over the lines in the html once, since we always have labels before references to them
    for line in lines:
        newline = line
        if line.startswith('<div id="eq:'):
            in_labelled_eqn = True
        if n_eqns_left>0 and line.startswith('<div id="'+refs_in_math[n_eqns_found]):
            in_search_eqn = True
        if in_labelled_eqn and line.startswith('</div>'):
            if in_search_eqn:
                in_search_eqn = False
            in_labelled_eqn = False
        # Search for label and add to label2numbermap when it's found
        if n_eqns_left>0:
            if in_search_eqn and line.startswith(eqno_prefix) and n_eqns_left > 0:
                label2numbermap[refs_in_math[n_eqns_found]] = find_eqn_num(line, number_start_index)
                n_eqns_left -= 1
                n_eqns_found += 1
        # Search for references and replace
        if n_eqns_found>0 and line.startswith('(\\ref{eq:'):
            for label in refs_in_math[:n_eqns_found]:
                #print('refs_in_eqns:', label2numbermap[label])
                newline = line.replace('\\ref{'+label+'}', label2numbermap[label])
        fout.write(newline)
    fout.close()
        
    # Tell me if you don't find all the labels in refs_in_math
    if n_eqns_left > 0:
        print("WARNING: Looks like we didn't find all the equations - check refs_in_math keys")
    
####

def find_eqn_num(line, number_start_index):
    """
    Find the equation number, this won't work for labels in the appendices.
    """
    i = number_start_index
    num = ''
    chap_num = ''
    while ord('0') <= ord(line[i]) <= ord('9'):
        num = num+line[i]
        i+=1
        if line[i]=='.':
            chap_num = num
            num = ''
            i+=1
    print('Eqn ref in eqn: ', chap_num+'.'+num)
    return chap_num+'.'+num

####