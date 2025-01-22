import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime

# Precios de renta y servicios
PRECIOS_RENTA = {
    "Planta Baja": 14000,
    "Planta Alta (Semana)": 7000,
    "Planta Alta (Fin de Semana)": 12000
}
COSTO_HORA_EXTRA = 2000
PRECIOS_COMIDA = {
    "Básico": 250,
    "Tradicional": 300,
    "Premium": 350,
    "Gourmet": 400
}
PRECIOS_SERVICIOS = {
    "DJ": 2500,
    "Grupo Musical": 3500,
    "Mesero": 500
}

# Estilo visual
st.set_page_config(page_title="Cotizador de Eventos - Plaza Alquimia 73", layout="wide")
st.markdown(
    """
    <style>
        body {
            background-image: url('alquimia1.png');
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: white;
        }
        .css-1p3h7l5 {
            color: #FFFFFF;
        }
        .stButton>button {
            background-color: #008CBA;
            color: white;
            font-weight: bold;
        }
        .stTextInput>div>input {
            background-color: #f0f0f0;
            border-radius: 5px;
        }
        .stSelectbox>div>div>input {
            background-color: #f0f0f0;
            border-radius: 5px;
        }
        .stMultiselect>div>div>input {
            background-color: #f0f0f0;
            border-radius: 5px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Título
st.title("Cotizador de Eventos - Plaza Alquimia 73")

# Selección de datos
fecha_evento = st.date_input("Selecciona la fecha del evento", datetime.date.today())
fecha_reservada = pd.to_datetime("2025-01-25")  # Simulando una fecha reservada
if fecha_evento == fecha_reservada:
    st.warning("Esta fecha ya está reservada. Elige otra.")
else:
    planta = st.selectbox("Selecciona la ubicación", list(PRECIOS_RENTA.keys()))
    horas_extra = st.number_input("Horas adicionales", min_value=0, step=1)
    n_personas = st.number_input("Número de personas", min_value=1, step=1)
    paquete_comida = st.selectbox("Selecciona el paquete de alimentos", list(PRECIOS_COMIDA.keys()))

    # Servicios adicionales
    servicios_seleccionados = st.multiselect("Servicios adicionales", list(PRECIOS_SERVICIOS.keys()))

    # Cálculo de costos
    costo_renta = PRECIOS_RENTA[planta] + (horas_extra * COSTO_HORA_EXTRA)
    costo_comida = PRECIOS_COMIDA[paquete_comida] * n_personas
    costo_servicios = sum(PRECIOS_SERVICIOS[servicio] for servicio in servicios_seleccionados)
    costo_total = costo_renta + costo_comida + costo_servicios

    st.write(f"### Costo Total: ${costo_total}")

    # Generar cotización en PDF
    def generar_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, "Cotización de Evento", ln=True, align="C")
        pdf.cell(200, 10, f"Fecha del Evento: {fecha_evento}", ln=True)
        pdf.cell(200, 10, f"Ubicación: {planta}", ln=True)
        pdf.cell(200, 10, f"Número de Personas: {n_personas}", ln=True)
        pdf.cell(200, 10, f"Paquete de Comida: {paquete_comida} - ${costo_comida}", ln=True)
        pdf.cell(200, 10, f"Costo de Renta: ${costo_renta}", ln=True)
        pdf.cell(200, 10, f"Servicios Adicionales: {', '.join(servicios_seleccionados)} - ${costo_servicios}", ln=True)
        pdf.cell(200, 10, f"Costo Total: ${costo_total}", ln=True)
        pdf.output("cotizacion_evento.pdf")
        st.success("PDF generado con éxito")

    if st.button("Generar Cotización PDF"):
        generar_pdf()

    # Generar link de WhatsApp
    def generar_link_whatsapp():
        mensaje = f"Cotización Plaza Alquimia 73%0AFecha: {fecha_evento}%0AUbicación: {planta}%0APersonas: {n_personas}%0AComida: {paquete_comida} - ${costo_comida}%0ARenta: ${costo_renta}%0AServicios: {', '.join(servicios_seleccionados)} - ${costo_servicios}%0ATotal: ${costo_total}"
        numero = st.text_input("Número de WhatsApp (con código de país, sin '+')", "52")  # 52 es el código de México
        link = f"https://wa.me/{numero}?text={mensaje}"

        if st.button("Generar Link de WhatsApp"):
            st.markdown(f"[Enviar Cotización por WhatsApp]({link})", unsafe_allow_html=True)

    generar_link_whatsapp()

    # Apartado de datos de contacto
    st.subheader("Deja tus datos para contacto")
    nombre_contacto = st.text_input("Nombre completo")
    correo_contacto = st.text_input("Correo electrónico")
    telefono_contacto = st.text_input("Teléfono")
    mensaje_contacto = st.text_area("Mensaje (opcional)")
    if st.button("Enviar Información de Contacto"):
        st.success("¡Tu información ha sido enviada exitosamente!")


