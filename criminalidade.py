# importar pacotes
from typing import Any, Union

import streamlit as st
import pandas as pd
import pydeck as pdk

# carregar os meus dados
from pandas import DataFrame, Series
from pandas.io.parsers import TextFileReader

df: Union[Union[TextFileReader, Series, DataFrame, None], Any] = pd.read_csv('criminalidade_sp.csv')
# dashboard
st.title('Criminalidade em São Paulo')
st.markdown(
    """
A **criminalidade** é um dos problemas sociais mais recorrentes no Brasil.
A implementação de políticas públicas de segurança busca reduzir os índices.
O mapeamento e o diagnóstico dos dados de criminalidade, por meio da utilização dos insights que a **Ciência de Dados** fornece, pode garantir a efetividade das políticas públicas de segurança pública.
    """)
#Sidebar
st.sidebar.info("Foram carregadas {} linhas".format(df.shape[0]))
if st.sidebar.checkbox("Ver tabela com dados"):
    st.header("Raw Data")
    st.write(df)

df.time = pd.to_datetime(df.time)
ano = st.sidebar.slider("Ano", 2010, 2018, 2015)
df_selected = df[df.time.dt.year == ano]
#Mapa
st.subheader("Mapa da Criminalidade")
# st.map(df)
st.pydeck_chart(pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=-23.567145,
        longitude=-45.648936,
        zoom=8,
        pitch=50
    ),
    layers=[
        pdk.Layer(
            'HexagonLayer',
            data=df_selected[['latitude', 'longitude']],
            get_position='[longitude, latitude]',
            auto_highlight=True,
            elevation_scale=50,
            pickable=True,
            elevation_range=[0, 3000],
            extruded=True,
            coverage=1
        )
    ]
    )
)
