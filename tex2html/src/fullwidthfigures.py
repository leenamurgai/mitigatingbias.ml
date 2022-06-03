import os

def make_figures_fullwidth(html_file_in, html_file_out, img_src_lst):
    """For the images in img_src_lst, replace the associated string '<figure>'
    (in the line above) with '<figure class="fullwidth">'

    Images must be in the order they appear in html_file_out.
    """
    fin = open(html_file_in, "r")       # input file 
    lines = fin.readlines()             # list of lines in the input file
    fin.close()
    
    if os.path.exists(html_file_out):   # if output file exists       
        os.remove(html_file_out)        # remove it
    fout = open(html_file_out, 'w')     # output file
    
    # iterate over the list of images
    i_img = 0
    search_str = '<img src="'+img_src_lst[i_img]
    # iterate over the lines in the html_file
    for i_line, line in enumerate(lines):
        if i_line != 0:
            if line.startswith(search_str):
                #if 'class="fullwidth"' in lines[i_line-1]:
                #    print("Warning: Looks like this figure's already fullwith")
                fout.write(lines[i_line-1].replace('<figure', '<figure class="fullwidth"'))
                i_img+=1
                if i_img<len(img_src_lst):
                    search_str = '<img src="'+img_src_lst[i_img]
            else:
                fout.write(lines[i_line-1])
    fout.write(line)
    fout.close()