import os
import datetime
import pandas as pd
import numpy

import sys
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtWidgets import *
from data_process import *

SSV_THROUGHPUT_PERIOD = 60  # seconds

# 5G SSV KPI
SSV_NR_DL_THROUGHPUT_KPI = '5G-NR RLC Throughput NR-DL RLC DL RLC Throughput [Mbps]'
SSV_ENDC_DL_THROUGHPUT_KPI = '5G-NR EN-DC RLC Throughput DL RLC Throughput(Total PDU) Total DL RLC Throughput [Mbps]'
SSV_NR_UL_THROUGHPUT_KPI = '5G-NR RLC Throughput NR-UL RLC UL RLC Throughput [Mbps]'
SSV_ENDC_UL_THROUGHPUT_KPI = '5G-NR EN-DC RLC Throughput UL RLC Throughput(Total PDU) Total UL RLC Throughput [Mbps]'
# LTE SSV KPI
SSV_LTE_DL_THROUGHPUT_KPI = 'LTE KPI RLC DL Throughput [Mbps]'
#SSV_CA_DL_THROUGHPUT_KPI = 'LTE KPI RLC DL Throughput [Mbps]'
SSV_CA_DL_THROUGHPUT_KPI = 'LTE KPI PDCP DL Throughput [Mbps]'
SSV_LTE_UL_THROUGHPUT_KPI = 'LTE KPI RLC UL Throughput [Mbps]'
SSV_CA_UL_THROUGHPUT_KPI = 'LTE KPI RLC UL Throughput [Mbps]'
XCAL_TIME_STAMP = 'TIME_STAMP'

nr_ssv_dl_thp_export_list = [['Lon'],
                             ['Lat'],
                             ['5G-NR RLC Throughput NR-DL RLC DL RLC Throughput [Mbps]'],
                             ['5G-NR PCell RF Serving PCI'], ['5G-NR PCell RF NR-ARFCN'],
                             ['5G-NR PCell RF Serving SS-RSRP [dBm]'], ['5G-NR PCell RF Serving SS-SINR [dB]'],
                             ['5G-NR PCell Layer1 DL BLER [%]'], ['5G-NR PCell Layer1 DL Layer Num (Avg)'],
                             ['5G-NR PCell Layer1 DL MCS (Avg)'],
                             ['Qualcomm 5G-NR MAC PDSCH Info PCell RB Num[Avg]',
                              'Qualcomm 5G-NR MAC PDSCH Info PCell RB Num[Including 0]']]

nr_ssv_ul_thp_export_list = [['Lon'],
                             ['Lat'],
                             ['5G-NR RLC Throughput NR-UL RLC UL RLC Throughput [Mbps]'],
                             ['5G-NR PCell RF Serving PCI'], ['5G-NR PCell RF NR-ARFCN'], ['5G-NR PCell RF Serving SS-RSRP [dBm]'],
                             ['5G-NR PCell RF Serving SS-SINR [dB]'], ['5G-NR PCell Layer1 UL BLER [%]'],
                             ['5G-NR PCell Layer1 UL MCS (Avg)'],
                             ['5G-NR PCell Layer1 UL RB Num (Including 0)', '5G-NR PCell Layer1 UL RB Num (Avg)'],
                             ['Qualcomm 5G-NR MAC PUSCH Info PCell Layer Num[Avg]']]

endc_ssv_dl_thp_export_list = [['Lon'],
                               ['Lat'],
                               ['5G-NR EN-DC RLC Throughput DL RLC Throughput(Total PDU) Total DL RLC Throughput [Mbps]',
                                '5G-NR RLC Throughput NR-DL RLC DL RLC Throughput [Mbps]',
                                'LTE KPI RLC DL Throughput [Mbps]', 'LTE KPI PCell MAC DL Throughput [Mbps]'],
                               ['5G-NR PCell RF Serving PCI', 'LTE KPI PCell Serving PCI'],
                               ['5G-NR PCell RF NR-ARFCN'], ['LTE KPI PCell Serving EARFCN(DL)'],
                               ['5G-NR PCell RF Serving SS-RSRP [dBm]', 'LTE KPI PCell Serving RSRP [dBm]'],
                               ['5G-NR PCell RF Serving SS-SINR [dB]', 'LTE KPI PCell SINR [dB]'],
                               ['5G-NR PCell Layer1 DL Layer Num (Avg)', 'LTE KPI PCell WB RI'],
                               ['5G-NR PCell Layer1 DL MCS (Avg)', 'LTE KPI PCell DL MCS0', 'LTE KPI PCell DL MCS1'],
                               ['5G-NR PCell Layer1 DL RB Num (Avg)',
                                'Qualcomm 5G-NR MAC PDSCH Info PCell RB Num[Including 0]',
                                'LTE KPI PDSCH PRB Number(Avg)(Total)'],
                               ['5G-NR PCell Layer1 DL BLER [%]', 'LTE KPI PCell PDSCH BLER [%]']]

endc_ssv_ul_thp_export_list = [['Lon'],
                               ['Lat'],
                               ['5G-NR EN-DC RLC Throughput UL RLC Throughput(Total PDU) Total UL RLC Throughput [Mbps]',
                                '5G-NR RLC Throughput NR-UL RLC UL RLC Throughput [Mbps]',
                                'LTE KPI RLC UL Throughput [Mbps]'],
                               ['5G-NR PCell RF Serving PCI', 'LTE KPI PCell Serving PCI'],
                               ['5G-NR PCell RF NR-ARFCN'], ['LTE KPI PCell Serving EARFCN(DL)'],
                               ['5G-NR PCell RF Serving SS-RSRP [dBm]', 'LTE KPI PCell Serving RSRP [dBm]'],
                               ['5G-NR PCell RF Serving SS-SINR [dB]', 'LTE KPI PCell SINR [dB]'],
                               ['5G-NR PCell Layer1 UL MCS (Avg)', 'LTE KPI PCell UL MCS'],
                               ['5G-NR PCell Layer1 UL RB Num (Avg)', '5G-NR PCell Layer1 UL RB Num (Including 0)',
                                'LTE KPI PCell PUSCH PRB Number(Including 0)'],
                               ['5G-NR PCell Layer1 UL BLER [%]', 'LTE KPI PCell PUSCH BLER [%]'],
                               ['LTE KPI PCell Total Tx Power [dBm]', 'LTE KPI PCell PUSCH Power [dBm]'],
                               ['Qualcomm 5G-NR MAC PUSCH Info PCell Layer Num[Avg]']]

# lte_ssv_dl_thp_export_list = [['Lon'],
#                              ['Lat'],
#                               ['LTE KPI RLC DL Throughput [Mbps]', 'LTE KPI PCell MAC DL Throughput [Mbps]'],
#                               ['LTE KPI PCell Serving PCI'],
                               # ['LTE KPI PCell Serving EARFCN(DL)'],
#                               ['LTE KPI PCell Serving RSRP [dBm]'],
#                               ['LTE KPI PCell SINR [dB]'],
#                               ['LTE KPI PCell WB RI'],
#                               ['LTE KPI PCell DL MCS0', 'LTE KPI PCell DL MCS1'],
#                               ['LTE KPI PCell PDSCH PRB Number(Avg)'],
#                               ['LTE KPI PCell PDSCH BLER [%]']]

