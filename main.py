from argparse import ArgumentParser, RawTextHelpFormatter
import os
from pathlib import Path
import sys

from _bitrate_analyzer import analyze_bitrate
from _plotter import plot_results


def main():
    if len(sys.argv) == 1:
        print("To see more details about the available arguments, "
              "enter 'python main.py -h'")

    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('-i', '--input-video-path', type=str, required=True,
                        help='Enter the path of the original '
                             'video. A relative or absolute path can be '
                             'specified.')
    parser.add_argument('-f', '--output-format',
                        type=str, default='xml', choices=['xml', 'json'],
                        help='Specify the output format for the file written\n'
                             'by FFProbe. (default: \'xml\')')

    arguments = parser.parse_args()

    video_file = arguments.input_video_path
    output_format = arguments.output_format

    if not os.path.exists(video_file):
        print('File specified for -i could not be found. Exiting.')
        sys.exit()

    results = analyze_bitrate(video_file, output_format)
    print('Done. Now plotting results ...')

    graph_title = Path(video_file).name
    graph_filename = Path(video_file).stem

    plot_results(results, graph_title, graph_filename)
    print(f'Done. Check {graph_filename}.png and '
          f'{graph_filename}.{output_format}!')


if __name__ == "__main__":
    main()
