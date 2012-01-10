#!/bin/bash
 
function tex (){
    pdflatex --interaction=nonstopmode $1
    pdflatex --interaction=nonstopmode $1
    bibtex $(basename $1 .tex)
    pdflatex --interaction=nonstopmode $1
    bibtex $(basename $1 .tex)
    makeindex $(basename $1 .tex).glo -s $(basename $1 .tex).ist -t $(basename $1 .tex).glg -o $(basename $1 .tex).gls
    makeindex -s $(basename $1 .tex).ist -t $(basename $1 .tex).nlg -o $(basename $1 .tex).ntn $(basename $1 .tex).not

    pdflatex --interaction=nonstopmode $1
    bibtex $(basename $1 .tex)
    makeindex $(basename $1 .tex).glo -s $(basename $1 .tex).ist -t $(basename $1 .tex).glg -o $(basename $1 .tex).gls
    makeindex -s $(basename $1 .tex).ist -t $(basename $1 .tex).nlg -o $(basename $1 .tex).ntn $(basename $1 .tex).not

    pdflatex --interaction=nonstopmode $1
    pdflatex --interaction=nonstopmode $1
    pdflatex --interaction=nonstopmode $1
    
    os=`uname -s`
    if [ "$os" == "Darwin" ]; then
      [ -e $(basename $1 .tex).pdf ] && open $(basename $1 .tex).pdf&
    else
      [ -e $(basename $1 .tex).pdf ] && evince $(basename $1 .tex).pdf&
    fi
}
tex $@
