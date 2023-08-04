#!/bin/env python

import csv
import glob
import sys
import argparse

'''
def is_good_process_name(name):
    good_process_names = [
            "QCD",
            "W",
            "Z",
            "top",
            "1top",
            "ttbar",
            "diboson",
            "Zg",
            "ttw",
            "ttz",
            "ww",
            "wz",
            "zz",
            "VH",
            "ggHToZZTo4L",
            "WWW",
            "WWZ",
            "WZZ",
            "ZZZ",
            "Bkg",
            "Sig",
            "SMWWW",
            "SMWWZ",
            "SMWZZ",
            "SMZZZ",
            "SMSig",
            ## ADDED BY COLE
            "DY",
            "TTbar",
            "WJets",
            "WW",
            "WZ",
            "ZZ",
            "ttV",
            "Other",
            "Top",
            "restbkg",
            "SMVVV",
            "sm",
            ]
    is_good = name in good_process_names
    return is_good
'''

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
    # procs = headers[1::3]
    # procerrsUp = headers[2::3]
    # procerrsDown = headers[3::3]
    # for proc in procs:
    #     if not is_good_process_name(proc):
    #         print("{} is not a good process name!".format(proc))
    #         sys.exit(1)
    # for procerr in procerrsUp:
    #     procstripped = procerr.replace("errUp", "")
    #     if not is_good_process_name(procstripped):
    #         print("{}errUp is not a good process error name!".format(procstripped))
    #         sys.exit(1)
    # for procerr in procerrsDown:
    #     procstripped = procerr.replace("errDown", "")
    #     if not is_good_process_name(procstripped):
    #         print("{}errDown is not a good process error name!".format(procstripped))
    #         sys.exit(1)

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
        self.cols_list = []
        self.cols = {}
        self.yields = {}
        self.errorsUp = {}
        self.errorsDown = {}
        self.errors = {}
        potential_cols = [s.strip() for s in self.values[0][1:]]
        Npot = len(potential_cols)
        # print(f'{Npot} potential columns...')
        # print(potential_cols)
        for i, col in enumerate(potential_cols):
            ind = i+1
            isCol = True
            if "err" in col:
                isCol = False
            if isCol:
                self.cols_list.append(col)
                self.cols[col] = ind
                self.yields[col] = {'ind': ind, 'values': []}
        for col, ind in self.cols.items():
            if ind < (Npot - 1):
                Ncol = potential_cols[ind]
            if Ncol == col+'err':
                self.errors[col] = {'ind': ind+1, 'values': []}
            if ind < (Npot - 2):
                NNcol = potential_cols[ind+1]
                if (Ncol == col+'errUp') & (NNcol == col+'errDown'):
                    self.errorsUp[col] = {'ind': ind+1, 'values': []}
                    self.errorsDown[col] = {'ind': ind+2, 'values': []}

        # fill all dicts
        for dict_base in [self.yields, self.errors, self.errorsUp, self.errorsDown]:
            for col, col_dict in dict_base.items():
                ind = col_dict['ind']
                # loop through rows
                for line in self.values[1:]:
                    val = float(line[ind])
                    col_dict['values'].append(val)

        # print(f'cols: {self.cols}')
        # print(f'yields: {self.yields}')
        # print(f'errors: {self.errors}')
        # print(f'errorsUp: {self.errorsUp}')
        # print(f'errorsDown: {self.errorsDown}')

    def nrows(self):
        k = list(self.yields.keys())[0]
        return len(self.yields[k]['values'])

    def ncols(self):
        return len(self.cols.keys())

def get_SRMCYield_table(vvvcsv, bin_desc=[], caption="PUTSOMECAPTION", label="TAB:SOMETHING", needs_resizebox=False):

    # Latex header for the table
    rtnstr = '''\\begin{table}[!htbp]
    \\small
    \\center
    '''
    if needs_resizebox:
        rtnstr += '\\resizebox{\\textwidth}{!}{\n'

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
    colstyles = ['c'] # first one is for "Bin"
    for col in vvvcsv.cols:
        if col == "Bkg":
            colstyles.append("|c")
        elif col == "Sig":
            colstyles.append("|c")
        elif col == "SMSig":
            colstyles.append("|c")
        else:
            colstyles.append("c")
    rtnstr += "\\begin{tabular}{" + "|".join(colstyles) + "}\n"

    content_lines = []
    # Process header
    headers = [bin_desc[0]]
    for col in vvvcsv.cols_list:
        headers.append(col)
    content_lines.append("    " + " & ".join(headers) + "\\\\\n")

    # Process rows

    for irow in range(vvvcsv.nrows()):
        rowcontents = ["\\pbox{20cm}{ ~ \\\\"+bin_desc[irow+1]+"\\\\ }"]
        for col in vvvcsv.cols_list:
            if col in vvvcsv.errorsUp.keys():
                y = vvvcsv.yields[col]['values'][irow]
                eu = vvvcsv.errorsUp[col]['values'][irow]
                ed = vvvcsv.errorsDown[col]['values'][irow]
                rowcontents.append(f"${y}  ^{{+{eu}}}_{{-{ed}}}$")
            elif col in vvvcsv.errors.keys():
                y = vvvcsv.yields[col]['values'][irow]
                e = vvvcsv.errors[col]['values'][irow]
                rowcontents.append("${} \\pm {}$".format(y, e))
            else:
                y = vvvcsv.yields[col]['values'][irow]
                rowcontents.append("${}$".format(y))

        content_lines.append("    " + " & ".join(rowcontents) + "\\\\\n")
    rtnstr += "    \\hline\n".join(content_lines)

    rtnstr += '\\end{tabular}'
    if needs_resizebox:
        rtnstr += '}'
    rtnstr += '''
    \\caption{{{}}}
    \\label{{{}}}
\\end{{table}}
'''.format(caption, label)

    return rtnstr

def convert_csv(csvfilepath, texfilepath, bin_desc, caption, label, needs_resizebox):
    vvvcsv = VVVCSV(csvfilepath)
    table = get_SRMCYield_table(vvvcsv, bin_desc=bin_desc, caption=caption, label=label, needs_resizebox=needs_resizebox)
    f = open(texfilepath, "w")
    f.write(table)
