#!/bin/env python

import csv
import glob
import sys
import argparse

def get_table_types():
    table_types = ["SRMCYield",
                   # "CRMCYield", # TODO
                  ]
    return table_types

def is_good_process_name(name):
    good_process_names = [
            "QCD",
            "W",
            "Z",
            "1top",
            "ttbar",
            "diboson",
            "WWW",
            "WWZ",
            "WZZ",
            "ZZZ",
            "Bkg",
            "Sig",
            ]
    is_good = name in good_process_names
    return is_good

# Parse region keys from signal_region_defns.tex
def get_regions(defntex):
    f = open(defntex)
    lines = f.readlines()
    region_alias = [ line.split("{")[1].split("}")[0] for line in lines if "xspace" in line ]
    region_keys = [ line.split("{")[2].split("\\xspace")[0] for line in lines if "xspace" in line ]
    regions = dict(zip(region_keys, region_alias))
    return regions

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def check_csv_integrity(csv):
    f = open(csv)
    lines = [ line.strip() for line in f.readlines() ]

    # Checking headers
    headers = [ head.strip() for head in lines[0].split(",") ]
    if headers[0] != "Bin":
        print("First column header must be 'Bin'!")
        sys.exit(1)
    procs = headers[1::2]
    procerrs = headers[2::2]
    for proc in procs:
        if not is_good_process_name(proc):
            print("{} is not a good process name!".format(proc))
            sys.exit(1)
    for procerr in procerrs:
        procstripped = procerr.replace("err", "")
        if not is_good_process_name(procstripped):
            print("{}err is not a good process error name!".format(procstripped))
            sys.exit(1)

    # Checking Contents
    for line in lines[1:]:
        numbers = [ n.strip() for n in line.split(",") ]
        for n in numbers:
            if not isfloat(n):
                print("Found a non-number {} in {}!".format(n, csv))
                sys.exit(1)

class VVVCSV:
    def __init__(self, csvfilepath):
        self.csvfilepath = csvfilepath
        self.initialize()
        check_csv_integrity(csvfilepath)

    def initialize(self):
        self.f = open(self.csvfilepath)
        self.reader = csv.reader(self.f)
        self.values = list(self.reader)
        self.cols = [ col.strip() for col in self.values[0][1::2] ]
        self.yields = [ [ float(y) for y in line[1::2] ] for line in self.values[1:] ]
        self.errors = [ [ float(e) for e in line[2::2] ] for line in self.values[1:] ]

    def nrows(self):
        return len(self.yields)

    def ncols(self):
        return len(self.cols)

def get_SRMCYield_table(vvvcsv, bin_desc=[], caption="PUTSOMECAPTION", label="TAB:SOMETHING"):

    # Latex header for the table
    rtnstr = '''
\\begin{sidewaystable}[!htbp]
    \\small
    \\center'''

    # Process "first column" the description section
    if len(bin_desc) == 0:
        bin_desc = ["Bin"]
        for i in range(vvvcsv.nrows()):
            bin_desc.append(str(i+1))
    else:
        if len(bin_desc) != vvvcsv.nrows() + 1:
            print("The provided bin descriptions have length that is not consistent with number of rows in the table. len(bin_desc)={} vvvcsv.nrows={}".format(len(bin_desc), vvvcsv.nrows()))
            sys.exit(1)

    # Figure out how to format the columns
    colstyles = []
    for col in vvvcsv.cols:
        if col == "Bkg":
            colstyles.append("c|")
        elif col == "Sig":
            colstyles.append("|c")
        else:
            colstyles.append("c")
    rtnstr += "\\begin{tabular}{" + "|".join(colstyles) + "}\n"

    content_lines = []
    # Process header
    headers = [bin_desc[0]]
    for col in vvvcsv.cols:
        headers.append(col)
    content_lines.append("    " + " & ".join(headers) + "\\\\\n")

    # Process rows

    for irow in range(vvvcsv.nrows()):
        rowcontents = [bin_desc[irow+1]]
        for y, e in zip(vvvcsv.yields[irow], vvvcsv.errors[irow]):
            rowcontents.append("${} \\pm {}$".format(y, e))
        content_lines.append("    " + " & ".join(rowcontents) + "\\\\\n")
    rtnstr += "    \\hline\n".join(content_lines)

    rtnstr += '''
    \\end{{tabular}}
    \\caption{{{}}}
    \\label{{{}}}
\\end{{sidewaystable}}
\\newpage
'''.format(caption, label
)
    return rtnstr

def convert_csv(csvfilepath, texfilepath, bin_desc, caption, label):
    vvvcsv = VVVCSV(csvfilepath)
    table = get_SRMCYield_table(vvvcsv, bin_desc=bin_desc, caption=caption, label=label)
    f = open(texfilepath, "w")
    f.write(table)
