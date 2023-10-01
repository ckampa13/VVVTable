def make_main_tex(mainfile, texfile_lim_summary_dim6, texfile_lim_summary_dim8, channel_file_list, channel_file_list_syst, channel_file_list_signal_dict, WCs, WC_pretty_print_dict, subsection_list, subsection_signal_dict):
    text = '''\\documentclass[landscape, 12pt,letterpaper]{article}
\\usepackage[margin=0.5in]{geometry}
\\usepackage[utf8]{inputenc}
\\usepackage{rotating}
\\usepackage{pbox}
\\usepackage{amssymb}

\\title{CMS VVV Yield Tables\\\\EFT Analysis}
\\author{}
\\date{\\today}

'''

    # add in any WC commands
    for key, dict_ in WC_pretty_print_dict.items():
        WC_ = dict_['command']
        WCpret = dict_['tex'].replace("$", "")
        text += f'\\newcommand{WC_}'+'{\\ensuremath{'+WCpret+'}}\n'

    text += '''

\\begin{document}

\\maketitle
\\thispagestyle{empty}

\\newpage

\\section{Limits Summary Table}
'''
    # summary tables
    text += f'\\input{{{texfile_lim_summary_dim6}}}\n'
    text += f'\\input{{{texfile_lim_summary_dim8}}}\n'
    text += '\\newpage\n\n'

    # backgrounds
    text += '\\section{Background Tables}\n'
    for chan, chan_syst, subsec in zip(channel_file_list, channel_file_list_syst, subsection_list):
        text += f'\\subsection{{{subsec}}}\n'
        text += f"\\input{{{chan}}}\n"
        text += f"\\input{{{chan_syst}}}\n"
        text += '\\newpage\n\n'

    text += '\n\n'

    # add signal section
    text += '\\section{Signal Tables}\n'

    #for chan_signal, subsec in zip(channel_file_list_signal, subsection_list):
    for subsec in subsection_list:
        WCs_avail = subsection_signal_dict[subsec]
        text += f'\\subsection{{{subsec}}}\n'
        i = 0
        for WC in WCs:
            if WC in WCs_avail:
                i += 1
                chan_signal = channel_file_list_signal_dict[WC][subsec]
                text += f'\\subsubsection{{{WC}}}\n'
                text += f"\\input{{{chan_signal}}}\n\n"
                # if i % 2 == 0:
                #     text += '\\newpage\n\n'
                text += '\\newpage\n\n'
        text += '\\newpage\n\n'

    text += '\n\n'

    text += '\\end{document}\n'
    with open(mainfile, 'w') as f:
        f.write(text)
