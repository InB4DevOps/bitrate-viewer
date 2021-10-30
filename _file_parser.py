import json
import xml.etree.ElementTree as ET


class FileParser:
    def __calculate_bitrate_per_sec(self, bitrates):
        seconds = []
        bitrates_per_sec = []
        current_second = 0
        current_bitrate = 0
        frame_count = 0

        for bitrate in bitrates:
            current_bitrate += bitrate
            frame_count += 1

            if frame_count == self.__fps:
                seconds.append(current_second)
                bitrates_per_sec.append(current_bitrate / 1_000_000)  # megabit
                current_bitrate = 0
                frame_count = 0
                current_second += 1

        return seconds, bitrates_per_sec

    def __read_key_frame_time(self, frame) -> float:
        """
        reads frame time from pkt_pts_time if it exists
        or uses pkt_dts_time otherwise
        returns None if neither exists
        """
        frame_time = frame.get('pkt_pts_time')
        if not frame_time:
            frame_time = frame.get('pkt_dts_time')

        return (float(frame_time)) if frame_time else None

    def __load_xml(self):
        """
        Loads bitrate and I-frames from XML file
        """
        bitrates = []
        keyframes = []
        root = ET.parse(self.__filename).getroot()
        for frame in root.findall('frames/frame'):
            value = int(frame.get('pkt_size'))
            bitrates.append(value * 8)  # pkt_size is in byte

            if int(frame.get('key_frame')) == 1:
                keyframe_time = self.__read_key_frame_time(frame)
                if keyframe_time:
                    keyframes.append(keyframe_time)

        streams = root.findall('streams/stream')
        encoder = streams[0].get('codec_name')
        return bitrates, keyframes, encoder

    def __load_json(self):
        """
        Loads bitrate and I-frames JSON file
        """
        bitrates = []
        keyframes = []
        read_file = open(self.__filename, 'r')
        data = json.load(read_file)

        for frame in data['frames']:
            value = int(frame['pkt_size'])
            bitrates.append(value * 8)  # pkt_size is in byte

            if int(frame['key_frame']) == 1:
                keyframe_time = self.__read_key_frame_time(frame)
                if keyframe_time:
                    keyframes.append(keyframe_time)

        encoder = data['streams'][0]['codec_name']
        read_file.close()

        return bitrates, keyframes, encoder

    def run(self, filename, format, fps):
        """
        Loads the file written by FFprobe, reads the packet size of each frame
        and sums it up every <fps> seconds to calculate the bitrate / second.
        """
        bitrates = []
        keyframes = []
        encoder = str()
        self.__format = format
        self.__fps = fps
        self.__filename = filename

        if format == 'xml':
            bitrates, keyframes, encoder = self.__load_xml()
        elif format == 'json':
            bitrates, keyframes, encoder = self.__load_json()

        seconds, bitrates_per_sec = self.__calculate_bitrate_per_sec(bitrates)

        return tuple([seconds, bitrates_per_sec, keyframes, encoder])
