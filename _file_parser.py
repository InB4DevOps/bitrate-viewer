import json
import xml.etree.ElementTree as ET


class FileParser:
    def __init__(self):
        self.__result = ([], [], str())

    def __calculate_bitrate_per_sec(self, bitrates):
        seconds, bitrates_per_sec, _ = self.__result
        current_second = 1
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

    def __load_xml(self):
        """
        Loads bitrate from frames in XML file
        """
        bitrates = []
        root = ET.parse(self.__filename).getroot()
        for frame in root.findall('frames/frame'):
            value = int(frame.get('pkt_size'))
            bitrates.append(value * 8)  # pkt_size is in byte

        streams = root.findall('streams/stream')
        # stream = streams[0]
        encoder = streams[0].get('codec_name')
        # stream = streams[0]
        # encoder = stream.get('codec_name')
        return bitrates, encoder

    def __load_json(self):
        """
        Loads bitrate from frames in JSON file
        """
        bitrates = []
        read_file = open(self.__filename, 'r')
        data = json.load(read_file)

        for frame in data['frames']:
            value = int(frame['pkt_size'])
            bitrates.append(value * 8)  # pkt_size is in byte

        encoder = data['streams'][0]['codec_name']
        read_file.close()

        return bitrates, encoder

    def run(self, filename, format, fps):
        """
        Loads the file written by FFprobe, reads the packet size of each frame
        and sums it up every <fps> seconds to calculate the bitrate / second.
        """
        bitrates = []
        encoder = str()
        self.__format = format
        self.__fps = fps
        self.__filename = filename

        if format == 'xml':
            bitrates, encoder = self.__load_xml()
        elif format == 'json':
            bitrates, encoder = self.__load_json()

        result_list = list(self.__result)
        result_list[2] = encoder
        self.__result = tuple(result_list)

        self.__calculate_bitrate_per_sec(bitrates)
        return self.__result
