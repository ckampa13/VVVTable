#!/bin/env python

import tabletools

tabletools.convert_csv("table_SRMCYield_SR-0l-2fj.csv",
                       "table_SRMCYield_SR-0l-2fj.tex",
                       bin_desc=[
                           "Bin [\\GeV]",
                           "Inclusive",
                           "$1100-2000$",
                           "2000-2500",
                           "2500-"],
                       caption="Yields per bin for SR-0l-2fj. Backgrounds shown are Monte Carlo yields with statistical uncertainty only, and are compared to signal yields for triboson processes (all combinations combined) with EFT enhancement from $\\ftz = 1.0 \\TeVmfour$. Yields are quoted for the 2018 dataset \\todo{update to full Run 2, also this binning scheme is a work in progress, as we'd like to increase boundary of the last bin in order to remove more background events.}",
                       label="tab:0l2fj_bins")

tabletools.convert_csv("table_SRMCYield_SR-0l-3fj.csv",
                       "table_SRMCYield_SR-0l-3fj.tex",
                       bin_desc=[
                           "Bin [\\GeV]",
                           "Inclusive"],
                       caption="Yields per bin for SR-0l-3fj. Backgrounds shown are Monte Carlo yields with statistical uncertainty only, and are compared to signal yields for triboson processes (all combinations combined) with EFT enhancement from $\\ftz = 1.0 \\TeVmfour$. There is no binning in this channel. Yields are quoted for 2018 \\todo{update to full Run 2} ",
                       label="tab:0l3fj_bins")

tabletools.convert_csv("table_SRMCYield_SR-1l-mu-2fj.csv",
                       "table_SRMCYield_SR-1l-mu-2fj.tex",
                       bin_desc=[
                           "Bin [\\GeV]",
                           "Inclusive",
                           "$800-2400$",
                           "2400-3000",
                           "3000-"],
                       caption="Yields per bin for SR-1l-mu-2fj on Muon channel. Backgrounds shown are Monte Carlo yields with statistical uncertainty only, and are compared to signal yields for WWW processes with EFT enhancement from $\\ftz = 0.2 \\TeVmfour$. ",
                       label="tab:1lmu2fj_bins")

tabletools.convert_csv("table_SRMCYield_SR-1l-el-2fj.csv",
                       "table_SRMCYield_SR-1l-el-2fj.tex",
                       bin_desc=[
                           "Bin [\\GeV]",
                           "Inclusive",
                           "$800-2400$",
                           "2400-3000",
                           "3000-"],
                       caption="Yields per bin for 1l2fj on Electron channel. Backgrounds shown are Monte Carlo yields with statistical uncertainty only, and are compared to signal yields for WWW processes with EFT enhancement from $\\ftz = 0.2 \\TeVmfour$. ",
                       label="tab:1lel2fj_bins")
