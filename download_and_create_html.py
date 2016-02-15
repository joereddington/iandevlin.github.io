import pysrt
import csv
import get_files
import os
import argparse


def setup_argument_list():
        "creates and parses the argument list for naCount"
        parser = argparse.ArgumentParser(
            description=__doc__)
        parser.add_argument('-u', nargs="?", dest='url',
                            help="Updates one particular URL")
        return parser.parse_args()


def get_gformat_subs(filename):
        """returns the set of subtitles in a csv file,
        intended to parse files form google drive"""
        with open(filename, 'rb') as subs_file:
                reader = csv.reader(subs_file, skipinitialspace=True)
                headers = next(reader, None)[3:]
#                print "Headers", headers
                lines = filter(None, reader)
                return (headers, lines)


def convert_sup_to_srt(filename):
        names = []
        column = 2
        try:
#                print "Examining: "+filename
                (headers, group) = get_gformat_subs(filename)
                #print "Headers", headers
                for language in headers:
                        subs = pysrt.SubRipFile()
                       # print "We are currently looking at", language
                        column = column+1
                        tag = language.replace(" ", "_")
                        for line in group:
                                if (len(line[column]) > 1):
                                        current_sub = pysrt.SubRipItem()
                                        current_sub.start = line[
                                                0].replace(',', '.')
                                        current_sub.end = line[
                                                1].replace(',', '.')
                                        current_sub.text = line[
                                                column].decode('latin-1')
                                        subs.append(current_sub)
                        subs.save('temp.vtt')
                        new_filename = 'live/subtitles/' + os.path.splitext(
                                os.path.basename(filename))[0]+tag+'.vtt'
#                        print "Created:" + new_filename
                        os.system('echo WEBVTT > '+new_filename)
                        os.system('cat temp.vtt >> '+new_filename)
                        names.append((new_filename, len(subs), language))
                return names
        except IndexError:
                print "I'm Sorry - wrong sort of file :( "
                return ""


def create_webpage(filename):
#        print "Create_webpage in:", filename
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
        new_filename = "live/"+os.path.splitext(
            os.path.basename(filename))[0]+'.html'
        print new_filename
        with open(new_filename, "w") as myfile:
                myfile.write(mastertext)


def process_subfile(filename):
        "Subfiles might produce many many html files"
     #   print "here" + filename
        newfilenames = convert_sup_to_srt(filename)
        total_utterances = newfilenames[0][1]
     #   print total_utterances
        for newfilename in newfilenames:
     #           print newfilename[0]
#                print newfilename[1]
                percentage_complete = float(
                    newfilename[1])/float(total_utterances)*100
                print "{} version is  {}% complete with filename: {}".format(newfilename[2], percentage_complete, newfilename[0])
                create_webpage(newfilename[0])


def convert_folder_into_html(files_downloaded):
        """ Then we convert them into files that can be played by our player.
        while also creating the table of thier information"""
        for filename in files_downloaded:
                process_subfile(filename)

# First thing is that we download the files that are there.
#
args = setup_argument_list()
if args.url:
        url = args.url
        filename = get_files.download_file(args.url)
        process_subfile(filename)
else:
        convert_folder_into_html(get_files.download_folder())
