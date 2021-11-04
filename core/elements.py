import json
import pandas as pd
from pathlib import Path

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
    def __init__(self, dict):
        self._label = dict['A']
        self._position = dict['position']
        self._connected_nodes = dict['connected_nodes']
        self._successive  = {}

    @property
    def label(self):
        return self._label

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
    def __init__(self):
        self._label = str()
        self._length = float(0)
        self._successive = {}

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
        self._nodes = {}
        self._lines = {}
        with open(root/'resources'/'nodes.json') as f:
            nodes = json.load(f)







    def connect():
    # TODO this function has to set the successive attributes of all the network elements as dictionaries
    #  each node has a dict of lines and each line must have a dictionary of nodes

    def find_path(self, nodeStart, nodeEnd):
    # TODO this function returns all the paths that connects the two nodes

    def propagate(self, signal_information):
    # TODO this function has to propagate the signal_information through the path specified in it and returns the modified spectral information

    def draw(self):
    # TODO draw the graph using matplotlib