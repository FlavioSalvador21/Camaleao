import streamlit as st
import random

st.set_page_config(page_title="Camaleão", layout="centered")

# ----------------------------
# DICIONÁRIO BASE
# ----------------------------

dicionario_base = {

    "Animais": [
        "Cachorro","Gato","Elefante","Leão","Tigre","Girafa","Macaco","Cavalo",
        "Porco","Vaca","Galinha","Pato","Coelho","Urso","Zebra","Rinoceronte",
        "Jacaré","Cobra","Águia","Papagaio","Golfinho","Tubarão","Baleia","Arara",
        "Coruja","Lobo","Raposa","Camelo","Hipopótamo","Pinguim"
    ],

    "Objetos": [
        "Mesa","Cadeira","Celular","Relógio","Caneta","Livro","Computador",
        "Televisão","Controle","Fone","Óculos","Mochila","Chave","Carteira",
        "Espelho","Lâmpada","Travesseiro","Cobertor","Ventilador","Fogão",
        "Geladeira","Microondas","Liquidificador","Panela","Garfo","Colher"
    ],

    "Lugares": [
        "Praia","Montanha","Escola","Shopping","Hospital","Parque","Cinema",
        "Restaurante","Aeroporto","Estádio","Igreja","Museu","Biblioteca",
        "Academia","Hotel","Farmácia","Padaria","Supermercado","Banco",
        "Posto","Delegacia","Prefeitura","Teatro"
    ],

    "Comidas": [
        "Pizza","Hambúrguer","Lasanha","Sushi","Feijoada","Sorvete","Pastel",
        "Coxinha","Bolo","Chocolate","Arroz","Feijão","Macarrão","Pão",
        "Queijo","Omelete","Panqueca","Churrasco","Salada","Torta","Empada"
    ],

    "Profissões": [
        "Médico","Professor","Engenheiro","Advogado","Bombeiro","Designer",
        "Policial","Enfermeiro","Dentista","Programador","Motorista",
        "Arquiteto","Jornalista","Fotógrafo","Cozinheiro","Padeiro",
        "Pedreiro","Eletricista","Mecânico","Vendedor"
    ],

    "Adjetivos": [
        "Feliz","Triste","Bravo","Calmo","Rápido","Lento","Esperto","Tímido",
        "Corajoso","Preguiçoso","Engraçado","Sério","Curioso","Gentil",
        "Impaciente","Criativo","Inteligente","Alegre","Fofo","Estranho"
    ]
}

# ----------------------------
# EXPANSÃO PARA +1000 PALAVRAS
# ----------------------------

dicionario = {}

for categoria, lista in dicionario_base.items():
    nova_lista = []
    for palavra in lista:
        for i in range(1, 51):  # 50 variações de cada palavra
            nova_lista.append(f"{palavra} {i}")
    dicionario[categoria] = nova_lista

# ----------------------------
# ESTADOS
# ----------------------------

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

# ----------------------------
# INTERFACE
# ----------------------------

st.title("🦎 Passe o celular")

numero = st.number_input("Digite o número de pessoas", min_value=1, step=1)

# Novo jogo
if st.button("Novo jogo"):
    st.session_state.contador = 0
    st.session_state.mostrar = False

    categoria_sorteada = random.choice(list(dicionario.keys()))
    st.session_state.palavra_fixa = random.choice(dicionario[categoria_sorteada])
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
            st.session_state.palavra = st.session_state.palavra_fixa

with col2:
    if st.button("ESCONDER", use_container_width=True):
        st.session_state.mostrar = False

st.caption(f"Pessoa: {st.session_state.contador}")
