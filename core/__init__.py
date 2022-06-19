import elements
import utils
import random


def lab4exercises(network: elements.Network):
    # Create 100 connections with random starting and ending nodes and signal power of 1W
    # and stream all connections with latency optimization in mind
    signal_power = 1
    list_of_nodes = list(network.nodes.keys())
    list_of_connections = []
    for i in range(100):           # range(N) -> 0,1,2....N-1
        # extract random node
        nodes = random.sample(list_of_nodes, 2)  # selects randomly 2 different elements from the provided list
        start_node = nodes[0]
        dst_node = nodes[1]
        list_of_connections.append(elements.Connection(start_node, dst_node, signal_power))
    network.stream(list_of_connections, "latency")
    utils.plot_connections_latencies_distribution(list_of_connections)
    utils.free_all_lines(network)
    del list_of_connections

    # Create 100 connections with random starting and ending nodes and signal power of 1W
    # and stream all connections with snr optimization in mind
    signal_power = 1
    list_of_nodes = list(network.nodes.keys())
    list_of_connections = []
    for i in range(100):           # range(N) -> 0,1,2....N-1
        # extract random node
        nodes = random.sample(list_of_nodes, 2)  # selects randomly 2 different elements from the provided list
        start_node = nodes[0]
        dst_node = nodes[1]
        list_of_connections.append(elements.Connection(start_node, dst_node, signal_power))
    network.stream(list_of_connections, "snr")
    utils.plot_connections_snr_distribution(list_of_connections)
    utils.free_all_lines(network)
    del list_of_connections


def lab5exercise(network):
    # Create 100 connections with random starting and ending nodes and signal power of 1W
    # and stream all connections with snr optimization in mind
    signal_power = 1
    list_of_nodes = list(network.nodes.keys())
    list_of_connections = []
    for i in range(100):  # range(N) -> 0,1,2....N-1
        # extract random node
        nodes = random.sample(list_of_nodes, 2)  # selects randomly 2 different elements from the provided list
        start_node = nodes[0]
        dst_node = nodes[1]
        list_of_connections.append(elements.Connection(start_node, dst_node, signal_power))
    network.stream(list_of_connections, "snr")
    utils.plot_connections_snr_distribution(list_of_connections)
    utils.free_all_lines(network)
    del list_of_connections


def main():
    network = elements.Network()
    network.draw()
#    lab4exercises(network)
    lab5exercise(network)








if __name__ == '__main__':
    main()
