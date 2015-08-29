import pysrt
import csv

def get_gformat_subs():
    "returns the set of subtitles in a csv file, intended to parse files form google drive"
    with open('sources/Evetimed.csv', 'rb') as subs_file:
        reader = csv.reader(subs_file, skipinitialspace=True)
        lines = filter(None, reader)
        return lines

group=get_gformat_subs()
for line in group: 
    time_string=line[1]
    subtitle=line[3]
    print time_string + " " + subtitle

#subs = pysrt.open('subtitles/Eve.srt')
#for caption in subs:
#   caption.text= caption.text.replace('\n', ' ').replace('\r', '')
#   print caption.text
#
