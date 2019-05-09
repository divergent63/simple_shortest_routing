#!/usr/bin/env python
# coding=utf-8
"""

"""
from lxml import etree
from pathlib import Path
import os
import pandas as pd


def gen_trips(od):
    start_time = od['start_time'].values

    root = etree.Element("routes")
    for i in range(len(od.values)):

        veh_id = str(i)

        route = od['route'].values[i]
        route = route.split("'")
        route_list = []
        for j in range(len(route)):
            if len(route[j]) > 3:
                route_list.append(route[j])

        if len(route_list) == 4:
            route = str(route_list[0]) + ' ' + str(route_list[1]) + str(' ') + str(route_list[2]) + ' ' + str(route_list[3])
        if len(route_list) == 3:
            route = str(route_list[0]) + ' ' + str(route_list[1]) + str(' ') + str(route_list[2])
        if len(route_list) == 2:
            route = str(route_list[0]) + ' ' + str(route_list[1])

        root_1 = etree.SubElement(root, "vehicle", id=str(veh_id), depart=str(start_time[i] * 10))

        child_11 = etree.SubElement(
            root_1, "route", edges=route
        )

    with open(Path(Path(os.getcwd()) / 'conf' / Path('test0_trips.trips.xml')), 'w') as e_data:
        print(etree.tostring(root, pretty_print=True, encoding='unicode'), file=e_data)


if __name__ == '__main__':
    path = Path(os.getcwd()) / 'conf' / 'veh_info.csv'
    od = pd.read_csv(path).dropna()

    gen_trips(od)
