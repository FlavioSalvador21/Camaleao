import streamlit as st
import random

st.set_page_config(page_title="Camaleão", layout="centered")

# Dicionário de categorias
dicionario = {
    "Animais": ["Cachorro", "Gato", "Elefante", "Leão", "Tigre", "Girafa"],
    "Objetos": ["Mesa", "Cadeira", "Celular", "Relógio", "Caneta", "Livro"],
    "Lugares": ["Praia", "Montanha", "Escola", "Shopping", "Hospital", "Parque"],
    "Comidas": ["Pizza", "Hambúrguer", "Lasanha", "Sushi", "Feijoada", "Sorvete"],
    "Profissões": ["Médico", "Professor", "Engenheiro", "Advogado", "Bombeiro", "Designer"]
}

# Estados
if "contador" not in st.session_state:
    st.session_state.contador = 0

if "camaleao_index" not in st.session_state:
    st.session_state.camaleao_index = None

if "mostrar" not in st.session_state:
    st.session_state.mostrar = False

if "palavra" not in st.session_state:
    st.session_state.palavra = ""

if "palavra_fixa" not in st.session_state:
    st.session_state.palavra_fixa = ""

st.title("Passe o celular")

categoria = st.selectbox("Escolha a categoria", list(dicionario.keys()))

numero = st.number_input("Digite o número de pessoas", min_value=1, step=1)

# Novo jogo
if st.button("Novo jogo"):
    st.session_state.contador = 0
    st.session_state.mostrar = False
    st.session_state.camaleao_index = random.randint(1, numero)
    st.session_state.palavra_fixa = random.choice(dicionario[categoria])
    st.session_state.palavra = ""

st.divider()

# Área da palavra
if st.session_state.mostrar:
    st.markdown(
        f"<h1 style='text-align:center'>{st.session_state.palavra}</h1>",
        unsafe_allow_html=True
    )
else:
    st.markdown("<h1 style='text-align:center'>&nbsp;</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if st.button("MOSTRAR", use_container_width=True):
        st.session_state.contador += 1
        st.session_state.mostrar = True

        if st.session_state.contador == st.session_state.camaleao_index:
            st.session_state.palavra = "CAMALEÃO"
        else:
            st.session_state.palavra = st.session_state.palavra_fixa

with col2:
    if st.button("ESCONDER", use_container_width=True):
        st.session_state.mostrar = False

st.caption(f"Pessoa: {st.session_state.contador}")
