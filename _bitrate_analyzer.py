import io
from math import trunc
from pathlib import Path
import multiprocessing
import subprocess
from tqdm import tqdm

from _file_parser import FileParser
from _utils import get_framerate_float, get_duration


def analyze_bitrate(video_path, format='xml'):
    duration = round(float(get_duration(video_path)), 2)
    fps = get_framerate_float(video_path)
    fps_rounded = round(fps)
    cpu_count = multiprocessing.cpu_count()
    total_frames = trunc(int(duration) * fps) + 1
    output_filename = f'{Path(video_path).stem}.{format}'
    file = open(output_filename, 'w', encoding="utf-8")

    print(f'Now analyzing ~ {total_frames} frames.')
    progress_bar = tqdm(total_frames, unit=' frames', ncols=80)

    proc = subprocess.Popen(['ffprobe', '-hide_banner', '-show_frames',
                             '-show_streams',
                             '-threads', str(cpu_count),
                             '-loglevel', 'quiet',
                             # '-show_entries', 'frame=pkt_size',
                             '-print_format', 'xml' if format == 'xml' else
                                              'json',
                             '-select_streams', 'v:0',
                             video_path], stdout=subprocess.PIPE)

    for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
        file.write(line + '\n')

        if 'pkt_size' in line:
            progress_bar.update()

    proc.poll()
    progress_bar.close()
    file.close()

    parser = FileParser()
    result = parser.run(output_filename, format, fps_rounded)

    return result
