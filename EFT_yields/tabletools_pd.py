import os
from string import Template
import numpy as np
import pandas as pd

from numerics import round_limit
from WC_ALL import WC_pretty_print_dict

fpath = os.path.dirname(os.path.realpath(__file__))
ddir = os.path.abspath(os.path.join(fpath, 'data'))

class VVV_TeXTable_PD(object):
    def __init__(self, tablefilepath, WC):
        self.tablefilepath = tablefilepath
        self.WC = WC
        self.load_df(tablefilepath)

    def load_df(self, tablefilepath):
        if '.pkl' in tablefilepath:
            self.df = pd.read_pickle(tablefilepath)
        elif '.csv' in tablefilepath:
            self.df = pd.read_csv(tablefilepath)
            self.df.fillna('', inplace=True)
        else:
            raise ValueError('Input table file must be either CSV (.csv) or pickle (.pkl).')

    def coerce_df_to_csv(self, channel, subchannel):
        coerced_dict = {'Bin':[]}
        self.bin_desc = ['Bin [GeV]', 'Inclusive',]
        # print(self.df.channel.unique())
        # print(self.df.subchannel.unique())
        df_ = self.df.query(f'channel=="{channel}" and subchannel=="{subchannel}"')
        # print(df_)
        # grab the process names
        # print(df_.process.unique())
        df1 = df_.query('bin == 1')
        procs = [p for p in df1.process]
        # print(procs)
        cols_all = ['Bin']
        for p in procs + ['Bkg']:
            coerced_dict[f'{p}'] = []
            coerced_dict[f'{p}err'] = []
            cols_all.append(f'{p}')
            cols_all.append(f'{p}err')
        # make the inclusive row
        coerced_dict['Bin'].append(1)
        for p in procs:
            dfp = df_.query(f'process=="{p}"')
            val = dfp[f'yield'].sum()
            err = (np.sum(dfp[f'MCstat'].values**2))**(1/2)
            coerced_dict[f'{p}'].append(f'{val:0.2f}')
            coerced_dict[f'{p}err'].append(f'{err:0.2f}')
        # total background
        dfp = df_
        val = dfp['yield'].sum()
        err = (np.sum(dfp['MCstat'].values**2))**(1/2)
        coerced_dict[f'Bkg'].append(f'{val:0.1f}')
        coerced_dict[f'Bkgerr'].append(f'{err:0.1f}')
        # loop through each bin
        for bin_ in df_.bin.unique():
            df0 = df_.query(f'bin == {bin_}')
            binlo = df0.iloc[0].bin_low
            binhi = df0.iloc[0].bin_high
            self.bin_desc.append(f'${int(binlo):d}-{int(binhi):d}$')
            i = bin_ + 1
            coerced_dict['Bin'].append(i)
            for p in procs:
                dfp = df0.query(f'process=="{p}"').iloc[0]
                val = dfp[f'yield']
                err = dfp[f'MCstat']
                coerced_dict[f'{p}'].append(f'{val:0.2f}')
                coerced_dict[f'{p}err'].append(f'{err:0.2f}')
            # get Bkg for that bin
            dfp = df0
            val = dfp['yield'].sum()
            err = (np.sum(dfp['MCstat'].values**2))**(1/2)
            coerced_dict[f'Bkg'].append(f'{val:0.1f}')
            coerced_dict[f'Bkgerr'].append(f'{err:0.1f}')
        # update final bin to be overflow
        temp = self.bin_desc[-1].split('-')[0]
        self.bin_desc[-1] = f'{temp}-$'
        # print(coerced_dict)
        df_coerced = pd.DataFrame(coerced_dict)
        # print(df_coerced)
        df_coerced = df_coerced[cols_all]
        # substitute any column names
        column_subs = {'sm': 'SMVVV', 'smerr': 'SMVVVerr'}
        df_coerced.rename(columns=column_subs, inplace=True)
        # save to temporary csv
        df_coerced.to_csv(os.path.join(ddir,'temp.csv'), index=False)

    def coerce_df_to_csv_syst(self, channel, subchannel):
        coerced_dict = {'Bin':[]}
        self.bin_desc = ['Bin [GeV]', 'Inclusive',]
        # print(self.df.channel.unique())
        # print(self.df.subchannel.unique())
        df_ = self.df.query(f'channel=="{channel}" and subchannel=="{subchannel}"')
        # print(df_)
        # grab the process names
        # print(df_.process.unique())
        df1 = df_.query('bin == 1')
        procs = [p for p in df1.process]
        # print(procs)
        cols_all = ['Bin']
        for p in procs + ['Bkg']:
            coerced_dict[f'{p}'] = []
            coerced_dict[f'{p}errUp'] = []
            coerced_dict[f'{p}errDown'] = []
            cols_all.append(f'{p}')
            cols_all.append(f'{p}errUp')
            cols_all.append(f'{p}errDown')
        # make the inclusive row
        coerced_dict['Bin'].append(1)
        for p in procs:
            dfp = df_.query(f'process=="{p}"')
            val = dfp[f'yield'].sum()
            errUp = (np.sum(dfp[f'syst_quadrature_Up'].values**2))**(1/2)
            errDown = (np.sum(dfp[f'syst_quadrature_Down'].values**2))**(1/2)
            coerced_dict[f'{p}'].append(f'{val:0.2f}')
            coerced_dict[f'{p}errUp'].append(f'{errUp:0.2f}')
            coerced_dict[f'{p}errDown'].append(f'{errDown:0.2f}')
        # total background
        dfp = df_
        val = dfp['yield'].sum()
        errUp = (np.sum(dfp['syst_quadrature_Up'].values**2))**(1/2)
        errDown = (np.sum(dfp['syst_quadrature_Down'].values**2))**(1/2)
        coerced_dict[f'Bkg'].append(f'{val:0.1f}')
        coerced_dict[f'BkgerrUp'].append(f'{errUp:0.1f}')
        coerced_dict[f'BkgerrDown'].append(f'{errDown:0.1f}')
        # loop through each bin
        for bin_ in df_.bin.unique():
            df0 = df_.query(f'bin == {bin_}')
            binlo = df0.iloc[0].bin_low
            binhi = df0.iloc[0].bin_high
            self.bin_desc.append(f'${int(binlo):d}-{int(binhi):d}$')
            i = bin_ + 1
            coerced_dict['Bin'].append(i)
            for p in procs:
                dfp = df0.query(f'process=="{p}"').iloc[0]
                val = dfp[f'yield']
                errUp = dfp[f'syst_quadrature_Up']
                errDown = dfp[f'syst_quadrature_Down']
                coerced_dict[f'{p}'].append(f'{val:0.2f}')
                coerced_dict[f'{p}errUp'].append(f'{errUp:0.2f}')
                coerced_dict[f'{p}errDown'].append(f'{errDown:0.2f}')
            # get Bkg for that bin
            dfp = df0
            val = dfp['yield'].sum()
            errUp = (np.sum(dfp['syst_quadrature_Up'].values**2))**(1/2)
            errDown = (np.sum(dfp['syst_quadrature_Down'].values**2))**(1/2)
            coerced_dict[f'Bkg'].append(f'{val:0.1f}')
            coerced_dict[f'BkgerrUp'].append(f'{errUp:0.1f}')
            coerced_dict[f'BkgerrDown'].append(f'{errDown:0.1f}')
        # update final bin to be overflow
        temp = self.bin_desc[-1].split('-')[0]
        self.bin_desc[-1] = f'{temp}-$'
        # print(coerced_dict)
        df_coerced = pd.DataFrame(coerced_dict)
        # print(df_coerced)
        df_coerced = df_coerced[cols_all]
        # substitute any column names
        column_subs = {'sm': 'SMVVV', 'smerrUp': 'SMVVVerrUp', 'smerrDown': 'SMVVVerrDown'}
        df_coerced.rename(columns=column_subs, inplace=True)
        # save to temporary csv
        df_coerced.to_csv(os.path.join(ddir,'temp_syst.csv'), index=False)

    def coerce_df_to_csv_signal(self, channel, subchannel):
        WC = self.WC
        WC_com = WC_pretty_print_dict[WC]['command']
        coerced_dict = {'Bin':[]}
        self.bin_desc = ['Bin [GeV]', 'Inclusive',]
        # print(self.df.channel.unique())
        # print(self.df.subchannel.unique())
        df_ = self.df.query(f'channel=="{channel}" and subchannel=="{subchannel}"')
        # print(df_)
        # grab the process names
        # print(df_.process.unique())
        df1 = df_.query('bin == 1')
        #procs = [p for p in df1.process]
        # print(procs)
        yield_col_comb = f'all_comb_yield_{WC}_95CL'
        yield_col_comb_pretty = "\\pbox{20cm}{"+'VVV \\\\ '+WC_com+' @ $95\\%$ CL - SM \\\\ }}'
        procs = ['sm']
        cols_all = ['Bin']
        cols_err = ['Bkg']
        for p in ['Bkg']+procs+[yield_col_comb]:
            coerced_dict[f'{p}'] = []
            cols_all.append(f'{p}')
            if p in cols_err:
                coerced_dict[f'{p}err'] = []
                cols_all.append(f'{p}err')
        # make the inclusive row
        coerced_dict['Bin'].append(1)
        for p in procs:
            dfp = df_.query(f'process=="{p}"')
            val = dfp[f'yield'].sum()
            coerced_dict[f'{p}'].append(f'{val:0.2f}')
            # this does not end up running, since nothing in "procs" has an error
            # keep it in case that changes
            if p in cols_err:
                eU = dfp[f'syst_quadrature_Up'].values
                eD = dfp[f'syst_quadrature_Down'].values
                eUD = (eU + eD) / 2.
                eS = dfp[f'MCstat'].values
                eSYST = (np.sum(eUD**2))**(1/2)
                eSTAT = (np.sum(eS**2))**(1/2)
                eTOT = (eSYST**2 + eSTAT**2)**(1/2)
                coerced_dict[f'{p}err'].append(f'{eTOT:0.2f}')
        # total background
        dfp = df_
        val = dfp['yield'].sum()
        coerced_dict[f'Bkg'].append(f'{val:0.1f}')
        if 'Bkg' in cols_err:
            eU = dfp[f'syst_quadrature_Up'].values
            eD = dfp[f'syst_quadrature_Down'].values
            eUD = (eU + eD) / 2.
            eS = dfp[f'MCstat'].values
            eSYST = (np.sum(eUD**2))**(1/2)
            eSTAT = (np.sum(eS**2))**(1/2)
            eTOT = (eSYST**2 + eSTAT**2)**(1/2)
            coerced_dict[f'Bkgerr'].append(f'{eTOT:0.1f}')
        # combined yield
        # need only one row of each bin and want to subtract SMVVV, so query that
        dfp = df_.query(f'process=="sm"')
        val = ((dfp[yield_col_comb+'_LL'] + dfp[yield_col_comb+'_UL'])/2. - dfp['yield']).sum()
        coerced_dict[yield_col_comb].append(f'{val:0.2f}')
        # loop through each bin
        for bin_ in df_.bin.unique():
            df0 = df_.query(f'bin == {bin_}')
            binlo = df0.iloc[0].bin_low
            binhi = df0.iloc[0].bin_high
            self.bin_desc.append(f'${int(binlo):d}-{int(binhi):d}$')
            i = bin_ + 1
            coerced_dict['Bin'].append(i)
            for p in procs:
                dfp = df0.query(f'process=="{p}"').iloc[0]
                val = dfp[f'yield']
                coerced_dict[f'{p}'].append(f'{val:0.2f}')
                if p in cols_err:
                    eU = dfp[f'syst_quadrature_Up']
                    eD = dfp[f'syst_quadrature_Down']
                    eUD = (eU + eD) / 2.
                    eS = dfp[f'MCstat']
                    eSYST = eUD
                    eSTAT = eS
                    eTOT = (eSYST**2 + eSTAT**2)**(1/2)
                    coerced_dict[f'{p}err'].append(f'{eTOT:0.2f}')
            # get Bkg for that bin
            dfp = df0
            val = dfp['yield'].sum()
            coerced_dict[f'Bkg'].append(f'{val:0.1f}')
            if 'Bkg' in cols_err:
                eU = dfp[f'syst_quadrature_Up'].values
                eD = dfp[f'syst_quadrature_Down'].values
                eUD = (eU + eD) / 2.
                eS = dfp[f'MCstat'].values
                eSYST = (np.sum(eUD**2))**(1/2)
                eSTAT = (np.sum(eS**2))**(1/2)
                eTOT = (eSYST**2 + eSTAT**2)**(1/2)
                coerced_dict[f'Bkgerr'].append(f'{eTOT:0.1f}')
            # get WC yield for that bin
            dfp = df0.query(f'process=="sm"').iloc[0]
            val = (dfp[yield_col_comb+'_LL'] + dfp[yield_col_comb+'_UL'])/2. - dfp['yield']
            coerced_dict[yield_col_comb].append(f'{val:0.2f}')
        # update final bin to be overflow
        temp = self.bin_desc[-1].split('-')[0]
        self.bin_desc[-1] = f'{temp}-$'
        # print(coerced_dict)
        df_coerced = pd.DataFrame(coerced_dict)
        # print(df_coerced)
        df_coerced = df_coerced[cols_all]
        # substitute any column names
        column_subs = {'sm': 'SMVVV', yield_col_comb: yield_col_comb_pretty}
        df_coerced.rename(columns=column_subs, inplace=True)
        # save to temporary csv
        df_coerced.to_csv(os.path.join(ddir,f'temp_signal_{WC}.csv'), index=False)

