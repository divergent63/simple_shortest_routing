
"""

1. 已知O, D, 根据.net.xml中的connection（from, to）搜索可达路径.
2. 根据.net.xml中的edge（length）.
3. 求解所有可达路径的总长度, 并根据总长度确定最短路径.
"""
from lxml import etree
from pathlib import Path
import os
import sys

import logging
FORMAT = '[%(levelname)s: %(filename)s: %(lineno)4d]: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT, stream=sys.stdout)
logger = logging.getLogger(__name__)

import subprocess
import pandas as pd
import numpy as np


# read od info
path = Path(os.getcwd()) / 'conf' / 'veh_info_test.csv'
od = pd.read_csv(path).dropna()

# parse .net.xml
net_xml_dir = Path(os.getcwd()) / 'conf' / Path('test0.net.xml')
if os.path.exists(net_xml_dir):
    tree = etree.parse(str(net_xml_dir))

    edge_info_list = []
    for elem_ in tree.iter(tag='lane'):
        lane_id = elem_.attrib['id']

        if not lane_id.split(':')[0] == '':
            edge_id = elem_.attrib['id'].split('_')[0]
            length = elem_.attrib['length']
            edge_info_list.append([edge_id, length])

    connection_list = []
    for elem in tree.iter(tag='connection'):
        from_edge = elem.attrib['from']

        if not from_edge.split(':')[0] == '':
            to_edge = elem.attrib['to']
            connection_list.append([from_edge, to_edge])

potential_od_list = ['-gneE9', '-gneE12', '-gneE6', '-gneE3', 'gneE10', 'gneE7', 'gneE1', 'gneE4']

# parse nod file
nod_xml_dir = Path(os.getcwd()) / 'conf' / Path('test0.nod.xml')
if os.path.exists(nod_xml_dir):
    tree = etree.parse(str(nod_xml_dir))
    nodes_edge_len = []
    for elem_ in tree.iter(tag='link'):
        link_id = elem_.attrib['id']

        link_from = elem_.attrib['from']
        link_to = elem_.attrib['to']
        link_len = elem_.attrib['length']

        for k in range(len(edge_info_list)):
            if round(float(edge_info_list[k][1]), 2) == round(int(link_len) / 1000, 2):
                if str('-' + edge_info_list[k][0]) not in nodes_edge_len:
                    nodes_edge_len.append([link_id, edge_info_list[k][0], link_len, link_from, link_to])

else:
    print("nod file not exist!")

nodes_edge_len_df = pd.DataFrame(nodes_edge_len, columns=['link', 'edge', 'len', 'from_node', 'to_node'])
nodes_edge_len_df = nodes_edge_len_df.drop_duplicates(['link']).drop_duplicates(['edge'])


# def graph
from collections import defaultdict


class Graph():
    def __init__(self):
        """
        self.edges is a dict of all possible next nodes
        e.g. {'X': ['A', 'B', 'C', 'E'], ...}
        self.weights has all the weights between two nodes,
        with the two nodes as a tuple as the key
        e.g. {('X', 'A'): 7, ('X', 'B'): 2, ...}
        """
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        # Note: assumes edges are bi-directional
        """
        edges: 所有node具有的所有连接，如node 5具有的所有连接为['4', '6', '0', '9']
        :param from_node:
        :param to_node:
        :param weight:
        :return:
        """
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight


# shortest routing with dijsktra
def dijsktra(graph, initial, end):
    # shortest routes is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    """
        http://benalexkeen.com/implementing-djikstras-shortest-path-algorithm-with-python/
    :param graph:
    :param initial:
    :param end:
    :return:
    """
    logger.info("processing...")
    shortest_routes = {initial: (None, 0)}
    current_node = initial
    visited = set()

    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]            # destinations：当前节点的可能下一目的节点列表
        weight_to_current_node = shortest_routes[current_node][1]            # weight_to_current_node：destinations中当前节点至起点的距离权重

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node          # next_node的weight为当前节点至下一节点的距离权重与起点至当前节点的距离权重之和

            # 下一节点若不在shortest_routes中，则加入shortest_routes；若已经在，则对比旧的weight并更新shortest_paths
            if next_node not in shortest_routes:
                shortest_routes[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_routes[next_node][1]
                if current_shortest_weight > weight:
                    shortest_routes[next_node] = (current_node, weight)

        next_destinations = {node: shortest_routes[node] for node in shortest_routes if node not in visited}            # next_destinations：shortest_routes中未经过的节点集合
        if not next_destinations:
            return "Route Not Possible"
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])            # 更新当前节点，将next_destinations字典中值（weight）最小的键（node）作为下一代当前节点

    # Work back through destinations in shortest route
    route = []
    while current_node is not None:
        route.append(current_node)
        next_node = shortest_routes[current_node][0]
        current_node = next_node
    # Reverse route
    route = route[::-1]
    logger.info("processed")

    return route


# process
edges_new = [(nodes_edge_len_df['from_node'].values[i],
              nodes_edge_len_df['to_node'].values[i],
              float(nodes_edge_len_df['len'].values[i]) / 1000) for i in range(len(nodes_edge_len_df.values))]
graph = Graph()

for edge in edges_new:
    graph.add_edge(*edge)

for r in range(12):
    for r_ in range(12):
        shortest_route = dijsktra(graph, str(r), str(r_))
        if len(shortest_route) > 1:
            logger.info('shortest route is {}'.format(shortest_route))

