#!/usr/bin/env python3

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


DIR = '/static/images/network/'
EDGE_LENGTH_MATH = 150

nodes = []

nodes.append({'id': 1, 'label': 'IOS路由器', 'image': DIR + 'Router.png', 'shape': 'image'})
nodes.append({'id': 2, 'label': 'ASA防火墙', 'image': DIR + 'FW.png', 'shape': 'image'})
nodes.append({'id': 3, 'label': 'Core_SW', 'image': DIR + 'Core_SW.png', 'shape': 'image'})
nodes.append({'id': 4, 'label': 'Access_SW1', 'image': DIR + 'Switch.png', 'shape': 'image'})
nodes.append({'id': 5, 'label': 'Access_SW2', 'image': DIR + 'Switch.png', 'shape': 'image'})
nodes.append({'id': 6, 'label': 'Internet', 'image': DIR + 'Internet.png', 'shape': 'image'})

edges = []

edges.append({'from': 1, 'to': 2, 'length': EDGE_LENGTH_MATH, 'label': "E0/1 --- E0"})
edges.append({'from': 1, 'to': 6, 'length': EDGE_LENGTH_MATH, 'label': "E0/2 --- Internet"})
edges.append({'from': 2, 'to': 3, 'length': EDGE_LENGTH_MATH, 'label': "E1 --- E1/3"})
edges.append({'from': 3, 'to': 4, 'length': EDGE_LENGTH_MATH, 'label': "E1/2 --- E1/1"})
edges.append({'from': 3, 'to': 5, 'length': EDGE_LENGTH_MATH, 'label': "E1/1 --- E1/1"})


def devnet_topology(request):
    return render(request, 'devnet_topology.html')


def devnet_topology_json(request):
    return JsonResponse({'nodes': nodes, 'edges': edges})
