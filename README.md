# bitrate-viewer
Plots a graph showing the variation of the bitrate as well as up to 75 I-Frames throughout your video. The average bitrate is shown on the legend. In addition to this, the minimum, maximum and standard deviation is shown above the graph. See the example below:



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
                        Enter the path of the input video. 
                        A relative or absolute path can bespecified.
  -f {xml,json}, --output-format {xml,json}
                        Specify the output format for the file written
                        by FFProbe. (default: 'xml')
  -s {csv}, --save-file DATA.CSV
                        Specify optional csv file to save avg, min, and max bitrate)
```

Example: `python main.py -i video.mp4 -s data.csv -f json`

This forces FFprobe to write its output in JSON (default is XML) and saves it as <video_file_name>.json.
The graph will be saved as <video_file_name>.png.

Special thanks to [@CrypticSignal]( https://github.com/CrypticSignal ) for helping me along the way.
