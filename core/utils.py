import seaborn as sns
import elements
import matplotlib.pyplot as plt


def plot_connections_latencies_distribution(list_of_connections: list[elements.Connection]):
    latencies = []
    for conn in list_of_connections:
        latencies.append(conn.latency*1e3)

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
