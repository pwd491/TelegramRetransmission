import sys
import subprocess

RTMP_SERVER = ""
RTMP_KEY = ""

processes: list[subprocess.Popen] = []

def streaming() -> None:
    """
    Converting video to FLV and starts Telegram Live Broadcast. Converted video
    saved into RAM by using PIPE. You can change everything except the encoding
    libx264. 
    
    Read about the arguments here: https://ffmpeg.org/ffmpeg.html
    """
    with subprocess.Popen((
        "ffmpeg", 
        "-y",
        "-i", "source/file.mp4",
        "-c:v", "libx264",
        "-preset", "medium", 
        "-b:v", "6000k",
        "-maxrate", "3000k",
        "-bufsize", "6000k",
        "-vf", "scale=1920:-1, format=yuv420p",
        "-g", "50",
        "-c:a", "aac",
        "-b:a", "128k",
        "-ac", "2",
        "-ar", "44100",
        "-f", "flv",
        "-"
    ), stdout=subprocess.PIPE, encoding="utf-8") as converter:
        processes.append(converter)
        with subprocess.Popen((
            "ffmpeg",
            "-re",
            "-i", "-",
            "-codec", "copy",
            "-f", "flv",
            RTMP_SERVER  + RTMP_KEY
        ), stdin=converter.stdout) as stream:
            processes.append(stream)


if __name__ == '__main__':
    try:
        streaming()
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()
            process.kill()
    finally:
        sys.exit(1)
