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

