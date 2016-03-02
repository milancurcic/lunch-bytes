# ==========

TARGET = mypaper

PDFTARGET = $(TARGET).pdf

#Making Your Project (More) Portable
PYTHON := python
TEXCMD := pdflatex -interaction=batchmode
TEX_OPTS := -draftmode
VIEWCMD := open -a Preview

# Set Directories and files
FIGDIR = ./figs
SCRPDIR = ./scripts
DATADIR = ./data
PDFFIGS := $(wildcard $(FIGDIR)/*.pdf)

# Define  general Targets 
all: AO_NAO_PNA figures $(PDFTARGET)
data: AO_NAO_PNA
paper: $(PDFTARGET)

# Define independent targets
AO_NAO_PNA:
	cd $(DATADIR);\
	wget http://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/monthly.ao.index.b50.current.ascii
	cd $(DATADIR);\
	wget http://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.nao.monthly.b5001.current.ascii
	cd $(DATADIR);\
	wget http://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.pna.monthly.b5001.current.ascii

figures:
	$(PYTHON) $(SCRPDIR)/mypaper_figs.py

# Define dependent targets
$(PDFFIGS): $(SCRPDIR)/mypaper_figs.py
	$(PYTHON) $(SCRPDIR)/mypaper_figs.py

$(PDFTARGET): $(TARGET).tex $(PDFFIGS) 
	$(TEXCMD) $(TARGET).tex
	bibtex $(TARGET).aux
	$(TEXCMD) $(TARGET).tex
	$(TEXCMD) $(TARGET).tex

# View main tex file
view:  $(PDFTARGET)
	$(VIEWCMD) $(PDFTARGET)

# Clean up stray files but leave pdf
clean_aux:
	rm -fv $(TARGET).aux $(TARGET).log $(TARGET).blg $(TARGET).bbl $(TARGET).synctex.gz
clean:
	rm -fv $(TARGET).aux $(TARGET).log $(TARGET).blg $(TARGET).bbl $(TARGET).synctex.gz
	rm -fv $(PDFTARGET)

