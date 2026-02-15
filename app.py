import streamlit as st
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Impostor/Camaleão", page_icon="🦎")

# Inicialização das variáveis de estado
if 'jogo_ativo' not in st.session_state:
    st.session_state.jogo_ativo = False
    st.session_state.dados_jogadores = {}
    st.session_state.tema = ""
    st.session_state.indice_jogador = 0

# --- MENU LATERAL (CONFIGURAÇÕES) ---
with st.sidebar:
    st.header("⚙️ Configurações")
    total_jogadores = st.number_input("Qtd de Jogadores", min_value=3, max_value=30, value=5)
    total_impostores = st.number_input("Qtd de Impostores", min_value=1, max_value=total_jogadores-2, value=1)
    
    biblioteca_temas = {
        "Profissões": ["Bombeiro", "Astronauta", "Médico", "Chef de Cozinha", "Pescador"],
        "Filmes": ["Star Wars", "Titanic", "Shrek", "Batman", "Vingadores"],
        "Cidades": ["Rio de Janeiro", "Paris", "Tóquio", "Londres", "Nova York"],
        "Música": ["Baixista", "Guitarrista", "Baterista", "Vocalista", "Pianista"]
    }
    
    tema_escolhido = st.selectbox("Escolha o Tema", list(biblioteca_temas.keys()))

    if st.button("🚀 Iniciar/Resetar Jogo"):
        palavra_secreta = random.choice(biblioteca_temas[tema_escolhido])
        ids_jogadores = [f"Jogador {i+1}" for i in range(total_jogadores)]
        lista_camaleoes = random.sample(ids_jogadores, total_impostores)
        
        st.session_state.dados_jogadores = {pj: ("CAMALEÃO" if pj in lista_camaleoes else palavra_secreta) for pj in ids_jogadores}
        st.session_state.tema = tema_escolhido
        st.session_state.jogo_ativo = True
        st.session_state.indice_jogador = 0
        
        # Resetamos o valor do seletor manualmente para o Jogador 1
        if 'seletor_jogador' in st.session_state:
            st.session_state.seletor_jogador = ids_jogadores[0]
        st.rerun()

# --- TELA PRINCIPAL ---
st.title("🦎 Jogo do Camaleão")

if st.session_state.jogo_ativo:
    st.info(f"**TEMA:** {st.session_state.tema}")
    
    lista_nomes = list(st.session_state.dados_jogadores.keys())
    
    # O selectbox usa a chave 'seletor_jogador'
    escolha = st.selectbox(
        "Quem é você?", 
        options=lista_nomes, 
        key="seletor_jogador"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"Revelar para {escolha}"):
            resultado = st.session_state.dados_jogadores[escolha]
            if resultado == "CAMALEÃO":
                st.error(f"⚠️ VOCÊ É O **{resultado}**!")
            else:
                st.success(f"Sua palavra é: **{resultado}**")
    
    with col2:
        if st.button("Limpar e Próximo ➡️"):
            # 1. Encontrar o índice atual
            indice_atual = lista_nomes.index(escolha)
            # 2. Calcular o próximo (com loop para o início)
            proximo_indice = (indice_atual + 1) % len(lista_nomes)
            # 3. ATUALIZAR DIRETAMENTE A CHAVE DO WIDGET
            st.session_state.seletor_jogador = lista_nomes[proximo_indice]
            
            st.rerun()

    st.divider()
    if st.checkbox("Mostrar todos os papéis (Fim do Jogo)"):
        st.write(st.session_state.dados_jogadores)
else:
    st.warning("Abra o menu lateral para configurar a partida.")
