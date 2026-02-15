import streamlit as st
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Impostor Streamlit", page_icon="🦎")

# Inicialização das variáveis de estado (se não existirem)
if 'jogo_iniciado' not in st.session_state:
    st.session_state.jogo_iniciado = False
    st.session_state.jogadores_info = {} # Dicionário: {Nome: Papel}
    st.session_state.palavra_rodada = ""

# --- MENU DE CONFIGURAÇÕES (SIDEBAR) ---
with st.sidebar:
    st.header("⚙️ Configurações do Jogo")
    
    # 1. Quantidade de pessoas
    num_jogadores = st.number_input("Total de Jogadores", min_value=3, max_value=20, value=4)
    
    # 2. Quantidade de impostores
    max_impostores = num_jogadores - 2  # Pelo menos 2 inocentes
    num_impostores = st.number_input("Quantidade de Impostores", min_value=1, max_value=max_impostores, value=1)
    
    # Entrada de nomes dinâmica
    st.subheader("Nomes dos Participantes")
    nomes_input = []
    for i in range(num_jogadores):
        nome = st.text_input(f"Jogador {i+1}", f"Jogador {i+1}", key=f"input_{i}")
        nomes_input.append(nome)

    # Botão para Gerar o Jogo
    if st.button("Gerar Nova Rodada"):
        # Temas simples para teste (podes expandir)
        temas = {"Objetos": ["Cadeira", "Relógio", "Televisão"], "Lugar": ["Paris", "Cozinha", "Marte"]}
        tema = random.choice(list(temas.keys()))
        palavra = random.choice(temas[tema])
        
        # Sorteio dos Impostores
        impostores_escolhidos = random.sample(nomes_input, num_impostores)
        
        # Criar dicionário de papéis
        progresso_jogo = {}
        for nome in nomes_input:
            progresso_jogo[nome] = "CAMALEÃO" if nome in impostores_escolhidos else palavra
            
        # Salvar no estado
        st.session_state.jogadores_info = progresso_jogo
        st.session_state.palavra_rodada = palavra
        st.session_state.tema_rodada = tema
        st.session_state.jogo_iniciado = True
        st.success("Jogo configurado! Fecha o menu e joga.")

# --- PÁGINA PRINCIPAL ---
st.title("🦎 Jogo do Camaleão")

if not st.session_state.jogo_iniciado:
    st.info("Configura o jogo no menu lateral e clica em 'Gerar Nova Rodada' para começar!")
else:
    st.subheader(f"Tema: {st.session_state.tema_rodada}")
    
    # Seleção de quem vai ver a palavra agora
    jogador_vez = st.selectbox("Quem vai ver a palavra?", list(st.session_state.jogadores_info.keys()))
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"Revelar para {jogador_vez}"):
            resultado = st.session_state.jogadores_info[jogador_vez]
            if resultado == "CAMALEÃO":
                st.error(f"Tu és o **{resultado}**!")
            else:
                st.success(f"A palavra é: **{resultado}**")
    
    with col2:
        if st.button("Esconder Palavra"):
            st.rerun()

    st.divider()
    if st.checkbox("Revelar todos os papéis (Fim do Jogo)"):
        st.write(st.session_state.jogadores_info)