lte_ssv_dl_thp_export_list = [['Lon'],
                              ['Lat'],
                               ['LTE KPI RLC DL Throughput [Mbps]', 'LTE KPI MAC DL Throughput [Mbps]'], #'APP All FWD Throughput (kbps)'],
                               ['LTE KPI PCell Serving PCI'],
                               ['LTE KPI PCell Serving EARFCN(DL)'],
                               ['LTE KPI PCell Serving RSRP [dBm]'],
                               ['LTE KPI PCell SINR [dB]'],
                               ['LTE KPI PCell WB RI'],
                               ['LTE KPI PCell DL MCS0', 'LTE KPI PCell DL MCS1'],
                               ['LTE KPI PCell PDSCH PRB Number(Avg)', 'LTE KPI PCell PDSCH PRB Number(Including 0)'],
                               ['LTE KPI PCell PDSCH BLER [%]'],
                               ['LTE KPI PCell PUSCH BLER [%]'],
                               ['LTE KPI PCell WB CQI CW0', 'LTE KPI PCell WB CQI CW1']]

lte_ssv_ul_thp_export_list = [['Lon'],
                               ['Lat'],
                               ['LTE KPI RLC UL Throughput [Mbps]'], #'APP All RVS Throughput (kbps)'],
                               ['LTE KPI PCell Serving PCI'],
                               ['LTE KPI PCell Serving EARFCN(DL)'],
                               ['LTE KPI PCell Serving RSRP [dBm]'],
                               ['LTE KPI PCell SINR [dB]'],
                               ['LTE KPI PCell UL MCS'],
                               ['LTE KPI PCell PUSCH PRB Number(Avg)', 'LTE KPI PCell PUSCH PRB Number(Including 0)'],
                               ['LTE KPI PCell PDSCH BLER [%]'],
                               ['LTE KPI PCell PUSCH BLER [%]'],
                               ['LTE KPI PCell Total Tx Power [dBm]', 'LTE KPI PCell PUSCH Power [dBm]']]
                               #['LL1 Uplink Info PCell Path Loss [dB]']]

lte_ssv_ca_dl_thp_export_list = [['Lon'],
                               ['Lat'],
                               [#'APP All FWD Throughput (kbps)',
                                'LTE KPI RLC DL Throughput [Mbps]',
                                'LTE KPI PCell MAC DL Throughput [Mbps]',
                                'LTE KPI SCell[1] SCell[1] MAC DL Throughput [Mbps]',
                                'LTE KPI SCell[2] SCell[2] MAC DL Throughput [Mbps]',
                                'LTE KPI SCell[3] SCell[3] MAC DL Throughput [Mbps]',
                                'LTE KPI SCell[4] SCell[4] MAC DL Throughput [Mbps]'],
                               ['LTE KPI PCell Serving PCI', 'LTE KPI SCell[1] SCell[1] Serving PCI',
                                'LTE KPI SCell[2] SCell[2] Serving PCI', 'LTE KPI SCell[3] SCell[3] Serving PCI',
                                'LTE KPI SCell[4] SCell[4] Serving PCI'],
                               ['LTE KPI PCell Serving EARFCN(DL)',
                                'LTE KPI SCell[1] SCell[1] Serving EARFCN(DL)',
                                'LTE KPI SCell[2] SCell[2] Serving EARFCN(DL)', 'LTE KPI SCell[3] SCell[3] Serving EARFCN(DL)',
                                'LTE KPI SCell[4] SCell[4] Serving EARFCN(DL)'],
                               ['LTE KPI PCell Serving RSRP [dBm]', 'LTE KPI SCell[1] SCell[1] Serving RSRP [dBm]',
                                'LTE KPI SCell[2] SCell[2] Serving RSRP [dBm]', 'LTE KPI SCell[3] SCell[3] Serving RSRP [dBm]',
                                'LTE KPI SCell[4] SCell[4] Serving RSRP [dBm]'],
                               ['LTE KPI PCell SINR [dB]', 'LTE KPI PCell SINR [dB]', 'LTE KPI SCell[1] SCell[1] SINR [dB]',
                                'LTE KPI SCell[2] SCell[2] SINR [dB]', 'LTE KPI SCell[3] SCell[3] SINR [dB]',
                                'LTE KPI SCell[4] SCell[4] SINR [dB]'],
                               ['LTE KPI PCell WB RI', 'LTE KPI PCell WB RI', 'LTE KPI SCell[1] SCell[1] WB RI',
                                'LTE KPI SCell[2] SCell[2] WB RI', 'LTE KPI SCell[3] SCell[3] WB RI',
                                'LTE KPI SCell[4] SCell[4] WB RI'],
                               ['LTE KPI PCell DL MCS0', 'LTE KPI SCell[1] SCell[1] DL MCS0', 'LTE KPI SCell[2] SCell[2] DL MCS0',
                                'LTE KPI SCell[3] SCell[3] DL MCS0', 'LTE KPI SCell[4] SCell[4] DL MCS0'],
                               ['LTE KPI PCell DL MCS1', 'LTE KPI SCell[1] SCell[1] DL MCS1', 'LTE KPI SCell[2] SCell[2] DL MCS1',
                                'LTE KPI SCell[3] SCell[3] DL MCS1', 'LTE KPI SCell[4] SCell[4] DL MCS1'],
                               ['LTE KPI PCell PDSCH PRB Number(Avg)', 'LTE KPI SCell[1] SCell[1] PDSCH PRB Number(Avg)',
                                'LTE KPI SCell[2] SCell[2] PDSCH PRB Number(Avg)', 'LTE KPI SCell[3] SCell[3] PDSCH PRB Number(Avg)',
                                'LTE KPI SCell[4] SCell[4] PDSCH PRB Number(Avg)'],
                               ['LTE KPI PCell PDSCH PRB Number(Including 0)', 'LTE KPI SCell[1] SCell[1] PDSCH PRB Number(Including 0)',
                                'LTE KPI SCell[2] SCell[2] PDSCH PRB Number(Including 0)', 'LTE KPI SCell[3] SCell[3] PDSCH PRB Number(Including 0)',
                                'LTE KPI SCell[4] SCell[4] PDSCH PRB Number(Including 0)'],
                               ['LTE KPI PCell PDSCH BLER [%]', 'LTE KPI SCell[1] SCell[1] PDSCH BLER [%]',
                                'LTE KPI SCell[2] SCell[2] PDSCH BLER [%]', 'LTE KPI SCell[3] SCell[3] PDSCH BLER [%]',
                                'LTE KPI SCell[4] SCell[4] PDSCH BLER [%]'],
                               ['LTE KPI PCell WB CQI CW0', 'LTE KPI PCell WB CQI CW1'],
                               ['LTE KPI SCell[1] SCell[1] WB CQI CW0', 'LTE KPI SCell[1] SCell[1] WB CQI CW1'],
                               ['LTE KPI SCell[2] SCell[2] WB CQI CW0', 'LTE KPI SCell[2] SCell[2] WB CQI CW1'],
                               ['LTE KPI SCell[3] SCell[3] WB CQI CW0', 'LTE KPI SCell[3] SCell[3] WB CQI CW1'],
                               ['LTE KPI SCell[4] SCell[4] WB CQI CW0', 'LTE KPI SCell[4] SCell[4] WB CQI CW1']]

