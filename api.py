from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
# from lsa_process import get_LSA, clear_files
import os
import pyrebase

app = Flask(__name__)
api = Api(app)
CORS(app)

firebaseConfig = {
  "apiKey": "AIzaSyDhz498FkxVmBi5vANkCAUB1vLnKtk9Roo",
  "authDomain": "abv-api.firebaseapp.com",
  "projectId": "abv-api",
  "storageBucket": "abv-api.appspot.com",
  "databaseURL": "",
  "serviceAccount": {
    "type": "service_account",
    "project_id": "abv-api",
    "private_key_id": "c7b85dd07ea738a4427a369bf7575b8b383797c1",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCpFSTmTCnHNSNU\nFQTyFatWs+2xMpARXBpOuhfVbjrW/yMmLK1kzNvo/D7RztzG0n6Voc6qmtFNFs98\nzOP0sIDRHHJ/XTyZGu0au0NF3AziemPwA0g/l2PR6iRnvVsciUFsxk3tm8R2kKav\nRH6mn73T7axIcNQODmGSU9uzm30eTx+UDtLEKEhxFYmKPnoHWteqetHfa5yEOGK3\ntXrB4rmn7FRq1n5+2fZZU28chGmtQYe6l3NpKEmHONWZPJNlDgijBI4XVW5FApRF\nNmS98HR0Vo5VA92TFeSwhNNkhYtqy4NVfH1wJByysLpoHPjz9/yx+A9pJebcw6yX\nsyYAcxb1AgMBAAECggEACNT32xIrEEZGkvnXp1jg+VkndyQ304EzY0FAcAM0nJx5\nBO+8Kc5d092/3vOb3FKajuJ1qi0jEnPxoPMOqPyJsLDNp9Vexx/nxUC+TZBfJ7PL\nerL1osUp67PRO8caYPpg31QR/TihrFeT2Oox9BHWzNnBaRlHqXeiD+O2QVf8mhAc\niyUoaiRyTGl8uFmE2AAZZf9B5Wh7AMhdgm7HGSPJ7zJ3tWEjXU4fBETGRNoniUfO\ndeXyTCB5pc4ZLPSqQc52c1JOQsI35mMBy5fPn2VjaO5g78L6Nkdr1UeEHAJAohxk\nnCnu2KxZmvTUVGVe/X+PIp40GdEOq0dZV5SpKDVzcwKBgQDdnkfV3sF59jUnd4Im\nsFhlsQ1G9ps0tkxvbIWP85Jsu1Lf0J5U6NJhmH1t9Ck/rIfghFdVqjWrtsUYw7wQ\nUPAebNzlT5tQcKBk1oTz+Vff6OI4YRL+DUWGbFGzskhOGPeX4S11vRZTnonX9RnC\nocKxihqJ4ADNfl9tbSMww9ILfwKBgQDDUF+NKV9P3ziXWM0UMohYlS7qmf+w6L69\nRTmEHp4LHfNUcwDjdhYU025HZc29F3iCGsu2JGks6wGb7QIKHuCaePhfzOv53TCa\nhF87AlC8yXCQo1g8iWKc6AeQL/7l44a/s9l66PPyvABIrivE7H4TYDNmna+K68hQ\nFKFTt5mniwKBgCas0aJ8Lk2Hbv1FONxhl/ufK08ACFPpoGstiB14B0ycYDkY4hi1\nTMmlX/ZJTs2C4W+ICOm1O4qM6daJig9a4JyeqOoHu3YNQaB3Y1pkYDZ+IMRwBG17\niW+NBbETYtTmPIcvz8wlRHkxSKL8bhNuQVjUXg9DnUA/Vo31JtgCxGwnAoGBAKai\nqgMbqy/P+M5XexCiVGWPUiniHZ5n1GRS7VFldd1yPipsu/NUyl4WTV4o4zFTFwOZ\nrPfHdNxX3FWWDkloMqRYVUAW67WQG2mZSk5kGVIYYytj0WJErJfF9r3z1Pt59XsV\nDJWqrocIEw3vW3R1eNM7Hl+MZTqXE54PG9z7JeMlAoGASuZ0SPJg9XwcHGevPaOT\nu5QzgGIaKOwPM2hyiy00ibKR+o5L1+oae5oZjNdXe3NiAU/bz075zrmZFY8XKoMy\npp057fcSqZdeLeV3ZIplMRDvo4yC+CniBHaJsdciA6qOJekZf1+DmZESg0li0BpO\n6dLY1YWPTy9j3Grvf/88F4w=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-eiryc@abv-api.iam.gserviceaccount.com",
    "client_id": "102445652903248906867",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-eiryc%40abv-api.iam.gserviceaccount.com"
  }
};

firebase_storage = pyrebase.initialize_app(firebaseConfig)
storage = firebase_storage.storage()


# download_file('KX879603.pdf', 'artigos/qualquer.pdf')

