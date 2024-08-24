import streamlit as st
import pandas as pd
import os

# Funções para carregar e salvar dados no arquivo CSV
def carregar_dados():
    if os.path.exists("inscritos.csv"):
        return pd.read_csv("inscritos.csv")
    return pd.DataFrame(columns=["Nome Completo", "Email", "Telefone", "Categoria", "Data de Inscrição"])

def salvar_dados(df):
    df.to_csv("inscritos.csv", index=False)

# Carregar os dados do CSV
df_inscritos = carregar_dados()

# Aplicar CSS para estilizar os campos de entrada e os botões
st.markdown(
    """
    <style>
    /* Cor de fundo da página */
    .stApp {
        background-color: #f0f2f6;
    }

    /* Estilizar os campos de entrada */
    div[data-baseweb="input"] input {
        background-color: #FFFFFF;
        color: #000000;
        border: 2px solid #0B0C45;
        border-radius: 10px;
        padding: 8px;
    }

    /* Centralizar texto de sucesso */
    .centered-text {
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: #0B0C45;
    }

    /* Estilizar a mensagem de sucesso */
    .success-box {
        background-color: #FFFFFF;
        border: 2px solid #0B0C45;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
    }

    /* Linha azul de separação */
    .separator {
        border: 5px solid #0B0C45;
        margin-top: 30px;
        margin-bottom: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Inicializar variáveis de estado
if "mostrar_associado" not in st.session_state:
    st.session_state["mostrar_associado"] = False
if "mostrar_nao_associado" not in st.session_state:
    st.session_state["mostrar_nao_associado"] = False
if "pagina" not in st.session_state:
    st.session_state["pagina"] = ""
if "botao_ativo" not in st.session_state:
    st.session_state["botao_ativo"] = True
if "inscricao_enviada" not in st.session_state:
    st.session_state["inscricao_enviada"] = False

# Fluxo da primeira tela: escolha entre ASSOCIADO e NÃO ASSOCIADO
st.image("logo.png", width=200)
st.markdown("<h1 style='text-align: center;'>I Congresso de Papiloscopia da ASIIP Comparação Facial Humana</h1>", unsafe_allow_html=True)

st.write("Escolha uma opção para prosseguir com a inscrição:")
col1, col2 = st.columns(2)

if col1.button("ASSOCIADO"):
    st.session_state["mostrar_associado"] = True
    st.session_state["mostrar_nao_associado"] = False
    st.session_state["pagina"] = ""
    st.session_state["botao_ativo"] = True
    st.session_state["inscricao_enviada"] = False

if col2.button("NÃO ASSOCIADO"):
    st.session_state["mostrar_nao_associado"] = True
    st.session_state["mostrar_associado"] = False
    st.session_state["pagina"] = ""
    st.session_state["botao_ativo"] = True
    st.session_state["inscricao_enviada"] = False

# Exibe o formulário de associado se o botão foi clicado
if st.session_state["mostrar_associado"]:
    st.subheader("Formulário de Inscrição - Associado")
    
    # Exibir a mensagem de sucesso logo abaixo do título
    if st.session_state["inscricao_enviada"]:
        if st.session_state["pagina"] == "sucesso":
            st.markdown("""
                <div class="success-box">
                    <div class="centered-text">
                        <p>INSCRIÇÃO EFETUADA COM SUCESSO</p>
                        <p>I Congresso de Papiloscopia da ASIIP Comparação Facial Humana</p>
                        <p>30 DE NOVEMBRO 7:30</p>
                        <p>Rua Barão do Rio Branco, 370 - Centro, Curitiba/PR</p>
                        <p>Churrasco de Confraternização</p>
                        <p>30 DE NOVEMBRO 13:30</p>
                        <p>Local do churras a definir, Curitiba/PR</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        elif st.session_state["pagina"] == "negociacao":
            st.markdown("""
                <div class="success-box">
                    <div class="centered-text">
                        <p>SUA INSCRIÇÃO SERÁ EFETIVADA APÓS O PAGAMENTO DE 50% DO VALOR TOTAL</p>
                        <p>I Congresso de Papiloscopia da ASIIP Comparação Facial Humana</p>
                        <p>30 DE NOVEMBRO 7:30</p>
                        <p>Rua Barão do Rio Branco, 370 - Centro, Curitiba/PR</p>
                        <p>Churrasco de Confraternização</p>
                        <p>30 DE NOVEMBRO 13:30</p>
                        <p>Local do churras a definir, Curitiba/PR</p>
                        <p><strong>PIX CNPJ: 39.486.619/0001-93</strong></p>
                        <p><strong>VALOR: R$ 00,00</strong></p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        elif st.session_state["pagina"] == "mensalidades_atrasada":
            st.markdown("""
                <div class="success-box">
                    <div class="centered-text">
                        <p>SUA INSCRIÇÃO SERÁ EFETIVADA APÓS O PAGAMENTO DO VALOR TOTAL</p>
                        <p>I Congresso de Papiloscopia da ASIIP Comparação Facial Humana</p>
                        <p>30 DE NOVEMBRO 7:30</p>
                        <p>Rua Barão do Rio Branco, 370 - Centro, Curitiba/PR</p>
                        <p>Churrasco de Confraternização</p>
                        <p>30 DE NOVEMBRO 13:30</p>
                        <p>Local do churras a definir, Curitiba/PR</p>
                        <p><strong>PIX CNPJ: 39.486.619/0001-93</strong></p>
                        <p><strong>VALOR: R$ 00,00</strong></p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # Campos do formulário para associados
    nome_completo = st.text_input("Nome Completo (Associado)")
    email = st.text_input("Email (Associado)")
    telefone = st.text_input("Telefone (Associado)")

    col1, col2, col3 = st.columns(3)

    # Botão ADIMPLETE
    with col1:
        if st.button("ADIMPLETE", disabled=st.session_state["inscricao_enviada"]):
            if nome_completo and email and telefone:
                # Envia a inscrição para o CSV apenas uma vez
                if not st.session_state["inscricao_enviada"]:
                    novo_inscrito = pd.DataFrame({
                        "Nome Completo": [nome_completo],
                        "Email": [email],
                        "Telefone": [telefone],
                        "Categoria": ["ADIMPLETE"],
                        "Data de Inscrição": [pd.Timestamp.now()]
                    })
                    df_inscritos = pd.concat([df_inscritos, novo_inscrito], ignore_index=True)
                    salvar_dados(df_inscritos)
                    st.session_state["inscricao_enviada"] = True
                    st.session_state["pagina"] = "sucesso"
                st.session_state["botao_ativo"] = False
            else:
                st.error("Por favor, preencha todos os campos antes de enviar.")
        st.caption("Gratos pela sua colaboração perito papiloscopista, nesse evento você será VIP, tudo sem nenhum custo: palestra e churrasco de confraternização.")

    # Botão EM NEGOCIAÇÃO
    with col2:
        if st.button("EM NEGOCIAÇÃO", disabled=st.session_state["inscricao_enviada"]):
            if nome_completo and email and telefone:
                # Envia a inscrição para o CSV apenas uma vez
                if not st.session_state["inscricao_enviada"]:
                    novo_inscrito = pd.DataFrame({
                        "Nome Completo": [nome_completo],
                        "Email": [email],
                        "Telefone": [telefone],
                        "Categoria": ["EM NEGOCIAÇÃO"],
                        "Data de Inscrição": [pd.Timestamp.now()]
                    })
                    df_inscritos = pd.concat([df_inscritos, novo_inscrito], ignore_index=True)
                    salvar_dados(df_inscritos)
                    st.session_state["inscricao_enviada"] = True
                    st.session_state["pagina"] = "negociacao"
                st.session_state["botao_ativo"] = False
            else:
                st.error("Por favor, preencha todos os campos antes de enviar.")
        st.caption("Gratos pela negociação dos pagamentos perito papiloscopista, nesse evento terá o desconto de 50% do valor da palestra e do churrasco.")

    # Botão MENSALIDADES ATRASADA
    with col3:
        if st.button("MENSALIDADES ATRASADA", disabled=st.session_state["inscricao_enviada"]):
            if nome_completo and email and telefone:
                # Envia a inscrição para o CSV apenas uma vez
                if not st.session_state["inscricao_enviada"]:
                    novo_inscrito = pd.DataFrame({
                        "Nome Completo": [nome_completo],
                        "Email": [email],
                        "Telefone": [telefone],
                        "Categoria": ["MENSALIDADES ATRASADA"],
                        "Data de Inscrição": [pd.Timestamp.now()]
                    })
                    df_inscritos = pd.concat([df_inscritos, novo_inscrito], ignore_index=True)
                    salvar_dados(df_inscritos)
                    st.session_state["inscricao_enviada"] = True
                    st.session_state["pagina"] = "mensalidades_atrasada"
                st.session_state["botao_ativo"] = False
            else:
                st.error("Por favor, preencha todos os campos antes de enviar.")
        st.caption("Ficaremos gratos caso queira negociar as parcelas atrasadas e ai receberá 50% de desconto no valor do evento (entre em contato via contato@asiip.com.br), caso ainda não esteja pronto para a negociação clique nesse botão.")

# Exibe o formulário de não associado se o botão foi clicado
if st.session_state["mostrar_nao_associado"]:
    st.subheader("Formulário de Inscrição - NÃO Associado")

    # Exibir a mensagem de sucesso logo abaixo do título
    if st.session_state["inscricao_enviada"] and st.session_state["pagina"] == "sucesso_nao_associado":
        st.markdown("""
            <div class="success-box">
                <div class="centered-text">
                    <p>INSCRIÇÃO EFETUADA COM SUCESSO</p>
                    <p>I Congresso de Papiloscopia da ASIIP Comparação Facial Humana</p>
                    <p>30 DE NOVEMBRO 7:30</p>
                    <p>Rua Barão do Rio Branco, 370 - Centro, Curitiba/PR</p>
                    <p>Churrasco de Confraternização</p>
                    <p>30 DE NOVEMBRO 13:30</p>
                    <p>Local do churras a definir, Curitiba/PR</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Campos do formulário para não associados
    nome_completo_na = st.text_input("Nome Completo (NÃO Associado)")
    email_na = st.text_input("Email (NÃO Associado)")
    telefone_na = st.text_input("Telefone (NÃO Associado)")

    if st.button("Enviar Inscrição (NÃO Associado)", disabled=st.session_state["inscricao_enviada"]):
        if nome_completo_na and email_na and telefone_na:
            # Envia a inscrição para o CSV apenas uma vez
            if not st.session_state["inscricao_enviada"]:
                novo_inscrito = pd.DataFrame({
                    "Nome Completo": [nome_completo_na],
                    "Email": [email_na],
                    "Telefone": [telefone_na],
                    "Categoria": ["NÃO ASSOCIADO"],
                    "Data de Inscrição": [pd.Timestamp.now()]
                })
                df_inscritos = pd.concat([df_inscritos, novo_inscrito], ignore_index=True)
                salvar_dados(df_inscritos)
                st.session_state["inscricao_enviada"] = True
                st.session_state["pagina"] = "sucesso_nao_associado"
        else:
            st.error("Por favor, preencha os campos com os seus dados.")

# Linha de separação azul grossa
st.markdown("<div class='separator'></div>", unsafe_allow_html=True)
