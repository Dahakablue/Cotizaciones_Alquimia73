import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime
from PIL import Image

# Precios de renta y servicios
PRECIOS_RENTA = {
    "Entre semana Planta Baja": 14000,
    "Fin de semana Planta Baja": 15000,
    "Entre semana Planta Alta": 7000,
    "Fin de semana Planta Alta": 12000
}
COSTO_HORA_EXTRA = 2000
PRECIOS_COMIDA = {
    "Básico": 250,
    "Tradicional": 300,
    "Premium": 350,
    "Gourmet": 400
}
DESCRIPCIONES_COMIDA = {
    "Básico": "Menú económico con platillos sencillos, ideal para eventos casuales.",
    "Tradicional": "Menú con platillos mexicanos típicos, ideal para todos los gustos.",
    "Premium": "Menú de calidad superior con opciones gourmet y sabores sofisticados.",
    "Gourmet": "Menú exclusivo con platillos de alta cocina, ideal para eventos de lujo."
}
PRECIOS_SERVICIOS = {
    "DJ": 2500,
    "Grupo Musical": 3500,
    "Mesero": 500
}

# Estilo visual
st.set_page_config(page_title="Cotizador de Eventos - Plaza Alquimia 73", layout="wide", initial_sidebar_state="collapsed")

# Cargar imagen de fondo
img = Image.open('alquimia1.png')
st.image(img, use_container_width=True)

# Título de la página con estilo
st.markdown("""
    <style>
        .title {
            color: #FFFFFF;
            font-size: 36px;
            text-align: center;
            font-weight: bold;
            font-family: 'Arial', sans-serif;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
        }
        .subheader {
            color: #FFD700;
            font-size: 24px;
            font-weight: bold;
        }
        .description {
            font-size: 16px;
            color: #FFFFFF;
        }
        .card {
            background-color: rgba(0, 0, 0, 0.5);
            padding: 20px;
            border-radius: 10px;
            color: #FFFFFF;
            margin-bottom: 20px;
        }
        .button {
            background-color: #FFD700;
            color: #000000;
            font-size: 16px;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 10px;
            cursor: pointer;
        }
        .button:hover {
            background-color: #FFA500;
        }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<h1 class="title">Cotizador de Eventos - Plaza Alquimia 73</h1>', unsafe_allow_html=True)

# Selección de datos con tarjetas estilizadas
with st.expander("Selecciona tus opciones para el evento", expanded=True):
    fecha_evento = st.date_input("Selecciona la fecha del evento", datetime.date.today())
    fecha_reservada = pd.to_datetime("2025-01-25")  # Simulando una fecha reservada
    if fecha_evento == fecha_reservada:
        st.warning("Esta fecha ya está reservada. Elige otra.")
    else:
        planta = st.selectbox(
            "Selecciona la ubicación",
            [
                "Entre semana Planta Baja - $14,000",
                "Fin de semana Planta Baja - $15,000",
                "Entre semana Planta Alta - $7,000",
                "Fin de semana Planta Alta - $12,000"
            ]
        )
        horas_extra = st.number_input("Horas adicionales", min_value=0, step=1)
        n_personas = st.number_input("Número de personas", min_value=1, step=1)

        # Paquete de comida con descripciones
        paquete_comida = st.selectbox(
            "Selecciona el paquete de alimentos",
            [
                "Básico - $250",
                "Tradicional - $300",
                "Premium - $350",
                "Gourmet - $400"
            ]
        )
        st.markdown(f"**Descripción del paquete de comida:** {DESCRIPCIONES_COMIDA[paquete_comida.split(' - ')[0]]}")

        # Servicios adicionales
        servicios_seleccionados = st.multiselect(
            "Servicios adicionales",
            [
                "DJ - $2,500",
                "Grupo Musical - $3,500",
                "Mesero - $500"
            ]
        )

        # Cálculo de costos
        if planta == "Entre semana Planta Baja - $14,000":
            costo_renta = 14000
        elif planta == "Fin de semana Planta Baja - $15,000":
            costo_renta = 15000
        elif planta == "Entre semana Planta Alta - $7,000":
            costo_renta = 7000
        elif planta == "Fin de semana Planta Alta - $12,000":
            costo_renta = 12000

        costo_renta += (horas_extra * COSTO_HORA_EXTRA)
        costo_comida = PRECIOS_COMIDA[paquete_comida.split(" - ")[0]] * n_personas
        costo_servicios = sum(PRECIOS_SERVICIOS[servicio.split(" - ")[0]] for servicio in servicios_seleccionados)
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

        if st.button("Generar Cotización PDF", key="pdf_button"):
            generar_pdf()

        # Generar link de WhatsApp
        def generar_link_whatsapp():
            mensaje = f"Cotización Plaza Alquimia 73%0AFecha: {fecha_evento}%0AUbicación: {planta}%0APersonas: {n_personas}%0AComida: {paquete_comida} - ${costo_comida}%0ARenta: ${costo_renta}%0AServicios: {', '.join(servicios_seleccionados)} - ${costo_servicios}%0ATotal: ${costo_total}"
            numero = st.text_input("Número de WhatsApp (con código de país, sin '+')", "52")  # 52 es el código de México
            link = f"https://wa.me/{numero}?text={mensaje}"

            if st.button("Generar Link de WhatsApp", key="whatsapp_button"):
                st.markdown(f"[Enviar Cotización por WhatsApp]({link})", unsafe_allow_html=True)

        generar_link_whatsapp()

        # Apartado de datos de contacto
        st.subheader("Deja tus datos para contacto")
        nombre_contacto = st.text_input("Nombre completo")
        correo_contacto = st.text_input("Correo electrónico")
        telefono_contacto = st.text_input("Teléfono")
        mensaje_contacto = st.text_area("Mensaje (opcional)")
        if st.button("Enviar Información de Contacto", key="contact_button"):
            st.success("¡Tu información ha sido enviada exitosamente!")