lte_ssv_ca_ul_thp_export_list = [['Lon'],
                               ['Lat'],
                               [#'APP All RVS Throughput (kbps)',
                                'LTE KPI RLC UL Throughput [Mbps]',
                                'LTE KPI PCell MAC UL Throughput [Mbps]',
                                'LTE KPI SCell[1] SCell[1] MAC UL Throughput [Mbps]'],
                               ['LTE KPI PCell Serving EARFCN(DL)',
                                'LTE KPI SCell[1] SCell[1] Serving EARFCN(DL)'],
                               ['LTE KPI PCell Serving PCI', 'LTE KPI SCell[1] SCell[1] Serving PCI'],
                               ['LTE KPI PCell Serving RSRP [dBm]', 'LTE KPI SCell[1] SCell[1] Serving RSRP [dBm]'],
                               ['LTE KPI PCell SINR [dB]', 'LTE KPI SCell[1] SCell[1] SINR [dB]'],
                               ['LTE KPI PCell UL MCS', 'LTE KPI SCell[1] SCell[1] UL MCS'],
                               ['LTE KPI PCell PUSCH PRB Number(Avg)', 'LTE KPI SCell[1] SCell[1] PUSCH PRB Number(Avg)'],
                               ['LTE KPI PCell PUSCH BLER [%]', 'LTE KPI SCell[1] SCell[1] PUSCH BLER [%]'],
                               ['LTE KPI PCell Total Tx Power [dBm]', 'LTE KPI SCell[1] SCell[1] Total Tx Power [dBm]'],
                               ['LTE KPI PCell PUSCH Power [dBm]', 'LTE KPI SCell[1] SCell[1] PUSCH Power [dBm]']]

endc_DT_dl_thp_export_list = [['Lon'],
                               ['Lat'],
                               ['5G-NR EN-DC RLC Throughput DL RLC Throughput(Total PDU) Total DL RLC Throughput [Mbps]',
                                '5G-NR RLC Throughput NR-DL RLC DL RLC Throughput [Mbps]',
                                'LTE KPI RLC DL Throughput [Mbps]', 'LTE KPI PCell MAC DL Throughput [Mbps]'],
                               ['5G-NR PCell RF Serving PCI', 'LTE KPI PCell Serving PCI'],
                               ['5G-NR PCell RF NR-ARFCN'], ['LTE KPI PCell Serving EARFCN(DL)'],
                               ['5G-NR PCell RF Serving SS-RSRP [dBm]', 'LTE KPI PCell Serving RSRP [dBm]'],
                               ['5G-NR PCell RF Serving SS-SINR [dB]', 'LTE KPI PCell SINR [dB]'],
                               ['5G-NR PCell Layer1 DL Layer Num (Avg)', 'LTE KPI PCell WB RI'],
                               ['5G-NR PCell Layer1 DL MCS (Avg)', 'LTE KPI PCell DL MCS0', 'LTE KPI PCell DL MCS1'],
                               ['5G-NR PCell Layer1 DL RB Num (Avg)',
                                '5G-NR MAC PDSCH Info PCell RB Num[Including 0]',
                                'LTE KPI PDSCH PRB Number(Avg)(Total)'],
                               ['5G-NR PCell Layer1 DL BLER [%]', 'LTE KPI PCell PDSCH BLER [%]']]

Spark_DT_ENDC_DL_Export_list = [['Lon'], ['Lat'],
                                ['5G KPI Total Info Layer2 PDCP DL Throughput(+Split Bearer) [Mbps]',
                                '5G KPI Total Info Layer2 RLC DL Throughput [Mbps]',
                                '5G KPI Total Info Layer2 MAC DL Throughput [Mbps]',
                                'LTE KPI MAC DL Throughput [Mbps]'],
                                ['5G-NR PCell RF Serving PCI', 'LTE KPI PCell Serving PCI'],
                                ['5G-NR PCell RF Serving SS-RSRP [dBm]', 'LTE KPI PCell Serving RSRP [dBm]'],
                                ['5G-NR PCell RF Serving SS-SINR [dB]', 'LTE KPI PCell SINR [dB]'],
                                ['5G-NR PCell RF Serving SS-RSRQ [dB]', 'LTE KPI PCell Serving RSRQ [dB]'],
                                ['5G-NR PCell RF RI', 'LTE KPI PCell WB RI'],
                                ['5G-NR PCell Layer1 DL MCS (Avg)', 'LTE KPI PCell DL MCS0', 'LTE KPI PCell DL MCS1'],
                                ['5G-NR PCell Layer1 DL RB Num (Avg)',
                                '5G-NR PCell Layer1 DL RB Num (Including 0)',
                                'LTE KPI PCell PDSCH PRB Number(Avg)'],
                                ['5G-NR PCell Layer1 DL BLER [%]', 'LTE KPI PCell PDSCH BLER [%]'],
                              ['5G-NR PCell RF CQI', 'LTE KPI PCell WB CQI CW0', 'LTE KPI PCell WB CQI CW1']]

Spark_DT_ENDC_UL_Export_list = [['Lon'], ['Lat'],
                                ['5G-NR Total Info Layer2 PDCP UL Throughput(+Split Bearer) [Mbps]',
                                '5G-NR Total Info Layer2 RLC DL Throughput [Mbps]',
                                '5G-NR Total Info Layer2 MAC DL Throughput [Mbps]',
                                'LTE KPI MAC UL Throughput [Mbps]'],
                                ['5G-NR PCell RF Serving PCI', 'LTE KPI PCell Serving PCI'],
                                ['5G-NR PCell RF Serving SS-RSRP [dBm]', 'LTE KPI PCell Serving RSRP [dBm]'],
                                ['5G-NR PCell RF Serving SS-SINR [dB]', 'LTE KPI PCell SINR [dB]'],
                                ['5G-NR PCell RF Serving SS-RSRQ [dB]', 'LTE KPI PCell Serving RSRQ [dB]'],
                                ['5G-NR PCell RF PUSCH Power [dBm]', 'LTE KPI PCell PUSCH Power [dBm]',
                                 'LTE KPI PCell Total Tx Power [dBm]'],
                                ['5G-NR PCell Layer1 UL MCS (Avg)', 'LTE KPI PCell UL MCS'],
                                ['5G-NR PCell Layer1 DL RB Num (Avg)',
                                '5G-NR PCell Layer1 DL RB Num (Including 0)',
                                'LTE KPI PCell PUSCH PRB Number(Avg)'],
                                ['5G-NR PCell Layer1 DL BLER [%]', 'LTE KPI PCell PUSCH BLER [%]']]

