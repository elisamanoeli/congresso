import os
import pandas as pd
import streamlit as st
import requests
from io import BytesIO
from google.oauth2 import service_account
import gspread
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

# Função para enviar e-mail de confirmação
def enviar_email_confirmacao(nome, email):
    # Configurações do servidor SMTP
    smtp_server = "mail.asiip.com.br"
    smtp_port = 465
    smtp_user = "contato@asiip.com.br"
    smtp_password = "Co2326@Asi"  # Substitua pela sua senha

    # Configurando a mensagem
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = email
    msg['Subject'] = "Confirmação de Inscrição - I Congresso de Papiloscopia da ASIIP"

    body = f"""
    Olá {nome},

    Sua inscrição no I Congresso de Papiloscopia da ASIIP - Comparação Facial Humana foi efetuada com sucesso!

    Detalhes do evento:
    Data: 30 de Novembro
    Horário: 7:30
    Local: Rua Barão do Rio Branco, 370 - Centro, Curitiba/PR

    Churrasco de Confraternização:
    Data: 30 de Novembro
    Horário: 13:30
    Local: A definir, Curitiba/PR

    Aguardamos sua presença!

    Atenciosamente,
    ASIIP
    """

    msg.attach(MIMEText(body, 'plain'))

    # Enviando o e-mail
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, email, msg.as_string())
        server.quit()
        st.success("E-mail de confirmação enviado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao enviar o e-mail: {e}")

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

# Definir a página principal
pagina = st.session_state.get("pagina", "inicio")

# Página inicial com as opções de botão
if pagina == "inicio":
    st.image("logo.png", use_column_width=False, width=200)
    st.markdown("<h1 style='text-align: center;'>I Congresso de Papiloscopia da ASIIP - Comparação Facial Humana</h1>", unsafe_allow_html=True)
    st.write("Escolha uma opção para prosseguir com a inscrição:")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("ADIMPLENTE"):
            st.session_state["pagina"] = "form_adimplente"
            st.experimental_rerun()
    with col2:
        if st.button("EM NEGOCIAÇÃO"):
            st.session_state["pagina"] = "form_negociacao"
            st.experimental_rerun()
    with col3:
        if st.button("MENSALIDADE ATRASADA"):
            st.session_state["pagina"] = "form_atrasada"
            st.experimental_rerun()

# Página de formulário para ADIMPLENTE
if pagina == "form_adimplente":
    st.subheader("Formulário de Inscrição - ADIMPLENTE")
    nome_completo = st.text_input("Nome Completo", key="input_nome_completo_adimplente")
    email = st.text_input("Email", key="input_email_adimplente")
    telefone = st.text_input("Telefone", key="input_telefone_adimplente")

    if st.button("ENVIAR", key="btn_enviar_adimplente"):
        if nome_completo and email and telefone:
            status_selecionado = "adimplente"
            if not consultar_status_associado(nome_completo, status_selecionado):
                st.error(f"O nome {nome_completo} não corresponde a um associado com status {status_selecionado}.")
            elif not email_valido(email):
                st.error("Por favor, insira um email válido.")
            elif not telefone_valido(telefone):
                st.error("Por favor, insira um telefone válido (11 dígitos, apenas números, com DDD).")
            else:
                salvar_inscricao_google_sheets(nome_completo, email, telefone, status_selecionado, "ASSOCIADO")
                enviar_email_confirmacao(nome_completo, email)
                st.success("Inscrição realizada com sucesso!")
                st.balloons()

    if st.button("VOLTAR"):
        st.session_state["pagina"] = "inicio"
        st.experimental_rerun()

# Página de formulário para EM NEGOCIAÇÃO
if pagina == "form_negociacao":
    st.subheader("Formulário de Inscrição - EM NEGOCIAÇÃO")
    nome_completo = st.text_input("Nome Completo", key="input_nome_completo_negociacao")
    email = st.text_input("Email", key="input_email_negociacao")
    telefone = st.text_input("Telefone", key="input_telefone_negociacao")

    if st.button("ENVIAR", key="btn_enviar_negociacao"):
        if nome_completo and email and telefone:
            status_selecionado = "em negociação"
            if not consultar_status_associado(nome_completo, status_selecionado):
                st.error(f"O nome {nome_completo} não corresponde a um associado com status {status_selecionado}.")
            elif not email_valido(email):
                st.error("Por favor, insira um email válido.")
            elif not telefone_valido(telefone):
                st.error("Por favor, insira um telefone válido (11 dígitos, apenas números, com DDD).")
            else:
                salvar_inscricao_google_sheets(nome_completo, email, telefone, status_selecionado, "ASSOCIADO")
                enviar_email_confirmacao(nome_completo, email)
                st.success("Inscrição realizada com sucesso!")
                st.balloons()

    if st.button("VOLTAR"):
        st.session_state["pagina"] = "inicio"
        st.experimental_rerun()

# Página de formulário para MENSALIDADE ATRASADA
if pagina == "form_atrasada":
    st.subheader("Formulário de Inscrição - MENSALIDADE ATRASADA")
    nome_completo = st.text_input("Nome Completo", key="input_nome_completo_atrasada")
    email = st.text_input("Email", key="input_email_atrasada")
    telefone = st.text_input("Telefone", key="input_telefone_atrasada")

    if st.button("ENVIAR", key="btn_enviar_atrasada"):
        if nome_completo and email and telefone:
            status_selecionado = "mensalidade atrasada"
            if not consultar_status_associado(nome_completo, status_selecionado):
                st.error(f"O nome {nome_completo} não corresponde a um associado com status {status_selecionado}.")
            elif not email_valido(email):
                st.error("Por favor, insira um email válido.")
            elif not telefone_valido(telefone):
                st.error("Por favor, insira um telefone válido (11 dígitos, apenas números, com DDD).")
            else:
                salvar_inscricao_google_sheets(nome_completo, email, telefone, status_selecionado, "ASSOCIADO")
                enviar_email_confirmacao(nome_completo, email)
                st.success("Inscrição realizada com sucesso!")
                st.balloons()

    if st.button("VOLTAR"):
        st.session_state["pagina"] = "inicio"
        st.experimental_rerun()
