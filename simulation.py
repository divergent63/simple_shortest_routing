#!/usr/bin/env python
# coding=utf-8
"""

"""
import os
import subprocess
import sys
from pathlib import Path
import pandas as pd

try:
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))
    from sumolib import checkBinary

except ImportError:
    sys.exit(
        "please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')"
    )


def xml2csv():
    sumo_home = os.environ.get("SUMO_HOME")
    # SUMO_HOME=/usr/local/share/sumo-1.1.0         # in Ubuntu Server
    # SUMO_HOME=g:\software\SUMO\sumo-win64-1.0.1\sumo-1.0.1            # in Windows 10

    input_xml = Path(os.getcwd()) / 'conf' / 'fcd.xml'

    subprocess.call(
        "python " + str(sumo_home) + "/tools/xml/xml2csv.py " + str(input_xml) + " --separator ,",
        shell=True
    )


def fcd2veh_info():
    path = Path(os.getcwd()) / 'conf' / 'fcd.csv'
    fcd = pd.read_csv(path).dropna()

    veh_i_list = []
    for i, veh_id in enumerate(fcd['vehicle_id'].dropna().unique()):
        fcd_v0 = fcd.loc[fcd['vehicle_id'] == veh_id].sort_values(by=['timestep_time'])

        fcd_v0_id = fcd_v0['vehicle_id'].values[0]
        fcd_v0_O = \
        fcd_v0.loc[fcd_v0['timestep_time'] == fcd_v0['timestep_time'].values[0]]['vehicle_lane'].values[0].split('_')[0]
        fcd_v0_D = \
        fcd_v0.loc[fcd_v0['timestep_time'] == fcd_v0['timestep_time'].values[-1]]['vehicle_lane'].values[0].split('_')[
            0]
        fcd_v0_strat_time = fcd_v0['timestep_time'].values[0]
        fcd_v0_travel_time = fcd_v0['timestep_time'].values[-1] - fcd_v0['timestep_time'].values[0]
        route = list(fcd_v0['vehicle_lane'].unique())
        route_true = []
        for j in range(len(route)):
            if not route[j][0] == ':':
                route_true.append(route[j].split('_')[0])

        veh_i = [fcd_v0_id, fcd_v0_O, fcd_v0_D, fcd_v0_strat_time, fcd_v0_travel_time, route_true]
        veh_i_list.append(veh_i)

    veh_i_list_df = pd.DataFrame(veh_i_list, columns=['veh_id', 'O', 'D', 'start_time', 'travel_time', 'route'])

    veh_i_list_df_list = []
    for k in range(len(veh_i_list_df.values)):
        if not len(str(veh_i_list_df['route'].values[k]).split(',')) == 1:
            veh_i_list_df_list_true = veh_i_list_df.values[k]
            veh_i_list_df_list.append(veh_i_list_df_list_true)

    veh_i_list_df_ = pd.DataFrame(veh_i_list_df_list,
                                  columns=['veh_id', 'O', 'D', 'start_time', 'travel_time', 'route'])
    veh_i_list_df_['O'] = veh_i_list_df_['O'].astype(str)
    veh_i_list_df_['D'] = veh_i_list_df_['D'].astype(str)

    path_s = Path(os.getcwd()) / 'conf' / 'veh_info_test.csv'

    veh_i_list_df_csv = veh_i_list_df_
    veh_i_list_df_csv.to_csv(path_s)


if __name__ == '__main__':

    sumo_cmd = "sumo -c conf/test0.sumocfg --fcd-output conf/fcd.xml -W"
    subprocess.call(sumo_cmd, shell=True)

    xml2csv()

    fcd2veh_info()

