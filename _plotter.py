import matplotlib.pyplot as plt
import numpy as np

from _utils import get_mbit_str, get_pretty_codec_name


def plot_results(results, graph_title, graph_filename):
    seconds, bitrates, encoder = results

    avg_bitrate = get_mbit_str(round(np.mean(bitrates), 2))
    min_bitrate = get_mbit_str(round(min(bitrates), 2))
    max_bitrate = get_mbit_str(round(max(bitrates), 2))
    std_bitrate = get_mbit_str(round(np.std(bitrates), 2))
    encoder = get_pretty_codec_name(encoder)

    plt.figure(figsize=(19.20, 10.80))
    plt.suptitle(f'{graph_title} | Codec: {encoder}\n\
                Min: {min_bitrate} | Max: {max_bitrate} | Standard Deviation: '
                 f'{std_bitrate}')
    plt.plot(seconds, bitrates, label=f'Bitrate (Average: {avg_bitrate})')
    plt.xlabel('Seconds')
    plt.ylabel('Video Bitrate (Mbps)')
    plt.legend(loc='lower right')
    plt.grid(True)

    plt.savefig(f'{graph_filename}.png')
