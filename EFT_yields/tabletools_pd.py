import os
from string import Template
import numpy as np
import pandas as pd

fpath = os.path.dirname(os.path.realpath(__file__))
ddir = os.path.abspath(os.path.join(fpath, 'data'))

"""
header = '''
\\begin{sidewaystable}[!htbp]
    \\small
    \\center
'''
footer_ = '''
    \\end{tabular}
    \\caption{$caption}
    \\label{$label}
\\end{sidewaystable}
\\newpage
'''
footer_template = Template(footer_)

table_helper_dict = {
    # Latex header for the table
    'header': header,
    'footer_template': footer_template,
    'hline': '    \\hline\n'
}
"""

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
        coerced_dict[f'Bkg'].append(f'{val:0.2f}')
        coerced_dict[f'Bkgerr'].append(f'{err:0.2f}')
        # loop through each bin
        for bin_ in df_.bin.unique():
            df0 = df_.query(f'bin == {bin_}')
            binlo = df0.iloc[0].bin_low
            binhi = df0.iloc[0].bin_high
            self.bin_desc.append(f'${binlo:0.1f}-{binhi:0.1f}$')
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
            coerced_dict[f'Bkg'].append(f'{val:0.2f}')
            coerced_dict[f'Bkgerr'].append(f'{err:0.2f}')
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
        coerced_dict[f'Bkg'].append(f'{val:0.2f}')
        coerced_dict[f'BkgerrUp'].append(f'{errUp:0.2f}')
        coerced_dict[f'BkgerrDown'].append(f'{errDown:0.2f}')
        # loop through each bin
        for bin_ in df_.bin.unique():
            df0 = df_.query(f'bin == {bin_}')
            binlo = df0.iloc[0].bin_low
            binhi = df0.iloc[0].bin_high
            self.bin_desc.append(f'${binlo:0.1f}-{binhi:0.1f}$')
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
            coerced_dict[f'Bkg'].append(f'{val:0.2f}')
            coerced_dict[f'BkgerrUp'].append(f'{errUp:0.2f}')
            coerced_dict[f'BkgerrDown'].append(f'{errDown:0.2f}')
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
        yield_col_comb_pretty = "\\pbox{20cm}{"+f'VVV \\\\ {WC} @ $95\\%$ CL - SM \\\\ }}'
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
        coerced_dict[f'Bkg'].append(f'{val:0.2f}')
        if 'Bkg' in cols_err:
            eU = dfp[f'syst_quadrature_Up'].values
            eD = dfp[f'syst_quadrature_Down'].values
            eUD = (eU + eD) / 2.
            eS = dfp[f'MCstat'].values
            eSYST = (np.sum(eUD**2))**(1/2)
            eSTAT = (np.sum(eS**2))**(1/2)
            eTOT = (eSYST**2 + eSTAT**2)**(1/2)
            coerced_dict[f'Bkgerr'].append(f'{eTOT:0.2f}')
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
            self.bin_desc.append(f'${binlo:0.1f}-{binhi:0.1f}$')
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
            coerced_dict[f'Bkg'].append(f'{val:0.2f}')
            if 'Bkg' in cols_err:
                eU = dfp[f'syst_quadrature_Up'].values
                eD = dfp[f'syst_quadrature_Down'].values
                eUD = (eU + eD) / 2.
                eS = dfp[f'MCstat'].values
                eSYST = (np.sum(eUD**2))**(1/2)
                eSTAT = (np.sum(eS**2))**(1/2)
                eTOT = (eSYST**2 + eSTAT**2)**(1/2)
                coerced_dict[f'Bkgerr'].append(f'{eTOT:0.2f}')
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

    '''
    def make_table(self, method, caption='This is a caption.', label='tab:atable'):
        if method == 'default':
            self.keep_cols = self.df.columns
        else:
            raise ValueError(f'The "method"=="{method}" is not implemented. Please select from the avaialble methods: ["default",]')

        self._make_table_helper(caption, label)

    def _make_table_helper(self, caption, label):
        table = table_helper_dict['header']
        colstyles = []
        # here add any rules for different column styles
        for col in self.keep_cols:
            colstyles.append('c|')
        table += '\\begin{tabular}{|' + '|'.join(colstyles) + '}\n'
        # add column names
        colstrings = []
        for col in self.keep_cols:
            if col in ['bin_low', 'bin_high']:
                colstrings.append(f'{col} [GeV]')
            else:
                colstrings.append(f'{col}')
        table += '    '+'  &  '.join(colstrings) + ' \\\\ \n'
        table += table_helper_dict['hline']
        # add values
        df_ = self.df[self.keep_cols]
        first = True
        #for row in df_.itertuples():
        for i in range(len(df_)):
            row = df_.iloc[i]
            valuestrings = []
            for col in self.keep_cols:
                val = row[col]
                try:
                    val = float(val)
                    if val < -999:
                        val = '-'
                    else:
                        val = f'{val:0.2f}'
                except:
                    pass
                valuestrings.append(val)
            if not first:
                table += table_helper_dict['hline']
            table += '    $' + '$  &  $'.join(valuestrings) + '$ \\\\ \n'
            if first:
                first = False
        table += table_helper_dict['footer_template'].substitute(caption=caption, label=label)
        self.table = table

    def write_tex(self, texfilepath):
        with open(texfilepath, 'w') as f:
            f.write(self.table)
    '''
