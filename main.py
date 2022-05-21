from argparse import ArgumentParser, RawTextHelpFormatter
from importlib.resources import path
from operator import concat
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
    parser.add_argument('-s', '--save-file',
                        type=str, default=None,
                        help='Specify a csv filename to save to avg,min,max data.\n')

    arguments = parser.parse_args()

    video_file = arguments.input_video_path
    output_format = arguments.output_format
    save_file = arguments.save_file

    dir_output = "./BitRate_Reports"

    if not os.path.exists(video_file):
        print('File specified for -i could not be found. Exiting.')
        sys.exit()
    if not os.path.isdir(dir_output):
        os.mkdir(dir_output)
    csv_file_path = os.path.join(dir_output,save_file)

    results = analyze_bitrate(video_file, output_format,dir_output)
    print('Done. Now plotting results ...')

    graph_title = Path(video_file).name
    graph_filename = Path(video_file).stem

    plot_results(results, graph_title, graph_filename, csv_file_path,dir_output)
    print(f'Done. Check {graph_filename}.png and '
          f'{graph_filename}.{output_format}!')
    if save_file:
        print(f'Saved to {save_file}')


if __name__ == "__main__":
    main()
