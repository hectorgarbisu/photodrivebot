from pydrive.auth import GoogleAuth
from googleapiclient.http import MediaFileUpload
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
#gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
gauth.LoadCredentialsFile("data/mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.CommandLineAuth() #para remotos
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("data/mycreds.txt")

drive = GoogleDrive(gauth)

folder_id = None

def setFolder(folder): 
    global folder_id
    folder_id = folder


def uploadFile(path = 'data/blep.txt'):
    if not folder_id:
        print("Please, first set a folder with driveUploader.setFolder(_)")
        return
    
    options = {"parents": [{"kind": "drive#fileLink", "id": folder_id}]}
    file = drive.CreateFile(options)
    file.SetContentFile(path)
    file.Upload()
