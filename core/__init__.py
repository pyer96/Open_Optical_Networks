import elements


def main():
    network = elements.Network()
    print(network.nodes)
    print(network.lines)
    test: list = network.find_paths('A', 'D')
    network.draw()

if __name__ == '__main__':
    main()
