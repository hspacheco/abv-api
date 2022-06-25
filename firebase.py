import pyrebase
# import os

firebaseConfig = {
  "apiKey": "AIzaSyDhz498FkxVmBi5vANkCAUB1vLnKtk9Roo",
  "authDomain": "abv-api.firebaseapp.com",
  "projectId": "abv-api",
  "storageBucket": "abv-api.appspot.com",
  "databaseURL": "",
  "serviceAccount": "serviceAccountKey.json"
};

firebase_storage = pyrebase.initialize_app(firebaseConfig)
storage = firebase_storage.storage()

def download_file(file_ref, save_name):
  storage.child(file_ref).download(save_name)

def get_all_files():
  files = storage.list_files()
  storageFiles = [] 
  for file in files:
    storageFiles.append(file.name)
    print(file.name)
  
  return storageFiles

# def download_all_files():
#   file_names = get_all_files()
#   if (os.path.isdir('artigos') == False):
#     os.mkdir('artigos')
  
#   for file_name in file_names:
#     download_file(file_name, f'artigos/{file_name}')

# clear_files()

# storage.child("AF192906.pdf").put("AF192906.pdf")

# print(storage.child("KX879603.pdf").get_url(None))