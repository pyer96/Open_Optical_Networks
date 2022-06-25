import json
import math
from pathlib import Path
import science_utils as sci_util
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import parameters as params



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


class Lightpath(Signal_Information):
    def __init__(self, signal_power: float, path: list, channel: int):
        Signal_Information.__init__(self, signal_power, path)
        self._channel = channel

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, ch: int):
        self._channel = ch


class Node:
    def __init__(self, label: str, dictionary: dict):
        self._label: str = label
        self._position: tuple = dictionary['position']
        self._connected_nodes: list = dictionary['connected_nodes']
        self._successive: dict = {}
        self._switching_matrix = None

    # Instance Variables Getters
    @property
    def switching_matrix(self):
        return self._switching_matrix

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

    @switching_matrix.setter
    def switching_matrix(self, switching_matrix):
        self._switching_matrix = switching_matrix

    @connected_nodes.setter
    def connected_nodes(self, connected_nodes):
        self._connected_nodes = connected_nodes

    @successive.setter
    def successive(self, succ):
        self._successive = succ

    # Node Class Methods
    def propagate(self, lightpath: Lightpath):
        lightpath.path.remove(self._label)  # path is a list
        if lightpath.path.__len__() != 0:  # if this node is not the destination one
            self.successive[self._label + lightpath.path[0]].propagate(lightpath)

    def probe(self, sig_info: Signal_Information):
        sig_info.path.remove(self._label)   # path is a list
        if sig_info.path.__len__() != 0:
            self.successive[self._label + sig_info.path[0]].probe(sig_info)


