import streamlit as st
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Impostor/Camaleão", page_icon="🦎", layout="centered")

# Inicialização do estado do jogo
if 'jogo_ativo' not in st.session_state:
    st.session_state.jogo_ativo = False
    st.session_state.dados_jogadores = {}
    st.session_state.tema = ""

# --- MENU LATERAL (CONFIGURAÇÕES) ---
with st.sidebar:
    st.header("⚙️ Configurações")
    
    # Define quantidade de pessoas e impostores
    total_jogadores = st.number_input("Qtd de Jogadores", min_value=3, max_value=30, value=5)
    total_impostores = st.number_input("Qtd de Impostores", min_value=1, max_value=total_jogadores-2, value=1)
    
    # Lista de Temas (Podes expandir aqui)
    biblioteca_temas = {
        "Profissões": ["Bombeiro", "Astronauta", "Médico", "Chef de Cozinha", "Pescador"],
        "Filmes": ["Star Wars", "Titanic", "Shrek", "Batman", "Vingadores"],
        "Cidades": ["Rio de Janeiro", "Paris", "Tóquio", "Londres", "Nova York"]
    }
    
    tema_escolhido = st.selectbox("Escolha o Tema", list(biblioteca_temas.keys()))

    if st.button("🚀 Iniciar/Resetar Jogo"):
        # Lógica de sorteio
        palavra_secreta = random.choice(biblioteca_temas[tema_escolhido])
        
        # Criar lista de "IDs" de jogadores (Ex: Jogador 1, Jogador 2...)
        ids_jogadores = [f"Jogador {i+1}" for i in range(total_jogadores)]
        
        # Sortear quem serão os camaleões
        lista_camaleoes = random.sample(ids_jogadores, total_impostores)
        
        # Atribuir palavras
        dict_jogo = {}
        for pj in ids_jogadores:
            dict_jogo[pj] = "CAMALEÃO" if pj in lista_camaleoes else palavra_secreta
            
        st.session_state.dados_jogadores = dict_jogo
        st.session_state.tema = tema_escolhido
        st.session_state.jogo_ativo = True
        st.success("Jogo Gerado! Recolha o menu lateral.")

# --- TELA PRINCIPAL ---
st.title("🦎 Jogo do Camaleão")

if st.session_state.jogo_ativo:
    st.info(f"**TEMA:** {st.session_state.tema}")
    st.write("Passe o dispositivo para cada jogador selecionar o seu número.")

    # Seletor para o jogador atual
    opcoes = ["-- Selecione seu Número --"] + list(st.session_state.dados_jogadores.keys())
    escolha = st.selectbox("Quem é você?", options=opcoes)

    if escolha != "-- Selecione seu Número --":
        # Botão para revelar a palavra (usa o estado para não sumir no clique)
        if st.button(f"Revelar palavra para {escolha}"):
            resultado = st.session_state.dados_jogadores[escolha]
            
            if resultado == "CAMALEÃO":
                st.error(f"⚠️ VOCÊ É O **{resultado}**!")
                st.caption("Tente descobrir a palavra secreta ouvindo as dicas dos outros.")
            else:
                st.success(f"Sua palavra é: **{resultado}**")
                st.caption("Dê uma dica sutil para provar que você sabe a palavra.")
        
        if st.button("Limpar Tela (Próximo Jogador)"):
            st.rerun()

    st.divider()
    # Opção para o fim da rodada
    if st.checkbox("Mostrar todos os papéis"):
        st.write(st.session_state.dados_jogadores)
else:
    st.warning("Aguardando configuração... Use o menu lateral (setinha no topo esquerdo) para começar!")