Spark_DT_NR_DL_Export_list = [['Lon'],
                               ['Lat'],
                               ['5G KPI Total Info Layer2 PDCP DL Throughput(+Split Bearer) [Mbps]',
                                '5G KPI Total Info Layer2 RLC DL Throughput [Mbps]', 'LTE KPI MAC DL Throughput [Mbps]'],
                               ['5G-NR PCell RF Serving PCI', 'LTE KPI PCell Serving PCI'],
                               ['5G-NR PCell RF Serving SS-RSRP [dBm]', 'LTE KPI PCell Serving RSRP [dBm]'],
                               ['5G-NR PCell RF Serving SS-SINR [dB]', 'LTE KPI PCell SINR [dB]'],
                               ['5G-NR PCell RF Serving SS-RSRQ [dB]', 'LTE KPI PCell Serving RSRQ [dB]'],
                               ['5G-NR PCell RF RI', 'LTE KPI PCell WB RI'],
                               ['5G-NR PCell Layer1 DL MCS (Avg)', 'LTE KPI PCell DL MCS0', 'LTE KPI PCell DL MCS1'],
                               ['5G-NR PCell Layer1 DL RB Num (Avg)',
                                '5G-NR PCell Layer1 DL RB Num (Including 0)',
                                'LTE KPI PCell PDSCH PRB Number(Avg)'],
                               ['5G-NR PCell Layer1 DL BLER [%]', 'LTE KPI PCell PDSCH BLER [%]'],
                              ['5G-NR PCell RF CQI', 'LTE KPI PCell WB CQI CW0', 'LTE KPI PCell WB CQI CW1']]

Spark_DT_NR_DL_Export_list2 = [['Lon'],
                               ['Lat'],
                               ['5G-NR Total Info Layer2 PDCP DL Throughput(+Split Bearer) [Mbps]',
                                '5G-NR Total Info Layer2 RLC DL Throughput [Mbps]', 'LTE KPI MAC DL Throughput [Mbps]'],
                               ['5G-NR PCell RF Serving PCI', 'LTE KPI PCell Serving PCI'],
                               ['5G-NR PCell RF Serving SS-RSRP [dBm]', 'LTE KPI PCell Serving RSRP [dBm]'],
                               ['5G-NR PCell RF Serving SS-SINR [dB]', 'LTE KPI PCell SINR [dB]'],
                               ['5G-NR PCell RF Serving SS-RSRQ [dB]', 'LTE KPI PCell Serving RSRQ [dB]'],
                               ['5G-NR PCell RF RI', 'LTE KPI PCell WB RI'],
                               ['5G-NR PCell Layer1 DL MCS (Avg)', 'LTE KPI PCell DL MCS0', 'LTE KPI PCell DL MCS1'],
                               ['5G-NR PCell Layer1 DL RB Num (Avg)',
                                '5G-NR PCell Layer1 DL RB Num (Including 0)',
                                'LTE KPI PCell PDSCH PRB Number(Avg)'],
                               ['5G-NR PCell Layer1 DL BLER [%]', 'LTE KPI PCell PDSCH BLER [%]'],
                              ['5G-NR PCell RF CQI', 'LTE KPI PCell WB CQI CW0', 'LTE KPI PCell WB CQI CW1']]

Spark_DT_NR_UL_Export_list = [['Lon'],
                               ['Lat'],
                               ['5G KPI Total Info Layer2 PDCP UL Throughput(+Split Bearer) [Mbps]',
                                '5G KPI Total Info Layer2 RLC UL Throughput [Mbps]', 'LTE KPI MAC UL Throughput [Mbps]',
                                '5G KPI Total Info Layer2 MAC UL Throughput [Mbps]', 'LTE KPI RLC UL Throughput [Mbps]'],
                               ['5G-NR PCell RF Serving PCI', 'LTE KPI PCell Serving PCI'],
                               ['5G-NR PCell RF Serving SS-RSRP [dBm]', 'LTE KPI PCell Serving RSRP [dBm]'],
                               ['5G-NR PCell RF Serving SS-SINR [dB]', 'LTE KPI PCell SINR [dB]'],
                               ['5G-NR PCell RF Serving SS-RSRQ [dB]', 'LTE KPI PCell Serving RSRQ [dB]'],
                               ['5G-NR PCell RF PUSCH Power [dBm]', 'LTE KPI PCell PUSCH Power [dBm]', 'LTE KPI PCell Total Tx Power [dBm]'],
                               ['5G-NR PCell Layer1 UL MCS (Avg)', 'LTE KPI PCell UL MCS'],
                               ['5G-NR PCell Layer1 UL RB Num (Avg)',
                                '5G-NR PCell Layer1 UL RB Num (Including 0)',
                                'LTE KPI PCell PUSCH PRB Number(Avg)'],
                               ['5G-NR PCell Layer1 UL BLER [%]', 'LTE KPI PCell PDSCH BLER [%]']]

Spark_DT_LTE_DL_Export_list = [['Lon'],
                               ['Lat'],
                               ['LTE KPI MAC DL Throughput [Mbps]'],
                               ['LTE KPI PCell Serving PCI'],
                               ['LTE KPI PCell Serving RSRP [dBm]'],
                               ['LTE KPI PCell SINR [dB]'],
                               ['LTE KPI PCell Serving RSRQ [dB]'],
                               ['LTE KPI PCell WB RI'],
                               ['LTE KPI PCell DL MCS0', 'LTE KPI PCell DL MCS1'],
                               ['LTE KPI PCell PDSCH PRB Number(Avg)'],
                               ['LTE KPI PCell PDSCH BLER [%]'],
                               ['LTE KPI PCell WB CQI CW0'],
                               ['LTE KPI PCell WB CQI CW1']]

Spark_DT_ENDC_DL_Export_list_New = [['Lon'], ['Lat'],
                                ['5G KPI Total Info Layer2 PDCP DL Throughput(+Split Bearer) [Mbps]',
                                '5G KPI Total Info Layer2 RLC DL Throughput [Mbps]',
                                '5G KPI Total Info Layer2 MAC DL Throughput [Mbps]',
                                'LTE KPI MAC DL Throughput [Mbps]'],
                                ['5G-NR PCell RF Serving PCI', 'LTE KPI PCell Serving PCI'],
                                ['5G-NR PCell RF Serving SS-RSRP [dBm]', 'LTE KPI PCell Serving RSRP [dBm]'],
                                ['5G-NR PCell RF Serving SS-SINR [dB]', 'LTE KPI PCell SINR [dB]'],
                                ['5G-NR PCell RF Serving SS-RSRQ [dB]', 'LTE KPI PCell Serving RSRQ [dB]'],
                                ['5G-NR PCell RF RI', 'LTE KPI PCell WB RI'],
                                ['5G-NR PCell Layer1 DL MCS (Avg)', 'LTE KPI PCell DL MCS0', 'LTE KPI PCell DL MCS1'],
                                ['5G-NR PCell Layer1 DL RB Num (Avg)',
                                '5G-NR PCell Layer1 DL RB Num (Including 0)',
                                'LTE KPI PCell PDSCH PRB Number(Avg)'],
                                ['5G-NR PCell Layer1 DL BLER [%]', 'LTE KPI PCell PDSCH BLER [%]'],
                              ['5G-NR PCell RF CQI', 'LTE KPI PCell WB CQI CW0', 'LTE KPI PCell WB CQI CW1']]

