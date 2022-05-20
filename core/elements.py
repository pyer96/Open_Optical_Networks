import json
import math
import pandas as pd
from pathlib import Path
test
class Signal_Information:
    def __init__(self, path :list):
        self._signal_power  =   float(10)
        self._noise_power   =   float(0)
        self._latency       =   float(0)
        self._path          =   path
    @property
    def signal_power(self):
            return self._signal_power
    @signal_power.setter
    def signal_power(self, signal_power):
            self._signal_power = signal_power
    @property
    def noise_power(self):
        return self._noise_power
    @noise_power.setter
    def noise_power(self, noise_power):
        self._noise_power = noise_power
    @property
    def latency(self):
        return self._latency
    @latency.setter
    def latency(self, latency):
        self._latency = latency
    @property
    def path(self):
        return self.path
    @path.setter
    def path(self, path):
        self._path = path

class Node:
    def __init__(self, label, dict):
        self._label = label
        self._position = dict['position']
        self._connected_nodes = dict['connected_nodes']
        self._successive  = {}
    @property
    def label(self):
        return self._label
    @property
    def position(self):
        return self._position
    @property
    def connected_nodes(self):
        return self._connected_nodes
    @property
    def successive(self):
        return self._successive
    @successive.setter
    def successive(self, succ):
        self._successive =  succ

    def propagate(self, sig_info_obj :Signal_Information):
        sig_info_obj.path.remove(self._label)
        sig_info_obj.path[0].propagate(sig_info_obj)

class Line:
    def __init__(self, label, length):
        self._label = label
        self._length = length
        self._successive = {}

    @property
    def label(self):
        return self._label

    @property
    def successive(self):
        return self._successive
    @successive.setter
    def successive(self, successive):
        self._successive = successive
    def latency_generation(self):
        return float(self._length / ((2/3)*3e8))

    def noise_generation(self, signal_power):
        return 1e-9 * signal_power * self._length

    def propagate(self, sig_info :Signal_Information):
        sig_info.noise_power = sig_info.noise_power + self.noise_generation(sig_info.signal_power)
        sig_info.latency = sig_info.latency + self.latency_generation()
        # TODO
        #  self._successive[0].propagate()

class Network:
    def __init__(self):
        root = Path(__file__).parent.parent
        self._lines = {}
        self._nodes = {}
        with open(root/'resources/nodes.json') as f:
            json_dict = json.load(f)
        for key in json_dict.keys():
            self._nodes[key] = Node(key, json_dict[key])
            for neighbour in json_dict[key]['connected_nodes']:
                x1 = float(self._nodes[key].position[0])
                y1 = float(self._nodes[key].position[1])
                x2 = float(json_dict[neighbour]['position'][0])
                y2 = float(json_dict[neighbour]['position'][1])
                length = math.sqrt(math.pow(x1-x2, 2) + math.pow(y1-y2, 2))
                self._lines[key+neighbour] = Line(key+neighbour, length)

    @property
    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    def connect(self):
        for node in self.nodes.values():
            for neighbour in node.connected_nodes:
                node.successive[node.label+neighbour] = self.lines[node.label+neighbour]
        for line in self._lines.values():
            line.successive[line.label[-1]] = self.nodes[line.label[-1]]

    def find_paths(self, nodeStart, nodeEnd):
        beingVisited = {}
        allPaths = []
        for node in self.nodes.keys():
            beingVisited[node] = False
        currentPath = [nodeStart]
        self.Depth_First_Search(nodeStart, nodeEnd, beingVisited, currentPath, allPaths)


    def Depth_First_Search(self, nodeStart, nodeEnd, beingVisited, currentPath, allPaths):
        beingVisited[nodeStart] = True
        if nodeStart == nodeEnd:
            allPaths.append(currentPath)
            print(allPaths)
            return

        for neighbour in self.nodes[nodeStart].connected_nodes:
            if not beingVisited[neighbour]:
                currentPath.append(neighbour)
                self.Depth_First_Search(neighbour, nodeEnd, beingVisited, currentPath, allPaths)
                currentPath.remove(neighbour)
                beingVisited[neighbour] = False
        beingVisited[nodeStart] = False


    #def propagate(self, signal_information):
        #TODO this function has to propagate the signal_information through the path specified in it and returns the modified spectral information

    #def draw(self):
        #TODO draw the graph using matplotlib