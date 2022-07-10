import seaborn as sns
import elements
import matplotlib.pyplot as plt
import parameters as params
from itertools import cycle
import numpy as np




def plot_connections_latencies_distribution(list_of_connections: list[elements.Connection]):
    latencies = []
    for conn in list_of_connections:
        if conn.latency == 'None':
            latencies.append(-1)
        else:
            latencies.append(conn.latency * 1e3)

    sns.displot(latencies, stat="probability")
    plt.title(r"$latencies\ distribution$")
    plt.xlabel(r'$milliseconds$')
    plt.ylabel(r'$count$')
    plt.show()


def plot_connections_snr_distribution(list_of_connections: list[elements.Connection]):
    snrs = []
    for conn in list_of_connections:
        snrs.append(conn.snr)

    sns.displot(snrs, stat="probability")
    plt.title(r"$SNR\ distribution\ with\ SNR\ optimization$")
    plt.xlabel(r'$dB$')
    plt.ylabel(r'$count$')
    plt.show()


def plot_connections_bitrate_distribution(list_of_connections: list[elements.Connection]):
    bitrates = []
    num_active_connections = 0
    sum_of_bitrates = 0
    for conn in list_of_connections:
        if conn.bitrate > 0:
            bitrates.append(conn.bitrate / 1e9)
            sum_of_bitrates = sum_of_bitrates + conn.bitrate
            num_active_connections = num_active_connections + 1

    avg_bitrate = sum_of_bitrates / num_active_connections
    sns.displot(bitrates, stat="probability")
    plt.title(r"$Bitrate\ distribution\ with\ SNR\ optimization\ Total\ Capacity:" +
              str(sum_of_bitrates/1e12/50) + "Tbps\ Avg\ Bitrate:" + str(avg_bitrate/1e9) + "Gbps$")
    plt.xlabel(r'$Gbps$')
    plt.ylabel(r'$count$')
    plt.show()


def free_all_lines(network: elements.Network):
    for Line in network.lines.values():
        Line.state = ['free', 'free', 'free', 'free', 'free', 'free', 'free', 'free', 'free', 'free']
    network._init_route_space()


def update_links_occupancy(net: elements.Network, links_occupancy: dict[list], M: int):
    for line in net.lines.values():
        links_occupancy[line.label][M] += (line.state.count('occupied')/params.NUM_CHANNELS)*100


def update_deployed_traffic(list_of_connections: list[elements.Connection], deployed_traffic: list, M: int):
    for connection in list_of_connections:
        deployed_traffic[M] += connection.bitrate


def update_congestion_ratio(net: elements.Network, congestion_ratio: list, M: int):
    lines = net.lines.values()
    total_channels = len(lines) * params.NUM_CHANNELS
    occupied_channels = 0
    for line in lines:
        occupied_channels += line.state.count('occupied')
    congestion_ratio[M] += (occupied_channels/total_channels)*100


def plot_deployed_traffic_overM(Deployed_Traffic: list[float], Occurrencies: list[int], MonteCarloIterations: int):
    x_axis = list(range(1, 61))
    # Normalize the vector
    normalized_deployed_traffic = list(Deployed_Traffic)
    for i in range(len(normalized_deployed_traffic)):
        if Occurrencies[i] == 0:
            normalized_deployed_traffic[i] = 0
        else:
            normalized_deployed_traffic[i] = normalized_deployed_traffic[i]/Occurrencies[i]/1e12 # expressed in Tbps
    plt.plot(x_axis, normalized_deployed_traffic, '-bo')
    plt.xlabel(r'$M$')
    plt.ylabel(r"Tbps")
    plt.title(r"$Deployed\ Capacity\ versus\ M\ averaged\ over\ "+str(MonteCarloIterations)+"\ Monte\ Carlo\ Iterations$")
    plt.grid()
    plt.xticks(np.arange(61))
    plt.show()


def plot_congestion_ratio_overM(Congestion_Ratio: list[float], Occurrencies: list[int], MonteCarloIterations: int):
    x_axis = list(range(1, 61))
    # Normalize the vector
    normalized_congestion_ratio = list(Congestion_Ratio)
    for i in range(len(normalized_congestion_ratio)):
        if Occurrencies[i] == 0:
            normalized_congestion_ratio[i] = 0
        else:
            normalized_congestion_ratio[i] = normalized_congestion_ratio[i] / Occurrencies[i]
    plt.plot(x_axis, normalized_congestion_ratio, '-bo')
    plt.xlabel(r'$M$')
    plt.ylabel(r"%")
    plt.title(r"$Congestion\ Ratio\ versus\ M\ averaged\ over\ " + str(
        MonteCarloIterations) + "\ Monte\ Carlo\ Iterations$")
    plt.grid()
    plt.xticks(np.arange(61))
    plt.show()


def plot_links_occupancy_ratio_overM(Links_Occupancy: dict[list], Occurrencies: list[int], MonteCarloIterations: int):
    cycol = cycle('bgrcmky')     # for colors
    style = cycle(['-', '--', '-.'])
    # Normalize the values
    links = Links_Occupancy.keys()
    for line in links:
        for i in range(len(Links_Occupancy[line])):
            if Occurrencies[i] == 0:
                Links_Occupancy[line][i] = 0
            else:
                Links_Occupancy[line][i] = Links_Occupancy[line][i]/Occurrencies[i]
    x_axis = list(range(1, 61))
    for line in links:
        plt.plot(x_axis, Links_Occupancy[line], color=next(cycol), linestyle=next(style), label=line)
    plt.title(r"$Optical\ Lines\ Congestion\ Ratio\ versus\ M\ averaged\ over\ " + str(
        MonteCarloIterations) + "\ Monte\ Carlo\ Iterations$")
    plt.xlabel(r"M")
    plt.ylabel(r"%")
    plt.xticks(np.arange(61))
    plt.legend()
    plt.grid()
    plt.show()






