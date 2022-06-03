import os

def move_figures_to_margin(html_file_in, html_file_out, img_src_lst):
    """For the images in img_src_lst, replace the associated string '<figure'
    (in the line above) with '<span class="marginnote"<figure' and '</figure>' with '</figure></span>'.

    Images must be in the order they appear in html_file_out.
    """
    fin = open(html_file_in, "r")       # input file 
    lines = fin.readlines()             # list of lines in the input file
    fin.close()
    
    if os.path.exists(html_file_out):   # if output file exists       
        os.remove(html_file_out)        # remove it
    fout = open(html_file_out, 'w')     # output file
    
    # iterate over the list of images
    nskip = 0
    i_img = 0
    search_str = '<img src="'+img_src_lst[i_img]
    # iterate over the lines in the html_file
    for i_line, line in enumerate(lines):
        if i_line != 0:
            if line.startswith(search_str):
                #if '<span class="marginnote">' in lines[i_line-1]:
                #    print("Warning: Looks like this figure's already in the margin")
                fout.write(lines[i_line-1].replace('<figure', '<span class="marginnote"><figure'))
                in_fig = True
                i_img+=1
                if i_img<len(img_src_lst):
                    search_str = '<img src="'+img_src_lst[i_img]
                fout.write(line)
                fout.write(lines[i_line+1].replace('</figure>', '</figure></span>', 1))
                nskip = 2
            else:
                if nskip == 0:
                    fout.write(lines[i_line-1])
                else:
                    nskip -= 1
    fout.write(line)
    fout.close()