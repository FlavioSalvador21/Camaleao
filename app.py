import streamlit as st
import random
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Jogo do Camaleão", page_icon="🦎", layout="centered")

# --- FUNÇÃO PARA CARREGAR PALAVRAS ---
def carregar_palavras():
    caminho = "palavras.txt"
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return [linha.strip() for linha in f.readlines() if linha.strip()]
    # Caso o arquivo não exista, retorna uma lista padrão para não quebrar o app
    return ["Avião", "Bicicleta", "Cachorro", "Dente", "Elefante", "Futebol", "Guitarra"]

# --- INICIALIZAÇÃO DO ESTADO ---
if 'jogo_ativo' not in st.session_state:
    st.session_state.jogo_ativo = False
    st.session_state.dados_jogadores = {}
    st.session_state.seletor_jogador = "Jogador 1"

# --- FUNÇÃO CALLBACK: PRÓXIMO JOGADOR ---
def proximo_jogador_callback():
    lista_nomes = list(st.session_state.dados_jogadores.keys())
    nome_atual = st.session_state.seletor_jogador
    
    try:
        indice_atual = lista_nomes.index(nome_atual)
        proximo_indice = (indice_atual + 1) % len(lista_nomes)
        st.session_state.seletor_jogador = lista_nomes[proximo_indice]
    except ValueError:
        st.session_state.seletor_jogador = lista_nomes[0]

# --- MENU LATERAL (CONFIGURAÇÕES) ---
with st.sidebar:
    st.header("⚙️ Configurações")
    total_jogadores = st.number_input("Qtd de Jogadores", min_value=3, max_value=30, value=5)
    total_impostores = st.number_input("Qtd de Impostores", min_value=1, max_value=total_jogadores-2, value=1)
    
    if st.button("🚀 Iniciar/Resetar Jogo"):
        pool_palavras = carregar_palavras()
        palavra_secreta = random.choice(pool_palavras)
        
        # Gerar identificação automática dos jogadores
        ids_jogadores = [f"Jogador {i+1}" for i in range(total_jogadores)]
        
        # Sortear camaleões
        lista_camaleoes = random.sample(ids_jogadores, total_impostores)
        
        # Atribuir palavras ou "CAMALEÃO"
        st.session_state.dados_jogadores = {
            pj: ("CAMALEÃO" if pj in lista_camaleoes else palavra_secreta) 
            for pj in ids_jogadores
        }
        
        st.session_state.jogo_ativo = True
        st.session_state.seletor_jogador = ids_jogadores[0]
        st.success("Jogo Gerado! Recolha este menu.")
        st.rerun()

# --- TELA PRINCIPAL ---
st.title("🦎 Jogo do Camaleão")

if st.session_state.jogo_ativo:
    st.write("### 📢 A rodada começou!")
    st.caption("Selecione seu número, veja sua palavra e passe para o próximo.")
    
    lista_nomes = list(st.session_state.dados_jogadores.keys())
    
    # Selectbox controlado pelo session_state via chave 'seletor_jogador'
    escolha = st.selectbox(
        "Quem é você?", 
        options=lista_nomes, 
        key="seletor_jogador"
    )

    col1, col2 = st.columns(2)

    with col1:
        # Chave dinâmica para evitar que o botão fique "preso" no estado anterior
        if st.button(f"👁️ Revelar para {escolha}", key=f"btn_{escolha}"):
            resultado = st.session_state.dados_jogadores[escolha]
            if resultado == "CAMALEÃO":
                st.error(f"⚠️ VOCÊ É O **{resultado}**!")
            else:
                st.success(f"Sua palavra é: **{resultado}**")
    
    with col2:
        # O callback atualiza o seletor ANTES de recarregar a página
        st.button("Limpar e Próximo ➡️", on_click=proximo_jogador_callback)

    st.divider()
    st.info("Dica: Se você for o Camaleão, tente fingir que sabe a palavra!")

else:
    st.warning("Aguardando configuração... Use o menu lateral (seta no topo esquerdo) para começar!")
