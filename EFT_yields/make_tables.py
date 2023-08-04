#!/bin/env python

import os
import argparse
import tabletools
import tabletools_asymm
import tabletools_generic
from tabletools_pd import VVV_TeXTable_PD
from main_tex import make_main_tex
from WC_ALL import WC_ALL

fpath = os.path.dirname(os.path.realpath(__file__))
# datacard_dir = os.path.abspath(os.path.join(fpath,'..'))

ddir = os.path.abspath(os.path.join(fpath, 'data'))
odir = os.path.abspath(os.path.join(fpath, 'output'))

if __name__=='__main__':
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename',
                        help=f'CSV Filename. Assumed placed in "VVVTable/EFT_yields/data/". If "WC" is present in the csv name, it will be replaced with any args.WC.')
    parser.add_argument('-m', '--method',
                        help=f'Which method for generating the table? ["default" (default),]')
    parser.add_argument('-w', '--WC',
                        help=f'Which Wilson Coefficient(s) to generate a table for? If not supplied, this is parsed from the CSV file name. If multiple, supply in a comma-separated list (e.g. "-w cW,cHq3")')
    parser.add_argument('-wa', '--WCall',
                        help=f'Which Wilson Coefficients to include in the limits summary table? If not supplied, this will default to pull all parameters in the WC_ALL.py file. If multiple, supply in a comma-separated list (e.g. "-wa cW,cHq3")')
    args = parser.parse_args()
    if args.filename is None:
        raise ValueError('Please suppply a CSV filename (-f)!')
    if args.method is None:
        args.method = 'default'
    if args.WC is None:
        WCs = [args.filename.split('_')[2].split('.')[0]]
    else:
        if "," in args.WC:
            WCs = [a.strip() for a in args.WC.split(',')]
            if not "WC" in args.filename:
                raise ValueError('Cannot run on multiple WCs if "WC" is not present in --filename for replacement.')
        else:
            WCs = [args.WC.strip()]
    if args.WCall is None:
        WCs_all = WC_ALL
    else:
        if "," in args.WCall:
            WCs_all = [a.strip() for a in args.WCall.split(',')]
        else:
            WCs_all = [args.WCall.strip()]
    # check if all CSVs are available
    if "WC" in args.filename:
        avail_csvs = os.listdir(ddir)
        missing_files = []
        for WC in set(WCs+WCs_all):
            fname = args.filename.replace('WC', WC)
            if not fname in avail_csvs:
                missing_files.append(fname)
        if len(missing_files) > 0:
            raise ValueError(f'The following CSV files are missing in VVVTable/EFT_yields/data/: {",".join(missing_files)}')
    # generate full filenames
    filecsv_temp = os.path.join(ddir, 'temp.csv')
    filecsv_temp_syst = os.path.join(ddir, 'temp_syst.csv')
    filetex_main = os.path.join(odir, 'main_'+args.filename.replace('.csv', f'.tex'))
    # print(f'Using {filecsv} to generate {filetex}...')
    print(f'Using base file: {args.filename}...')
    # load all CSV into a dict
    VVVTable_dict = {}
    # allchannels = []
    # allsubchannels = []
    for WC in WCs:
        if "WC" in args.filename:
            filecsv = os.path.join(ddir, args.filename.replace('WC', WC))
        else:
            filecsv = os.path.join(ddir, args.filename)
        myVVVTable = VVV_TeXTable_PD(filecsv, WC)
        VVVTable_dict[WC] = {'table': myVVVTable, 'filecsv': filecsv}
    #     allchannels.append(myVVVTable.df.channel.values)
    #     allsubchannels.append(myVVVTable.df.subchannel.values)
    # allchannels = np.concatenate(allchannels)
    # allsubchannels = np.concatenate(allsubchannels)
    # all_ch_sch_tup = set([[ch, sch] for ch, sch in zip(allchannels, allsubchannels)])
    # print(all_ch_sch_tup)
    # grab the zero table for backgrounds
    myVVVTable_ = VVVTable_dict[WCs[0]]['table']
    filecsv_ = VVVTable_dict[WCs[0]]['filecsv']
    print("For background tables, we have the following channgels: ", myVVVTable_.df.channel.unique())
    # add any channels that have enough processes to need resizing
    channels_resizebox = ['0Lepton_2FJ', '0Lepton_3FJ',]
    channels_resizebox_syst = []
    channels_resizebox_signal = []
    chan_file_list = []
    chan_file_list_syst = []
    chan_file_list_signal_dict = {WC: {} for WC in WCs}
    subsection_list = []
    subsection_signal_dict = {WC: [] for WC in WCs}
    for channel in myVVVTable_.df.channel.unique():
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
        df_ = myVVVTable_.df.query(f'channel=="{channel}"')
        for subchannel in df_.subchannel.unique():
            print(f'{channel}{subchannel} processing...')
            filetex = args.filename.replace('.csv', f'.{args.method}.{channel}{subchannel}.tex')
            filetex_syst = args.filename.replace('.csv', f'.{args.method}_syst.{channel}{subchannel}.tex')
            chan_file_list.append(filetex)
            chan_file_list_syst.append(filetex_syst)
            filetex = os.path.join(odir, filetex)
            filetex_syst = os.path.join(odir, filetex_syst)
            texsafe_ch = channel.replace('_', '')
            texsafe_sch = subchannel.replace('_', '')
            subsection_list.append(f'{texsafe_ch} {texsafe_sch}')
            subsection_signal_dict[f'{texsafe_ch} {texsafe_sch}'] = []
            print(f'stat only')
            myVVVTable_.coerce_df_to_csv(channel=channel, subchannel=subchannel)
            tabletools.convert_csv(filecsv_temp,
                                   filetex,
                                   bin_desc=myVVVTable_.bin_desc,
                                   caption=f"Yields per bin for SR {texsafe_ch}{texsafe_sch}. Backgrounds shown are Monte Carlo yields with statistical uncertainty only. Yields are quoted for the full Run 2 dataset.",
                                   label=f"tab:{texsafe_ch}{texsafe_sch}$bins",
                                   needs_resizebox=resize)
            print(f'syst only')
            myVVVTable_.coerce_df_to_csv_syst(channel=channel, subchannel=subchannel)
            tabletools_asymm.convert_csv(filecsv_temp_syst,
                                         filetex_syst,
                                         bin_desc=myVVVTable_.bin_desc,
                                         caption=f"Yields per bin for SR {texsafe_ch}{texsafe_sch}. Backgrounds shown are Monte Carlo yields with all systematic uncertainties added in quadrature. Yields are quoted for the full Run 2 dataset.",
                                         label=f"tab:{texsafe_ch}{texsafe_sch}$binssyst",
                                         needs_resizebox=resize_syst)
            print(f'signal: ', end='')
            # loop through WCs
            i = 0
            for WC in WCs:
                myVVVTable = VVVTable_dict[WC]['table']
                filecsv = VVVTable_dict[WC]['filecsv']
                if channel not in myVVVTable.df['channel'].unique():
                    continue
                if i == 0:
                    print(f'{WC}', end='')
                else:
                    print(f', {WC}', end='')
                i += 1
                filecsv_temp_signal = os.path.join(ddir, f'temp_signal_{WC}.csv')
                filetex_signal = args.filename.replace('.csv', f'.{args.method}_signal.{channel}{subchannel}.tex')
                if "WC" in filetex_signal:
                    filetex_signal = filetex_signal.replace('WC', WC)
                chan_file_list_signal_dict[WC][f'{texsafe_ch} {texsafe_sch}'] = filetex_signal
                subsection_signal_dict[f'{texsafe_ch} {texsafe_sch}'].append(WC)
                filetex_signal = os.path.join(odir, filetex_signal)
                myVVVTable.coerce_df_to_csv_signal(channel=channel, subchannel=subchannel)
                LL = myVVVTable.df.iloc[0][f'all_comb_{WC}_95CL_LL']
                UL = myVVVTable.df.iloc[0][f'all_comb_{WC}_95CL_UL']
                tabletools_generic.convert_csv(filecsv_temp_signal,
                                               filetex_signal,
                                               bin_desc=myVVVTable.bin_desc,
                                               caption=f"Yields per bin for SR {texsafe_ch}{texsafe_sch}, including the VVV yield from {WC} at the $95$\\% exclusion point. The limits on {WC} are: [${LL:0.3f}$,~${UL:0.3f}$]. All Monte Carlo background yields have been combined, and the statistical uncertainties and symmetrized systematic uncertainties for the total background are added in quadrature. Yields are quoted for the full Run 2 dataset.",
                                               label=f"tab:{texsafe_ch}{texsafe_sch}$binssignal",
                                               needs_resizebox=resize_signal)
            print()

    # MAKE LIMIT SUMMARY PLOT OUTSIDE THE LOOP

    # after making all tables, make the main file
    make_main_tex(filetex_main, chan_file_list, chan_file_list_syst, chan_file_list_signal_dict, WCs, subsection_list, subsection_signal_dict)
