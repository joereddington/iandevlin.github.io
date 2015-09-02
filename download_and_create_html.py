import pysrt
import csv
import get_files
import os


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
                new_filename = 'live/subtitles/' + \
                    os.path.splitext(os.path.basename(filename))[0]+'.vtt'
                print "Created:" + new_filename
                os.system('echo WEBVTT > '+new_filename)
                os.system('cat temp.vtt >> '+new_filename)
                return new_filename
        except IndexError:
                print "I'm Sorry - wrong sort of file :( "
                return ""


def create_webpage(filename):
        print  "Create_webpage in:", filename
        """Creates a html file inserts the subtitle filename and saves it with
        the correct filename"""
        mastertext = """
<!DOCTYPE html>
<html lang="en-IE">
   <head>
      <meta charset="utf-8" />
      <title>Supertitle Exmaple</title>
      <link rel="stylesheet" href="css/styles.css" />
   </head>
   <body>
      <video id="video" controls preload="metadata">
         <source src="video/output.mp4" type="video/mp4">
         <track label="hope" kind="subtitles" srclang="en" src="../{}" default>
      </video>
      <script src="js/video-player.js"></script>
   </body>
</html>""".format(filename)
        new_filename = "live/"+os.path.splitext(os.path.basename(filename))[0]+'.html'
        print new_filename
        with open(new_filename, "w") as myfile:
                myfile.write(mastertext)


# First thing is that we download the files that are there.
#
files_downloaded = get_files.download_folder()
#
# Then we convert them into files that can be played by our player.
for episode in files_downloaded:
        print episode
        newfilename = convert_sup_to_srt(episode)
        print "New filename is: ", newfilename
        create_webpage(newfilename)
