import argparse
import gensim
import numpy as np
import pickle
from sklearn import preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from keras.models import model_from_json
from pyvi import ViTokenizer

MODEL_PATH = "model_new/"

DATA_PATH = "data_new/"

def process_text(lines, model_path=MODEL_PATH, data_path=DATA_PATH):
    # Process the input text
    lines = lines.splitlines()
    lines = ' '.join(lines)
    lines = gensim.utils.simple_preprocess(lines)
    lines = ' '.join(lines)
    lines = ViTokenizer.tokenize(lines)

    # Load stopwords
    with open(data_path + 'vietnamese-stopwords-dash.txt', 'r', encoding='utf-8') as f:
        stopwords = set([w.strip() for w in f.readlines()])

    try:
        split_words = [x.strip('0123456789%@$.,=+-!;/()*"&^:#|\n\t\'').lower() for x in lines.split()]
    except TypeError:
        split_words = []
    lines = ' '.join([word for word in split_words if word not in stopwords])
    x = [lines]

    # Load encoder classes
    encoder = preprocessing.LabelEncoder()
    encoder.classes_ = np.load(model_path + 'classes.npy')

    # Load vectorizer
    tfidf_vect = TfidfVectorizer(analyzer='word', max_features=30000)
    tfidf_vect = pickle.load(open(model_path + "vectorizer.pickle", "rb"))

    tfidf_x = tfidf_vect.transform(x)

    # Load SVD selector
    svd = TruncatedSVD(n_components=500, random_state=1998)
    svd = pickle.load(open(model_path + "selector.pickle", "rb"))
    tfidf_x_svd = svd.transform(tfidf_x)

    # Load and predict with model
    json_file = open(model_path + 'model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(model_path + "model.h5")

    # Predict and decode the output
    prediction = encoder.inverse_transform([np.argmax(loaded_model.predict(np.array(tfidf_x_svd))[0])])[0]
    
    return prediction

text= '''CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM Độc lập - Tự do - Hạnh phúc SOCIALISTREPUBLIC OFVIETNAM Identity Card Số định danh cá nhân/No: Họ, chữ đệm và tên khai sinh / Surname, given names:  Ngày, tháng, năm sinh / Date of bir Cổ giá trị 
đến / Date of expiry     Giới tính / Sex: Quốc tịch / Nationality: i cư trù/ Place of Residence: A (*) (*) (*) Noi đăng ký khai sinh / Place of birth registration:  Ngày, tháng, năm cấp / Date, month, year BỘ CÔNG AN  MINISTRY OF PUBLIC SECURITY'''

result = process_text(text)
print("Prediction:", result)

