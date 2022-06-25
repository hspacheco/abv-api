import pyrebase
import os

firebaseConfig = {
  "apiKey": "AIzaSyDhz498FkxVmBi5vANkCAUB1vLnKtk9Roo",
  "authDomain": "abv-api.firebaseapp.com",
  "projectId": "abv-api",
  "storageBucket": "abv-api.appspot.com",
  "databaseURL": "",
  "serviceAccount": "serviceAccountKey.json"
};

try:
  firebase_storage = pyrebase.initialize_app(firebaseConfig)
  storage = firebase_storage.storage()
except Exception as inst:
  print(inst.args)

def download_file(file_ref, save_name):
  storage.child(file_ref).download(save_name)

def get_all_files():
  files = storage.list_files()
  storageFiles = [] 
  for file in files:
    storageFiles.append(file.name)
    print(file.name)
  
  return storageFiles

def download_all_files():
  file_names = get_all_files()
  if (os.path.isdir('artigos') == False):
    os.mkdir('artigos')
  
  for file_name in file_names:
    download_file(file_name, f'artigos/{file_name}')
