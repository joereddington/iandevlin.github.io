import pysrt,csv
import get_files
import os
from os.path import basename

#filename = "traffic-cops-series-13-2-excess-alcohol.csv.csv"


def get_gformat_subs(filename):
        """returns the set of subtitles in a csv file,
        intended to parse files form google drive"""
        with open(filename, 'rb') as subs_file:
                reader = csv.reader(subs_file, skipinitialspace=True)
                next(reader, None)  # skip the header row
                lines = filter(None, reader)
                return lines

def convert_sup_to_srt(filename):
    try:
        print "Examining: "+filename
        group = get_gformat_subs(filename)
        subs = pysrt.SubRipFile()
        for line in group:
                current_sub = pysrt.SubRipItem()
                current_sub.start = line[0].replace(',', '.')
                current_sub.end = line[1].replace(',', '.')
                current_sub.text = line[3].decode('latin-1')
                subs.append(current_sub)

        subs.save('temp.vtt')
        new_filename='live/subtitles/'+os.path.splitext(os.path.basename(filename))[0]+'.vtt'
        print "Created:"+ new_filename
        os.system('echo WEBVTT > '+new_filename)
        os.system('cat temp.vtt >> '+new_filename)
        return new_filename
    except IndexError:
        print "I'm Sorry - wrong sort of file :( "
        return ""




#First thing is that we download the files that are there.
#
files_downloaded=get_files.download_folder()
#
#Then we convert them into files that can be played by our player.
for episode in files_downloaded:
        print episode
	newfilename=convert_sup_to_srt(episode)
#	createWebpage(newfilename)



