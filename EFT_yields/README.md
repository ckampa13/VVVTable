# VVV EFT Analysis Tables

- Developed to work on tables output by Higgs combine codes: [https://github.com/Saptaparna/EFTAnalysis/tree/master/EFTAnalysisFitting](https://github.com/Saptaparna/EFTAnalysis/tree/master/EFTAnalysisFitting)

- Structure:
```
|-- VVVTable
|   |-- EFT_yields
|   |   |-- data
|   |   |-- output
|   |   |-- make_tex_table.py
```

# Instructions
	1. Place yield CSV in VVVTable/EFT_yields/data/
		a. File name is expected to be: yield_table_$WC.csv, where $WC is replaced by the appropriate WC (e.g. cW) --> $CSVFILENAME
	2. Run table generation script with appropriate command line arguments: python make_tex_table.py
		a. Required cmdline args:
        	1. -f(--filename) : the CSV filename
        b. Optional cmdline args:
        	1. -m (--method) : the method for generating the table: ['default' (default),] --> $TABLEMETHOD
        	2. -w (--WC) : the WC, which will by default be parsed from the CSV filename.
    3. Find the output .tex in VVVTable/EFT_yields/output/
    	a. File name will be $CSVFILENAME.$TABLEMETHOD.tex
