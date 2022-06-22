from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
import os

app = Flask(__name__)
api = Api(app)
CORS(app)

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

FILE_NAMES = [
  'EF555196',
  'DQ181797',
  'AF547225',
  'KX197192',
  'KU556802',
  'AY692465',
  'FJ882857',
  'KU820897',
  'AY606062',
  'AY326412',
  'LC146714',
  'AB010982',
  'U18425',
  'DQ859059',
  'EU359008',
  'AY593235',
  'AF192906',
  'AF547232',
  'DQ678928',
  'AY099337',
  'KF383015',
  'L11422',
  'FJ807886',
  'KX879603',
  'AY770511',
  'AY702030',
  'KX827268',
  'KM851039',
  'LN999960',
  'AY099340',
  'KY435454',
  'KY435455',
  'KU752544',
  'HM067744'
]

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')

class SymptomsList(Resource):
    def get(self):
        return SYMPTOMS

class FileNames(Resource):
    def get(self):
        # file_names = []
        # for root, dirs, files in os.walk("./articles"):
        #   for filename in files:
        #     file_names.append(filename)
        
        return FILE_NAMES



api.add_resource(SymptomsList, '/symptoms')
api.add_resource(FileNames, '/file-names')

if __name__ == '__main__':
    app.run(debug=True)