Spark_DT_ENDC_DL_Export_list_New2 = [['Lon'], ['Lat'],
                                ['5G-NR Total Info Layer2 PDCP DL Throughput(+Split Bearer) [Mbps]',
                                '5G-NR Total Info Layer2 RLC DL Throughput [Mbps]',
                                '5G-NR Total Info Layer2 MAC DL Throughput [Mbps]',
                                'LTE KPI MAC DL Throughput [Mbps]'],
                                ['5G-NR PCell RF Serving PCI', 'LTE KPI PCell Serving PCI'],
                                ['5G-NR PCell RF Serving SS-RSRP [dBm]', 'LTE KPI PCell Serving RSRP [dBm]'],
                                ['5G-NR PCell RF Serving SS-SINR [dB]', 'LTE KPI PCell SINR [dB]'],
                                ['5G-NR PCell RF Serving SS-RSRQ [dB]', 'LTE KPI PCell Serving RSRQ [dB]'],
                                ['5G-NR PCell RF RI', 'LTE KPI PCell WB RI'],
                                ['5G-NR PCell Layer1 DL MCS (Avg)', 'LTE KPI PCell DL MCS0', 'LTE KPI PCell DL MCS1'],
                                ['5G-NR PCell Layer1 DL RB Num (Avg)',
                                '5G-NR PCell Layer1 DL RB Num (Including 0)',
                                'LTE KPI PCell PDSCH PRB Number(Avg)'],
                                ['5G-NR PCell Layer1 DL BLER [%]', 'LTE KPI PCell PDSCH BLER [%]'],
                              ['5G-NR PCell RF CQI', 'LTE KPI PCell WB CQI CW0', 'LTE KPI PCell WB CQI CW1']]

Spark_DT_Beamforming_DL_Export_list = [['Lon'], ['Lat'],
                                ['5G-NR Total Info Layer2 PDCP DL Throughput(+Split Bearer) [Mbps]',
                                '5G-NR Total Info Layer2 RLC DL Throughput [Mbps]',
                                '5G-NR Total Info Layer2 MAC DL Throughput [Mbps]',
                                'LTE KPI MAC DL Throughput [Mbps]'],
                                ['5G-NR PCell RF Serving PCI', 'LTE KPI PCell Serving PCI'],
                                ['5G-NR PCell RF Serving SS-RSRP [dBm]', '5G-NR PCell RF Best Beam SS-RSRP [dBm]', 'LTE KPI PCell Serving RSRP [dBm]'],
                                ['5G-NR PCell RF Serving SS-SINR [dB]', '5G-NR PCell RF Best Beam SS-SINR [dBm]', 'LTE KPI PCell SINR [dB]'],
                                ['5G-NR PCell RF Serving SS-RSRQ [dB]', 'LTE KPI PCell Serving RSRQ [dB]'],
                                ['5G-NR PCell RF RI', 'LTE KPI PCell WB RI'],
                                ['5G-NR PCell Layer1 DL MCS (Avg)', 'LTE KPI PCell DL MCS0', 'LTE KPI PCell DL MCS1'],
                                ['5G-NR PCell Layer1 DL RB Num (Avg)',
                                '5G-NR PCell Layer1 DL RB Num (Including 0)',
                                'LTE KPI PCell PDSCH PRB Number(Avg)'],
                                ['5G-NR PCell Layer1 DL BLER [%]', 'LTE KPI PCell PDSCH BLER [%]'],
                              ['5G-NR PCell RF CQI', 'LTE KPI PCell WB CQI CW0', 'LTE KPI PCell WB CQI CW1']]

Spark_DT_Beamforming_DL_Export_list_2 = [['Lon'], ['Lat'],
                                ['5G KPI Total Info Layer2 PDCP DL Throughput(+Split Bearer) [Mbps]',
                                '5G KPI Total Info Layer2 RLC DL Throughput [Mbps]',
                                '5G KPI Total Info Layer2 MAC DL Throughput [Mbps]',
                                'LTE KPI MAC DL Throughput [Mbps]'],
                                ['5G-NR PCell RF Serving PCI', 'LTE KPI PCell Serving PCI'],
                                ['5G-NR PCell RF Serving SS-RSRP [dBm]', '5G-NR PCell RF Best Beam SS-RSRP [dBm]', 'LTE KPI PCell Serving RSRP [dBm]'],
                                ['5G-NR PCell RF Serving SS-SINR [dB]', '5G-NR PCell RF Best Beam SS-SINR [dBm]', 'LTE KPI PCell SINR [dB]'],
                                ['5G-NR PCell RF Serving SS-RSRQ [dB]', 'LTE KPI PCell Serving RSRQ [dB]'],
                                ['5G-NR PCell RF RI', 'LTE KPI PCell WB RI'],
                                ['5G-NR PCell Layer1 DL MCS (Avg)', 'LTE KPI PCell DL MCS0', 'LTE KPI PCell DL MCS1'],
                                ['5G-NR PCell Layer1 DL RB Num (Avg)',
                                '5G-NR PCell Layer1 DL RB Num (Including 0)',
                                'LTE KPI PCell PDSCH PRB Number(Avg)'],
                                ['5G-NR PCell Layer1 DL BLER [%]', 'LTE KPI PCell PDSCH BLER [%]'],
                              ['5G-NR PCell RF CQI', 'LTE KPI PCell WB CQI CW0', 'LTE KPI PCell WB CQI CW1']]

Spark_DT_Beamforming_DL_Export_list_2_no_BF = [['Lon'], ['Lat'],
                                ['5G KPI Total Info Layer2 PDCP DL Throughput(+Split Bearer) [Mbps]',
                                '5G KPI Total Info Layer2 RLC DL Throughput [Mbps]',
                                '5G KPI Total Info Layer2 MAC DL Throughput [Mbps]',
                                'LTE KPI MAC DL Throughput [Mbps]'],
                                ['5G-NR PCell RF Serving PCI', 'LTE KPI PCell Serving PCI'],
                                ['5G-NR PCell RF Serving SS-RSRP [dBm]', 'LTE KPI PCell Serving RSRP [dBm]'],
                                ['5G-NR PCell RF Serving SS-SINR [dB]', 'LTE KPI PCell SINR [dB]'],
                                ['5G-NR PCell RF Serving SS-RSRQ [dB]', 'LTE KPI PCell Serving RSRQ [dB]'],
                                ['5G-NR PCell RF RI', 'LTE KPI PCell WB RI'],
                                ['5G-NR PCell Layer1 DL MCS (Avg)', 'LTE KPI PCell DL MCS0', 'LTE KPI PCell DL MCS1'],
                                ['5G-NR PCell Layer1 DL RB Num (Avg)',
                                '5G-NR PCell Layer1 DL RB Num (Including 0)',
                                'LTE KPI PCell PDSCH PRB Number(Avg)'],
                                ['5G-NR PCell Layer1 DL BLER [%]', 'LTE KPI PCell PDSCH BLER [%]'],
                              ['5G-NR PCell RF CQI', 'LTE KPI PCell WB CQI CW0', 'LTE KPI PCell WB CQI CW1']]

