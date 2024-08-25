import pandas as pd
import streamlit as st
from google.oauth2 import service_account
import gspread

# Permitir o upload manual do arquivo Excel
uploaded_file = st.file_uploader("Escolha o arquivo de status dos associados", type=["xlsx"])

if uploaded_file is not None:
    # Carregar o Excel em um DataFrame do pandas
    df_associados = pd.read_excel(uploaded_file)

    # Exibir as colunas do DataFrame para garantir que a leitura foi correta
    st.write("Colunas do arquivo:", df_associados.columns)

    # Função para consultar o status do associado na planilha Excel
    def consultar_status_associado(nome_completo):
        # Verificar se a coluna "Nome Completo" existe
        if 'Nome Completo' in df_associados.columns:
            associado = df_associados[df_associados['Nome Completo'] == nome_completo]
            
            if not associado.empty:
                return associado['Status'].values[0]  # Substitua 'Status' pelo nome correto da coluna do status
            else:
                return None
        else:
            st.error("A coluna 'Nome Completo' não foi encontrada no arquivo.")
            return None

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

# Exibe o formulário se o arquivo Excel foi carregado
if uploaded_file is not None:
    nome_completo = st.text_input("Nome Completo")
    email = st.text_input("Email")
    telefone = st.text_input("Telefone")

    if st.button("ENVIAR"):
        # Certifique-se de que as variáveis estejam preenchidas
        if nome_completo and email and telefone:
            status_associado = consultar_status_associado(nome_completo)
            
            if status_associado:
                salvar_inscricao_google_sheets(nome_completo, email, telefone, status_associado)
                st.success(f"Inscrição realizada com sucesso! Status: {status_associado}")
            else:
                st.error("Não encontramos seu nome na lista de associados.")
        else:
            st.error("Por favor, preencha todos os campos.")

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
col1, col2 = st.columns([1, 1])  # Dois botões centralizados e com espaço entre eles

# Botões centralizados
with col1:
    if st.button("ASSOCIADO"):
        st.session_state["opcao_escolhida"] = "associado"
        st.session_state["botao_clicado"] = None
        st.session_state["formulario_preenchido"] = False

with col2:
    if st.button("NÃO ASSOCIADO"):
        st.session_state["opcao_escolhida"] = "nao_associado"
        st.session_state["botao_clicado"] = None
        st.session_state["formulario_preenchido_nao_associado"] = False

st.markdown("</div>", unsafe_allow_html=True)

# Exibe o formulário se ASSOCIADO foi clicado
if st.session_state["opcao_escolhida"] == "associado":
    st.subheader("Selecione a Situação - Associado")

    col1, col2, col3 = st.columns(3)

    if col1.button("ADIMPLENTE"):
        st.session_state["botao_clicado"] = "adimplente"
    if col2.button("EM NEGOCIAÇÃO"):
        st.session_state["botao_clicado"] = "em_negociacao"
    if col3.button("MENSALIDADE ATRASADA"):
        st.session_state["botao_clicado"] = "mensalidade_atrasada"

    col1.caption("Gratos pela sua colaboração, perito papiloscopista. Nesse evento, você será VIP, sem nenhum custo: palestra e churrasco de confraternização.")
    col2.caption("Gratos pela negociação dos pagamentos, perito papiloscopista. Nesse evento, você terá 50% de desconto no valor da palestra e do churrasco.")
    col3.caption("Ficaremos gratos caso queira negociar as parcelas atrasadas e aí receberá 50% de desconto no valor do evento (entre em contato via contato@asiip.com.br), caso ainda não esteja pronto para a negociação clique no botão MENSALIDADE ATRASADA.")

# Exibe o formulário de inscrição para ASSOCIADO
if st.session_state["botao_clicado"] and uploaded_file is not None:
    st.subheader("Preencha o Formulário de Inscrição")
    
    # Defina as variáveis a partir dos campos do formulário
    nome_completo = st.text_input("Nome Completo")
    email = st.text_input("Email")
    telefone = st.text_input("Telefone")

    if st.button("ENVIAR"):
        # Certifique-se de que as variáveis estejam preenchidas
        if nome_completo and email and telefone:
            status_associado = consultar_status_associado(nome_completo)
            if status_associado:
                salvar_inscricao_google_sheets(nome_completo, email, telefone, status_associado)
                st.success(f"Inscrição realizada com sucesso! Status: {status_associado}")
            else:
                st.error("Não encontramos seu nome na lista de associados.")
        else:
            st.error("Por favor, preencha todos os campos.")

# Exibe o formulário de inscrição para NÃO ASSOCIADO
if st.session_state["opcao_escolhida"] == "nao_associado":
    st.subheader("Preencha o Formulário de Inscrição - NÃO Associado")
    
    nome_completo_na = st.text_input("Nome Completo (NÃO Associado)")
    email_na = st.text_input("Email (NÃO Associado)")
    telefone_na = st.text_input("Telefone (NÃO Associado)")

    if st.button("ENVIAR (NÃO ASSOCIADO)"):
        if nome_completo_na and email_na and telefone_na:
            # Salvar a inscrição no Google Sheets
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
                    <p>Rua Barão do Rio Branco, 370 - Centro, Curitiba/PR
                    <p>Churrasco de Confraternização</p>
                    <p>30 DE NOVEMBRO 13:30</p>
                    <p>Local do churrasco a definir, Curitiba/PR</p>
                    <p><strong>PIX CNPJ: 39.486.619/0001-93</strong></p>
                    <p><strong>VALOR: R$ 00,00</strong></p>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Botão para limpar sessão (centralizado)
if st.session_state["opcao_escolhida"] or st.session_state["botao_clicado"]:
    st.markdown("<div class='clear-session-container'>", unsafe_allow_html=True)
    if st.button("Limpar Sessão"):
        st.session_state.clear()
        st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)