# for limit summary table
class VVV_TeXSummaryTable_PD(object):
    def __init__(self, list_of_VVV_TeXTable_PD):
        WCs = []
        LLs = []
        ULs = []
        for VVV_TeXTable_PD in list_of_VVV_TeXTable_PD:
            WC = VVV_TeXTable_PD.WC
            WC_com = WC_pretty_print_dict[WC]['command']
            row = VVV_TeXTable_PD.df.iloc[0]
            UL_name = f'all_comb_{WC}_95CL_UL'
            LL_name = f'all_comb_{WC}_95CL_LL'
            UL = row[UL_name]
            LL = row[LL_name]
            WCs.append(WC_com)
            #ULs.append(f'{UL:0.3f}')
            #LLs.append(f'{LL:0.3f}')
            # better sig fig rounding
            ULs.append(round_limit(UL, sig_figs=2, special_1_rule=True))
            LLs.append(round_limit(LL, sig_figs=2, special_1_rule=True))
        self.df = pd.DataFrame({'Wilson Coefficient': WCs, 'LL': LLs, 'UL': ULs})
        # sort by most sensitive (average)
        #self.df.eval('lim_mean = (abs(LL) + UL)/2.', inplace=True)
        self.df.loc[:, 'lim_mean'] = (self.df.loc[:, 'LL'].astype(float).abs() + self.df.loc[:, 'UL'].astype(float))/2.
        self.df.sort_values(by=['lim_mean'], inplace=True)
        self.df = self.df[['Wilson Coefficient', 'LL', 'UL']]

