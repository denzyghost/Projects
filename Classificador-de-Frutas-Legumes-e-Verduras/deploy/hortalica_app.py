# streamlit run hortalica_app.py

import numpy as np
import re
import pickle
from scipy.sparse import csr_matrix
import streamlit as st
import os
import sklearn
from unidecode import unidecode


print(sklearn.__version__)

dir_path = os.path.dirname(os.path.realpath(__file__))


def processador_de_texto(data):
    data = unidecode(data)
    data = re.sub('[^\w\s]', '', str(data.lower()))
    data = data.replace("\r", " ")
    data = data.replace("\n", " ")
    data = data.replace("  ", " ")
    data = data.split(" ")
    return data


def classify_new(input_, myvectorizer):

    input_vect = myvectorizer.transform(input_)

    input_vect_array = np.array(input_vect)
    input_vect_array_csr_matrix = csr_matrix((input_vect_array).all())

    return input_vect_array_csr_matrix


with open(f"{dir_path}/hortalicia_vectorizer.pickle", "rb") as f:
    h_vectorizer = pickle.load(f)

with open(f"{dir_path}/hortalicia_model.pkl", "rb") as f:
    model = pickle.load(f)

h_classes = {0.0: "Fruta", 1.0: "Legume", 2.0: "Verdura", }

# Título da página
st.title("Bem-vindo ao meu Classificador de Frutas, Legumes e Verduras")

# Create a text element and let the reader know the data is loading.
data_load_state = st.text(
    'Este é um projeto de classificação de frutas, legumes e verduras usando machine learning.' +
    '\nO tipo de modelo que escolhi para essa tarefa é um modelo de Árvore de Decisão' +
    ', especificamente o Random Forest Classifier.\n' +
    'Forneça o nome de uma fruta, legume ou verdura e veja o resultado da classificação em tempo real!')

data_load_state = st.text('Aviso: Embora eu tenha criado com muito cuidado este projeto, e o modelo\n' +
                          'por tás dele esteja performando muito bem, algums das classificações sugeridas\n' +
                          'pelo modelo podem estar incorretas, portanto, atente-se a isso!')

# Input do usuário
input_value = st.text_input("Digite o nome de uma fruta, legume ou verdura:")

# Mostra o resultado para o usuário
if input_value:
    st.write("Você digitou:", input_value)

# Adicionando um botão para o usuário clicar
if st.button("Executar modelo"):
    # Aqui você pode colocar o código para fazer a classificação usando o input do usuário

    classify_vector = classify_new(
        processador_de_texto(input_value), h_vectorizer)

    proba = model.predict_proba(classify_vector)
    classification = model.predict(classify_vector)

    result = f"'{input_value}' é classificado como '{h_classes[classification[0]]}'!!!"
    st.success(result)

data_load_state = st.text(
    'Projeto de machine learning criado por Alisson Silva\n' +
    'Meu GitHub: https://github.com/Dhytm\n' +
    'Código Fonte deste projeto: https://github.com/Dhytm/Projects/tree/main/Classificador-de-Frutas-Legumes-e-Verduras\n' +
    'Licença: https://github.com/Dhytm/Projects/blob/main/LICENSE\n')

data_load_state = st.text(
    'Gostou do projeto e quer me comprar um café?!\n' +
    'Pix: alissondin.developer@gmail.com'
)
