import pandas as pd
import streamlit as st
from google.oauth2 import service_account
import gspread

# CSS personalizado para ocultar a barra superior do Streamlit e remover o padding superior
st.markdown(
    """
    <style>
    /* Remove the top header */
    header {visibility: hidden;}
    
    /* Remove the padding of the main block */
    .block-container {
        padding-top: 0rem;
    }

    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .block-container {
            background-color: #0e1117;
            color: white;
        }
        .stButton>button {
            background-color: #4b5563;
            color: white;
        }
        .stButton>button:hover {
            background-color: #6b7280;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Carregar o arquivo Excel do GitHub
url_excel = "https://github.com/elisamanoeli/congresso/raw/main/ASIIP%20PGTOS%202024%20-%20STATUS.xlsx"
df_associados = pd.read_excel(url_excel)

# Função para consultar o status do associado na planilha Excel
def consultar_status_associado(nome_completo, status_selecionado):
    nome_completo = nome_completo.strip().lower()
    df_associados['Nome Completo'] = df_associados['Nome Completo'].str.strip().str.lower()

    associado = df_associados[
        (df_associados['Nome Completo'] == nome_completo) & 
        (df_associados['status'].str.lower() == status_selecionado.lower())
    ]
    
    return not associado.empty

# Funções de validação
def email_valido(email):
    return "@" in email and "." in email

def telefone_valido(telefone):
    telefone = telefone.strip().replace(" ", "")  # Remover espaços em branco
    return telefone.isdigit() and len(telefone) == 11

# Carregar as credenciais do Streamlit Secrets
creds = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

# Acessar o Google Sheets pelo ID da planilha
client = gspread.authorize(creds)
sheet = client.open_by_key("1UauLe5ti6lQVaZED5bPatnXTYUx5PgwicdLO6fs1BzY")
worksheet = sheet.get_worksheet(0)

# Função para enviar dados para o Google Sheets
def salvar_inscricao_google_sheets(nome, email, telefone, categoria):
    worksheet.append_row([nome, email, telefone, categoria, pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')])

# CSS personalizado para layout
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    .block-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
    .button-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 20px;
    }
    .clear-session-container {
        display: flex;
        justify-content: center;
        margin-top: 30px;
        margin-bottom: 30px;
    }
    .stButton>button {
        background-color: #0B0C45;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: 2px solid #0B0C45;
    }
    .stButton>button:hover {
        background-color: #28a745;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Inicializar variáveis de estado
if "opcao_escolhida" not in st.session_state:
    st.session_state["opcao_escolhida"] = None
if "botao_clicado" not in st.session_state:
    st.session_state["botao_clicado"] = None
if "formulario_preenchido" not in st.session_state:
    st.session_state["formulario_preenchido"] = False
if "formulario_preenchido_nao_associado" not in st.session_state:
    st.session_state["formulario_preenchido_nao_associado"] = False

# Exibe o layout dos botões centrados
st.image("logo.png", width=200)
st.markdown("<h1 style='text-align: center;'>I Congresso de Papiloscopia da ASIIP - Comparação Facial Humana</h1>", unsafe_allow_html=True)

st.write("Escolha uma opção para prosseguir com a inscrição:")

# Criando um contêiner para centralizar os botões
st.markdown("<div class='button-container'>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])

# Botões centralizados
with col1:
    if st.button("ASSOCIADO", key="btn_associado"):
        st.session_state["opcao_escolhida"] = "associado"
        st.session_state["botao_clicado"] = None
        st.session_state["formulario_preenchido"] = False

with col2:
    if st.button("NÃO ASSOCIADO", key="btn_nao_associado"):
        st.session_state["opcao_escolhida"] = "nao_associado"
        st.session_state["botao_clicado"] = None
        st.session_state["formulario_preenchido_nao_associado"] = False

st.markdown("</div>", unsafe_allow_html=True)

# Exibe o formulário se ASSOCIADO foi clicado
if st.session_state["opcao_escolhida"] == "associado":
    st.subheader("Selecione a Situação - Associado")

    col1, col2, col3 = st.columns(3)

    if col1.button("ADIMPLENTE", key="btn_adimplente"):
        st.session_state["botao_clicado"] = "adimplente"
    if col2.button("EM NEGOCIAÇÃO", key="btn_em_negociacao"):
        st.session_state["botao_clicado"] = "em_negociacao"
    if col3.button("MENSALIDADE ATRASADA", key="btn_mensalidade_atrasada"):
        st.session_state["botao_clicado"] = "mensalidade_atrasada"

    col1.caption("Gratos pela sua colaboração, perito papiloscopista. Nesse evento, você será VIP, sem nenhum custo.")
    col2.caption("Gratos pela negociação. Você terá 50% de desconto no valor do evento.")
    col3.caption("Ficaremos gratos caso queira negociar as parcelas atrasadas e aí receberá 50% de desconto no valor do evento (entre em contato via contato@asiip.com.br), caso ainda não esteja pronto para a negociação clique nesse botão.")

# Exibe o formulário de inscrição para ASSOCIADO
if st.session_state["botao_clicado"]:
    st.subheader("Preencha o Formulário de Inscrição")
    
    nome_completo = st.text_input("Nome Completo", key="input_nome_completo")
    email = st.text_input("Email", key="input_email")
    telefone = st.text_input("Telefone", key="input_telefone")

    if st.button("ENVIAR", key="btn_enviar"):
        if nome_completo and email and telefone:
            status_selecionado = st.session_state["botao_clicado"].replace("_", " ")

            if not consultar_status_associado(nome_completo, status_selecionado):
                st.error(f"O nome {nome_completo} não corresponde a um associado com status {status_selecionado}.")
            elif not email_valido(email):
                st.error("Por favor, insira um email válido.")
            elif not telefone_valido(telefone):
                st.error("Por favor, insira um telefone válido (11 dígitos, apenas números, com DDD).")
            else:
                salvar_inscricao_google_sheets(nome_completo, email, telefone, status_selecionado)
                st.session_state["formulario_preenchido"] = True
        else:
            st.error("Por favor, preencha todos os campos.")

    if st.session_state["formulario_preenchido"]:
        if st.session_state["botao_clicado"] == "adimplente":
            st.markdown("""
                <div class="success-box" style="background-color:#FFFFFF; border:2px solid #0B0C45; border-radius:10px; padding:20px; margin-top:20px;">
                    <div style="text-align:center; color:#0B0C45;">
                        <p>INSCRIÇÃO EFETUADA COM SUCESSO</p>
                        <p>I Congresso de Papiloscopia da ASIIP - Comparação Facial Humana</p>
                        <p>30 DE NOVEMBRO 7:30</p>
                        <p>Rua Barão do Rio Branco, 370 - Centro, Curitiba/PR</p>
                        <p>Churrasco de Confraternização</p>
                        <p>30 DE NOVEMBRO 13:30</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        elif st.session_state["botao_clicado"] == "em_negociacao":
            st.markdown("""
                <div class="success-box" style="background-color:#FFFFFF; border:2px solid #0B0C45; border-radius:10px; padding:20px; margin-top:20px;">
                    <div style="text-align:center; color:#0B0C45;">
                        <p>SUA INSCRIÇÃO SERÁ EFETIVADA APÓS O PAGAMENTO DE 50%</p>
                        <p>I Congresso de Papiloscopia da ASIIP - Comparação Facial Humana</p>
                        <p>30 DE NOVEMBRO 7:30</p>
                        <p>Rua Barão do Rio Branco, 370 - Centro, Curitiba/PR</p>
                        <p>Churrasco de Confraternização</p>
                        <p>30 DE NOVEMBRO 13:30</p>
                        <p>Local do churrasco a definir, Curitiba/PR</p>
                        <p><strong>PIX CNPJ: 39.486.619/0001-93</strong></p>
                        <p><strong>VALOR: R$ 00,00</strong></p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        elif st.session_state["botao_clicado"] == "mensalidade_atrasada":
            st.markdown("""
                <div class="success-box" style="background-color:#FFFFFF; border:2px solid #0B0C45; border-radius:10px; padding:20px; margin-top:20px;">
                    <div style="text-align:center; color:#0B0C45;">
                        <p>SUA INSCRIÇÃO SERÁ EFETIVADA APÓS O PAGAMENTO DO VALOR TOTAL</p>
                        <p>I Congresso de Papiloscopia da ASIIP - Comparação Facial Humana</p>
                        <p>30 DE NOVEMBRO 7:30</p>
                        <p>Rua Barão do Rio Branco, 370 - Centro, Curitiba/PR</p>
                        <p>Churrasco de Confraternização</p>
                        <p>30 DE NOVEMBRO 13:30</p>
                        <p>Local do churrasco a definir, Curitiba/PR</p>
                        <p><strong>PIX CNPJ: 39.486.619/0001-93</strong></p>
                        <p><strong>VALOR: R$ 00,00</strong></p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# Exibe o formulário de inscrição para NÃO ASSOCIADO
if st.session_state["opcao_escolhida"] == "nao_associado":
    st.subheader("Preencha o Formulário de Inscrição - NÃO Associado")
    
    nome_completo_na = st.text_input("Nome Completo (NÃO Associado)", key="input_nome_completo_na")
    email_na = st.text_input("Email (NÃO Associado)", key="input_email_na")
    telefone_na = st.text_input("Telefone (NÃO Associado)", key="input_telefone_na")

    if st.button("ENVIAR (NÃO ASSOCIADO)", key="btn_enviar_nao_associado"):
        if nome_completo_na and email_na and telefone_na:
            if not email_valido(email_na):
                st.error("Por favor, insira um email válido.")
            elif not telefone_valido(telefone_na):
                st.error("Por favor, insira um telefone válido (11 dígitos, apenas números, com DDD).")
            else:
                salvar_inscricao_google_sheets(nome_completo_na, email_na, telefone_na, "NÃO ASSOCIADO")
                st.session_state["formulario_preenchido_nao_associado"] = True
        else:
            st.error("Por favor, preencha todos os campos.")

    if st.session_state["formulario_preenchido_nao_associado"]:
        st.markdown("""
            <div class="success-box" style="background-color:#FFFFFF; border:2px solid #0B0C45; border-radius:10px; padding:20px; margin-top:20px;">
                <div style="text-align:center; color:#0B0C45;">
                    <p>SUA INSCRIÇÃO SERÁ EFETIVADA APÓS O PAGAMENTO DO VALOR TOTAL</p>
                    <p>I Congresso de Papiloscopia da ASIIP - Comparação Facial Humana</p>
                    <p>30 DE NOVEMBRO 7:30</p>
                    <p>Rua Barão do Rio Branco, 370 - Centro, Curitiba/PR</p>
                    <p>Churrasco de Confraternização</p>
                    <p>30 DE NOVEMBRO 13:30</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Botão para limpar sessão (centralizado)
if st.session_state["opcao_escolhida"] or st.session_state["botao_clicado"]:
    st.markdown("<div class='clear-session-container'>", unsafe_allow_html=True)
    
    # Se o botão "Limpar Sessão" for clicado
    if st.button("Limpar Sessão", key="btn_limpar_sessao"):
        # Limpa os campos do formulário
        st.session_state["botao_clicado"] = None
                st.session_state["formulario_preenchido"] = False
        st.session_state["formulario_preenchido_nao_associado"] = False

    st.markdown("</div>", unsafe_allow_html=True)


