import elements
import math

def main():
    signal_power = 1e-3
    network = elements.Network()
    network.draw()

    print(network.weighted_paths.to_string())







if __name__ == '__main__':
    main()
