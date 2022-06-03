####

import os

####

def letter_appendices(html_file_in, html_file_out, appendix_lettermap, labels_pre_post, app_label_prefixes):
    """
    Iterate over the appendices in appendix_lettermap,
    1. Iterate over the lines
       1.1. Find the chapter number, corresponding to the title (key) in appendix_lettermap, from their <h1> headers. Save them in number2lettermap.
       1.2. Check if the line has appendix references if it does get the list line_refs
    2.  Iterate over line_refs to construct new_line_refs with number2lettermap.
    3. Iterate over the lines again
       3.1. Replace numbering in labels with the corresponding letter with
            labels_pre_post and number2lettermap
       3.2. Replace numbering in references to appendix items with letters
    """
    fin = open(html_file_in, "r")       # input file 
    lines = fin.readlines()             # list of lines in the input file
    fin.close()
    
    if os.path.exists(html_file_out):   # if output file exists       
        os.remove(html_file_out)        # remove it
    fout = open(html_file_out, 'w')     # output file
    
    number2lettermap = {}
    header_prefix = '<h1 data-number="'
    number_start_index = len(header_prefix)

    linked_app_refs = {}
    n_apps_left = len(appendix_lettermap)
    # Example linked_ref
    # <a href="#app_Install" data-reference-type="ref" data-reference="app_Install">5</a>
    ref_start_str = '<a href="#'
    ref_end_str = '</a>'

    # Iterate over the lines in the html to get what we need to know what to replace
    for line in lines:
        for title in appendix_lettermap:

            # Search for appendix h1 headers to populate number2lettermap
            if title in line and line.startswith(header_prefix) and n_apps_left > 0:
                number2lettermap[find_chap_num(line, number_start_index)] = appendix_lettermap[title]
                n_apps_left -= 1
        find_linked_app_refs(line, ref_start_str, ref_end_str, app_label_prefixes, linked_app_refs)
    
    # print(number2lettermap)
    
    # Tell me if you don't find all the titles in appendix_lettermap
    if n_apps_left > 0:
        print("WARNING: Looks like we didn't find all the appendices - check appendix_lettermap keys")
    
    # Iterate over linked_app_refs (now we have number2lettermap) and construct the replacement refs
    for ref, newref in linked_app_refs.items():
        newref = ref
        for number, letter in number2lettermap.items():
            newref = newref.replace('>'+number, '>'+letter)
        linked_app_refs[ref] = newref

    """
    print()
    for link, new_link in linked_app_refs.items():
        print(link)
        print(new_link)
        print()
    """

    # Iterate over the lines again (now we have number2lettermap and linked_app_refs)
    for line in lines:
        newline = line
        # Iterate over the appendix chapters and replace labels
        for number, letter in number2lettermap.items():
            for prefix, postfix in labels_pre_post:
                newline = newline.replace(prefix+number+postfix, prefix+letter+postfix)
        for ref, newref in linked_app_refs.items():
            newline = newline.replace(ref, newref)
        fout.write(newline)
    fout.close()

####

def find_chap_num(line, number_start_index):
    """
    Find the chapter number, Given the h1 header line and the first index of the number
    """
    i = number_start_index
    chap_num = ''
    while ord('0') <= ord(line[i]) <= ord('9'):
        chap_num = chap_num+line[i]
        i+=1
    return chap_num

####

def find_linked_app_refs(line, ref_start_str, ref_end_str, app_label_prefixes, linked_app_refs):
    """
    Find all the linked references to appendix items
    """
    # if there's an appendix reference in the line
    if 'app_' in line:
        # set the first reference start index
        ref_start = 0
        ref_end = len(line)-1
        while 0 <= ref_start < len(line)-1:
            ref_start = line.find(ref_start_str, ref_start)
            ref_end_str_start_index = line.find(ref_end_str, ref_start)
            if ref_end_str_start_index < 0:
                break
            else:
                ref_end = ref_end_str_start_index + len(ref_end_str)
            """print(line[ref_start:ref_end])"""
            is_app_ref = False
            for label_prefix in app_label_prefixes:
                if line.startswith(ref_start_str+label_prefix, ref_start, ref_end):
                    is_app_ref  = True
                    break
            if is_app_ref:
                linked_app_refs[line[ref_start:ref_end]] = ''
            ref_start = ref_end