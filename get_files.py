from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

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
#from http://stackoverflow.com/a/24542604/170243
gauth.LocalWebserverAuth()


drive = GoogleDrive(gauth)


# Auto-iterate through all files in the root folder.
file_list = drive.ListFile({'q':"'0BxcNVxCOXNUvfkIyMWxIcGU2WkdfX0FiOTljYzVlZ1V5eW5NXzY0bHpQUGpPV3hfTkI1VHM' in parents and trashed=false"}).GetList()
for file1 in file_list:
  print 'title: %s, id: %s' % (file1['title'], file1['id'])
  print file1['mimeType']
 
  if file1['mimeType']=="application/vnd.google-apps.spreadsheet":
     filename="sources/"+file1['title'].replace(" ","")+".csv"
     file1.GetContentFile(filename, mimetype='text/csv')
     continue 

  if file1['mimeType']=="application/vnd.google-apps.folder":
     continue
     filename="sources/"+file1['title'].replace(" ","")+".txt"
     file1.GetContentFile(filename, mimetype='text/plain')
