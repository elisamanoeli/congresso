import os
import pandas as pd
import streamlit as st
import requests
from io import BytesIO
from google.oauth2 import service_account
import gspread

# Verifica se as credenciais do GCP estão no st.secrets
if "gcp_service_account" in st.secrets:
    creds = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
else:
    st.error("Credenciais do GCP não encontradas. Verifique o arquivo secrets.toml.")

# Tentar carregar o arquivo Excel do GitHub com requests
url_excel = "https://github.com/elisamanoeli/congresso/raw/main/ASIIP_STATUS.xlsx"
try:
    response = requests.get(url_excel)
    response.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
    df_associados = pd.read_excel(BytesIO(response.content))
except requests.exceptions.RequestException as e:
    st.error(f"Não foi possível carregar o arquivo Excel: {e}")

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

# Verificação das credenciais e conexão com o Google Sheets
if "gcp_service_account" in st.secrets:
    # Acessar o Google Sheets pelo ID da planilha
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1UauLe5ti6lQVaZED5bPatnXTYUx5PgwicdLO6fs1BzY")
    worksheet = sheet.get_worksheet(0)

    # Função para enviar dados para o Google Sheets
    def salvar_inscricao_google_sheets(nome, email, telefone, categoria, instituicao):
        worksheet.append_row([nome, email, telefone, categoria, instituicao, pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')])
else:
    st.error("Não foi possível carregar as credenciais do GCP. A integração com o Google Sheets não está disponível.")

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

    /* Ensures compatibility with Edge */
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
        -ms-flex-direction: column; /* Edge support */
        -webkit-flex-direction: column; /* Safari support */
    }
    .button-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 20px;
        -ms-flex-wrap: wrap; /* Edge support */
    }
    .stButton>button {
        background-color: #0B0C45;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: 2px solid #0B0C45;
        -ms-touch-action: manipulation; /* Edge support */
    }
    .stButton>button:hover {
        background-color: #28a745;
        color: white;
    }

    /* Estilo para os campos de texto */
    input[type="text"], input[type="email"], input[type="tel"] {
        border: 2px solid #0B0C45;  /* mesma cor azul dos botões */
        border-radius: 10px;
        padding: 10px;
        width: 100%;
        box-sizing: border-box;
    }

    /* Foco nos campos de texto */
    input[type="text"]:focus, input[type="email"]:focus, input[type="tel"]:focus {
        border-color: #28a745;  /* cor verde ao focar */
        outline: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
        st.session_state["instituicao_selecionada"] = False

st.markdown("</div>", unsafe_allow_html=True)

# Exibe o formulário se ASSOCIADO foi clicado
if st.session_state.get("opcao_escolhida") == "associado":
    st.subheader("Selecione a Situação - Associado")

    col1, col2, col3 = st.columns(3)

    if col1.button("ADIMPLENTE", key="btn_adimplente"):
        st.session_state["botao_clicado"] = "adimplente"
    if col2.button("EM NEGOCIAÇÃO", key="btn_em_negociacao"):
        st.session_state["botao_clicado"] = "em_negociacao"
    if col3.button("MENSALIDADE ATRASADA", key="btn_mensalidade_atrasada"):
        st.session_state["botao_clicado"] = "mensalidade_atrasada"

    col1.caption("Gratos pela sua colaboração, perito papiloscopista. Nesse evento, você será VIP, sem nenhum custo.")
    col2.caption("Gratos pela negociação. Você terá 50% de desconto no valor do evento. Se ainda não negociou as mensalidades atrasadas, envie um email para contato@asiip.com.br")
    col3.caption("Ficaremos gratos caso queira negociar as parcelas atrasadas e aí receberá 50% de desconto no valor do evento (envie um email para contato@asiip.com.br), caso ainda não esteja pronto para a negociação clique no botão MENSALIDADE ATRASADA.")

# Exibe o formulário de inscrição para ASSOCIADO
if st.session_state.get("botao_clicado") and st.session_state.get("opcao_escolhida") == "associado":
    st.subheader("Preencha o Formulário de Inscrição")
    
    nome_completo = st.text_input("Nome Completo", key="input_nome_completo_associado")
    email = st.text_input("Email", key="input_email_associado")
    telefone = st.text_input("Telefone", key="input_telefone_associado")

    if st.button("ENVIAR", key="btn_enviar_associado"):
        if nome_completo and email and telefone:
            status_selecionado = st.session_state["botao_clicado"].replace("_", " ")

            if not consultar_status_associado(nome_completo, status_selecionado):
                if st.session_state["botao_clicado"] == "adimplente":
                    st.error(f"O nome {nome_completo} não corresponde a um associado com status {status_selecionado}. Caso tenha efetuado o pagamento da mensalidade neste mês, por favor, envie os comprovantes para o email contato@asiip.com.br. Entraremos em contato para confirmar e efetivar sua inscrição.")
                elif st.session_state["botao_clicado"] == "em_negociacao":
                    st.error(f"O nome {nome_completo} não corresponde a um associado com status {status_selecionado}. Caso tenha efetuado o pagamento das mensalidades no trâmite em negociação, por favor, envie os comprovantes para o email contato@asiip.com.br. Entraremos em contato para confirmar e efetivar sua inscrição, com 50% de desconto.")
                elif st.session_state["botao_clicado"] == "mensalidade_atrasada":
                    st.error(f"O nome {nome_completo} não corresponde a um associado com status {status_selecionado}.")
            elif not email_valido(email):
                st.error("Por favor, insira um email válido.")
            elif not telefone_valido(telefone):
                st.error("Por favor, insira um telefone válido (11 dígitos, apenas números, com DDD).")
            else:
                salvar_inscricao_google_sheets(nome_completo, email, telefone, status_selecionado, "ASSOCIADO")
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

            # Exibe o botão "ENVIAR COMPROVANTE" após a mensagem de sucesso
            if st.button("ENVIAR COMPROVANTE"):
                st.write("Aqui você pode adicionar a lógica para enviar o comprovante.")

# Exibe o formulário de inscrição para NÃO ASSOCIADO
if st.session_state.get("opcao_escolhida") == "nao_associado":
    st.subheader("Selecione sua instituição:")
    
    instituicao = st.radio(
        "Escolha uma opção:",
        ("Polícia Federal", "Polícia Civil", "Polícia Militar", "Guarda Municipal"),
        key="instituicao"
    )

    if instituicao:
        st.session_state["instituicao_selecionada"] = True

if st.session_state.get("instituicao_selecionada") and st.session_state.get("opcao_escolhida") == "nao_associado":
    st.subheader("Preencha o Formulário de Inscrição - NÃO Associado")
        
    nome_completo_na = st.text_input("Nome Completo (NÃO Associado)", key="input_nome_completo_na")
    email_na = st.text_input("Email (NÃO Associado)", key="input_email_na")
    telefone_na = st.text_input("Telefone", key="input_telefone_na")

    if st.button("ENVIAR (NÃO ASSOCIADO)", key="btn_enviar_nao_associado"):
        if nome_completo_na and email_na and telefone_na:
            if not email_valido(email_na):
                st.error("Por favor, insira um email válido.")
            elif not telefone_valido(telefone_na):
                st.error("Por favor, insira um telefone válido (11 dígitos, apenas números, com DDD).")
            else:
                salvar_inscricao_google_sheets(nome_completo_na, email_na, telefone_na, "NÃO ASSOCIADO", st.session_state.get("instituicao"))
                st.session_state["formulario_preenchido_nao_associado"] = True
        else:
            st.error("Por favor, preencha todos os campos.")

    if st.session_state.get("formulario_preenchido_nao_associado"):
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

        # Exibe o botão "ENVIAR COMPROVANTE" após a mensagem de sucesso
        if st.button("ENVIAR COMPROVANTE"):
            st.write("Aqui você pode adicionar a lógica para enviar o comprovante.")