Spark_DT_Beamforming_UL_Export_list = [['Lon'], ['Lat'],
                                ['5G-NR Total Info Layer2 PDCP UL Throughput(+Split Bearer) [Mbps]',
                                '5G-NR Total Info Layer2 RLC UL Throughput [Mbps]',
                                '5G-NR Total Info Layer2 MAC UL Throughput [Mbps]',
                                'LTE KPI MAC UL Throughput [Mbps]'],
                                ['5G-NR PCell RF Serving PCI', 'LTE KPI PCell Serving PCI'],
                                ['5G-NR PCell RF Serving SS-RSRP [dBm]', '5G-NR PCell RF Best Beam SS-RSRP [dBm]', 'LTE KPI PCell Serving RSRP [dBm]'],
                                ['5G-NR PCell RF Serving SS-SINR [dB]', '5G-NR PCell RF Best Beam SS-SINR [dBm]', 'LTE KPI PCell SINR [dB]'],
                                ['5G-NR PCell RF Serving SS-RSRQ [dB]', 'LTE KPI PCell Serving RSRQ [dB]', 'LTE KPI PCell Serving RSRQ [dB]'],
                                ['5G-NR PCell RF PUSCH Power [dBm]', 'LTE KPI PCell PUSCH Power [dBm]',
                                 'LTE KPI PCell Total Tx Power [dBm]'],
                                ['5G-NR PCell Layer1 UL MCS (Avg)', 'LTE KPI PCell UL MCS'],
                                ['5G-NR PCell Layer1 UL RB Num (Avg)',
                                '5G-NR PCell Layer1 UL RB Num (Including 0)',
                                'LTE KPI PCell PUSCH PRB Number(Avg)'],
                                ['5G-NR PCell Layer1 UL BLER [%]', 'LTE KPI PCell PUSCH BLER [%]'],
                                ['5G-NR PCell RF Pathloss [dB]'],
                                ['PCell Summary Serving Distance']]

Spark_DT_Beamforming_UL_Export_list_2 = [['Lon'], ['Lat'],
                                ['5G KPI Total Info Layer2 PDCP UL Throughput(+Split Bearer) [Mbps]',
                                '5G KPI Total Info Layer2 RLC UL Throughput [Mbps]',
                                '5G KPI Total Info Layer2 MAC UL Throughput [Mbps]',
                                'LTE KPI MAC UL Throughput [Mbps]'],
                                ['5G-NR PCell RF Serving PCI', 'LTE KPI PCell Serving PCI'],
                                ['5G-NR PCell RF Serving SS-RSRP [dBm]', '5G-NR PCell RF Best Beam SS-RSRP [dBm]', 'LTE KPI PCell Serving RSRP [dBm]'],
                                ['5G-NR PCell RF Serving SS-SINR [dB]', '5G-NR PCell RF Best Beam SS-SINR [dBm]', 'LTE KPI PCell SINR [dB]'],
                                ['5G-NR PCell RF Serving SS-RSRQ [dB]', 'LTE KPI PCell Serving RSRQ [dB]', 'LTE KPI PCell Serving RSRQ [dB]'],
                                ['5G-NR PCell RF PUSCH Power [dBm]', 'LTE KPI PCell PUSCH Power [dBm]',
                                 'LTE KPI PCell Total Tx Power [dBm]'],
                                ['5G-NR PCell Layer1 UL MCS (Avg)', 'LTE KPI PCell UL MCS'],
                                ['5G-NR PCell Layer1 UL RB Num (Avg)',
                                '5G-NR PCell Layer1 UL RB Num (Including 0)',
                                'LTE KPI PCell PUSCH PRB Number(Avg)'],
                                ['5G-NR PCell Layer1 UL BLER [%]', 'LTE KPI PCell PUSCH BLER [%]'],
                                ['5G-NR PCell RF Pathloss [dB]'],
                                ['PCell Summary Serving Distance']]

Spark_DT_ENDC_UL_Export_list_New = [['Lon'], ['Lat'],
                                ['5G-NR Total Info Layer2 PDCP UL Throughput(+Split Bearer) [Mbps]',
                                '5G-NR Total Info Layer2 RLC UL Throughput [Mbps]',
                                '5G-NR Total Info Layer2 MAC UL Throughput [Mbps]',
                                'LTE KPI MAC UL Throughput [Mbps]'],
                                ['5G-NR PCell RF Serving PCI', 'LTE KPI PCell Serving PCI'],
                                ['5G-NR PCell RF Serving SS-RSRP [dBm]', 'LTE KPI PCell Serving RSRP [dBm]'],
                                ['5G-NR PCell RF Serving SS-SINR [dB]', 'LTE KPI PCell SINR [dB]'],
                                ['5G-NR PCell RF Serving SS-RSRQ [dB]', 'LTE KPI PCell Serving RSRQ [dB]'],
                                ['5G-NR PCell RF PUSCH Power [dBm]', 'LTE KPI PCell PUSCH Power [dBm]',
                                 'LTE KPI PCell Total Tx Power [dBm]'],
                                ['5G-NR PCell Layer1 UL MCS (Avg)', 'LTE KPI PCell UL MCS'],
                                ['5G-NR PCell Layer1 UL RB Num (Avg)',
                                '5G-NR PCell Layer1 UL RB Num (Including 0)',
                                'LTE KPI PCell PUSCH PRB Number(Avg)'],
                                ['5G-NR PCell Layer1 UL BLER [%]', 'LTE KPI PCell PUSCH BLER [%]']]

nr_sinr_bin_size = numpy.arange(-9.5, 30.5, 1)
nr_rsrp_bin_size = numpy.arange(-130.5, -40.5, 1)
nr_pl_bin_size = numpy.arange(60.5, 160.5, 1)
nr_pusch_power_bin_size = numpy.arange(-1.5, 23.5, 1)

lte_sinr_bin_size = numpy.arange(-5.5, 30.5, 1)
lte_rsrp_bin_size = numpy.arange(-124.5, -40.5, 1)

distance_bin_size = numpy.arange(0, 1000, 10)

DT_TYPE = '4G_DT'
if DT_TYPE == '4G_DT':
# Drive Test Data Input for Feilding
    SINR_BIN_SIZE = lte_sinr_bin_size
    RSRP_BIN_SIZE = lte_rsrp_bin_size
    SINR_BIN_KPI = 'LTE KPI PCell SINR [dB]'
    RSRP_BIN_KPI = 'LTE KPI PCell Serving RSRP [dBm]'
    AREA_BINNING_SIZE = 20
    STATISTICS_LIST = lte_ssv_dl_thp_export_list
    dt_trace = "C:\Work\Spark_5G\Dunedin\Field_Test\DN2\\Pre_TC9_CA_DL_PS LONG CALL_KPIs Export_DN2_RSRP Filter.xlsx"