class Line:
    def __init__(self, label: str, length: float):
        self._label = label
        self._length = length
        self._successive: dict = {}
        self._state: list[str] = ['free', 'free', 'free', 'free', 'free', 'free', 'free', 'free', 'free', 'free']

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
    def state(self, state: list[str]):
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

    def probe(self, sig_info: Signal_Information):
        sig_info.increment_noise_power(self.noise_generation(sig_info.signal_power))
        sig_info.increment_latency(self.latency_generation())
        self.successive[sig_info.path[0]].probe(sig_info)

    def propagate(self, lightpath: Lightpath):
        # set the corresponding channel as occupied
        self._state[lightpath.channel] = 'occupied'
        lightpath.increment_noise_power(self.noise_generation(lightpath.signal_power))
        lightpath.increment_latency(self.latency_generation())
        self.successive[lightpath.path[0]].propagate(lightpath)


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
        self._route_space: pd.DataFrame = pd.DataFrame(columns=['Path', 'Channel_Occupancy'])
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
        self._init_route_space()

    # Instance Variables Getters
    @property
    def weighted_paths(self):
        return self._weighted_paths

    @property
    def route_space(self):
        return self._route_space
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

    @route_space.setter
    def route_space(self, dataframe: pd.DataFrame):
        self._route_space = dataframe

    @nodes.setter
    def nodes(self, nodes):
        self._nodes = nodes

    @lines.setter
    def lines(self, lines):
        self._lines = lines

    # Network class Methods
    def connect(self):
        for node in self.nodes.values():
            # Initialize each node's switching matrix
            node.switching_matrix = {}
            for neighbour in node.connected_nodes:
                node.successive[node.label + neighbour] = self._lines[node.label + neighbour]
                # For the switching matrix initialization
                node.switching_matrix[neighbour] = {}
                for other_neighbour in node.connected_nodes:
                    if other_neighbour == neighbour:
                        node.switching_matrix[neighbour][other_neighbour] = np.zeros(params.NUM_CHANNELS)
                    elif other_neighbour != neighbour:
                        node.switching_matrix[neighbour][other_neighbour] = np.ones(params.NUM_CHANNELS)
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

    def propagate(self, lightpath: Lightpath) -> Lightpath:
        self._nodes[lightpath.path[0]].propagate(lightpath)
        return lightpath

    def probe(self, signal_information: Signal_Information) -> Signal_Information:
        self._nodes[signal_information.path[0]].probe(signal_information)
        return signal_information

    def _init_weighted_paths(self):
        # FOR EVERY POSSIBLE PATH PROPAGATE A SIGNAL
        for node in self._nodes.keys():
            for othernode in self._nodes.keys():
                if othernode != node:
                    all_paths_in_between = self.find_paths(node, othernode)
                    for path in all_paths_in_between:
                        signal = Signal_Information(sci_util.signal_power, list(path))
                        signal_after_propagation = self.probe(signal)
                        self._weighted_paths = self._weighted_paths.append({'Path': '->'.join(path),
                                                                            'Total_Latency': signal_after_propagation.latency,
                                                                            'Total_Noise': signal_after_propagation.noise_power,
                                                                            'SNR': 10 * math.log(
                                                                                signal_after_propagation.signal_power / signal_after_propagation.noise_power)},
                                                                           ignore_index=True)

    def _init_route_space(self):
        self._route_space['Path'] = self.weighted_paths['Path']
        for i in range(self.weighted_paths.shape[0]):
            self._route_space._set_value(i, 'Channel_Occupancy', ['free'] * 10)

    def _update_route_space(self, path: list[str], channel: int):
        # when we propagate a lightpath each line sets the state of the corresponding channel to occupied
        for i in range(self._route_space.shape[0]):
            path = self._route_space['Path'][i]
            nodes = path.split('->')
            channel_occupancy = ['free'] * params.NUM_CHANNELS
            # for every route we prepare a list o all its line labels
            lines = []
            for j in range(len(nodes)-1):
                lines.append(nodes[j]+nodes[j+1])
            # for line we count for the occupied channels
            for line_index in range(len(lines)):
                for channel in range(params.NUM_CHANNELS):
                    if lines[line_index] != lines[-1]:  # if it is not the last line of the path we check both the line
                        # state and the arrival node's switching matrix in order to check if it's feasible for him to
                        # forward the connection
                        if self._lines[lines[line_index]].state[channel] == 'free' \
                          and self._nodes[lines[line_index][-1]].switching_matrix[lines[line_index][0]][lines[line_index+1][-1]][channel] == 1:
                            channel_occupancy[channel] = 'free'
                        else:
                            channel_occupancy[channel] = 'occupied'
                    elif lines[line_index] == lines[-1]: # if it is the last line of the path we just need to check the line state
                        # and not the last node's capability of switching the request
                        if self._lines[lines[line_index]].state[channel] == 'free':
                            channel_occupancy[channel] = 'free'
                        else:
                            channel_occupancy[channel] = 'occupied'
            # update the overall path with the channel occupancy status
            self._route_space._set_value(i, 'Channel_Occupancy', channel_occupancy)

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

    def find_best_snr(self, start_node: str, dst_node: str) -> (list[str], int):
        routes = self._weighted_paths[self._weighted_paths.Path.str.startswith(start_node) &
                                      self._weighted_paths.Path.str.endswith(dst_node)]
        routes = routes.reset_index(drop=True)
        while routes.shape[0] > 0:
            # Identify the path with the best snr available
            index_of_max_snr = routes['SNR'].idxmax()
            path = str(routes.iloc[[index_of_max_snr]]['Path'].values[0])
            # we retrieve the channel occupancy within this path
            channel_occupancy_list = self._route_space[self.route_space['Path'] == path]['Channel_Occupancy'].values[0]
            # we choose a free channel
            if 'free' in channel_occupancy_list:
                channel = channel_occupancy_list.index('free')
                path = path.split('->')
                return path, channel
            else:
                routes: pd.DataFrame = routes.drop(routes.index[index_of_max_snr])
                routes = routes.reset_index(drop=True)
        return [], 'None'

    def find_best_latency(self, start_node: str, dst_node: str) -> (list[str], int):
        routes = self._weighted_paths[self._weighted_paths.Path.str.startswith(start_node) &
                                      self._weighted_paths.Path.str.endswith(dst_node)]
        routes = routes.reset_index(drop=True)
        while routes.shape[0] > 0:
            # Identify the path with the lowest latency available
            index_of_min_latency = routes['Total_Latency'].idxmin()
            path = str(routes.iloc[[index_of_min_latency]]['Path'].values[0])
            # we retrieve the channel occupancy within this path
            channel_occupancy_list = self._route_space[self.route_space['Path'] == path]['Channel_Occupancy'].values[0]
            # we choose a free channel
            if 'free' in channel_occupancy_list:
                channel = channel_occupancy_list.index('free')
                path = path.split('->')
                return path, channel
            else:
                routes: pd.DataFrame = routes.drop(routes.index[index_of_min_latency])
                routes = routes.reset_index(drop=True)
        return [], 'None'

    def stream(self, connections_list: list[Connection], optimizeWhat: str = "latency"):
        if optimizeWhat == "latency":
            for connection in connections_list:
                path_with_lowest_latency, channel = self.find_best_latency(connection.input, connection.output)
                if len(path_with_lowest_latency) > 0:
                    lightpath = Lightpath(connection.signal_power, path_with_lowest_latency, channel)
                    lightpath_after_propagation = self.propagate(lightpath)
                    connection.latency = lightpath_after_propagation.latency
                    connection.snr = 10 * math.log(lightpath_after_propagation.signal_power / lightpath_after_propagation.noise_power)
                    self._update_route_space(path_with_lowest_latency, channel)
                elif len(path_with_lowest_latency) == 0:
                    connection.latency = 'None'
                    connection.snr = 0
        elif optimizeWhat == "snr":
            for connection in connections_list:
                path_with_best_snr, channel = self.find_best_snr(connection.input, connection.output)
                if len(path_with_best_snr) > 0:
                    lightpath = Lightpath(connection.signal_power,path_with_best_snr,channel)
                    lightpath_after_propagation = self.propagate(lightpath)
                    connection.latency = lightpath_after_propagation.latency
                    connection.snr = 10 * math.log(lightpath_after_propagation.signal_power / lightpath_after_propagation.noise_power)
                elif len(path_with_best_snr) == 0:
                    connection.latency = 'None'
                    connection.snr = 0








