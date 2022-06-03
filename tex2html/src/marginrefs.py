import os

def move_refs_to_margin(html_file_in, html_file_out, n_lines_per_ref):
    """
    Put references in the margin and delete the chapter References
    """
    fin = open(html_file_in, "r")       # input file 
    lines = fin.readlines()             # list of lines in the input file
    fin.close()
    
    if os.path.exists(html_file_out):   # if output file exists       
        os.remove(html_file_out)        # remove it
    fout = open(html_file_out, 'w')     # output file
    
    references = []
    iref = -1
    search_str = '<div id="ref-'
    # iterate over the lines in the html_file to get the requres references
    for i_line, line in enumerate(lines):
        if iref >= 0 and line.startswith(search_str):
            newline = ''.join(lines[i_line:i_line+n_lines_per_ref])
            references.append(newline.replace('<div', '<span').replace('</div>', '</span>'))
            iref += 1
        if line.startswith('<div id="refs" class="references csl-bib-body" role="doc-bibliography">'):
            iref = 0
    
    # iterate over the lines again 
    prefix = 'role="doc-biblioref">['
    suffix = ']</a></span>'
    iref = 0
    search_str = prefix+str(iref+1)+suffix
    inrefsec = False
    for line in lines:
        if line.startswith('<section id="bibliography" class="level1 unnumbered">'):
            inrefsec = True
        if not(inrefsec):
            if iref<len(references):
                newline = line
                while search_str in newline:
                    newline = newline.replace(search_str, search_str+'<span class="marginnote">'+references[iref]+'</span>', 1)
                    iref += 1
                    search_str = prefix+str(iref+1)+suffix
                fout.write(newline)
            else:
                fout.write(line)
        if inrefsec:
            # Remove links to references section
            if line.startswith('<div id="ref-'):
                fout.write('<div class="csl-entry" role="doc-biblioentry">\n')
            else:
                fout.write(line)
            if line.startswith('\section'):
                inrefsec = False
    fout.close()