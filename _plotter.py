import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np
import os

from _utils import (
    get_mbit_str,
    get_pretty_codec_name,
    save_to_file)


def plot_results(results, graph_title, graph_filename, csv_file_name=None, dir_name=None):
    seconds, bitrates, keyframes, encoder = results

    number_of_keyframes = len(keyframes)
    if number_of_keyframes > 75:
        print(f'Warning:\n{str(number_of_keyframes)} I-Frames detected.\n'
              'I-Frames are not shown on the graph for a video with more '
              'than 75 I-Frames as this results in a cluttered graph.\n'
              'Plotting the bitrate graph without I-frame markings...')
        # drop keyframes
        keyframes = []
    bit_rate_data = {}
    bit_rate_data['video_name'] = graph_filename
    bit_rate_data['avg_bitrate'] = get_mbit_str(round(np.mean(bitrates), 2))
    bit_rate_data['min_bitrate'] = get_mbit_str(round(min(bitrates), 2))
    bit_rate_data['max_bitrate'] = get_mbit_str(round(max(bitrates), 2))
    bit_rate_data['std_bitrate'] = get_mbit_str(round(np.std(bitrates), 2))
    bit_rate_data['encoder'] = get_pretty_codec_name(encoder)

    # init the plot
    plt.figure(figsize=(19.20, 10.80))
    plt.suptitle(f'{graph_title} | Codec: {encoder}\n\
                Min: {bit_rate_data["min_bitrate"]} | Max: {bit_rate_data["max_bitrate"]} | Standard Deviation: '
                 f'{bit_rate_data["std_bitrate"]}')
    plt.xlabel('Seconds')
    plt.ylabel('Video Bitrate (Mbps)')
    plt.grid(True)

    # actually plot the data
    bitrate_line, = plt.plot(seconds, bitrates,
                             label=f'Bitrate (Average: {bit_rate_data["avg_bitrate"]})')
    # plot vertical lines for keyframes
    for frame in keyframes:
        plt.axvline(frame, color='r', linestyle='--', linewidth=1)

    # create legend for I-frame-lines
    label_text = 'I-Frames' if number_of_keyframes <= 75 else \
                 'Too many I-Frames'
    i_frame_legend = mlines.Line2D([], [], color='red', linestyle='--',
                                   markersize=10, label=label_text)
    # setup plot legend
    plt.legend(handles=[bitrate_line, i_frame_legend],
               labels=[bitrate_line.get_label(),
                       i_frame_legend.get_label()],
               loc='lower right')

    # save the plot
    plt.savefig(os.path.join(dir_name, f'{graph_filename}.png'))

    # Save to csv
    if csv_file_name and dir_name:
        save_to_file(bit_rate_data, csv_file_name)