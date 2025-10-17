import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from io import BytesIO

# ----------------------------
# CONFIGURAÇÕES INICIAIS
# ----------------------------
st.set_page_config(
    page_title="FirstAppTest", 
    layout="wide", 
    page_icon="https://static.vecteezy.com/system/resources/thumbnails/068/205/805/small/app-website-3d-icon-png.png"
)

st.title("🚕 Uber pickups in NYC")


# ----------------------------
# FUNÇÃO PARA CARREGAR OS DADOS
# ----------------------------
DATE_COLUMN = 'date/time'
DATA_URL = (
    'https://s3-us-west-2.amazonaws.com/'
    'streamlit-demo-data/uber-raw-data-sep14.csv.gz'
)

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data.columns = data.columns.str.lower()
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


# ----------------------------
# CARREGAMENTO E EXIBIÇÃO DOS DADOS
# ----------------------------
data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("✅ Done! (using st.cache_data)")

if st.sidebar.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)


# ----------------------------
# GRÁFICO DE COLETAS POR HORA
# ----------------------------
st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24)
)[0]
st.bar_chart(hist_values)


# ----------------------------
# FILTRAR POR HORA E EXIBIR MAPA
# ----------------------------
hour_to_filter = st.sidebar.slider('Hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)


# ----------------------------
# DATAFRAME DE EXEMPLO
# ----------------------------
dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=(f'col {i}' for i in range(20))
)
st.dataframe(dataframe.style.highlight_max(axis=0))


# ----------------------------
# COLUNAS E INTERAÇÃO
# ----------------------------
left_column, right_column = st.columns(2)
left_column.button('Press me!')

with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin")
    )
    st.write(f"You are in {chosen} house!")


# ----------------------------
# QUADRO DESENHÁVEL (CANVAS)
# ----------------------------
st.write("## ✏️ Testando a aplicação de um quadro desenhável")

canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # cor de preenchimento
    stroke_width=3,
    stroke_color="black",
    background_color="#eee",
    height=300,
    width=500,
    drawing_mode="freedraw",
    key="canvas",
)

# ----------------------------
# EXIBIR E BAIXAR O DESENHO
# ----------------------------
if canvas_result.image_data is not None:
    st.image(canvas_result.image_data, caption="Seu desenho:")

    # Converter imagem para bytes
    img = Image.fromarray((canvas_result.image_data).astype("uint8"))
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="📥 Baixar desenho como PNG",
        data=byte_im,
        file_name="meu_desenho.png",
        mime="image/png",
    )
