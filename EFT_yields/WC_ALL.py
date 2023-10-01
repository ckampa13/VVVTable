# FIXME! This should be tied to EFTAnalysis/EFTAnalysisFitting/scripts/VERSIONS_DICT.py-->WC_ALL
# WC_ALL = ['cW', 'cHW', 'cHWB', 'cHB', 'cHDD', 'cHbox','cHl3', 'cHq1', 'cHq3', 'cll1', 'cHu', 'cHd'] # all dim6
# WC_ALL = ['cT0', 'cM0'] # all dim8
WC_ALL = ['cW', 'cHW', 'cHWB', 'cHB', 'cHDD', 'cHbox','cHl3', 'cHq1', 'cHq3', 'cll1', 'cHu', 'cHd', 'cT0', 'cM0'] # all dim6 & dim8

WC_pretty_print_dict = {
    # dim6
    'cW': {'command':'\\cW', 'tex': r'$C_W$'},
    'cHq3': {'command':'\\cHqqq', 'tex': r'$C_{Hq3}$'},
    'cHq1': {'command':'\\cHq', 'tex': r'$C_{Hq1}$'},
    'cHu': {'command':'\\cHu', 'tex': r'$C_{Hu}$'},
    'cHd': {'command':'\\cHd', 'tex': r'$C_{Hd}$'},
    'cHW': {'command':'\\cHW', 'tex': r'$C_{HW}$'},
    'cHB': {'command':'\\cHB', 'tex': r'$C_{HB}$'},
    'cHWB': {'command':'\\cHWB', 'tex': r'$C_{HWB}$'},
    'cHl3': {'command':'\\cHlll', 'tex': r'$C_{Hl3}$'},
    'cll1': {'command':'\\cll', 'tex': r'$C_{ll1}$'},
    'cHbox': {'command':'\\cHbox', 'tex': r'$C_{H\square}$'},
    'cHDD': {'command':'\\cHDD', 'tex': r'$C_{HDD}$'},
    'cT0': {'command':'\\FTZero', 'tex': r'$f_{T0}$'},
    'cM0': {'command':'\\FMZero', 'tex': r'$f_{M0}$'},
}

# dimension 6 -- 81 ops
dim6_ops = [
    'cG', 'cGtil', 'cH', 'cHB', 'cHBtil', 'cHDD', 'cHG', 'cHGtil',
    'cHW', 'cHWB', 'cHWBtil', 'cHWtil', 'cHbox', 'cHd', 'cHe', 'cHl1',
    'cHl3', 'cHq1', 'cHq3', 'cHu', 'cHudAbs', 'cHudPh', 'cW', 'cWtil',
    'cdBAbs', 'cdBPh', 'cdGAbs', 'cdGPh', 'cdHAbs', 'cdHPh', 'cdWAbs', 'cdWPh',
    'cdd', 'cdd1', 'ceBAbs', 'ceBPh', 'ceHAbs', 'ceHPh', 'ceWAbs', 'ceWPh',
    'ced', 'cee', 'ceu', 'cld', 'cle', 'cledqAbs', 'cledqPh', 'clequ1Abs',
    'clequ1Ph', 'clequ3Abs', 'clequ3Ph', 'cll', 'cll1', 'clq1', 'clq3', 'clu',
    'cqd1', 'cqd8', 'cqe', 'cqq1', 'cqq11', 'cqq3', 'cqq31', 'cqu1',
    'cqu8', 'cquqd1Abs', 'cquqd1Ph', 'cquqd8Abs', 'cquqd8Ph', 'cuBAbs', 'cuBPh', 'cuGAbs',
    'cuGPh', 'cuHAbs', 'cuHPh', 'cuWAbs', 'cuWPh', 'cud1', 'cud8', 'cuu',
    'cuu1'
]
