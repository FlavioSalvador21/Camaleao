import streamlit as st
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Impostor/Camaleão", page_icon="🦎")

# --- BANCO DE PALAVRAS (Pool Geral) ---
# Adicione ou remova palavras à vontade nesta lista
PALAVRAS_GERAIS = [
    "Avião", "Bateria", "Cachorro-quente", "Dentista", "Elevador", 
    "Futebol", "Geladeira", "Hambúrguer", "Igreja", "Jardim", 
    "Ketchup", "Lâmpada", "Microfone", "Navio", "Óculos", 
    "Piscina", "Queijo", "Relógio", "Sapato", "Televisão", 
    "Urso", "Vassoura", "Xadrez", "Yoga", "Zebra",
    "Bicicleta", "Astronauta", "Pizza", "Montanha Russa", "Pirata",
    "Smartphone", "Notebook", "Café", "Sushi", "Praia",
    "Violão", "Baixo", "Bateria", "Piano", "Flauta",
    "Batman", "Harry Potter", "Coringa", "Sherlock Holmes",
    "Brasil", "Japão", "França", "Itália", "Canadá"
]

# Inicialização das variáveis de estado
if 'jogo_ativo' not in st.session_state:
    st.session_state.jogo_ativo = False
    st.session_state.dados_jogadores = {}
    st.session_state.palavra_atual = ""
    st.session_state.seletor_jogador = "Jogador 1"

# --- FUNÇÃO CALLBACK ---
def proximo_jogador():
    lista_nomes = list(st.session_state.dados_jogadores.keys())
    nome_atual = st.session_state.seletor_jogador
    
    try:
        indice_atual = lista_nomes.index(nome_atual)
        proximo_indice = (indice_atual + 1) % len(lista_nomes)
        st.session_state.seletor_jogador = lista_nomes[proximo_indice]
    except ValueError:
        st.session_state.seletor_jogador = lista_nomes[0]

# --- MENU LATERAL (Configurações Escondidas) ---
with st.sidebar:
    st.header("⚙️ Configurações")
    total_jogadores = st.number_input("Qtd de Jogadores", min_value=3, max_value=30, value=5)
    total_impostores = st.number_input("Qtd de Impostores", min_value=1, max_value=total_jogadores-2, value=1)
    
    if st.button("🚀 Iniciar/Resetar Jogo"):
        # Sorteio de uma palavra aleatória do pool geral
        palavra_secreta = random.choice(PALAVRAS_GERAIS)
        
        # Gerar IDs dos jogadores
        ids_jogadores = [f"Jogador {i+1}" for i in range(total_jogadores)]
        
        # Sortear camaleões
        lista_camaleoes = random.sample(ids_jogadores, total_impostores)
        
        # Atribuir papéis
        st.session_state.dados_jogadores = {
            pj: ("CAMALEÃO" if pj in lista_camaleoes else palavra_secreta) 
            for pj in ids_jogadores
        }
        
        st.session_state.palavra_atual = palavra_secreta
        st.session_state.jogo_ativo = True
        st.session_state.seletor_jogador = ids_jogadores[0]
        st.rerun()

# --- TELA PRINCIPAL ---
st.title("🦎 Jogo do Camaleão")

if st.session_state.jogo_ativo:
    st.write("### 📢 A rodada começou!")
    st.write("Passe o aparelho para cada jogador e clique no botão para ver sua identidade.")
    
    lista_nomes = list(st.session_state.dados_jogadores.keys())
    
    # Seletor de jogador (Atualizado via callback)
    escolha = st.selectbox(
        "Quem é você?", 
        options=lista_nomes, 
        key="seletor_jogador"
    )

    col1, col2 = st.columns(2)

    with col1:
        # Usamos uma chave dinâmica para o botão de revelar não "travar" entre jogadores
        if st.button(f"👁️ Revelar para {escolha}", key=f"btn_rev_{escolha}"):
            resultado = st.session_state.dados_jogadores[escolha]
            if resultado == "CAMALEÃO":
                st.error(f"⚠️ VOCÊ É O **{resultado}**!")
            else:
                st.success(f"Sua palavra é: **{resultado}**")
    
    with col2:
        st.button("Limpar e Próximo ➡️", on_click=proximo_jogador)

    st.divider()
    st.caption("Dica: O Camaleão deve tentar adivinhar a palavra secreta para vencer se for descoberto!")

else:
    st.info("👋 Bem-vindo! Abra o menu lateral para definir o número de jogadores e começar a partida.")
