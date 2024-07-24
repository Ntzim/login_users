import streamlit as st
import mysql.connector
import bcrypt
import plotly.express as px
import pandas as pd

# Função para autenticar usuário
def authenticate(email, password):
    conn = mysql.connector.connect(
        host="project.cdyci0i4soya.us-east-1.rds.amazonaws.com",
        user="admin",
        password="grupo123#",
        database="Projeto"
    )
    cursor = conn.cursor()
    cursor.execute('SELECT email, password, nome FROM usuarios WHERE email = %s', (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
        return user[2]
    else:
        return None

# Tela de login
def login_screen():
    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate(email, password)
        if user:
            st.success(f"Welcome {user}!")
            dashboard_screen()
        else:
            st.error("Invalid email or password")

# Tela de registro
def register_screen():
    st.title("Register")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    nome = st.text_input("Nome")
    setor = st.text_input("Setor")
    cargo = st.text_input("Cargo")

    if st.button("Register"):
        if email and password and nome and setor and cargo:
            conn = mysql.connector.connect(
                host="your_host",
                user="your_user",
                password="your_password",
                database="your_database"
            )
            cursor = conn.cursor()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute('INSERT INTO usuarios (email, password, nome, setor, cargo) VALUES (%s, %s, %s, %s, %s)',
                           (email, hashed_password, nome, setor, cargo))
            conn.commit()
            cursor.close()
            conn.close()
            st.success("User registered successfully!")
        else:
            st.error("Please fill all the fields.")

# Tela do dashboard
def dashboard_screen():
    st.title("Dashboard")

    # Dados fictícios
    total_inscritos = 20000
    total_certificados = 10000
    total_projetos = 10

    # Gráfico de inscritos
    inscritos_data = pd.DataFrame({'Category': ['Inscritos'], 'Count': [total_inscritos]})
    fig_inscritos = px.bar(inscritos_data, x='Category', y='Count', title='Total de Inscritos')

    # Gráfico de certificados
    certificados_data = pd.DataFrame({'Category': ['Certificados'], 'Count': [total_certificados]})
    fig_certificados = px.bar(certificados_data, x='Category', y='Count', title='Total de Certificados')

    # Gráfico de projetos
    projetos_data = pd.DataFrame({'Category': ['Projetos'], 'Count': [total_projetos]})
    fig_projetos = px.bar(projetos_data, x='Category', y='Count', title='Total de Projetos')

    # Exibir gráficos no Streamlit
    st.plotly_chart(fig_inscritos)
    st.plotly_chart(fig_certificados)
    st.plotly_chart(fig_projetos)

# Função principal
def main():
    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        login_screen()
    elif choice == "Register":
        register_screen()

if __name__ == "__main__":
    main()