if DT_TYPE == '5G_DT':
# Drive Test Data Input for 5G20A feature
    SINR_BIN_SIZE = nr_sinr_bin_size
    RSRP_BIN_SIZE = nr_rsrp_bin_size
    RSRP_BIN_SIZE_2 = lte_rsrp_bin_size
    PL_BIN_SIZE = nr_pl_bin_size
    DISTANCE_BIN_SIZE = distance_bin_size
    PUSCH_POWER_BIN_SIZE = nr_pusch_power_bin_size
    SINR_BIN_KPI = '5G-NR PCell RF Serving SS-SINR [dB]'
    RSRP_BIN_KPI = '5G-NR PCell RF Serving SS-RSRP [dBm]'
    RSRP_BIN_KPI_2 = 'LTE KPI PCell Serving RSRP [dBm]'
    PL_BIN_KPI = '5G-NR PCell RF Pathloss [dB]'
    NR_PUSCH_POWER_BIN_KPI = '5G-NR PCell RF PUSCH Power [dBm]'
    DISTANCE_BIN_KPI = 'PCell Summary Serving Distance'
    AREA_BINNING_SIZE = 10
    # STATISTICS_LIST = Spark_DT_ENDC_DL_Export_list_New
    # STATISTICS_LIST = Spark_DT_ENDC_DL_Export_list_New2
    STATISTICS_LIST = Spark_DT_Beamforming_DL_Export_list_2_no_BF
    dt_trace = 'C:\Work\Spark_5G\Dunidin\Acceptance\Spark_Golden_Cluster\Palmerston_North_nonBF\DL_NR\\drive9_nr_dl_thp_0ocns_pure_5g.xlsx'


filename = "C:\Work\Spark_5G\Golden_Cluster\Test\SSV\\5g\cjas\s2\cjas_s2_dl_endc_2nd_device_info.xlsx"

trace_folder = "C:\Work\Spark_5G\Feilding\Test\SSV\Post_Swap\CFDS\Process"

#dt_trace = 'C:\Work\Spark_5G\Golden_Cluster\Test\DriveTest\Report\\5G_dl_long_data_call\Drive4_NR_DL_Long_Data_Call.xlsx'

filetype = 'XCAP'

#site_list = ['cter', 'ckvg', 'cmil', 'clov', 'ctak', 'cpnx', 'cjas', 'cpae']
#sector_list = ['s1', 's2', 's3']
#calltype_list = ['5g', 'endc']
#direction_list = ['dl', 'ul']
#site_list = ['CFDE', 'CFDS', 'CFET', 'CFLD']
#site_list = ['CFET']
site_list = ['CFDE', 'CFDS', 'CFET', 'CFLD']
sector_list = ['S1', 'S2', 'S3']
calltype_list = ['L700', 'L1800', 'L2600', 'L2300', 'CA']
#calltype_list = ['L2600', 'CA']
direction_list = ['DL', 'UL']

