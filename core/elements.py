import enum
import json
import math
from pathlib import Path
import science_utils as sci_util
import matplotlib.pyplot as plt
import pandas as pd
from enum import Enum


class State(Enum):
    free = 1
    occupied = 2


class Signal_Information:
    def __init__(self, signal_power: float, path: list):
        self._signal_power: float = signal_power
        self._noise_power = float(0)
        self._latency = float(0)
        self._path: list = path

    # Instance Variables Getters
    @property
    def signal_power(self):
        return self._signal_power

    @property
    def noise_power(self):
        return self._noise_power

    @property
    def latency(self):
        return self._latency

    @property
    def path(self):
        return self._path

    # Instance Variables Setters
    @signal_power.setter
    def signal_power(self, signal_power):
        self._signal_power = signal_power

    @noise_power.setter
    def noise_power(self, noise_power):
        self._noise_power = noise_power

    @latency.setter
    def latency(self, latency):
        self._latency = latency

    @path.setter
    def path(self, path: list):
        self._path = path

    # Instance Methods
    def increment_signal_power(self, increment: float):
        self._signal_power += increment

    def increment_noise_power(self, increment: float):
        self._noise_power += increment

    def increment_latency(self, increment: float):
        self._latency += increment

    def remove_crossed_node(self):
        # removes the first label in the list path
        self._path.pop(0)


class Node:
    def __init__(self, label: str, dictionary: dict):
        self._label: str = label
        self._position: tuple = dictionary['position']
        self._connected_nodes: list = dictionary['connected_nodes']
        self._successive: dict = {}

    # Instance Variables Getters
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

    # Instance Variables Setters
    @label.setter
    def label(self, label: str):
        self._label = label

    @position.setter
    def position(self, pos):
        self._position = pos

    @connected_nodes.setter
    def connected_nodes(self, connected_nodes):
        self._connected_nodes = connected_nodes

    @successive.setter
    def successive(self, succ):
        self._successive = succ

    # Node Class Methods
    def propagate(self, sig_info_obj: Signal_Information):
        sig_info_obj.path.remove(self._label)  # path is a list
        if sig_info_obj.path.__len__() != 0:  # if this node is not the destination one
            self.successive[self._label + sig_info_obj.path[0]].propagate(sig_info_obj)


class Line:
    def __init__(self, label: str, length: float):
        self._label = label
        self._length = length
        self._successive: dict = {}
        self._state: State = State.free

    # Instance Variables Getters
    @property
    def state(self):
        return self._state
    @property
    def label(self):
        return self._label
    @property
    def length(self):
        return self._length
    @property
    def successive(self):
        return self._successive

    # Instance Variables Getters
    @state.setter
    def state(self, state: State):
        self._state = state
    @label.setter
    def label(self, label: str):
        self._label = label

    @length.setter
    def length(self, length: float):
        self._length = length

    @successive.setter
    def successive(self, successive: dict):
        self._successive = successive

    # Line Class Methods
    def latency_generation(self):
        return float(self._length / ((2 / 3) * sci_util.light_speed))

    def noise_generation(self, signal_power: float):
        return 1e-9 * signal_power * self._length

    def propagate(self, sig_info: Signal_Information):
        sig_info.increment_noise_power(self.noise_generation(sig_info.signal_power))
        sig_info.increment_latency(self.latency_generation())
        self.successive[sig_info.path[0]].propagate(sig_info)


class Connection:
    def __init__(self, inp: str, out: str, signal_power: float):
        self._input: str = inp
        self._output: str = out
        self._signal_power: float = sci_util.signal_power
        self._latency: float = 0  # has to be initialized to zero
        self._snr: float = 0    # has to be initialized to zero

    # Instance Variables Getters
    @property
    def input(self):
        return self._input
    @property
    def output(self):
        return self._output
    @property
    def signal_power(self):
        return self._signal_power
    @property
    def latency(self):
        return self._latency
    @property
    def snr(self):
        return self._snr

    # Instance Variables Setters
    @input.setter
    def input(self, inp: str):
        self._input = inp
    @output.setter
    def output(self, out: str):
        self._output = out
    @signal_power.setter
    def signal_power(self, sig_pow: float):
        self._signal_power = sig_pow
    @latency.setter
    def latency(self, latency: float):
        self._latency = latency
    @snr.setter
    def snr(self, snr: float):
        self._snr = snr


