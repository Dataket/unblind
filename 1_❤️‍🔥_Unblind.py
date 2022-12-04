import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title='Unblind', page_icon="https://i.imgur.com/glZSzm1.png")

# sidebar menu
with st.sidebar:
    st.image('https://i.imgur.com/mee3uqn.png') 
    selected = option_menu("Unblind", ["Home", "Upload",  "Tasks", 'Settings'], 
    icons=['house', 'cloud-upload', "list-task", 'gear'], 
    menu_icon="cast", default_index=0, orientation="vertical",
    styles={
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#2a9d8e"},
    }
)
st.title('Proyecto📈')
st.markdown('Desarrollamos una paquetería en Python 🐍 que se encarga del tratamiento de datos, creación de visualizaciones y el desarrollo de modelos predictivos. Utilizando nuestra página web podrá obtener gráficos dinámicos de su interés u archivos excel, con la información que requiera ¡En tan solo unos minutos ⏰!. Esta librería podrá ser utilizada por cualquier persona que tenga un poco de experiencia en programación, permitiendo tener un alcance más grande en el análisis de datos. Como extra la libería también incluye funciones que desarrollan modelos predictivos con la utilización de Machine Learning, lo que ayuda a obtener **posibles casos de corrupción**.')
st.markdown('**⚠️''Es importante destacar que los modelos no arrojan casos de corrupción reales, solo permiten observar los casos de mayor preocupación. ⚠️**')
st.markdown('🔗 Repositorio de GitHub: https://github.com/Dataket/unblind.git')
st.title('Video🎥')
st.video("https://youtu.be/KkR3yv8d4v0")
st.title('Equipo')
st.markdown('#### Somos un equipo de estudiantes con gusto por la ciencia de datos, el desarrollo web, y otras sorpresas ✨')
col1, col2, col3 = st.columns(3)
with col1:
  st.image('https://i.imgur.com/7RKQmvk.png', width=200,caption='Gil Rodríguez')
with col2:
   st.image('https://i.imgur.com/trSs5d2.png', width=200,caption='Missael Barco')
with col3:
   st.image('https://i.imgur.com/ckCWoZG.png', width=200,caption='Héctor Nieto')

col1, col2, col3 = st.columns(3)
with col1:
  st.image('https://i.imgur.com/dCQxmpb.png', width=200,caption='Estefanía Saucedo')
with col2:
  st.image('https://i.imgur.com/nhVzrox.png', width=200,caption='David Pedroza')

