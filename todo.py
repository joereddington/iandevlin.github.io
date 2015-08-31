import pysrt,csv
import get_files


def convert_srt_to_sup(input_file, out_file):
        subs = pysrt.open(input_file)
        with open(out_file, "wb") as f:
                writer = csv.writer(f)
                writer.writerow(
                    ("Start",
                     "End",
                     "Character",
                     "Original Text",
                     "Translation",
                     "Machine Translations"))
                for caption in subs:
                        print caption.text
                        writer.writerow(
                            (caption.start, caption.end, "", caption.text.encode('latin-1'), "", ""))



#So what do we have to do?


#First thing is that we download the files that are there.
#
get_files.download_folder()
#
#Then we convert them into files that can be played by our player.
#
#hang on - we have this going the other way right?
files=[]#pressumably something returned by the download_folder function
for episode in files:
	newfilename=convert_sup_to_srt(episode)
	createWebpage(newfilename)



