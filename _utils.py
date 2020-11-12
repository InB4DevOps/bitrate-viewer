import math
from ffmpeg import probe


def get_bitrate(video_path):
    bitrate = probe(video_path)['format']['bit_rate']
    return f'{math.trunc(int(bitrate) / 1000)} kbit/s'


def get_framerate_fraction(video_path):
    r_frame_rate = [stream for stream in probe(video_path)['streams']
                    if stream['codec_type'] == 'video'][0][
        'r_frame_rate']
    return r_frame_rate


def get_framerate_float(video_path):
    numerator, denominator = get_framerate_fraction(video_path).split('/')
    return round((int(numerator) / int(denominator)), 3)


def get_duration(video_path):
    return probe(video_path)['format']['duration']


def get_mbit_str(megabits):
    return f'{megabits} Mbps'


def get_pretty_codec_name(codec):
    result = str()
    if codec == 'h264':
        result = 'H.264 (AVC)'
    elif codec == 'hevc':
        result = 'H.265 (HEVC)'
    else:
        result = codec

    return result
