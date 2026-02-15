import streamlit as st
import random

st.set_page_config(page_title="Camaleão", layout="centered")

# Estados iniciais
if "contador" not in st.session_state:
    st.session_state.contador = 0

if "camaleao_index" not in st.session_state:
    st.session_state.camaleao_index = None

if "mostrar" not in st.session_state:
    st.session_state.mostrar = False

if "palavra" not in st.session_state:
    st.session_state.palavra = ""

st.title("Passe o celular")

numero = st.number_input("Digite o número de pessoas", min_value=1, step=1)

# Novo jogo quando muda o número
if st.button("Novo jogo"):
    st.session_state.contador = 0
    st.session_state.mostrar = False
    st.session_state.camaleao_index = random.randint(1, numero)
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
            st.session_state.palavra = "PALAVRA"

with col2:
    if st.button("ESCONDER", use_container_width=True):
        st.session_state.mostrar = False

st.caption(f"Pessoa: {st.session_state.contador}")
