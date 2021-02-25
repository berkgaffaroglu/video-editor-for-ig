import moviepy.editor as mp
import numpy as np
import sys
import subprocess
import os
import urllib.request

DEBUG = True if sys.argv[-1] == '-d' else False

def main():
    video_path = sys.argv[1]
    video_name = video_path.split('.')[0]
    video = mp.VideoFileClip(video_path)
    if sys.argv[2] != '-a':
        startvideo = int(sys.argv[2])
        endvideo = int(sys.argv[3])
    else:
        startvideo= 0
        endvideo = video.duration
    video = video.subclip(startvideo, endvideo).resize((800,800))
    video_with_logo = addLogo(video=video, pagename="@mymovieshowclips", pos='left')
    ALL_FILES = os.listdir()
    i = 1
    while True:
          VIDEO_OUTPUT_NAME = video_name + f'{i}' + '.mp4'
          if VIDEO_OUTPUT_NAME in ALL_FILES:
                i+=1
          else:
                break

    addTimeLine(video_with_logo).write_videofile(f'{VIDEO_OUTPUT_NAME}', temp_audiofile='temp-audio.m4a', remove_temp=True, codec="libx264", audio_codec="aac")
    if DEBUG:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, f"{VIDEO_OUTPUT_NAME}"])


def addTimeLine(video):
    WIDTH_VIDEO, HEIGHT_VIDEO = video.size
    VIDEO_DURATION = video.duration
    TIMELINE_HEIGHT = 7
    TIMELINE_Y = HEIGHT_VIDEO-TIMELINE_HEIGHT
    speed = WIDTH_VIDEO/VIDEO_DURATION * 1.05
    yellowBackground = (mp.ImageClip("yellow.png")
                        .set_duration(VIDEO_DURATION)
                        .resize(width=WIDTH_VIDEO)
                        .set_pos((0, TIMELINE_Y)))
    whiteBackground = (mp.ImageClip("white.jpg")
                       .set_duration(VIDEO_DURATION)
                       .resize(width=WIDTH_VIDEO)
                       .set_pos(lambda t: (t*speed, TIMELINE_Y)))
    edited_video = mp.CompositeVideoClip([video, yellowBackground])
    edited_video = mp.CompositeVideoClip([edited_video, whiteBackground])
    return edited_video


def addLogo(video, pagename="mymovieshowclips", pos='left', margin=(8,15)):
    LOGO_MARGIN_TOP, LOGO_MARGIN_HORIZONTAL = margin
    fontsize=15
    if pos == 'left':
        LOGO_POS = margin
    elif pos == 'right':
        LOGO_POS = (video.size[0] - fontsize - LOGO_MARGIN_HORIZONTAL, LOGO_MARGIN_TOP)
    elif pos == 'middle':
        LOGO_POS = (video.size[0]/2 - LOGO_MARGIN_HORIZONTAL, LOGO_MARGIN_TOP)    
    
    VIDEO_DURATION = video.duration
    logo = mp.TextClip(pagename, fontsize = fontsize, color = 'white').set_duration(VIDEO_DURATION).set_position(LOGO_POS)

    edited_video = mp.CompositeVideoClip([video, logo])
    return edited_video


if __name__ == "__main__":
    main()
