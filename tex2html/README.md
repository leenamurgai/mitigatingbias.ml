# tex2html

## 1. Conversion from LaTeX to HTML5

To convert ```MBML.tex``` to ```MBML.html```, (from the ```book``` folder) use the command:

```
python3 tex2html/src/tex2html.py
```

The ```tex2html``` script:
1. Calls pandoc to convert the file from ```MBML.tex``` to ```MBML.html```.
2. Then executes post-processing steps to create ```index.html``` from pandoc's output. The post-processing is discussed in the [README.md for the source code](https://github.com/leenamurgai/leenamurgai.github.io/tree/main/tex2html).

## 2. Pandoc

- This repository uses [pandoc version 2.14.02](https://github.com/jgm/pandoc) (same version as the [online converter](https://pandoc.org/try/), at the time of writing) to convert  ```MBML.tex```  to ```MBML.html```.
- Pandoc's [manual](https://pandoc.org/MANUAL.html).
- Pandoc is configured in [pandoc.yml](https://github.com/leenamurgai/leenamurgai.github.io/tree/master/book/tex2html/config/pandoc.yml)
- Pandoc works by converting the input file into an intermediary internal data structure - an abstract syntax tree (AST).

### 2.1 Pandoc Filters

Pandoc allows you to modify the internal AST (as part of the conversion process) using filters. The pandoc conversion in tex2html uses the following pandoc filters:
1. [date.lua](https://github.com/leenamurgai/leenamurgai.github.io/tree/master/book/tex2html/filters/date.lua): adds the option to use the date the file was converted.
2. [texref.lua](https://github.com/leenamurgai/leenamurgai.github.io/tree/master/book/tex2html/filters/texref.lua). This edits pandoc's AST in advance of applying pandoc-crossref, in order to ensure cross references to code listings and equations (provided by pandoc-crossref) work. See pandoc-crossref issue [[#319](https://github.com/lierdakil/pandoc-crossref/issues/319)].
3. [pandoc-crossref](https://github.com/lierdakil/pandoc-crossref): to manage cross references to figures, tables, code listings and equatons. It is configured in [pandoc-crossref.yml](https://github.com/leenamurgai/leenamurgai.github.io/tree/master/book/tex2html/config/pandoc-crossref.yml).
4. [citeproc](https://pandoc.org/MANUAL.html#citation-rendering): pandoc's inbuilt citation processing system.
5. [pandoc-sidenote](https://github.com/jez/pandoc-sidenote): to convert footnotes to sidenotes which are better suited to html format.

**Note:**
- Filters are applied in the order specified
- [pandoc-sidenote](https://github.com/jez/pandoc-sidenote) and [pandoc-crossref](https://github.com/lierdakil/pandoc-crossref) must be installed
- Since pandoc-crossref uses the same citation syntax as citeproc, the former should be specified before the latter. Accordingly citeproc must be specified as a filter (rather than using ```citeproc: true```) to ensure this happens.
- pandoc-crossref has a naming convention for labels which must be followed in order for it to find them.
  ```
  Figures:             \label{fig:id}
  Tables:              \label{tbl:id}
  Code Listings:       \label{lst:id}
  Equations:           \label{eq:id}
  ```

### 2.2 Pandoc only conversion from LaTeX to HTML5

To convert ```MBML.tex``` to ```MBML.html```, use the command:
```
pandoc --defaults tex2html/config/pandoc.yml
```
```MBML.html``` in this case will be the result of the pandoc conversion with no post-processing.

## 3. Notes on writing in LaTeX in order to optimise pandoc's output html file for readability

### 3.1 Header numbering

1. **\frontmatter chapter numbering:** Use ```\chapter*{title}``` with ```\addcontentsline{toc}{chapter}{title}``` (instead of just ```\chapter{title}```) to get the correct behaviour in the pandoc converted html.
2. **\paragraph numbering:** Use ```\paragraph*{title}``` (instead of just ```\paragraph{title}```) to get unnumbered ```<h5>``` headers in html.
3. **\subsubsection numbering:** Use ```\subsubsection*{title}``` (instead of just ```\subsubsection{title}```) to get unnumbered ```<h4>``` headers in html.
4. **Headers you don't want in the Table of Contents:** All ```<h1>``` and ```<h2>``` headers appear in the TOC of the HTML regardless of if they are numbered. If you don't want your header to appear in the TOC, it must be level 3 or below i.e. ```\subsection``` or below in LaTeX.

### 3.2 Header style formatting

1. ```\paragraph``` in LaTeX translates to ```<h5>``` in HTML. These are inline in LaTeX but not in HTML. If and inline is desired in HTML, use ```itemize``` or ```enumerate```  instead.
2. Don't use the ```description``` environment, it looks ugly in HTML.
3. ```{chapsumm}``` and ```{lookbox}```: Don't use the title options in ```{tcolorbox}``` use ```\cstitle{...}``` and ```\lbtitle{...}``` instead to make them easier to style in with CSS.

### 3.3 Figures

1. ```{minipage}```, ```{subfigure}``` and ```{tabular}``` inside ```{figure}``` don't work. Easier to just create a single figure with subfigures annotated inside it.
2. ```{wrapfigure}``` doesn't work, don't use it.
3. Convert ```.pdf_tex``` files into ```.png```s. HTML doesn't understand how to process these

### 3.4 Tables

I've optimised to achieve readability of tables in both LaTeX and HTML. In some cases this means that the table appearance is aesthetically suboptimal in one format or the other. I have noted where this is the case and issues have been filed for pandoc.

1. LaTeX package ```topcapt``` doesn't work. Instead of ```\topcaption{}```, just use ```\caption{}``` with ```\vspace{10pt}``` (the default) before ```\begin{tabular}```.
2. Use ```\multirow```, pandoc converts ```\cline``` to ```\hline```.
3. Pandoc does not correctly use the vertical alignment option from LaTeX's ```\multirow[]``` command. See [pandoc issue #7444](https://github.com/jgm/pandoc/issues/7444).

4. Table notes are tricky.
   - Use ```\textsuperscript{a}``` for the marker.
   - Use ```{``` before ```\centering``` and ```\par}``` after ```\end{tabular}``` so the table notes are not centred.
   - ```tablenotes``` environment:
     - After ```\end{tabular}``` add ```\vspace{4pt}``` for aesthetics.
     - Tablenotes should be in ```\footnotesize``` text.
   - ```\tnote{}``` macro
     - Start each note with a ```\par``` (this avoids having to leave a blank line between notes if there are multiple.)
     - To make sure the notes are indented, add ```\hspace{1.5em}``` (the default paragraph indentation size) before each table note.
     - Make the note marker superscript.

### 3.5 Equations

1. Can't use ```\mbox{}```, use ```\text{}``` or ```\textrm{}``` instead.
2. Can't use ```\mathbbm{1}``` or ```\mathbds{1}``` for the indicator function.
5. ```{alignat}``` doesn't render correctly, use only ```{align}```.
3. Can't use ```\nonumber``` with katex but it works with mathjax.
4. Only one label can be applied to an equation block. For the equation labels listed under ```Specific equation adjustments to numbering``` in ```tweak.css``` the label will be applied to the bottom of the math block.

### 3.6 Macros

1. In this ```\newenvironment```, you don't need the extra curly brackets for LaTeX but you do for pandoc to read it. This has been fixed in an unreleased version of pandoc. Again it helps to be verbose in your LaTeX.
   ```
   \newenvironment{tablenotes}{
   \vspace{4pt}
   \footnotesize}{}
   ```
## 4. Update the website

To update the website, use the command: ```python3 tex2html/src/updatewebsite.py```

- The files and folders which require updating are configured in [website.yml](https://github.com/leenamurgai/leenamurgai.github.io/tree/master/book/tex2html/config/wesite.yml).
- The code
  1. Updates the html file by running tex2html.
  2. Deletes the files (if they exist) and copies the specified files to the website repository locally.
- To update the website, the changes have to be pushed to the website repository [leenamurgai.github.io](https://github.com/leenamurgai/leenamurgai.github.io)

## 5. Remaining issues with the conversion from LaTeX to HTML

- **List Of Figures** and **List Of Tables** are missing from the HTML. Is it possible to get these via pandoc-crossref? See [issue #325](https://github.com/lierdakil/pandoc-crossref/issues/325)

