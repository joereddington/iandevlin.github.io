from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import sys
import csv


def enguage_auth():
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile("mycreds.txt")
        if gauth.credentials is None:
                # Authenticate if they're not there
                gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
                # Refresh them if expired
                gauth.Refresh()
        else:
                # Initialize the saved creds
                gauth.Authorize()
        # Save the current credentials to a file
        gauth.SaveCredentialsFile("mycreds.txt")
        # from http://stackoverflow.com/a/24542604/170243
        gauth.LocalWebserverAuth()
        return gauth


def chop_input_url(url):
        lastslash_loc = url.rfind("/")
        if lastslash_loc > 40:
                return url[:lastslash_loc]
        return url


def get_translated_subs(filename, english=False):
        "returns a sorted list of nextActions"
        with open(filename) as subs_file:
                reader = csv.reader(subs_file, skipinitialspace=True)
                for row in reader:
                        if english is True:
                                print row[3]
                        else:
                                print row[4]


def download_folder(url=""):
        drive = GoogleDrive(enguage_auth())
        search_string = "'0BxcNVxCOXNUvfkIyMWxIcGU2WkdfX0FiOTljYzVlZ1V5eW5NXzY0bHpQUGpPV3hfTkI1VHM' in parents and trashed=false"
        # Auto-iterate through all files in the root folder.
        files_found = []
        file_list = drive.ListFile(
            {'q': search_string}).GetList()
        for file1 in file_list:
                if url in file1['embedLink']:
                        print 'title: %s, id: %s' % (file1['title'], file1['id'])
                        if file1['mimeType'] == "application/vnd.google-apps.spreadsheet":
                                filename = "sources/" + \
                                    file1['title'].replace(" ", "")+".csv"
                                files_found.append(filename)
                                file1.GetContentFile(
                                    filename,
                                    mimetype='text/csv')
                                continue
                        if file1['mimeType'] == "application/vnd.google-apps.folder":
                                continue
        # get_translated_subs(filename)
        return files_found

if __name__ == "__main__":
# print
# chop_input_url("https://docs.google.com/spreadsheets/d/1p5f8Isz8ds-is5xnaD_bLZgnveF6jea3SYdJKVmRJbM")
        if len(sys.argv) > 1:
                download_folder(chop_input_url(sys.argv[1]))
        else:
                download_folder()
