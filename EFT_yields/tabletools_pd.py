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
    def __init__(self, tablefilepath):
        self.tablefilepath = tablefilepath
        self.load_df(tablefilepath)

    def load_df(self, tablefilepath):
        if '.pkl' in tablefilepath:
            self.df = pd.read_pickle(tablefilepath)
        elif '.csv' in tablefilepath:
            self.df = pd.read_csv(tablefilepath)
            self.df.fillna('', inplace=True)
        else:
            raise ValueError('Input table file must be either CSV (.csv) or pickle (.pkl).')

    def coerce_df_to_csv(self, channel, subchannel, statonly=True):
        if not statonly:
            raise NotImplementedError("Oops! Need to implement table with systematics still.")
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
        for p in procs:
            coerced_dict[f'{p}'] = []
            coerced_dict[f'{p}err'] = []
            cols_all.append(f'{p}')
            cols_all.append(f'{p}err')
        # make the inclusive row
        coerced_dict['Bin'].append(1)
        for p in procs:
            dfp = df_.query(f'process=="{p}"')
            val = dfp[f'yield'].sum()
            err = np.sum(dfp[f'MCstat'].values**2)**(1/2)
            coerced_dict[f'{p}'].append(f'{val:0.2f}')
            coerced_dict[f'{p}err'].append(f'{err:0.2f}')
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
        # print(coerced_dict)
        df_coerced = pd.DataFrame(coerced_dict)
        # print(df_coerced)
        df_coerced = df_coerced[cols_all]
        df_coerced.to_csv(os.path.join(ddir,'temp.csv'), index=False)

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
