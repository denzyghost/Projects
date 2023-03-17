# streamlit run hortalica_app.py

import streamlit as st
import numpy as np
import re
import pickle
from scipy.sparse import csr_matrix
import os
import sklearn
from unidecode import unidecode

st.set_page_config(page_title="Horticultural Classifier")

dir_path = os.path.dirname(os.path.realpath(__file__))


def processador_de_texto(data):
    data = unidecode(data)
    data = data.replace("-", " ")
    data = data.replace("  ", " ")
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
st.title("My Fruit and Vegetable Classifier")

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Este é um projeto de classificação de frutas, legumes e verduras que usa\n' +
                          'machine learning. Escolhi um modelo de Árvore de Decisão para essa tarefa,\n' +
                          'especificamente o Random Forest Classifier.\n' +
                          '\n'
                          'Forneça o nome de uma fruta, legume ou verdura e veja o resultado da\n' +
                          'classificação em tempo real!')
# Input do usuário
with st.form(key='my_form'):
    # st.text("Digite ou selecione algumas das opções")

    input_value = st.text_input("Digite o nome de uma fruta, legume ou verdura",
                                placeholder="Digite uma fruta, legume ou verdura e clique em Executar modelo")
    choice = st.selectbox("Ou experimente alguma das opções a seguir",
                          ["Selecionar [O campo acima precisa estar vazio]", "Lucuma", "Escorcioneira", "Caqui",
                           "Linhaça", "Cacau", "Cajá-manga", "Tarumã", "Sálvia",
                           "Rutabaga", "Wasabi (folha)", "Pinhão", "Bredo",
                           "Shissô", "Picão", "Gobô", "Kohlrabi", "Urtiga"],
                          help="Selecione uma opção e clique em Executar modelo")
    submit_button = st.form_submit_button(label='Executar modelo')


# Mostra o resultado para o usuário
if input_value or choice != "Selecionar [O campo acima precisa estar vazio]":

    if choice != "Selecionar" and input_value == "":
        input_value = choice

    # Adicionando um botão para o usuário clicar
    # if st.button("Executar modelo"):
    if submit_button:
        # Aqui você pode colocar o código para fazer a classificação usando o input do usuário

        classify_vector = classify_new(
            processador_de_texto(input_value), h_vectorizer)

        # !!!
        input_validation = True

        if not str(classify_vector):
            input_validation = False

        # !!!
        if input_validation:
            proba = model.predict_proba(classify_vector)
            classification = model.predict(classify_vector)

            result = f"'{input_value}' é classificado como '{h_classes[classification[0]]}'!!!"
            st.success(result)

        else:
            error_r = (
                f"""
            Desculpe-me, mas o pedido para '{input_value}' foi negado!\n
            Pode ser que tenha ocorrido alguma falha na digitação ou o termo pode não se enquadrar nas categorias permitidas!
            """
            )

            st.error(error_r)
            result = (
                """
                Caso acredite que tenha ocorrido um erro durante sua experiência de uso,
                por favor, reporte imediatamente ao meu desenvolvedor.
                Para isso, clique no botão "Reportar um bug" que pode ser acessado
                nas opções do menu localizado na lateral superior direita da tela.\n
                Obrigado por sua colaboração!
                """
            )
            st.info(result)
elif submit_button:
    st.error("Digite alguma coisa ou selecione um item!")

data_load_state = st.text(
    'Projeto de machine learning criado por Alisson Silva\n' +
    'Licença: https://github.com/Dhytm/Projects/blob/main/LICENSE\n')

data_load_state = st.text(
    'Gostou do projeto e quer me comprar um café?!\n' +
    'Pix: alissondin.developer@gmail.com'
)