SYMPTOMS = [
    {
        'slug': 'anorexia',
        'name': 'anorexia'
    },
    {
        'slug': 'abdominal_pain',
        'name': 'abdominal pain'
    },
    {
        'slug': 'arthalgiaasthenia',
        'name': 'arthalgiaasthenia'
    },
    {
        'slug': 'backache',
        'name': 'backache'
    },
    {
        'slug': 'bilateral_conjunctivitis',
        'name': 'bilateral conjunctivitis'
    },
    {
        'slug': 'bleeding',
        'name': 'bleeding'
    },
    {
        'slug': 'body_ache',
        'name': 'body ache'
    },
    {
        'slug': 'cardiomegaly',
        'name': 'cardiomegaly'
    },
    {
        'slug': 'chills',
        'name': 'chills'
    },
    {
        'slug': 'conjunctivitis',
        'name': 'conjunctivitis'
    },
    {
        'slug': 'cough',
        'name': 'cough'
    },
    {
        'slug': 'dermal_lesions',
        'name': 'dermal lesions'
    },
    {
        'slug': 'diarrehea',
        'name': 'diarrehea'
    },
    {
        'slug': 'disabling_pain',
        'name': 'disabling pain'
    },
    {
        'slug': 'epistaxis',
        'name': 'epistaxis'
    },
    {
        'slug': 'erythematous_exanthema',
        'name': 'erythematous exanthema'
    },
    {
        'slug': 'erythematous_rashes',
        'name': 'erythematous rashes'
    },
    {
        'slug': 'eye_pain',
        'name': 'eye pain'
    },
    {
        'slug': 'facial_swelling',
        'name': 'facial swelling'
    },
    {
        'slug': 'fatigue',
        'name': 'fatigue'
    },
    {
        'slug': 'fever',
        'name': 'fever'
    },
    {
        'slug': 'headache',
        'name': 'headache'
    },
    {
        'slug': 'hepatitis',
        'name': 'hepatitis'
    },
    {
        'slug': 'high_fever',
        'name': 'high fever'
    },
    {
        'slug': 'hyperaesthesia',
        'name': 'hyperaesthesia'
    },
    {
        'slug': 'hyperpigmentation',
        'name': 'hyperpigmentation'
    },
    {
        'slug': 'joint_pain',
        'name': 'joint pain'
    },
    {
        'slug': 'lack_os_appetite',
        'name': 'lack os appetite'
    },
    {
        'slug': 'low_trombocyte_counts',
        'name': 'low trombocyte counts'
    },
    {
        'slug': 'lumbar_pain',
        'name': 'lumbar pain'
    },
    {
        'slug': 'macopapular_rash',
        'name': 'macopapular rash'
    },
    {
        'slug': 'macular_rash',
        'name': 'macular rash'
    },
    {
        'slug': 'muscle_pain',
        'name': 'muscle pain'
    },
    {
        'slug': 'muscle_spasm',
        'name': 'muscle spasm'
    },
    {
        'slug': 'myalgia',
        'name': 'myalgia'
    },
    {
        'slug': 'myocarditis',
        'name': 'myocarditis'
    },
    {
        'slug': 'nausea',
        'name': 'nausea'
    },
    {
        'slug': 'pancytopenia',
        'name': 'pancytopenia'
    },
    {
        'slug': 'pedal_swelling',
        'name': 'pedal swelling'
    },
    {
        'slug': 'prostation',
        'name': 'prostation'
    },
    {
        'slug': 'pulmonary_congestion',
        'name': 'pulmonary congestion'
    },
    {
        'slug': 'rash',
        'name': 'rash'
    },
    {
        'slug': 'rheumatoid',
        'name': 'rheumatoid'
    },
    {
        'slug': 'arthritis',
        'name': 'arthritis'
    },
    {
        'slug': 'seizure',
        'name': 'seizure'
    },
    {
        'slug': 'severe_arthalgia',
        'name': 'severe arthalgia'
    },
    {
        'slug': 'severe_asthenia',
        'name': 'severe asthenia'
    },
    {
        'slug': 'severe',
        'name': 'severe'
    },
    {
        'slug': 'bilateral_arthalgia',
        'name': 'bilateral arthalgia'
    },
    {
        'slug': 'shortness_of_breath',
        'name': 'shortness of breath'
    },
    {
        'slug': 'tenosynovitis',
        'name': 'tenosynovitis'
    },
    {
        'slug': 'transient_macular_rash',
        'name': 'transient macular rash'
    },
    {
        'slug': 'unwell',
        'name': 'unwell'
    },
    {
        'slug': 'wrist_pain',
        'name': 'wrist pain'
    }
]

class SymptomsList(Resource):
    def get(self):
       return SYMPTOMS, 200

# class FileNames(Resource):
#     def get(self):
#         return get_all_files()

# class LsaScore(Resource):
#     def get(self):
#       parser = reqparse.RequestParser()
#       parser.add_argument('symptom', action='append', location='args')
#       args = parser.parse_args()

#       # download_all_files()
#       # lsa_result = get_LSA()
#       # clear_files()
#       return args['symptom'], 200



api.add_resource(SymptomsList, '/symptoms')
# api.add_resource(FileNames, '/file-names')
# api.add_resource(LsaScore, '/lsa-score')

if __name__ == '__main__':
    app.run(debug=True)
