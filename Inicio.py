
import streamlit as st
import paho.mqtt.client as mqtt
import json
import time

# --------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# --------------------------------------------------
st.set_page_config(
    page_title="SensorLab | Monitor MQTT",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# ESTILOS VISUALES
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg: #0b1020;
    --panel: #131b2e;
    --panel-light: #1a2540;
    --purple: #a78bfa;
    --cyan: #67e8f9;
    --text: #f1f5f9;
    --muted: #94a3b8;
    --border: rgba(148, 163, 184, 0.17);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 5% 0%, rgba(124,58,237,0.15), transparent 34%),
        radial-gradient(ellipse at 95% 5%, rgba(6,182,212,0.10), transparent 30%),
        var(--bg);
    color: var(--text);
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: #0e1628;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] * {
    color: var(--text);
}

[data-testid="stSidebar"] input {
    background: #172238;
    border: 1px solid #2a3855;
    border-radius: 10px;
}

.block-container {
    padding-top: 2.2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text) !important;
}

.hero {
    background: linear-gradient(120deg, #1b2440 0%, #171d36 55%, #142b3b 100%);
    border: 1px solid rgba(167,139,250,0.25);
    border-radius: 24px;
    padding: 30px 32px;
    position: relative;
    overflow: hidden;
    margin-bottom: 26px;
}

.hero:after {
    content: "";
    position: absolute;
    width: 210px;
    height: 210px;
    border-radius: 50%;
    right: -55px;
    top: -95px;
    background: rgba(103,232,249,0.08);
    border: 1px solid rgba(103,232,249,0.13);
}

.eyebrow {
    color: var(--cyan);
    font-size: 0.76rem;
    letter-spacing: 2.4px;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 700;
    line-height: 1.1;
    color: #ffffff;
    margin-bottom: 12px;
}

.hero-description {
    color: #b4c0d5;
    font-size: 1rem;
    max-width: 650px;
    line-height: 1.7;
}

.section-label {
    color: #c4b5fd;
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.info-card {
    background: linear-gradient(145deg, #172139, #111a2c);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 20px;
    min-height: 125px;
    margin-bottom: 12px;
}

.card-label {
    font-size: 0.78rem;
    color: #9aa9c2;
    letter-spacing: 0.7px;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.card-value {
    color: #ffffff;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.45rem;
    font-weight: 600;
    overflow-wrap: anywhere;
}

.card-hint {
    color: #7f91ae;
    font-size: 0.8rem;
    margin-top: 8px;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #192541, #131c30);
    border: 1px solid rgba(103,232,249,0.15);
    border-radius: 16px;
    padding: 20px;
    min-height: 125px;
}

[data-testid="stMetricLabel"] {
    color: #a5b4cc !important;
    font-size: 0.9rem !important;
}

[data-testid="stMetricValue"] {
    color: #67e8f9 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.8rem !important;
    overflow-wrap: anywhere;
}

[data-testid="stMetricDelta"] {
    font-size: 0.8rem;
}

.stButton > button {
    background: linear-gradient(110deg, #8b5cf6, #6366f1);
    color: white;
    border: 1px solid rgba(196,181,253,0.3);
    border-radius: 12px;
    padding: 0.8rem 1.3rem;
    font-weight: 700;
    min-height: 48px;
    box-shadow: 0 6px 24px rgba(99,102,241,0.18);
    transition: all 0.2s ease;
}

.stButton > button:hover {
    border-color: #c4b5fd;
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(139,92,246,0.25);
}

.status-pill {
    display: inline-block;
    background: rgba(52,211,153,0.1);
    color: #6ee7b7;
    border: 1px solid rgba(52,211,153,0.25);
    border-radius: 50px;
    padding: 7px 12px;
    font-size: 0.8rem;
    font-weight: 600;
}

.status-idle {
    display: inline-block;
    background: rgba(148,163,184,0.09);
    color: #cbd5e1;
    border: 1px solid rgba(148,163,184,0.2);
    border-radius: 50px;
    padding: 7px 12px;
    font-size: 0.8rem;
    font-weight: 600;
}

div[data-testid="stExpander"] {
    background: rgba(19,27,46,0.75);
    border: 1px solid var(--border);
    border-radius: 14px;
}

div[data-testid="stExpander"] summary {
    color: #e2e8f0;
}

hr {
    border-color: rgba(148,163,184,0.15);
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

.stCaption, [data-testid="stCaptionContainer"] {
    color: #8494af;
}

.footer {
    color: #64748b;
    font-size: 0.8rem;
    text-align: center;
    padding-top: 28px;
}

code {
    color: #a5f3fc !important;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# ESTADO DE LA APLICACIÓN
# --------------------------------------------------
if "sensor_data" not in st.session_state:
    st.session_state.sensor_data = None

if "last_topic" not in st.session_state:
    st.session_state.last_topic = None

if "last_updated" not in st.session_state:
    st.session_state.last_updated = None


# --------------------------------------------------
# FUNCIÓN MQTT
# --------------------------------------------------
def get_mqtt_message(broker, port, topic, client_id):
    """Conecta al broker, escucha el tópico y devuelve el primer mensaje."""
    message_received = {"received": False, "payload": None}

    def on_message(client, userdata, message):
        try:
            decoded = message.payload.decode("utf-8")
            try:
                payload = json.loads(decoded)
            except json.JSONDecodeError:
                payload = decoded

            message_received["payload"] = payload
            message_received["received"] = True
        except Exception as e:
            message_received["payload"] = {"error": str(e)}
            message_received["received"] = True

    client = None

    try:
        try:
            client = mqtt.Client(
                callback_api_version=mqtt.CallbackAPIVersion.VERSION1,
                client_id=client_id
            )
        except (AttributeError, TypeError):
            client = mqtt.Client(client_id=client_id)

        client.on_message = on_message
        client.connect(broker, int(port), 60)
        client.subscribe(topic)
        client.loop_start()

        timeout = time.time() + 5

        while not message_received["received"] and time.time() < timeout:
            time.sleep(0.1)

        if message_received["received"]:
            result = message_received["payload"]
        else:
            result = {
                "error": "No se recibió ningún mensaje en 5 segundos. "
                         "Verifica que el sensor esté publicando en este tópico."
            }

        return result

    except Exception as e:
        return {"error": str(e)}

    finally:
        if client is not None:
            try:
                client.loop_stop()
                client.disconnect()
            except Exception:
                pass


# --------------------------------------------------
# BARRA LATERAL
# --------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="padding: 12px 0 22px 0;">
        <div style="font-size: 2.3rem;">📡</div>
        <div style="font-family: 'Space Grotesk', sans-serif;
                    font-size: 1.4rem; font-weight: 700; color: white;">
            Sensor<span style="color:#a78bfa;">Lab</span>
        </div>
        <div style="font-size:0.8rem; color:#8494af;">
            MONITOREO EN TIEMPO REAL
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown('<div class="section-label">Conexión MQTT</div>',
                unsafe_allow_html=True)

    broker = st.text_input(
        "Servidor / Broker",
        value="broker.mqttdashboard.com",
        help="Dirección del broker MQTT"
    )

    port = st.number_input(
        "Puerto",
        value=1883,
        min_value=1,
        max_value=65535,
        step=1,
        help="El puerto más habitual es 1883"
    )

    topic = st.text_input(
        "Tópico del sensor",
        value="Sensor/THP2",
        help="Canal MQTT del que quieres recibir información"
    )

    client_id = st.text_input(
        "ID del cliente",
        value="streamlit_client",
        help="Identificador para esta conexión MQTT"
    )

    st.markdown("---")

    st.markdown(
        '<div style="font-size:0.8rem; color:#8494af; line-height:1.6;">'
        '<span style="color:#67e8f9;">●</span> Configura los datos del broker '
        'y consulta el último mensaje disponible en el tópico.'
        '</div>',
        unsafe_allow_html=True
    )

# --------------------------------------------------
# ENCABEZADO PRINCIPAL
# --------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="eyebrow">◈ Internet de las cosas · IoT</div>
    <div class="hero-title">Monitor de sensores</div>
    <div class="hero-description">
        Visualiza los datos transmitidos por tus dispositivos a través de MQTT.
        Conecta con tu broker y consulta la información de tus sensores
        desde un solo lugar.
    </div>
</div>
""", unsafe_allow_html=True)

# Resumen de la conexión configurada
col_broker, col_topic, col_status = st.columns([1.2, 1.2, 0.8])

with col_broker:
    st.markdown(f"""
    <div class="info-card">
        <div class="card-label">◉ Broker configurado</div>
        <div class="card-value" style="font-size:1.05rem;">{broker}</div>
        <div class="card-hint">Puerto {int(port)}</div>
    </div>
    """, unsafe_allow_html=True)

with col_topic:
    st.markdown(f"""
    <div class="info-card">
        <div class="card-label">⌁ Tópico seleccionado</div>
        <div class="card-value" style="font-size:1.05rem;">{topic}</div>
        <div class="card-hint">Canal de recepción MQTT</div>
    </div>
    """, unsafe_allow_html=True)

with col_status:
    if st.session_state.last_updated:
        status_html = (
            '<span class="status-pill">● Datos recibidos</span>'
        )
        status_hint = "Última consulta exitosa"
    else:
        status_html = (
            '<span class="status-idle">● En espera</span>'
        )
        status_hint = "Esperando consulta"

    st.markdown(f"""
    <div class="info-card">
        <div class="card-label">Estado</div>
        {status_html}
        <div class="card-hint">{status_hint}</div>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# BOTÓN DE CONSULTA
# --------------------------------------------------
st.markdown('<div class="section-label">CONSULTA DE DATOS</div>',
            unsafe_allow_html=True)

left, center, right = st.columns([1, 1.5, 1])

with center:
    consultar = st.button(
        "↻  Obtener datos del sensor",
        use_container_width=True
    )

if consultar:
    if not broker.strip() or not topic.strip() or not client_id.strip():
        st.warning("Completa el broker, el tópico y el ID del cliente.")
    else:
        with st.spinner("Conectando al broker MQTT y esperando el mensaje..."):
            sensor_data = get_mqtt_message(
                broker.strip(),
                int(port),
                topic.strip(),
                client_id.strip()
            )

        st.session_state.sensor_data = sensor_data
        st.session_state.last_topic = topic.strip()

        if not (isinstance(sensor_data, dict) and "error" in sensor_data):
            st.session_state.last_updated = time.strftime("%H:%M:%S")

# --------------------------------------------------
# RESULTADOS
# --------------------------------------------------
st.markdown("---")

st.markdown('<div class="section-label">LECTURAS DEL DISPOSITIVO</div>',
            unsafe_allow_html=True)

st.markdown("## 📊 Datos del sensor")

data = st.session_state.sensor_data

if data is None:
    st.markdown("""
    <div style="background:rgba(19,27,46,0.65);
                border:1px dashed rgba(148,163,184,0.3);
                border-radius:18px; padding:38px 20px;
                text-align:center; margin-top:12px;">
        <div style="font-size:2.8rem; margin-bottom:12px;">📡</div>
        <div style="font-family:'Space Grotesk',sans-serif;
                    font-size:1.2rem; color:#e2e8f0; font-weight:600;">
            Tu panel está listo
        </div>
        <div style="color:#94a3b8; font-size:0.9rem;
                    margin-top:8px; line-height:1.6;">
            Configura la conexión en el menú lateral y pulsa
            <b>Obtener datos del sensor</b> para consultar el primer mensaje.
        </div>
    </div>
    """, unsafe_allow_html=True)

elif isinstance(data, dict) and "error" in data:
    st.error(f"⚠️ No fue posible obtener los datos: {data['error']}")
    st.caption("Comprueba el broker, el puerto, el tópico y que el sensor esté publicando.")

else:
    if st.session_state.last_updated:
        st.caption(
            f"Última consulta: {st.session_state.last_updated} "
            f"· Tópico: {st.session_state.last_topic}"
        )

    st.success("Mensaje recibido correctamente")

    if isinstance(data, dict):
        if len(data) == 0:
            st.info("El mensaje recibido contiene un objeto JSON vacío.")
        else:
            # Distribuir las métricas en filas de máximo 3 columnas
            items = list(data.items())

            for start in range(0, len(items), 3):
                row_items = items[start:start + 3]
                columns = st.columns(3)

                for col, (key, value) in zip(columns, row_items):
                    with col:
                        if isinstance(value, (dict, list)):
                            display_value = json.dumps(
                                value, ensure_ascii=False
                            )
                        elif value is None:
                            display_value = "Sin dato"
                        else:
                            display_value = str(value)

                        st.metric(
                            label=str(key),
                            value=display_value
                        )

        with st.expander("⌘  Ver mensaje JSON completo"):
            st.json(data)

    elif isinstance(data, list):
        st.markdown("**Contenido recibido**")
        st.json(data)

    else:
        st.markdown("""
        <div class="info-card">
            <div class="card-label">Mensaje recibido</div>
        </div>
        """, unsafe_allow_html=True)

        st.code(str(data), language=None)

# --------------------------------------------------
# AYUDA
# --------------------------------------------------
with st.expander("ℹ️  Ayuda y solución de problemas"):
    st.markdown("""
    **¿Cómo funciona?**

    1. Introduce el servidor y el puerto del broker MQTT.
    2. Escribe el tópico donde publica tu sensor.
    3. Asigna un ID de cliente para esta conexión.
    4. Pulsa **Obtener datos del sensor**.
    5. Si llega un mensaje, la aplicación mostrará sus campos.

    **Brokers públicos para pruebas**
    - `broker.mqttdashboard.com`
    - `test.mosquitto.org`
    - `broker.hivemq.com`

    **Si no llegan datos**
    - Confirma que el sensor esté encendido y publicando.
    - Comprueba que el tópico coincida exactamente, incluidas mayúsculas.
    - Verifica el broker y el puerto.
    - Los brokers públicos pueden tener restricciones o estar temporalmente fuera de servicio.

    **Importante:** esta aplicación espera un mensaje durante un máximo de
    cinco segundos cada vez que pulsas el botón. No mantiene una suscripción
    permanente en segundo plano.
    """)

# --------------------------------------------------
# PIE DE PÁGINA
# --------------------------------------------------
st.markdown("""
<div class="footer">
    SENSORLAB · MQTT MONITOR &nbsp;•&nbsp; Powered by Streamlit
</div>
""", unsafe_allow_html=True)
