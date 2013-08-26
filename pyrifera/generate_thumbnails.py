# generate_thumbnails.py
# Usage:
#   python generate_thumbnails.py /Users/cburt/kfm_videos/
# 
# Generates thumbnails for use in pyrifera.marinemap.org.
# Must be run on a system with ffmpeg installed.

import os
import sys
rootdir = sys.argv[1]
for file in os.listdir(rootdir):
    if not '.mp4.jpg' in file and not '.py' in file:
        file = file.replace(' ', '\ ')
        command = 'ffmpeg -i %s%s -an -vframes 1 -ss 80:00:00 -s 480x320 %s%s.%%03d.jpg' % (rootdir, file, rootdir, file,)
        os.system(command)
        src = '%s%s.001.jpg' % (rootdir, file)
        dst = '%s%s.jpg' % (rootdir, file)
        print src
        print dst
        os.system('mv %s %s' % (src, dst))
        print "renamed"