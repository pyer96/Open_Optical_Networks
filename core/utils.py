import seaborn as sns
import elements
import matplotlib.pyplot as plt
import parameters as params


def plot_connections_latencies_distribution(list_of_connections: list[elements.Connection]):
    latencies = []
    for conn in list_of_connections:
        if conn.latency == 'None':
            latencies.append(-1)
        else:
            latencies.append(conn.latency * 1e3)

    sns.displot(latencies)
    plt.title(r"$latencies\ distribution\ for\ 100\ connections\ served\ with\ latency\ optimization$")
    plt.xlabel(r'$milliseconds$')
    plt.ylabel(r'$count$')
    plt.show()


def plot_connections_snr_distribution(list_of_connections: list[elements.Connection]):
    snrs = []
    for conn in list_of_connections:
        snrs.append(conn.snr)

    sns.displot(snrs)
    plt.title(r"$SNR\ distribution\ for\ 100\ connections\ served\ with\ snr\ optimization$")
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
    sns.displot(bitrates)
    plt.title(r"$Bitrate\ distribution\ with\ SNR\ optimization\ Total\ Capacity:" +
              str(sum_of_bitrates/1e12) + "Tbps\ Avg\ Bitrate:" + str(avg_bitrate/1e9) + "Gbps$")
    plt.xlabel(r'$Gbps$')
    plt.ylabel(r'$count$')
    plt.show()


def free_all_lines(network: elements.Network):
    for Line in network.lines.values():
        Line.state = ['free', 'free', 'free', 'free', 'free', 'free', 'free', 'free', 'free', 'free']
    network._init_route_space()


def update_links_occupancy(net: elements.Network, links_occupancy: dict[list], M: int):
    for line in net.lines:
        links_occupancy[line.label][M] += (line.state.count('occupied')/params.NUM_CHANNELS)*100


def update_deployed_traffic(list_of_connections: list[elements.Connection], deployed_traffic: list, M: int):
    for connection in list_of_connections:
        deployed_traffic[M] += connection.bitrate


def update_congestion_ratio(net: elements.Network, deployed_traffic: list, M: int):
    for line in net.lines:
        links_occupancy[line.label][M] += (line.state.count('occupied')/params.NUM_CHANNELS)*100
