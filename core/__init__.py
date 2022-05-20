import elements


def main():
    network = elements.Network()
    print(network.nodes)
    print(network.lines)
    network.find_paths('A', 'D')

if __name__ == '__main__':
    main()