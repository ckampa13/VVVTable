#!/bin/env python

import os
import argparse
import tabletools
import tabletools_asymm
import tabletools_generic
from tabletools_pd import VVV_TeXTable_PD
from main_tex import make_main_tex

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
    filecsv_temp_syst = os.path.join(ddir, 'temp_syst.csv')
    filecsv_temp_signal = os.path.join(ddir, f'temp_signal_{args.WC}.csv')
    filetex_main = os.path.join(odir, 'main_'+args.filename.replace('.csv', f'.tex'))
    # print(f'Using {filecsv} to generate {filetex}...')
    print(f'Using {filecsv}...')
    myVVVTable = VVV_TeXTable_PD(filecsv, args.WC)
    # add any channels that have enough processes to need resizing
    channels_resizebox = ['0Lepton_2FJ', '0Lepton_3FJ',]
    channels_resizebox_syst = []
    channels_resizebox_signal = []
    chan_file_list = []
    chan_file_list_syst = []
    chan_file_list_signal = []
    subsection_list = []
    for channel in myVVVTable.df.channel.unique():
        if channel in channels_resizebox:
            resize = True
        else:
            resize = False
        if channel in channels_resizebox_syst:
            resize_syst = True
        else:
            resize_syst = False
        if channel in channels_resizebox_signal:
            resize_signal = True
        else:
            resize_signal = False
        df_ = myVVVTable.df.query(f'channel=="{channel}"')
        for subchannel in df_.subchannel.unique():
            print(f'{channel}{subchannel} processing...')

            filetex = args.filename.replace('.csv', f'.{args.method}.{channel}{subchannel}.tex')
            filetex_syst = args.filename.replace('.csv', f'.{args.method}_syst.{channel}{subchannel}.tex')
            filetex_signal = args.filename.replace('.csv', f'.{args.method}_signal.{channel}{subchannel}.tex')
            chan_file_list.append(filetex)
            chan_file_list_syst.append(filetex_syst)
            chan_file_list_signal.append(filetex_signal)
            filetex = os.path.join(odir, filetex)
            filetex_syst = os.path.join(odir, filetex_syst)
            filetex_signal = os.path.join(odir, filetex_signal)
            texsafe_ch = channel.replace('_', '')
            texsafe_sch = subchannel.replace('_', '')
            subsection_list.append(f'{texsafe_ch} {texsafe_sch}')
            print(f'stat only')
            myVVVTable.coerce_df_to_csv(channel=channel, subchannel=subchannel)
            tabletools.convert_csv(filecsv_temp,
                                   filetex,
                                   bin_desc=myVVVTable.bin_desc,
                                   caption=f"Yields per bin for SR {texsafe_ch}{texsafe_sch}. Backgrounds shown are Monte Carlo yields with statistical uncertainty only. Yields are quoted for the full Run 2 dataset.",
                                   label=f"tab:{texsafe_ch}{texsafe_sch}$bins",
                                   needs_resizebox=resize)
            print(f'syst only')
            myVVVTable.coerce_df_to_csv_syst(channel=channel, subchannel=subchannel)
            tabletools_asymm.convert_csv(filecsv_temp_syst,
                                         filetex_syst,
                                         bin_desc=myVVVTable.bin_desc,
                                         caption=f"Yields per bin for SR {texsafe_ch}{texsafe_sch}. Backgrounds shown are Monte Carlo yields with all systematic uncertainties added in quadrature. Yields are quoted for the full Run 2 dataset.",
                                         label=f"tab:{texsafe_ch}{texsafe_sch}$binssyst",
                                         needs_resizebox=resize_syst)
            print(f'signal')
            myVVVTable.coerce_df_to_csv_signal(channel=channel, subchannel=subchannel)
            LL = myVVVTable.df.iloc[0][f'all_comb_{args.WC}_95CL_LL']
            UL = myVVVTable.df.iloc[0][f'all_comb_{args.WC}_95CL_UL']
            tabletools_generic.convert_csv(filecsv_temp_signal,
                                           filetex_signal,
                                           bin_desc=myVVVTable.bin_desc,
                                           caption=f"Yields per bin for SR {texsafe_ch}{texsafe_sch}, including the VVV yield from {args.WC} at the $95$\\% exclusion point. The limits on {args.WC} are: [${LL:0.3f}$,~${UL:0.3f}$]. All Monte Carlo background yields have been combined, and the statistical uncertainties and symmetrized systematic uncertainties for the total background are added in quadrature. Yields are quoted for the full Run 2 dataset.",
                                           label=f"tab:{texsafe_ch}{texsafe_sch}$binssignal",
                                           needs_resizebox=resize_signal)

    # after making all tables, make the main file
    make_main_tex(filetex_main, chan_file_list, chan_file_list_syst, chan_file_list_signal, subsection_list)
