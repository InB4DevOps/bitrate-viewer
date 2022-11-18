import math
from os import path
from ffmpeg import probe
from csv import DictWriter
from typing import Any

CSV_HEADERS = [
    "avg_bitrate",
    "max_bitrate",
    "min_bitrate",
    "encoder",
    "std_bitrate"]
class VideoAttributeExtractor():
    def __init__(self, video_path) -> None:
        self.source_file = video_path
        self._video_attributes = None

    @property 
    def video_attributes(self) -> dict:
        if not self._video_attributes: 
            self._video_attributes = probe(self.source_file)
        return self._video_attributes

    def get_bitrate(self) -> str:
        bitrate = self.video_attributes['format']['bit_rate']
        return f'{math.trunc(int(bitrate) / 1000)} kbit/s'


    def get_framerate_fraction(self) -> str:
        r_frame_rate = [stream for stream in self.video_attributes['streams']
                        if stream['codec_type'] == 'video'][0][
            'r_frame_rate']
        return r_frame_rate


    def get_framerate_float(self) -> str:
        numerator, denominator = self.get_framerate_fraction().split('/')
        return round((int(numerator) / int(denominator)), 3)


    def get_duration(self) -> str:
        return self.video_attributes['format']['duration']


def get_mbit_str(megabits) -> str:
    return f'{megabits} Mbps'


def get_pretty_codec_name(codec) -> dict:
    dict = {
                'h264': 'H.264 (AVC)',
                'hevc': 'H.265 (HEVC)'
            }

    return dict.get(codec, codec)
    
def save_to_file(csv_filename, bit_rate_data: dict=None):
    dict_as_csv = [bit_rate_data]
    """Save Bit Rate Data to file

    Args:
        csv_filename (str): _description_
        bit_rate_data (dict): Video analysis results
    """  
    if not path.isfile(csv_filename):
        with open(csv_filename, 'a') as csv_file:
            csv_writer = DictWriter(csv_file, fieldnames=CSV_HEADERS)
            csv_writer.writeheader()
            for bit_rate_row in dict_as_csv:
                print(bit_rate_row)
                csv_writer.writerow(bit_rate_row)