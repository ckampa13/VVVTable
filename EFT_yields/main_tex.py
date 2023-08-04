def make_main_tex(mainfile, channel_file_list, channel_file_list_syst, channel_file_list_signal, subsection_list):
    text = '''\\documentclass[landscape, 12pt,letterpaper]{article}
\\usepackage[margin=0.5in]{geometry}
\\usepackage[utf8]{inputenc}
\\usepackage{rotating}
\\usepackage{pbox}

\\title{CMS VVV Yield Tables\\\\EFT Analysis}
\\author{}
\\date{\\today}

\\begin{document}

\\maketitle
\\thispagestyle{empty}

\\newpage

% Adding tables for each channel
\\section{Background Tables}
'''

    for chan, chan_syst, subsec in zip(channel_file_list, channel_file_list_syst, subsection_list):
        text += f'\\subsection{{{subsec}}}\n'
        text += f"\\input{{{chan}}}\n"
        text += f"\\input{{{chan_syst}}}\n"
        text += '\\newpage\n\n'

    text += '\n\n'

    # add signal section
    text += '\\section{Signal Tables}\n'

    for chan_signal, subsec in zip(channel_file_list_signal, subsection_list):
        text += f'\\subsection{{{subsec}}}\n'
        text += f"\\input{{{chan_signal}}}\n"
        # do I need a new page here?
        text += '\\newpage\n\n'

    text += '\n\n'

    text += '\\end{document}\n'
    with open(mainfile, 'w') as f:
        f.write(text)
