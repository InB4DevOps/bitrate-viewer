import math
from os import path
from ffmpeg import probe


class VideoAttributeExtractor():
    def __init__(self, video_path) -> None:
        self.source_file = video_path

    @property 
    def video_attributes() -> dict:
        if not self._video_attributes: 
            return probe(self.source_file)
        return self._video_attributes: 

    def get_bitrate(self) -> str:
        bitrate = self.video_attributes['format']['bit_rate']
        return f'{math.trunc(int(bitrate) / 1000)} kbit/s'


    def get_framerate_fraction(self) -> str:
        r_frame_rate = [stream for stream in self.video_attributes['streams']
                        if stream['codec_type'] == 'video'][0][
            'r_frame_rate']
        return r_frame_rate


    def get_framerate_float(self) -> str:
        numerator, denominator = get_framerate_fraction(self.video_attributes).split('/')
        return round((int(numerator) / int(denominator)), 3)


    def get_duration(self) -> str:
        return self.video_attributes['format']['duration']


def get_mbit_str(megabits) -> str:
    return f'{megabits} Mbps'


def get_pretty_codec_name(codec):
    dict = {
                'h264': 'H.264 (AVC)',
                'hevc': 'H.265 (HEVC)'
            }

    return dict.get(codec, codec)
    
def save_to_file(csv_filename, avg_bitrate, min_bitrate, max_bitrate):
    if not path.isfile(csv_filename):
        with open(csv_filename, 'a') as file:
            file.write("Average Bitrate,Minimum Bitrate,Max BitRate" + "\n")
        
    with open(csv_filename, 'a') as file:
        file.write(avg_bitrate + "," + min_bitrate+ "," + max_bitrate + "," +"\n")
