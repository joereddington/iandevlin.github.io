import pysrt
import csv
import get_files
import os


#So the main thing to do now is to split this between the various languages that appear in an individual file

def get_gformat_subs(filename):
        """returns the set of subtitles in a csv file,
        intended to parse files form google drive"""
        with open(filename, 'rb') as subs_file:
                reader = csv.reader(subs_file, skipinitialspace=True)
                headers=next(reader, None)[3:]
                print "Headers", headers
                lines = filter(None, reader)
                return (headers,lines)


def convert_sup_to_srt(filename):
        names=[]
        column=2
        try:
                print "Examining: "+filename
                (headers, group) = get_gformat_subs(filename)
                print "Headers", headers
                for language in headers:
                    subs = pysrt.SubRipFile()
                    print "We are currently looking at", language
                    column=column+1
                    tag=language.replace(" ","_")
                    for line in group:
                            current_sub = pysrt.SubRipItem()
                            current_sub.start = line[0].replace(',', '.')
                            current_sub.end = line[1].replace(',', '.')
                            current_sub.text = line[column].decode('utf-8')
                            subs.append(current_sub)

                    subs.save('temp.vtt')
                    new_filename = 'live/subtitles/' + \
                        os.path.splitext(os.path.basename(filename))[0]+"_"+tag+'.vtt'
                    print "Created:" + new_filename
                    os.system('echo WEBVTT > '+new_filename)
                    os.system('cat temp.vtt >> '+new_filename)
                    names.append(new_filename)
                return names
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
        newfilenames = convert_sup_to_srt(episode)
        for newfilename in newfilenames:
            print "New filename is: ", newfilename
            create_webpage(newfilename)
