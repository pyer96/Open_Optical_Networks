import elements
import utils
import random
import parameters as params


def lab4exercises():
    network = elements.Network(params.JSON_FILE)
    network.draw()
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


def lab5exercise():
    network = elements.Network(params.JSON_FILE)
    network.draw()
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


def lab7exercise():
    # Goal of this exercise is to compare the lightpath deployment (with snr optimization) of 100 randomly chosen
    # connections: first with a network composed of network elements with a full switching matrix,
    # later with a network composed of network elements with a non full switching matrix
    # In order to provide more fair results, once generated the 100 random connection requests, they will be kept the
    # same for the test with the non-full switching matrices
    network = elements.Network('resources/nodes_full.json')
    network.draw()
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
    del list_of_nodes
    del network

    network = elements.Network('resources/nodes_not_full.json')
    signal_power = 1
    # the same list of 100 connections is kept
    network.stream(list_of_connections, "snr")
    utils.plot_connections_snr_distribution(list_of_connections)
    utils.free_all_lines(network)
    del list_of_connections
    del network


def lab7_second_part_exercise():
    network = elements.Network('resources/nodes_full_fixed_rate.json')
    network.draw()
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
    utils.plot_connections_bitrate_distribution(list_of_connections)
    utils.free_all_lines(network)
    del list_of_nodes
    del network

    network = elements.Network('resources/nodes_full_flex_rate.json')
    # the same list of 100 connections is kept
    network.stream(list_of_connections, "snr")
    utils.plot_connections_bitrate_distribution(list_of_connections)
    utils.free_all_lines(network)

    del network

    network = elements.Network('resources/nodes_full_shannon.json')
    # the same list of 100 connections is kept
    network.stream(list_of_connections, "snr")
    utils.plot_connections_bitrate_distribution(list_of_connections)
    utils.free_all_lines(network)
    del list_of_connections
    del network


def lab9_same_as_lab7_with_ase_nli_and_optimal_launch_power():
    network = elements.Network('resources/nodes_full_fixed_rate.json')
    network.draw()
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
    utils.plot_connections_bitrate_distribution(list_of_connections)
    utils.free_all_lines(network)
    del list_of_nodes
    del network

    network = elements.Network('resources/nodes_full_flex_rate.json')
    # the same list of 100 connections is kept
    network.stream(list_of_connections, "snr")
    utils.plot_connections_bitrate_distribution(list_of_connections)
    utils.free_all_lines(network)

    del network

    network = elements.Network('resources/nodes_full_shannon.json')
    # the same list of 100 connections is kept
    network.stream(list_of_connections, "snr")
    utils.plot_connections_bitrate_distribution(list_of_connections)
    utils.free_all_lines(network)
    del list_of_connections
    del network


def lab9_exercise7():
    JSON_FILES = ['resources/nodes_full_fixed_rate.json', 'resources/nodes_full_flex_rate.json',
                  'resources/nodes_full_shannon.json']
    for file in JSON_FILES:
        network = elements.Network(file)
        network.draw()
        list_of_nodes = list(network.nodes.keys())

        # TRAFFIC MATRIX GENERATION
        TRAFFIC_MATRIX = {}
        for node_start in list_of_nodes:
            TRAFFIC_MATRIX[node_start] = {}

        network_not_saturated = True
        M = 1
        connections = []
        while network_not_saturated:
            # TRAFFIC GENERATION
            for node_start in list_of_nodes:
                for node_end in list_of_nodes:
                    if node_start == node_end:
                        TRAFFIC_MATRIX[node_start][node_end] = 0
                    else:
                        TRAFFIC_MATRIX[node_start][node_end] = M * 100e9
            network_not_saturated, list_of_connections = network.manage_traffic_matrix(TRAFFIC_MATRIX)
            connections.extend(list_of_connections)
            M = M + 1
        print("M = " + str(M))
        utils.plot_connections_bitrate_distribution(connections)


def Monte_Carlo_Sim():
    # This is a Monte Carlo Simulation with the aim of collecting useful metrics of a network in order to estimate
    # its performances. The considered digital twin emulates the physical layer of the optical infrastructure in terms
    # of fiber cables, amplifiers, roadms, number of channel per fiber, transceivers' bitrate and the consequent signal
    # quality.
    # The derived performance metrics of interest are:
    # > Total Capacity
    # > Per Link Avg Capacity and GSNR
    # > Per Link Min/Max Capacity and GSNR
    # > Blocking Events

    # Draw the NETWORK of INTERESTS
    NETWORK_JSON_FILE = 'resources/279094/full_network.json'
    #  NETWORK_JSON_FILE = 'resources/279094/not_full_network.json'
    network = elements.Network(NETWORK_JSON_FILE)
    network.draw()

    # Prepare a TRAFFIC MATRIX
    TRAFFIC_MATRIX = {}
    list_of_nodes = list(network.nodes.keys())
    for node_start in list_of_nodes:
        TRAFFIC_MATRIX[node_start] = {}

    # Statistics Variables
    Deployed_Traffic = [0.0] * 60  # expressed in bitrate
    Congestion_Ratio = [0.0] * 60  # expressed in percentage
    Links_Occupancy = {}
    for line in network.lines.values():
        Links_Occupancy[line.label] = [0.0] * 60    # expressed in percentage
    Connections = []
    Occurrencies = [0] * 60 # To count how many times the simulation reaches a certain M

    # MONTE CARLO SIMULATION
    # M increments but at each increment the network is restored
    MonteCarloIterations = 50
    for iteration in range(MonteCarloIterations):
        print("ITERATION "+str(iteration))
        network_not_saturated = True
        M = 1
        while network_not_saturated:
            Occurrencies[M] += 1
            # TRAFFIC GENERATION
            for node_start in list_of_nodes:
                for node_end in list_of_nodes:
                    if node_start == node_end:
                        TRAFFIC_MATRIX[node_start][node_end] = 0
                    else:
                        TRAFFIC_MATRIX[node_start][node_end] = M * 100e9
            # Pass Traffic Matrix to network to stream it
            network_not_saturated, list_of_connections = network.manage_traffic_matrix(TRAFFIC_MATRIX)
            # For later plotting purposes
            utils.update_links_occupancy(network, Links_Occupancy, M)
            utils.update_deployed_traffic(list_of_connections, Deployed_Traffic, M)
            utils.update_congestion_ratio(network, Congestion_Ratio, M)
            if M == 5:
                Connections.extend(list_of_connections)
            M = M + 1
            network.reset_network()
    # PLOTS
    print(Occurrencies)
    utils.plot_deployed_traffic_overM(Deployed_Traffic, Occurrencies, MonteCarloIterations)
    utils.plot_congestion_ratio_overM(Congestion_Ratio, Occurrencies, MonteCarloIterations)
    utils.plot_links_occupancy_ratio_overM(Links_Occupancy, Occurrencies, MonteCarloIterations)
    utils.plot_connections_bitrate_distribution(Connections)
    utils.plot_connections_snr_distribution(Connections)
    utils.plot_connections_latencies_distribution(Connections)


def main():
    #   lab4exercises()
    #   lab5exercise()
    #   lab7exercise()
    #   lab7_second_part_exercise()
    #   lab9_same_as_lab7_with_ase_nli_and_optimal_launch_power()
    #   lab9_exercise7()
    Monte_Carlo_Sim()


if __name__ == '__main__':
    main()
