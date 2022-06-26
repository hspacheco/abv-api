import sklearn
# Import all of the scikit learn stuff
# from _future_ import print_function
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import Normalizer
from sklearn import metrics
from sklearn.cluster import KMeans, MiniBatchKMeans
import nltk
from nltk.corpus import stopwords
import pandas as pd
import warnings
import numpy as np
import os
import re
import PyPDF2 as pdf
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import json

warnings.filterwarnings("ignore", category=DeprecationWarning,
module="pandas", lineno=570)
nltk.download('stopwords')
stopset = set(stopwords.words("english"))
stopset.update(["et", "al", "chikv", "virus"])
np.seterr(invalid='ignore')	

def no_number_preprocessor(tokens):
    r = re.sub('(\d)+', '', tokens.lower())
    return r

def clear_files():
  for root, dirs, files in os.walk('./artigos'):
      for filename in files:
        os.remove(f'./artigos/{filename}')

def get_file_sentences(file_name):
  file = open(f'./artigos/{file_name}', 'rb')
  pdf_reader = pdf.PdfFileReader(file, strict=False)
  page_count = pdf_reader.getNumPages()
  file_sentences = []

  for page_num in range(page_count):
    page_text = (pdf_reader
      .getPage(page_num)
      .extractText()
      .replace("\n", " ")
      # .replace("\\", " ")
      .split(". "))
    file_sentences = file_sentences + page_text
  
  return file_sentences

def get_LSA(file_names):
  document_sentences = []
  document_dict = {}

  print('lsa filenames')
  print(file_names)

  for filename_string in file_names:
    file_sentence = get_file_sentences(filename_string)
    document_sentences.append(file_sentence)
    document_dict[filename_string] = file_sentence

  symptoms_arr = [
      "anorexia",
      "abdominal pain",
      "arthalgiaasthenia",
      "backache",
      "bilateral conjunctivitis",
      "bleeding",
      "body ache",
      "cardiomegaly",
      "chills",
      "conjunctivitis",
      "cough",
      "dermal lesions",
      "diarrhea",
      "disabling pain",
      "epistaxis",
      "erythematous exanthema",
      "erythematous rashes",
      "eye pain",
      "facial swelling",
      "fatigue",
      "fever",
      "headache",
      "hepatitis",
      "high fever",
      "hyperaesthesia",
      "hyperpigmentation",
      "joint pain",
      "lack os appetite",
      "low trombocyte counts",
      "lumbar pain",
      "macopapular rash",
      "macular rash",
      "muscle pain",
      "muscle spasm",
      "myalgia",
      "myocarditis",
      "nausea",
      "pancytopenia",
      "pedal swelling",
      "prostation",
      "pulmonary congestion",
      "rash",
      "rheumatoid",
      "arthritis",
      "seizure",
      "severe arthalgia",
      "severe asthenia",
      "severe",
      "bilateral arthalgia",
      "shortness of breath",
      "tenosynovitis",
      "transient macular rash",
      "unwell",
      "wrist pain"
  ]

  vectorizer = TfidfVectorizer(
      stop_words = stopset,
      vocabulary=[
        "anorexia",
        "abdominal pain",
        "arthalgiaasthenia",
        "backache",
        "bilateral conjunctivitis",
        "bleeding",
        "body ache",
        "cardiomegaly",
        "chills",
        "conjunctivitis",
        "cough",
        "dermal lesions",
        "diarrehea",
        "disabling pain",
        "epistaxis",
        "erythematous exanthema",
        "erythematous rashes",
        "eye pain",
        "facial swelling",
        "fatigue",
        "fever",
        "headache",
        "hepatitis",
        "high fever",
        "hyperaesthesia",
        "hyperpigmentation",
        "joint pain",
        "lack os appetite",
        "low trombocyte counts",
        "lumbar pain",
        "macopapular rash",
        "macular rash",
        "muscle pain",
        "muscle spasm",
        "myalgia",
        "myocarditis",
        "nausea",
        "pancytopenia",
        "pedal swelling",
        "prostation",
        "pulmonary congestion",
        "rash",
        "rheumatoid",
        "arthritis",
        "seizure",
        "severe arthalgia",
        "severe asthenia",
        "severe",
        "bilateral arthalgia",
        "shortness of breath",
        "tenosynovitis",
        "transient macular rash",
        "unwell",
        "wrist pain"
    ],
      preprocessor = no_number_preprocessor, 
      ngram_range=(1,2))

  main_matrix = pd.DataFrame().T

  for key, value in document_dict.items():
    dtm = vectorizer.fit_transform(value)
    dtm.shape
    
    lsa = TruncatedSVD(
        algorithm = 'randomized', 
        n_components=1, 
        n_iter=100)
    lsa.fit(dtm)

    terms = vectorizer.get_feature_names()
    
    encodingMatrix = pd.DataFrame(
        lsa.components_,
        index = [f'abs_{key}'],
        columns = terms
    ).T
    
    main_matrix[f'{key}'] = np.abs(encodingMatrix[f'abs_{key}'])
  
  pd.DataFrame(main_matrix).to_csv("./main_matrix.csv")
  return process_main_matrix(main_matrix, symptoms_arr)

def get_highest_values_idx(arr, count):
    return np.argpartition(arr, -count)[-count:]

def process_main_matrix(main_matrix, symptoms_arr):
  article_name_as_column = main_matrix.columns.to_numpy()
  articles_matrix = []

  for article_name in article_name_as_column:
    articles_matrix.append(main_matrix[article_name].to_numpy())

  cs = cosine_similarity(articles_matrix)
  cosine_matrix = pd.DataFrame(cs, 
              index = article_name_as_column,
              columns = article_name_as_column
              )

  # pd.DataFrame(cosine_matrix).to_csv("./cosine_matrix.csv")

  similarity_articles = defaultdict(list)

  for article_name in article_name_as_column:
    five_highest_values_idx = get_highest_values_idx(cosine_matrix[article_name].to_numpy(), 2)
    five_highest_symptoms_values_idx = get_highest_values_idx(main_matrix[article_name].to_numpy(), 5)

    similarity_articles[article_name] = {}

    for highest_idx in five_highest_values_idx:
      # similarity_articles[article_name].append({cosine_matrix[article_name][highest_idx], cosine_matrix.columns[highest_idx]})

      if 'associatedGenome' not in similarity_articles[article_name]:
        similarity_articles[article_name]['associatedGenome'] = []

      similarity_articles[article_name]['associatedGenome'].append({ 
          'name': cosine_matrix.columns[highest_idx], 
          'score': cosine_matrix[article_name][highest_idx] 
      })

    for highest_idx in five_highest_symptoms_values_idx:

      if 'symptoms' not in similarity_articles[article_name]:
        similarity_articles[article_name]['symptoms'] = []

      if (main_matrix[article_name][highest_idx] > 0):
        similarity_articles[article_name]['symptoms'].append({ 
            'name': symptoms_arr[highest_idx],
            'score': main_matrix[article_name][highest_idx] 
        })

  # print(json.dumps(similarity_articles, indent=4, sort_keys=True))
  return similarity_articles

# get_LSA()

# blabla = cosine_matrix["abs_KF383015.pdf"].to_numpy()
# value = get_highest_values_idx(cosine_matrix["abs_KF383015.pdf"].to_numpy(), 5)

# print(value)
# print(cosine_matrix.columns[21])
# pd.DataFrame(cosine_matrix).to_csv("./cosine_matrix.csv")