from argparse import ArgumentParser, RawTextHelpFormatter
from pathlib import Path
import os
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
                             'video. A relative or absolute path can be'
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
    plot_results(results, Path(video_file).name)
    print(f'Done. Check bitrate_graph.png and bitrate.{output_format}!')


if __name__ == "__main__":
    main()