class Network:
    'Class that holds information about topology'

    def __init__(self):
        root = Path(__file__).parent.parent
        # DICTIONARY of LINES objects
        self._lines: dict = {}  # Dictionary of Line objects
        # DICTIONARY of NODES objects
        self._nodes: dict = {}  # Dictionary of Node objects
        # DATAFRAME FOR COLLECTING SPECTRAL INFORMATION
        self._weighted_paths: pd.DataFrame = pd.DataFrame(columns=['Path', 'Total_Latency', 'Total_Noise', 'SNR'])
        with open(root / 'resources/nodes.json') as f:
            json_dict = json.load(f)
        for key in json_dict.keys():
            self._nodes[key] = Node(key, json_dict[key])
            for neighbour in json_dict[key]['connected_nodes']:
                x1 = float(self._nodes[key].position[0])
                y1 = float(self._nodes[key].position[1])
                x2 = float(json_dict[neighbour]['position'][0])
                y2 = float(json_dict[neighbour]['position'][1])
                length = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
                self._lines[key + neighbour] = Line(key + neighbour, length)
        self.connect()
        self._init_weighted_paths()

    # Instance Variables Getters
    @property
    def weighted_paths(self):
        return self._weighted_paths

    @property
    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    # Instance Variables Setters
    @weighted_paths.setter
    def weighted_paths(self, dataframe: pd.DataFrame):
        self._weighted_paths = dataframe

    @nodes.setter
    def nodes(self, nodes):
        self._nodes = nodes

    @lines.setter
    def lines(self, lines):
        self._lines = lines

    # Network class Methods
    def connect(self):
        for node in self.nodes.values():
            for neighbour in node.connected_nodes:
                node.successive[node.label + neighbour] = self._lines[node.label + neighbour]
        for line in self._lines.values():
            line.successive[line.label[-1]] = self._nodes[line.label[-1]]

    def find_paths(self, nodeStart, nodeEnd) -> list:
        beingVisited = {}
        allPaths = []
        for node in self.nodes.keys():
            beingVisited[node] = False
        currentPath = [nodeStart]
        self.Depth_First_Search(nodeStart, nodeEnd, beingVisited, currentPath, allPaths)
        return allPaths

    def Depth_First_Search(self, nodeStart: str, nodeEnd: str, beingVisited: dict, currentPath: list, allPaths: list):
        beingVisited[nodeStart] = True
        if nodeStart == nodeEnd:
            allPaths.append(list(currentPath))
            return

        for neighbour in self.nodes[nodeStart].connected_nodes:
            if not beingVisited[neighbour]:
                currentPath.append(neighbour)
                self.Depth_First_Search(neighbour, nodeEnd, beingVisited, currentPath, allPaths)
                currentPath.remove(neighbour)
                beingVisited[neighbour] = False
        beingVisited[nodeStart] = False

    def propagate(self, signal_information: Signal_Information) -> Signal_Information:
        self._nodes[signal_information.path[0]].propagate(signal_information)
        return signal_information

    def _init_weighted_paths(self):
        # FOR EVERY POSSIBLE PATH PROPAGATE A SIGNAL
        for node in self._nodes.keys():
            for othernode in self._nodes.keys():
                if othernode != node:
                    all_paths_in_between = self.find_paths(node, othernode)
                    for path in all_paths_in_between:
                        signal = Signal_Information(sci_util.signal_power, list(path))
                        signal_after_propagation = self.propagate(signal)
                        self._weighted_paths = self._weighted_paths.append({'Path': '->'.join(path),
                                                                            'Total_Latency': signal_after_propagation.latency,
                                                                            'Total_Noise': signal_after_propagation.noise_power,
                                                                            'SNR': 10 * math.log(
                                                                                signal_after_propagation.signal_power / signal_after_propagation.noise_power)},
                                                                           ignore_index=True)

    def draw(self):
        for node in self._nodes.values():
            x1 = node.position[0]
            y1 = node.position[1]
            for neighbour in node.connected_nodes:
                x2 = self.nodes[neighbour].position[0]
                y2 = self.nodes[neighbour].position[1]
                plt.plot([x1 / 1e3, x2 / 1e3], [y1 / 1e3, y2 / 1e3], 'r', linewidth=0.3)
            plt.annotate(node.label, (node.position[0] / 1e3, node.position[1] / 1e3),
                         size=13,
                         xytext=(node.position[0] / 1e3, node.position[1] / 1e3 + 20),
                         color='b')
        plt.title(r'$Loaded\ Network\ Structure$')
        plt.xlabel(r'$x\ [km]$')
        plt.ylabel(r'$y\ [km]$')
        plt.grid()
        plt.show()

    def find_best_snr(self, start_node: str, dst_node: str) -> list[str]:
        routes = self._weighted_paths[self._weighted_paths.Path.str.startswith(start_node) &
                                      self._weighted_paths.Path.str.endswith(dst_node)]
        routes = routes.reset_index(drop=True)
        index_of_max_snr = routes['SNR'].idxmax()
        path = str(routes.iloc[[index_of_max_snr]]['Path'].values[0])
        path = path.split("->")
        # TODO
        #   path_is_available = True
        #    for i in range(len(path) - 1):
        #        if self.lines[path[i]+path[i+1]].state = elements.State.
        return path

    def find_best_latency(self, start_node: str, dst_node: str) -> list[str]:
        routes = self._weighted_paths[self._weighted_paths.Path.str.startswith(start_node) &
                                      self._weighted_paths.Path.str.endswith(dst_node)]
        routes = routes.reset_index(drop=True)
        index_of_min_latency = routes['Total_Latency'].idxmin()
        path = str(routes.iloc[[index_of_min_latency]]['Path'].values[0])
        path = path.split("->")
        return path

    def stream(self, connections_list : list[Connection], optimizeWhat: str = "latency"):
        if optimizeWhat == "latency":
            for connection in connections_list:
                path_with_lowest_latency = self.find_best_latency(connection.input, connection.output)
                sig = Signal_Information(connection.signal_power,path_with_lowest_latency)
                sig_after_propagation = self.propagate(sig)
                connection.latency = sig_after_propagation.latency
                connection.snr = 10 * math.log(sig_after_propagation.signal_power / sig_after_propagation.noise_power)
        elif optimizeWhat == "snr":
            for connection in connections_list:
                path_with_best_snr = self.find_best_snr(connection.input, connection.output)
                sig = Signal_Information(connection.signal_power, path_with_best_snr)
                sig_after_propagation = self.propagate(sig)
                connection.latency = sig_after_propagation.latency
                connection.snr = 10 * math.log(sig_after_propagation.signal_power / sig_after_propagation.noise_power)






