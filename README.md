# bitrate-viewer
Calculates the actual bitrate per second for x264 and x265 and plots a graph.



![Example Graph](https://github.com/InB4DevOps/bitrate-viewer/blob/main/bitrate_graph.png?raw=true)

# Requirements:
- Python **3.6+**
- `pip install -r requirements.txt`
- FFprobe in your PATH.

# Usage
```
usage: main.py [-h] -i INPUT_VIDEO_PATH [-f {xml,json}]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_VIDEO_PATH, --input-video-path INPUT_VIDEO_PATH
                        Enter the path of the original video. A relative or absolute path can bespecified.
  -f {xml,json}, --output-format {xml,json}
                        Specify the output format for the file written
                        by FFProbe. (default: 'xml')
```

Example: `python main.py -i video.mp4 -f json`

This forces FFprobe to write its output in JSON and saves it as bitrate.json.
The graph will be saved to bitrate_graph.png.

Special thanks to [@BassThatHertz]( https://github.com/BassThatHertz ) for helping me along the way.