def ssv_kpi_summary(path):

    # assert kpi path is valid
    if not os.path.isdir(path):
        print('Please choose a kpi folder')
        exit(1)

    # Create folder for saving result and create final result file
    result_folder = os.path.join(path, 'SSV_Result_' + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    if not os.path.exists(result_folder):
        os.mkdir(result_folder)
    result_output_file = os.path.join(result_folder, 'SSV_Result.xlsx')

    print('======= Start SSV KPI analysis =======')

    # Create folder for saving result and create final result file
    trace_file_list = os.listdir(path)

    # Seperate uplink or downlink test first
    for direction in direction_list:
        direction_matching = [i for i in trace_file_list if direction in i]
        dbg_print(direction_matching)

        # Seperate different carrier secondly
        for calltype in calltype_list:
            calltype_matching = [i for i in direction_matching if calltype in i]
            dbg_print(calltype_matching)
            if not calltype_matching:
                continue

            tab_name = str(direction) + '_' + str(calltype)

            if direction == 'ul' or direction == 'UL':
                if calltype == '5g':
                    export_kpi_list = nr_ssv_ul_thp_export_list
                    searching_kpi_list = SSV_NR_UL_THROUGHPUT_KPI
                elif calltype == 'endc':
                    export_kpi_list = endc_ssv_ul_thp_export_list
                    searching_kpi_list = SSV_ENDC_UL_THROUGHPUT_KPI
                elif calltype == 'L700' or calltype == 'L1800' or calltype == 'L2600' or calltype == 'L2300':
                    export_kpi_list = lte_ssv_ul_thp_export_list
                    searching_kpi_list = SSV_LTE_UL_THROUGHPUT_KPI
                elif calltype == 'CA':
                    export_kpi_list = lte_ssv_ca_ul_thp_export_list
                    searching_kpi_list = SSV_CA_UL_THROUGHPUT_KPI
                else:
                    dbg_print('wrong calltype')
                    exit(1)
            elif direction == 'dl' or direction == 'DL':
                if calltype == '5g':
                    export_kpi_list = nr_ssv_dl_thp_export_list
                    searching_kpi_list = SSV_NR_DL_THROUGHPUT_KPI
                elif calltype == 'endc':
                    export_kpi_list = endc_ssv_dl_thp_export_list
                    searching_kpi_list = SSV_ENDC_DL_THROUGHPUT_KPI
                elif calltype == 'L700' or calltype == 'L1800' or calltype == 'L2600' or calltype == 'L2300':
                    export_kpi_list = lte_ssv_dl_thp_export_list
                    searching_kpi_list = SSV_LTE_DL_THROUGHPUT_KPI
                elif calltype == 'CA':
                    export_kpi_list = lte_ssv_ca_dl_thp_export_list
                    searching_kpi_list = SSV_CA_DL_THROUGHPUT_KPI
                else:
                    dbg_print('wrong calltype')
                    exit(1)
            else:
                dbg_print('wrong direction')
                exit(1)

            data_final = pd.DataFrame()

            for site in site_list:
                site_matching = [i for i in calltype_matching if site in i]
                dbg_print(site_matching)
                if not site_matching:
                    continue

                for sector in sector_list:
                    sector_matching = [i for i in site_matching if sector in i]
                    dbg_print(sector_matching)
                    if not sector_matching:
                        continue

                    for trace_file in sector_matching:
                        print('========== Analyzing Trace: ', trace_file, '==========')

                        result_output_file_charts = os.path.join(result_folder,
                                                                 trace_file.split('.')[0] + '_ssv_chart.pdf')

                        data = load_data(os.path.join(path, trace_file), filetype)


                        if 'APP All FWD Throughput (kbps)' in data.columns:
                            data['APP All FWD Throughput (kbps)'] = data['APP All FWD Throughput (kbps)'].apply(lambda x: x/1000)

                        if 'APP All FWD Throughput (kbps)' in data.columns:
                            data['APP All RVS Throughput (kbps)'] = data['APP All RVS Throughput (kbps)'].apply(lambda x: x/1000)

                        best_ssv_avg_data, best_ssv_avg_timestamp = calculate_best_avg_ssv_kpi(data, XCAL_TIME_STAMP,
                                                                                               searching_kpi_list,
                                                                                               SSV_THROUGHPUT_PERIOD)
                        best_ssv_max_data, best_ssv_max_timestamp = calculate_best_avg_ssv_kpi(data, XCAL_TIME_STAMP,
                                                                                               searching_kpi_list,
                                                                                               1)

                        data_all = pd.concat([best_ssv_avg_data.mean().to_frame().transpose(), best_ssv_max_data])

                        data_all.insert(loc=0, column='tracefile', value=[trace_file, trace_file])

                        data_final = data_final.append(data_all)

                        plot_ssv_kpi_to_pdf(result_output_file_charts, data, XCAL_TIME_STAMP,
                                            export_kpi_list, best_ssv_avg_timestamp, SSV_THROUGHPUT_PERIOD)

            if not data_final.empty:
                write_data_to_excel(result_output_file, tab_name, data_final, export_kpi_list)

def drive_test_post_process(tracefile):
    if not os.path.exists(tracefile):
        print('Trace file does not exist')
        exit(1)

    data = load_data(tracefile, filetype)

    rsrp_curve_datafile = os.path.join(os.path.dirname(tracefile),
                                    os.path.basename(tracefile).split('.')[0] + '_rsrp_curve.xlsx')
    rsrp_curve_datafile_2 = os.path.join(os.path.dirname(tracefile),
                                    os.path.basename(tracefile).split('.')[0] + '_rsrp_curve_2.xlsx')
    sinr_curve_datafile = os.path.join(os.path.dirname(tracefile),
                                    os.path.basename(tracefile).split('.')[0] + '_sinr_curve.xlsx')
    pl_curve_datafile = os.path.join(os.path.dirname(tracefile),
                                    os.path.basename(tracefile).split('.')[0] + '_pathloss_curve.xlsx')
    nr_pusch_power_datafile = os.path.join(os.path.dirname(tracefile),
                                    os.path.basename(tracefile).split('.')[0] + '_nr_pusch_power_curve.xlsx')
    distance_datafile = os.path.join(os.path.dirname(tracefile),
                                    os.path.basename(tracefile).split('.')[0] + '_distance_curve.xlsx')
    binning_datafile = os.path.join(os.path.dirname(tracefile),
                                    os.path.basename(tracefile).split('.')[0] + '_binning.xlsx')
    statistics_datafile = os.path.join(os.path.dirname(tracefile),
                                       os.path.basename(tracefile).split('.')[0] + '_statistics.xlsx')
    plot_datafile = os.path.join(os.path.dirname(tracefile),
                                 os.path.basename(tracefile).split('.')[0] + '_plotting.pdf')
    geoplotting_datafile = os.path.join(os.path.dirname(tracefile), os.path.basename(tracefile).split('.')[0] + '_geoplotting.html')

    binning_data = sample_spatial_binning(data, AREA_BINNING_SIZE, binning_datafile, 'median')

    sample_plot_on_map(binning_data, RSRP_BIN_KPI, geoplotting_datafile, '')

    plot_dt_kpi_to_pdf(plot_datafile, binning_data, XCAL_TIME_STAMP, STATISTICS_LIST)

    sample_discrete(binning_data, RSRP_BIN_KPI, RSRP_BIN_SIZE, 'median', rsrp_curve_datafile)
    sample_discrete(binning_data, SINR_BIN_KPI, SINR_BIN_SIZE, 'median', sinr_curve_datafile)
    if DT_TYPE == '5G_DT':
        sample_discrete(binning_data, RSRP_BIN_KPI_2, RSRP_BIN_SIZE_2, 'median', rsrp_curve_datafile_2)
        sample_discrete(binning_data, PL_BIN_KPI, PL_BIN_SIZE, 'median', pl_curve_datafile)
        sample_discrete(binning_data, NR_PUSCH_POWER_BIN_KPI, PUSCH_POWER_BIN_SIZE, 'median', nr_pusch_power_datafile)
        sample_discrete(binning_data, DISTANCE_BIN_KPI, DISTANCE_BIN_SIZE, 'median', distance_datafile)

    statistics_dt_kpi_to_excel(statistics_datafile, binning_data, STATISTICS_LIST)


def show_message_box(text, message_type):
    msg = QMessageBox()

    if message_type == "Question":
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Question")
    elif message_type == "Warning":
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Warning")
    elif message_type == "Critical":
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Critical")
    else: # "Information"
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Information")

    msg.setText(text)
    #msg.setInformativeText("This is additional information")
    #msg.setDetailedText("The details are as follows:")
    #msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    msg.exec_()


class DataProcessMainWindow(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.fileList = QStringListModel()
        self.setWindowTitle("Data Processing")
        self.resize(1200, 800)
        self.centralWidget = QLabel("Hello, World")
        self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.centralWidget)

        self._create_actions()
        self._create_menu_bar()
        self._create_widget()
        self._connect_actions()


    def _create_actions(self):
        # Creating action using the first constructor
        self.importAction = QAction(self)
        self.importAction.setText("&Import...")
        # Creating actions using the second constructor
        self.exportAction = QAction("E&xport...", self)
        self.exitAction = QAction("&Exit", self)
        self.copyAction = QAction("&Copy", self)
        self.pasteAction = QAction("&Paste", self)
        self.cutAction = QAction("C&ut", self)
        self.helpContentAction = QAction("&Help Content", self)
        self.aboutAction = QAction("&About", self)

    def _create_menu_bar(self):
        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)
        # Creating menus using a QMenu object
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        # Creating menus using a title
        editMenu = menuBar.addMenu("&Edit")
        helpMenu = menuBar.addMenu("&Help")
        #fileMenu.addMenu("&Import...")
        #fileMenu.addMenu("&Exit")

        fileMenu.addAction(self.importAction)
        fileMenu.addAction(self.exportAction)
        fileMenu.addAction(self.exitAction)

    def _connect_actions(self):
        # Connect File actions
        self.importAction.triggered.connect(self.import_data)
        self.exportAction.triggered.connect(self.export_data)

    def _create_widget(self):
        vlayout = QVBoxLayout()
        self.dataListView = QListView()
        self.dataListView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dataListView.setModel(self.fileList)
        self.dock = QDockWidget("Data List", self)
        self.dock.setWidget(self.dataListView)
        self.addDockWidget(Qt.TopDockWidgetArea, self.dock)

        #self.setLayout(vlayout)

    def import_data(self):
        # Logic for opening an existing file goes here...
        self.centralWidget.setText("<b>File > Import...</b> clicked")
        self.open_filename_dialog()

    def export_data(self):
        # Logic for opening an existing file goes here...
        self.centralWidget.setText("<b>File > Export...</b> clicked")

    def open_filename_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            if not fileName in self.fileList.stringList():
                self.centralWidget.setText(fileName)
                self.fileList.insertRow(0)
                self.fileList.setData(self.fileList.index(0), fileName)
            else:
                show_message_box(fileName + " has been loaded.", "Information")

if __name__ == '__main__':

    # best_ssv_avg_data, best_ssv_avg_timestamp = calculate_best_avg_ssv_kpi(data, XCAL_TIME_STAMP, SSV_DL_THROUGHPUT_KPI,
    #                                                                       SSV_THROUGHPUT_PERIOD)

    #best_ssv_max_data, best_ssv_max_timestamp = calculate_best_avg_ssv_kpi(data, XCAL_TIME_STAMP, SSV_DL_THROUGHPUT_KPI,
    #                                                                       1)

    #data_all = pd.concat([best_ssv_avg_data.mean().to_frame().transpose(), best_ssv_max_data])
    #write_data_to_excel(result_output_file, 'Result', data_all, endc_ssv_dl_thp_export_list)

    #plot_ssv_kpi_to_pdf(result_output_file_charts, data, XCAL_TIME_STAMP, endc_ssv_dl_thp_export_list, best_ssv_avg_timestamp, SSV_THROUGHPUT_PERIOD)
    #ssv_kpi_summary(trace_folder)

    app = QApplication(sys.argv)
    win = DataProcessMainWindow()
    win.show()
    sys.exit(app.exec_())
    #drive_test_post_process(dt_trace)




