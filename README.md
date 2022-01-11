# How to compile

## Download the zipped revtex4 file
```
wget https://cdn.journals.aps.org/test/0e380411-3c3b-492a-8e56-2101d1d4822f/revtex-tds-2020-10-22.zip
``` 

## Put the tex style files in the same directory as your tex files
```
cp -p revtex-tds/tex/latex/revtex/* .
```

## Put the bib style files in the same directory as your tex files
```
cp -p revtex-tds/bibtex/bst/revtex/*
```

## Compile
```
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Or compile with the following script
```
./makePDF main
```

## Output 
The produced PDF file is called main.pdf