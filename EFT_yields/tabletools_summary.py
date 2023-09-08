#!/bin/env python

import pandas as pd
# import glob
# import sys
# import argparse

# def get_table_types():
#     table_types = ["SRMCYield",
#                    # "CRMCYield", # TODO
#                   ]
#     return table_types

# def is_good_process_name(name):
#     good_process_names = [
#             "QCD",
#             "W",
#             "Z",
#             "top",
#             "1top",
#             "ttbar",
#             "diboson",
#             "Zg",
#             "ttw",
#             "ttz",
#             "ww",
#             "wz",
#             "zz",
#             "VH",
#             "ggHToZZTo4L",
#             "WWW",
#             "WWZ",
#             "WZZ",
#             "ZZZ",
#             "Bkg",
#             "Sig",
#             "SMWWW",
#             "SMWWZ",
#             "SMWZZ",
#             "SMZZZ",
#             "SMSig",
#             ## ADDED BY COLE
#             "DY",
#             "TTbar",
#             "WJets",
#             "WW",
#             "WZ",
#             "ZZ",
#             "ttV",
#             "Other",
#             "Top",
#             "restbkg",
#             "SMVVV",
#             "sm",
#             ]
#     is_good = name in good_process_names
#     return is_good

# def isfloat(num):
#     try:
#         float(num)
#         return True
#     except ValueError:
#         return False

# def check_csv_integrity(csv):
#     f = open(csv)
#     lines = [ line.strip() for line in f.readlines() ]

#     # Checking headers
#     headers = [ head.strip() for head in lines[0].split(",") ]
#     if headers[0] != "Bin":
#         print("First column header must be 'Bin'!")
#         sys.exit(1)
#     procs = headers[1::2]
#     procerrs = headers[2::2]
#     for proc in procs:
#         if not is_good_process_name(proc):
#             print("{} is not a good process name!".format(proc))
#             sys.exit(1)
#     for procerr in procerrs:
#         procstripped = procerr.replace("err", "")
#         if not is_good_process_name(procstripped):
#             print("{}err is not a good process error name!".format(procstripped))
#             sys.exit(1)

#     # Checking Contents
#     for line in lines[1:]:
#         numbers = [ n.strip() for n in line.split(",") ]
#         for n in numbers:
#             if not isfloat(n):
#                 print("Found a non-number {} in {}!".format(n, csv))
#                 sys.exit(1)

class VVVCSV:
    def __init__(self, csvfilepath, CL=0.95):
        self.csvfilepath = csvfilepath
        self.CL = CL
        self.initialize()
        # check_csv_integrity(csvfilepath)

    def initialize(self):
        self.df = pd.read_csv(self.csvfilepath, dtype=str)

    def nrows(self):
        return len(self.df)

    # def ncols(self):
    #     return len(self.cols)

def get_limit_summary_table(vvvcsv, caption="PUTSOMECAPTION", label="TAB:SOMETHING", needs_resizebox=False):

    # Latex header for the table
    rtnstr = '''\\begin{table}[!htbp]
    \\small
    \\center
    '''
    if needs_resizebox:
        rtnstr += '\\resizebox{\\textwidth}{!}{\n'

    # Process "first column" the description section
    # if len(bin_desc) == 0:
    #     bin_desc = ["Bin"]
    #     for i in range(vvvcsv.nrows()):
    #         bin_desc.append(str(i+1))
    # else:
    #     if len(bin_desc) != vvvcsv.nrows() + 1:
    #         print("The provided bin descriptions have length that is not consistent with number of rows in the table. len(bin_desc)={} vvvcsv.nrows={}".format(len(bin_desc), vvvcsv.nrows()))
    #         sys.exit(1)

    # Figure out how to format the columns
    colstyles = ['c|c'] # first one is for "Bin"
    # for col in vvvcsv.cols:
    #     if col == "Bkg":
    #         colstyles.append("|c")
    #     elif col == "Sig":
    #         colstyles.append("|c")
    #     elif col == "SMSig":
    #         colstyles.append("|c")
    #     else:
    #         colstyles.append("c")
    rtnstr += "\\begin{tabular}{" + "|".join(colstyles) + "}\n"

    content_lines = []
    # Process header
    name_cols = [c for c in vvvcsv.df.columns if ("UL" not in c) and ("LL" not in c)]
    if len(name_cols) > 1:
        raise NotImplementedError("Limits at only a single CL is currently implemented.")
    name_col = name_cols[0]
    headers = name_cols
    headers.append(f"Limit @ ${int(vvvcsv.CL*100):d}$\\% CL")
    # for col in vvvcsv.cols:
    #     headers.append(col)
    content_lines.append("    " + " & ".join(headers) + "\\\\\n")

    # Process rows
    for irow in range(vvvcsv.nrows()):
        row = vvvcsv.df.iloc[irow]
        #UL = f"{row['UL']:0.3f}"
        #LL = f"{row['LL']:0.3f}"
        # rounding in a previous step
        UL = row['UL']
        LL = row['LL']
        rowcontents = [row[name_col], f'[${LL}$, ${UL}$]']
        # for y, e in zip(vvvcsv.yields[irow], vvvcsv.errors[irow]):
        #     rowcontents.append("${} \\pm {}$".format(y, e))
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

def convert_csv(csvfilepath, texfilepath, caption, label, needs_resizebox):
    vvvcsv = VVVCSV(csvfilepath)
    table = get_limit_summary_table(vvvcsv, caption=caption, label=label, needs_resizebox=needs_resizebox)
    f = open(texfilepath, "w")
    f.write(table)
