import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title = "FirstAppTest", 
                   layout = "wide", 
                   page_icon = "https://static.vecteezy.com/system/resources/thumbnails/068/205/805/small/app-website-3d-icon-png.png")

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

if st.sidebar.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.sidebar.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))
left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")


from PIL import Image
from streamlit_drawable_canvas import st_canvas


# st.write("## Testando a aplicação de um quadro desenhavel")

# import os

# import numpy as np
# import streamlit as st
# from os.path import dirname
# from os.path import join
# import setuptools


# def readme() -> str:
#     """Utility function to read the README file.
#     Used for the long_description.  It's nice, because now 1) we have a top
#     level README file and 2) it's easier to type in the README file than to put
#     a raw string in below.
#     :return: content of README.md
#     """
#     return open(join(dirname(__file__), "README.md")).read()


# setuptools.setup(
#     name="streamlit-drawable-canvas",
#     version="0.0.1",
#     author="Fanilo ANDRIANASOLO",
#     author_email="andfanilo@gmail.com",
#     description="A Streamlit custom component for a free drawing canvas using Fabric.js.",
#     long_description=readme(),
#     long_description_content_type="text/plain",
#     url="https://github.com/andfanilo/streamlit-drawable-canvas",
#     packages=setuptools.find_packages(),
#     include_package_data=True,
#     classifiers=[],
#     python_requires=">=3.6",
# )
# _RELEASE = False  # on packaging, pass this to True

# if not _RELEASE:
#     _component_func = st.declare_component("st_canvas", url="http://localhost:3001",)
# else:
#     parent_dir = os.path.dirname(os.path.abspath(__file__))
#     build_dir = os.path.join(parent_dir, "frontend/build")
#     _component_func = st.declare_component("st_canvas", path=build_dir)


# def st_canvas(
#     brush_width=20,
#     brush_color="black",
#     background_color="#eee",
#     height=400,
#     width=600,
#     key="canvas",
# ):
#     """ Validate inputs + Post-process image from canvas
#         :param brush_width:
#         :param brush_color:
#         :param background_color:
#         :param height:
#         :param width:
#         :param key:
#         :return: Reshaped image
#         """
#     component_value = _component_func(
#         brush_width=brush_width,
#         brush_color=brush_color,
#         background_color=background_color,
#         height=height,
#         width=width,
#         key=key,
#         default=None,
#     )
#     if component_value is None:
#         return None

#     w = component_value["width"]
#     h = component_value["height"]
#     return np.reshape(component_value["data"], (h, w, 4))

