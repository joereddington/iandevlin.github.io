import pysrt


subs = pysrt.open('subtitles/Eve.srt')
for caption in subs:
   print caption.text.replace('\n', ' ').replace('\r', '')

