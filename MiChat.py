import streamlit as st
from groq import Groq


# CONFIG DE LA PÁGINA
st.set_page_config(page_title="1er ChatIA", page_icon="🐢")
st.title("Bienvenido a mi 1er app usando Streamlit!!!")


# SALUDO INICIAL
nombre = st.text_input("¿Cuál es tu nombre?")
if st.button("Saludar!"):
    st.write(f"¡Hola {nombre}! Estoy acá para resolver tus dudas 🤖")


# MODELOS
MODELOS = ['llama-3.1-8b-instant', 'llama-3.3-70b-versatile', 'deepseek-r1-distill-llama-70b']


# CONFIGURACIÓN DE LA PÁGINA Y SIDEBAR
def configurar_pagina():
    st.title("ChatIA de Wendyy")
    st.sidebar.title("Configuración")
    
    elegirModelo = st.sidebar.selectbox(
        "Elegí un modelo",
        options=MODELOS,
        index=0
    )
    return elegirModelo


# CLIENTE GROQ
def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)


# CONFIGURAR EL MODELO PARA RESPONDER
def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role":"user", "content": mensajeDeEntrada}],
        stream = True
    )

# ESTADO DEL CHAT
def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []


# GUARDAR MENSAJES EN EL HISTORIAL
def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})


# MOSTRAR HISTORIAL DE CHAT
def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])


# CONTENEDOR DE CHAT
def area_chat():
    contenedorDelChat = st.container(height=400, border=True)
    with contenedorDelChat:
        mostrar_historial()


# STREAMING DE RESPUESTAS (CLASE 9)
def generar_respuestas(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa


# MAIN
def main():
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    modelo = configurar_pagina()
    area_chat()

    mensaje = st.chat_input("Escribí tu mensaje:")
    if mensaje:
        actualizar_historial("user", mensaje, "🦔")

        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)

        if chat_completo:
            with st.chat_message("assistant", avatar="🤖"):
                respuesta_completa = st.write_stream(generar_respuestas(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "🤖")
                st.rerun()


if __name__ == "__main__":
    main()
