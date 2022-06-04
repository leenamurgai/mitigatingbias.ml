# Notes on source code

The code in the folder performs two main functions. post-processing pandoc's output converting from LaTeX to HTML, and updating the website.

## 1. Post-processing

Both the post processing and scripting (to run pandoc and post-process its output) are done in python (version 3.8).

1. At each post-processing step, we input the html file output by the previous step.
2. Finally we ensure both ```MBML.html``` and ```index.html``` are copies of the same output file.

Below we summarise the post-processing steps.

### 1.1 Full width figures

- Full width figures should take up the full width (including the margin).
- See ```fullwidthfigures``` in ```tex2html.yml```.
- Figures in pandoc's AST are represented as a single inline [Image](https://pandoc.org/lua-filters.html#type-image) inside a [Para](https://pandoc.org/lua-filters.html#type-para) block (see [pandoc issue #3177](https://github.com/jgm/pandoc/issues/3177)) which does not have the attribute ```classes```.
- Thus we are unable to add ```class="fullwidth"``` to the ```<figure>``` element of the html file with a pandoc filter.
- See the unused filter ```fullwidthfig.lua``` and [pandoc-discuss](https://groups.google.com/g/pandoc-discuss/c/NYS6FfbOhO0).
- Instead we do this by post-processing the pandoc output file.

### 1.2 Margin figures

- Margin figures should be in the margin.
- See ```marginfigures``` in ```tex2html.yml```.
- We do this by post-processing the pandoc output file and encapsulating it in a ```<span class="marginnote">```.

### 1.3 Table notes

- Encapsulate tablenotes in a ```<div class="tablenotes>``` so they can be styled appropriately. See [pandoc issue #7469](https://github.com/jgm/pandoc/issues/7469).
- To find them we look for ```<p><sup>```.

### 1.4 Linebreaks in table cells

- LaTeX tables allow you to specify the width of a given table cell to force linebreaks, HTML requires an explicit linebreak where desired.
- In this post-processing step we insert linebreaks in table cells where necessary to aid readability.
- In particular Tables ```B.1```, ```B.2``` and ```D.1```.
- See ```linebreak_lines``` in ```tex2html.yml```.

### 1.5 Appendices that are lettered (rather than numbered)

- For consistency with LaTeX, appendix chapters should be lettered.
- See [pandoc-discuss](https://groups.google.com/g/pandoc-discuss/c/31Vyxi_ZYDg/m/8Ud0oUdnAQAJ) and [pandoc-crossref issue #324](https://github.com/lierdakil/pandoc-crossref/issues/324).
- In order to identify references to the appendix, all labelled items in the appendix must include ```app_``` in the label. Furthermore, since all chapter and section headers are linked in the contents, we must label all chapters and sections in the appendicies (regardless of whether they are referenced). We use the following prefixes:
  - appendix header labels: ```app_```
  - appendix section labels: ```sec_app_```
  - appendix figure labels: ```fig:app_```
  - appendix table labels: ```tbl:app_```

- For each appendix chapter in the ```appendix_lettermap``` dict:
  - Iterate over the lines
    - Find the chapter number, corresponding to the title (key) in ```appendix_lettermap```, from their ```<h1>``` headers. Save them in ```number2lettermap```.
    - Check if the line has appendix references, if it does get the list of references in it (``` line_refs```).
  - Iterate over line_refs to
    - construct ```new_line_refs``` using ```number2lettermap```.
  - Iterate over the lines again:
    - Replace numbering in labels with the corresponding letter using ```labels_pre_post``` and ```number2lettermap```.
    - Replace numbering in references to appendix items with letters.

### 1.6 Move citation references to the margin

- In the pdf we have references at the end of every chapter
- In a browser, placement in the margin improves readability
- This can likely be done with a filter though it was more work than post-processing.
  - See unused filter ```marginref.lua```
  - See [pandoc pull request #7461](https://github.com/jgm/pandoc/pull/7461).
  - See [pandoc-discuss](https://groups.google.com/g/pandoc-discuss/c/WAKgw6i-mL4)
- Iterate over the lines to get the linked reference HTML
  - Replace divs with spans
  - concatenate the lines into a single string
- Iterate over the lines again to make the replacements
  - Postfix the first citation for any given reference with a marginnote containing the reference html.
  - Remove the id field for the references in the References chapter at the end.

### 1.7 Equation labels

- pandoc-crossref puts equation labels in math mode. We remove the encapsualting ```<span class="math display">\[```...```\]```.
- To do this we look for ```<td style="text-align: right;"><span class="math display">(```.
-  See [pandoc-crossref issue #323](https://github.com/lierdakil/pandoc-crossref/issues/323).

### 1.8 Equation references inside equations

- HTML does not handle references inside equations. Such references will always be to equations that are labelled ealier in the file. Thus we need only iterate over the file once.
- To fix this we keep an ordered list of labels corresponding to ```refs_in_math```.
- We iterate over the lines and look for the ```div``` corresponding to the first ```label``` in ```refs_in_math```.
- We find the equation number in the ```div``` and store it in ```label2numbermap``` and move on to the next ```label``` in ```refs_in_math```.
- Simultaneously we replace ```\ref{label}``` to the equations whose labels we have found.