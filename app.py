import streamlit as st
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Impostor/Camaleão", page_icon="🦎")

# Inicialização das variáveis de estado
if 'jogo_ativo' not in st.session_state:
    st.session_state.jogo_ativo = False
    st.session_state.dados_jogadores = {}
    st.session_state.tema = ""
    st.session_state.indice_jogador = 0  # Controla qual jogador está selecionado no selectbox

# --- MENU LATERAL (CONFIGURAÇÕES) ---
with st.sidebar:
    st.header("⚙️ Configurações")
    total_jogadores = st.number_input("Qtd de Jogadores", min_value=3, max_value=30, value=5)
    total_impostores = st.number_input("Qtd de Impostores", min_value=1, max_value=total_jogadores-2, value=1)
    
    biblioteca_temas = {
        "Profissões": ["Bombeiro", "Astronauta", "Médico", "Chef de Cozinha", "Pescador"],
        "Filmes": ["Star Wars", "Titanic", "Shrek", "Batman", "Vingadores"],
        "Cidades": ["Rio de Janeiro", "Paris", "Tóquio", "Londres", "Nova York"]
    }
    
    tema_escolhido = st.selectbox("Escolha o Tema", list(biblioteca_temas.keys()))

    if st.button("🚀 Iniciar/Resetar Jogo"):
        palavra_secreta = random.choice(biblioteca_temas[tema_escolhido])
        ids_jogadores = [f"Jogador {i+1}" for i in range(total_jogadores)]
        lista_camaleoes = random.sample(ids_jogadores, total_impostores)
        
        st.session_state.dados_jogadores = {pj: ("CAMALEÃO" if pj in lista_camaleoes else palavra_secreta) for pj in ids_jogadores}
        st.session_state.tema = tema_escolhido
        st.session_state.jogo_ativo = True
        st.session_state.indice_jogador = 0 # Reseta para o primeiro jogador
        st.success("Jogo Gerado!")

# --- TELA PRINCIPAL ---
st.title("🦎 Jogo do Camaleão")

if st.session_state.jogo_ativo:
    st.info(f"**TEMA:** {st.session_state.tema}")
    
    lista_nomes = list(st.session_state.dados_jogadores.keys())
    
    # O segredo está aqui: o parâmetro 'index' é alimentado pelo session_state
    escolha = st.selectbox(
        "Quem é você?", 
        options=lista_nomes, 
        index=st.session_state.indice_jogador,
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
            # Lógica para incrementar o índice ou resetar se chegar ao fim
            proximo_indice = st.session_state.indice_jogador + 1
            if proximo_indice < len(lista_nomes):
                st.session_state.indice_jogador = proximo_indice
            else:
                st.session_state.indice_jogador = 0 # Volta para o início se quiserem conferir
            
            st.rerun()

    st.divider()
    if st.checkbox("Mostrar todos os papéis (Fim do Jogo)"):
        st.write(st.session_state.dados_jogadores)

else:
    st.warning("Abra o menu lateral para configurar a partida.")
