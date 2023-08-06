#
# Create The Following Documents:
#
#   . Coopr User Manual: Getting Started with the Pyomo Modeling Language
#     pyomo.tex
#
#   . Coopr User Manual: Pyomo Modeling Language and Extension Packages
#     coopr.tex
#

REMOVABLE := coopr.aux coopr.bbl coopr.blg coopr.log coopr.pdf coopr.toc pyomo.aux pyomo.blg pyomo.bbl pyomo.log pyomo.out pyomo.pdf pyomo.toc


all: coopr pyomo

clean:
	rm -f $(REMOVABLE)

coopr:
	pdflatex coopr
	bibtex coopr
	pdflatex coopr
	pdflatex coopr
	cp coopr.pdf ../pub

pyomo:
	pdflatex pyomo
	bibtex pyomo
	pdflatex pyomo
	pdflatex pyomo
	cp pyomo.pdf ../pub

