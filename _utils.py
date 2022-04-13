import math
from ffmpeg import probe



def get_video_metadata(video_path) -> dict:
    return probe(video_path)

def get_bitrate(video_metadata) -> str:
    bitrate = video_metadata['format']['bit_rate']
    return f'{math.trunc(int(bitrate) / 1000)} kbit/s'


def get_framerate_fraction(video_metadata) -> str:
    r_frame_rate = [stream for stream in video_metadata['streams']
                    if stream['codec_type'] == 'video'][0][
        'r_frame_rate']
    return r_frame_rate


def get_framerate_float(video_metadata) -> str:
    numerator, denominator = get_framerate_fraction(video_metadata).split('/')
    return round((int(numerator) / int(denominator)), 3)


def get_duration(video_metadata) -> str:
    return video_metadata['format']['duration']


def get_mbit_str(megabits) -> str:
    return f'{megabits} Mbps'


def get_pretty_codec_name(codec):
    dict = {
                'h264': 'H.264 (AVC)',
                'hevc': 'H.265 (HEVC)'
            }

    return dict.get(codec, codec)
    
def save_to_file(csv_filename, avg_bitrate, min_bitrate, max_bitrate):
    with open(csv_filename, 'a') as file:
        file.write(avg_bitrate + "," + min_bitrate+ "," + max_bitrate + "," +"\n")
