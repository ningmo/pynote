#coding:utf-8


f = './aa.mp4';

# import imageio
# print imageio.plugins.ffmpeg.download()
import matplotlib
from moviepy.editor import  *

# Load myHolidays.mp4 and select the subclip 00:00:50 - 00:00:60
print VideoFileClip(f)
clip = VideoFileClip(f).subclip(50,-50)
clip = clip.volumex(0.8)

# Generate a text clip. You can customize the font, color, etc.
# txt_clip = TextClip("My Holidays 2013")
#
# # Say that you want it to appear 10s at the center of the screen
# txt_clip = txt_clip.set_pos('center').set_duration(10)
#imgclip = ImageClip("timg.jpeg")


# Overlay the text clip on the first video clip
video = CompositeVideoClip([clip])

# Write the result to a file (many options available !)
video.write_videofile("new.webm")