# for final bin summary
class VVV_TeXFinalBin_PD(object):
    def __init__(self, list_of_VVV_TeXTable_PD):
        # first handle backgrounds (using first list entry)
        df_processed = []
        self.df = list_of_VVV_TeXTable_PD[0].df
        for ch in self.df.channel.unique():
            #print(ch)
            df_ = self.df.query(f'channel == "{ch}"')
            for subch in df_.subchannel.unique():
                #print(subch)
                df0 = df_.query(f'subchannel == "{subch}"')
                procs = df0.process.unique()
                df00 = df0.query(f'process == "{procs[0]}"')
                max_bin = df00.bin.max()
                #print(max_bin)
                df_bin = df00.query(f'bin == {max_bin}')
                df_processed.append(df_bin)
        #print(df_processed)
        self.df = pd.concat(df_processed, ignore_index=True)


        '''
        WCs = []
        LLs = []
        ULs = []
        for VVV_TeXTable_PD in list_of_VVV_TeXTable_PD:
            WC = VVV_TeXTable_PD.WC
            WC_com = WC_pretty_print_dict[WC]['command']
            row = VVV_TeXTable_PD.df.iloc[0]
            UL_name = f'all_comb_{WC}_95CL_UL'
            LL_name = f'all_comb_{WC}_95CL_LL'
            UL = row[UL_name]
            LL = row[LL_name]
            WCs.append(WC_com)
            #ULs.append(f'{UL:0.3f}')
            #LLs.append(f'{LL:0.3f}')
            # better sig fig rounding
            ULs.append(round_limit(UL, sig_figs=2, special_1_rule=True))
            LLs.append(round_limit(LL, sig_figs=2, special_1_rule=True))
        self.df = pd.DataFrame({'Wilson Coefficient': WCs, 'LL': LLs, 'UL': ULs})
        # sort by most sensitive (average)
        #self.df.eval('lim_mean = (abs(LL) + UL)/2.', inplace=True)
        self.df.loc[:, 'lim_mean'] = (self.df.loc[:, 'LL'].astype(float).abs() + self.df.loc[:, 'UL'].astype(float))/2.
        self.df.sort_values(by=['lim_mean'], inplace=True)
        self.df = self.df[['Wilson Coefficient', 'LL', 'UL']]
        '''
