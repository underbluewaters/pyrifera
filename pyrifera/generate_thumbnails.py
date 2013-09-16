# generate_thumbnails.py
# Usage:
#   python generate_thumbnails.py /Users/cburt/kfm_videos/
# 
# Generates thumbnails for use in pyrifera.marinemap.org.
# Must be run on a system with ffmpeg installed.

import os
import sys
import subprocess
from os.path import normpath

for file in os.listdir("."):
    if not '.mp4.jpg' in file and not '.py' in file:
        file = normpath(file)
        print file
        subprocess.call([
            'ffmpeg', 
            '-ss',
            '00:02:30',
            '-i',
            file, 
            '-an', 
            '-vframes',
            '1',
            '-s',
            '480x320',
            ('%s.%%03d.jpg' % (file, ))
        ], shell=True)
        #command = 'ffmpeg -i %s%s -an -vframes 1 -ss 80:00:00 -s 480x320 %s%s.%%03d.jpg' % (rootdir, file,)
        #os.system(command)
        src = normpath('%s.001.jpg' % (file, ))
        dst = normpath('%s.jpg' % (file, ))
        print src
        print dst
        os.rename(src, dst)
        print "renamed"