import copy
import json
import math
from pathlib import Path
import science_utils as sci_util
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import special

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
        self._Rs = params.SYMBOL_RATE
        self._df = params.CHANNELS_SPACING

    @property
    def df(self):
        return self._df

    @property
    def Rs(self):
        return self._Rs

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, ch: int):
        self._channel = ch

    @Rs.setter
    def Rs(self, Rs: float):
        self._Rs = Rs

    @df.setter
    def df(self, df: float):
        self._df = df


class Node:
    def __init__(self, label: str, dictionary: dict):
        self._label: str = label
        self._position: tuple = dictionary['position']
        self._connected_nodes: list = dictionary['connected_nodes']
        self._successive: dict = {}
        self._switching_matrix = None
        self._transceiver: str = "fixed_rate"  # fixed-rate is the default value if no other is provided

    # Instance Variables Getters
    @property
    def transceiver(self):
        return self._transceiver

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
    @transceiver.setter
    def transceiver(self, transceiver: str):
        self._transceiver = transceiver

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
        if params.DINAMIC_SWITCHING_MATRIX == True:
            # Set the switching matrix of the next node to zero for the neighboring channels to the one being switched
            if lightpath.path.__len__() > 1:
                channel = lightpath.channel
                sx_channel = channel-1
                dx_channel = channel+1
                if sx_channel >= 0:     # channel 0 doesn't cause any interference on the not existing channel -1
                    self.successive[self._label + lightpath.path[0]].successive[lightpath.path[0]]\
                        .switching_matrix[self._label][lightpath.path[1]][sx_channel] = 0
                if dx_channel <= 9:     # channel 9 doesn't cause any interference on the not existing channel 10
                    self.successive[self._label + lightpath.path[0]].successive[lightpath.path[0]] \
                        .switching_matrix[self._label][lightpath.path[1]][dx_channel] = 0

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
        self._n_amplifiers = math.floor(self._length/params.DISTANCE_BETWEEN_AMP)
        self._gain = 10**params.AMPLIFIERS_GAIN/10        # the variable gain is expressed in its natural value, not dB
        self._noise_figure = 10**params.AMPLIFIERS_NOISE_FIGURE/10 # same as for gain
        self._alpha: float = params.FIBER_ALPHA
        self._beta: float = params.FIBER_BETA
        self._gamma: float = params.FIBER_GAMMA
        self._L_eff: float = 1/(2*self._alpha)
        self._n_span = int(np.ceil(self._length / params.DISTANCE_BETWEEN_AMP))
    # Instance Variables Getters
    @property
    def n_span(self):
        return self._n_span

    @property
    def L_eff(self):
        return self._L_eff

    @property
    def gamma(self):
        return self._gamma

    @property
    def beta(self):
        return self._beta

    @property
    def alpha(self):
        return self._alpha

    @property
    def noise_figure(self):
        return self._noise_figure

    @property
    def gain(self):
        return self._gain
    @property
    def n_amplifiers(self):
       return self._n_amplifiers
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

    # Instance Variables Setters
    @n_span.setter
    def n_span(self, n_span: int):
        self._n_span = n_span

    @L_eff.setter
    def L_eff(self, L_eff: float):
        self._L_eff = L_eff

    @gamma.setter
    def gamma(self, gamma: float):
        self._gamma = gamma

    @beta.setter
    def beta(self, beta: float):
        self._beta = beta

    @alpha.setter
    def alpha(self, alpha: float):
        self._alpha = alpha

    @noise_figure.setter
    def noise_figure(self, noise_figure):
        self._noise_figure = noise_figure

    @gain.setter
    def gain(self, gain):
        self._gain = gain

    @n_amplifiers.setter
    def n_amplifiers(self, n_ampl: int):
        self._n_amplifiers = n_ampl

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
    def optimized_launch_power(self):
        # This method determined the optimal launch power to propagate a signal over the line
        # exploiting the LOGO strategy (Local Optimization Global Optimization)
        eta = (16 / (27 * math.pi)) \
              * math.log(((math.pi ** 2) / 2) * (params.FIBER_BETA * (params.SYMBOL_RATE ** 2) / params.FIBER_ALPHA) \
                         * (params.NUM_CHANNELS ** (2 * params.SYMBOL_RATE / params.CHANNELS_SPACING)), math.e) \
              * (params.FIBER_ALPHA / params.FIBER_BETA) * (
                          (params.FIBER_GAMMA ** 2) * (self._L_eff ** 2) / (params.SYMBOL_RATE ** 3))
        return np.cbrt(self.ase_generation()/(2*params.NOISE_BANDWIDTH*self._n_span*eta))

    def nli_generation(self, lightpath_power: float):
        # This method computes the non linear interferences that the signal will be impaired with.
        # They depends on the fiber parameters, the symbol rate, the signal power and the noise bandwidth
        eta = (16/(27*math.pi))\
              * math.log(((math.pi**2)/2)*(params.FIBER_BETA*(params.SYMBOL_RATE**2)/params.FIBER_ALPHA)\
              * (params.NUM_CHANNELS**(2*params.SYMBOL_RATE/params.CHANNELS_SPACING)), math.e)\
              * (params.FIBER_ALPHA/params.FIBER_BETA)*((params.FIBER_GAMMA**2)*(self._L_eff**2)/(params.SYMBOL_RATE**3))

        return (lightpath_power**3)*eta*params.NOISE_BANDWIDTH

    def ase_generation(self):
        # This method computes the Amplified Spontaneous Emissions
        return self._n_amplifiers * sci_util.plank_constant * sci_util.c_band_center_frequency\
               * params.NOISE_BANDWIDTH * self._noise_figure * (self._gain - 1)

    def latency_generation(self):
        return float(self._length / ((2 / 3) * sci_util.light_speed))

    def noise_generation(self, signal_power: float):
        return self.ase_generation() + self.nli_generation(signal_power)

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
    def __init__(self, inp: str, out: str, signal_power: float = sci_util.signal_power):
        self._input: str = inp
        self._output: str = out
        self._signal_power: float = signal_power
        self._latency: float = 0  # has to be initialized to zero
        self._snr: float = 0    # has to be initialized to zero
        self._bitrate: float = 0

    # Instance Variables Getters
    @property
    def bitrate(self):
        return self._bitrate

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
    @bitrate.setter
    def bitrate(self, bitrate: float):
        self._bitrate = bitrate
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
    def __init__(self, JSON_FILENAME):
        root = Path(__file__).parent.parent
        # DICTIONARY of LINES objects
        self._lines: dict = {}  # Dictionary of Line objects
        # DICTIONARY of NODES objects
        self._nodes: dict = {}  # Dictionary of Node objects
        # DATAFRAME FOR COLLECTING SPECTRAL INFORMATION
        self._weighted_paths: pd.DataFrame = pd.DataFrame(columns=['Path', 'Total_Latency', 'Total_Noise', 'SNR'])
        self._route_space: pd.DataFrame = pd.DataFrame(columns=['Path', 'Channel_Occupancy'])
        self._initial_switching_matrices = {}
        with open(root / JSON_FILENAME) as f:
            json_dict = json.load(f)
        for key in json_dict.keys():
            if "switching_matrix" in json_dict[key].keys():
                self._initial_switching_matrices[key] = json_dict[key]["switching_matrix"]
            self._nodes[key] = Node(key, json_dict[key])
            for neighbour in json_dict[key]['connected_nodes']:
                x1 = float(self._nodes[key].position[0])
                y1 = float(self._nodes[key].position[1])
                x2 = float(json_dict[neighbour]['position'][0])
                y2 = float(json_dict[neighbour]['position'][1])
                length = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
                self._lines[key + neighbour] = Line(key + neighbour, length)
        self.connect(json_dict)
        self._init_weighted_paths()
        self._init_route_space()
        f.close()

    # Instance Variables Getters
    @property
    def initial_switching_matrices(self):
        return self._initial_switching_matrices

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
    @initial_switching_matrices.setter
    def initial_switching_matrices(self, switching_matrices):
        self._initial_switching_matrices = switching_matrices

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
    def connect(self, json_dictionary: dict):
        is_switching_matrix_provided: bool = False
        for node in self.nodes.values():
            if "switching_matrix" in json_dictionary[node.label].keys():
                is_switching_matrix_provided = True
            if "transceiver" in json_dictionary[node.label].keys():
                node.transceiver = json_dictionary[node.label]["transceiver"]
            if not is_switching_matrix_provided:    # if not provided, the switching matrix of each node is created manually
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
            elif is_switching_matrix_provided:     # if provided, we use the given switching matrix for each node
                # we make a copy of it since we need to decouple the node's own switching matrix and the initial one
                # that we store in the Network class. The node's one will be dinamically modified, we don't want to modify
                # also the reference one store in Network class
                node.switching_matrix = copy.deepcopy(json_dictionary[node.label]['switching_matrix'])
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

    def _update_route_space(self):
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
                        if self._lines[lines[line_index]].state[channel] == 'occupied' \
                          or self._nodes[lines[line_index][-1]].switching_matrix[lines[line_index][0]][lines[line_index+1][-1]][channel] == 0:
                            channel_occupancy[channel] = 'occupied'
                    elif lines[line_index] == lines[-1]: # if it is the last line of the path we just need to check the line state
                        # and not the last node's capability of switching the request
                        if self._lines[lines[line_index]].state[channel] == 'occupied':
                            channel_occupancy[channel] = 'occupied'
            # update the overall path with the channel occupancy status
            self.route_space._set_value(i, 'Channel_Occupancy', copy.deepcopy(channel_occupancy))

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

    def calculate_bit_rate(self, path: list[str], strategy: str) -> float:
        # initialize bitrate to zero
        bitrate = 0
        # retrieve the GSNR for the specified path
        # first we convert the path which is a list of strings into
        # a unique string in the form A->B->C->...
        unique_string_path = '->'.join(path)
        GSNR = self._weighted_paths[self._weighted_paths['Path'] == unique_string_path]['SNR'].values[0]
        if strategy == "fixed_rate":
            if GSNR >= (2 * special.erfcinv(2*params.BIT_ERROR_RATE)**2)*params.SYMBOL_RATE/params.NOISE_BANDWIDTH:
                bitrate = 100e9
        elif strategy == "flex_rate":
            if GSNR >= (2 * special.erfcinv(params.BIT_ERROR_RATE*2)**2)*params.SYMBOL_RATE/params.NOISE_BANDWIDTH:
                bitrate = 100e9
            if GSNR >= ((14/3)*special.erfcinv(params.BIT_ERROR_RATE*3/2)**2)*params.SYMBOL_RATE/params.NOISE_BANDWIDTH:
                bitrate = 200e9
            if GSNR >= (10*special.erfcinv(params.BIT_ERROR_RATE*8/3)**2)*params.SYMBOL_RATE/params.NOISE_BANDWIDTH:
                bitrate = 400e9
        elif strategy == "shannon":
            bitrate = (2*params.SYMBOL_RATE)*math.log(1+GSNR*params.SYMBOL_RATE/params.NOISE_BANDWIDTH,2)

        return bitrate

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
                if len(path_with_lowest_latency) > 0: # it means it was possible to find an available path
                    lightpath = Lightpath(connection.signal_power, list(path_with_lowest_latency), channel)
                    lightpath_after_propagation = self.propagate(lightpath)
                    connection.latency = lightpath_after_propagation.latency
                    connection.snr = 10 * math.log(lightpath_after_propagation.signal_power / lightpath_after_propagation.noise_power)
                    connection.bitrate = self.calculate_bit_rate(path_with_lowest_latency, self._nodes[path_with_lowest_latency[0]].transceiver)
                    self._update_route_space()
                elif len(path_with_lowest_latency) == 0: # it means it was not possible to find an available path
                    connection.latency = 'None'
                    connection.snr = 0
        elif optimizeWhat == "snr":
            for connection in connections_list:
                path_with_best_snr, channel = self.find_best_snr(connection.input, connection.output)
                if len(path_with_best_snr) > 0:  # it means it was possible to find an available path
                    lightpath = Lightpath(connection.signal_power, list(path_with_best_snr), channel)
                    lightpath_after_propagation = self.propagate(lightpath)
                    connection.latency = lightpath_after_propagation.latency
                    connection.snr = 10 * math.log(lightpath_after_propagation.signal_power / lightpath_after_propagation.noise_power)
                    connection.bitrate = self.calculate_bit_rate(path_with_best_snr,
                                                                 self._nodes[path_with_best_snr[0]].transceiver)
                    self._update_route_space()
                elif len(path_with_best_snr) == 0:  # it means it was not possible to find an available path
                    connection.latency = 'None'
                    connection.snr = 0








