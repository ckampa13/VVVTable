#!/bin/env python

import os
import argparse
import tabletools
from tabletools_pd import VVV_TeXTable_PD

fpath = os.path.dirname(os.path.realpath(__file__))
# datacard_dir = os.path.abspath(os.path.join(fpath,'..'))

ddir = os.path.abspath(os.path.join(fpath, 'data'))
odir = os.path.abspath(os.path.join(fpath, 'output'))

if __name__=='__main__':
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename',
                        help=f'CSV Filename. Assumed placed in "VVVTable/EFT_yields/data/"')
    parser.add_argument('-m', '--method',
                        help=f'Which method for generating the table? ["default" (default),]')
    parser.add_argument('-w', '--WC',
                        help=f'Which Wilson Coefficient to generate a table for? If not supplied, this is parsed from the CSV file name.')
    args = parser.parse_args()
    if args.filename is None:
        raise ValueError('Please suppply a CSV filename (-f)!')
    if args.method is None:
        args.method = 'default'
    if args.WC is None:
        args.WC = args.filename.split('_')[2].split('.')[0]
    # generate full filenames
    filecsv = os.path.join(ddir, args.filename)
    filecsv_temp = os.path.join(ddir, 'temp.csv')
    filetex_main = os.path.join(odir, 'main_'+args.filename.replace('.csv', f'.tex'))
    # print(f'Using {filecsv} to generate {filetex}...')
    print(f'Using {filecsv}...')
    ######### THIS GOES IN LOOP #####
    channel = '0Lepton_2FJ'
    subchannel = ''
    filetex = os.path.join(odir, args.filename.replace('.csv', f'.{args.method}.{channel}{subchannel}.tex'))

    myVVVTable = VVV_TeXTable_PD(filecsv)
    myVVVTable.coerce_df_to_csv(channel='0Lepton_2FJ', subchannel='')
    # myVVVTable.make_table(method='default')
    # myVVVTable.write_tex(filetex)
    texsafe_ch = channel.replace('_', '')
    texsafe_sch = subchannel.replace('_', '')

    tabletools.convert_csv(filecsv_temp,
                           filetex,
                           bin_desc=myVVVTable.bin_desc,
                           caption=f"Yields per bin for SR {texsafe_ch}{texsafe_sch}. Backgrounds shown are Monte Carlo yields with statistical uncertainty only. Yields are quoted for the full Run 2 dataset.",
                           label=f"tab:{texsafe_ch}{texsafe_sch}$bins")
