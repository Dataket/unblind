import streamlit as st

st.markdown('''

Unblind (0.0.5) se encuentra disponible en PyPi! 🎉. Puedes ver el paquete en [este link](https://pypi.org/project/unblind/).

Si gustas colaborar con el proyecto, puedes hacerlo en el repositorio de [GitHub](https://github.com/Dataket/unblind).

# Unblind
Protecto para el Datatón anticorrupción 2022 ✨.

# Descripción 📄
Librería en Python 🐍 que ayuda en el tratamiento de datos, creación de visualizaciones, y desarrollo de modelos predictivos, para los datos de la Plataforma Digital Nacional. También se creó una página web dinámica con ayuda de [streamlit](https://streamlit.io/) (Véase la rama de [streamlit](https://github.com/Dataket/unblind/tree/streamlit)).

# Requerimientos para el paquete 📦
- python 3.8+
- python-env

Para instalar Unblind y comenzar a usarlo, ejecuta el siguiente comando en tu terminal en tu entorno virtual:

```bash
pip install unblind
```

¡Y listo! 🎉

# Estructura de carpetas 📁
A continuación ser verá la estructura de carpetas utilizada en nuestro proyecto así como las descripciones de cada uno de los archivos.

```
.
├── data
│   └── process_data
├── unblind
│   ├── __init__.py
│   ├── dataviz.py
│   ├── etl.py
│   └── utils.py
├── LICENSE
├── README.md
├── pyproject.toml
├── requirements.txt
└── setup.py
```

- data: Carpeta que guarda todos los datos que son utilizados para los análisis y graficas.
	- process_data: Los datos de la __PDN__ procesados por nuestro módulo **unblind**. 
- unblind: Carpeta que alberga todo el código y lógica del paquete.
	- dataviz.py: Script donde se encuentra toda la lógica de la visualización de datos para el paquete.
	- etl.py: Script de Python donde está todo lo que tiene que ver con Extracción, Transformación y Carga de los datos para ser utilizados de manera más sencilla y comprensible (sirve mucho para encontrar errores).
	- utils.py: Script que contiene funciones *"helpers"* que ayudan en la obtención de datos a partir de la API de la PDN.


# Setup para desarrolladores🛠
Para poder modificar el código del paquete y contribuir, y ser capaz de hacer cambios en él, se necesitará seguir los siguientes pasos.

1. [¡Haz fork al repositorio!](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/about-forks)

2. Clona tu repositorio (sustituye la URL de abajo por la URL de tu fork)
```bash
git clone https://github.com/Dataket/unblind.git

cd unblind
```

3. Crea un ambiente de trabajo con Python-env
```bash
python -m venv venv
```
y actívalo con

```bash
# IOS
source venv/bin/activate
```
o con conda de la siguiente manera
```bash
conda create -n unblind-env
```

y actívalo con:
```bash
conda activate unblind-env
```

4. Instala las librerías requeridas: 
```bash
pip install -r requirements.txt
```

5. Y ahora puedes testear todas estas funcionalidades en un notebook, script o lo que quieras necesites.

# Ejemplo de uso 🔎

Vamos a aprender cómo hacer una visualización para el Sistema 2 de la PDN:

1. Importamos la librería y definimos los caminos:
```python
# Se importa el módulo unblind
from unblind import utils, etl, dataviz

# Se define el path de trabajo
working_path = '/working_path/'
root_path = working_path+'data/'
pdn_system = 's2'
```

2. Descargamos los archivos de los sistemas de la PDN:
```python
# Se descargan los sistemas de la PDN
utils.get_datasets(to_path=root_path)
```

3. Extraemos y tratamos los datos que nos interesan:
```python
# Se definen las palabras clave que nos interesa tomar del Sistema 2
keywords = ['Procedimiento']

# Se define el objeto de extracción de datos y se realiza la extracción de datos
extraction = etl.FeatureEngineering(pdn_system=pdn_system, root_path=root_path, keywords=keywords, metadata_columns=[])
extraction.extractData('extracted_data')

# Posteriormente se realiza la normalización de la tabla para evitar traer listas o diccionarios dentro de la extracción
extraction.normalizeData('extracted_data', 'normalized')

# Se sustituyen los valores missings por un cero
extraction.missingData(0, 'normalized_data', 'missing_data')

# Se guarda la tabla
extraction.tables['missing_data'].to_csv(root_path+system+'/ut_ug_m_data.csv', index=False) # El nombre es por Un-Tokenized + Un-Grouped + Missing-treated data
```

4. Creamos la visualización:
```python
# Una vez que ya tenemos guardado el csv tratado, podemos definir la clase de visualizaciones
dataviz = dataviz.DataViz(pdn_system=pdn_system, root_path=root_path)

# Realizamos nuestra primer gráfica
file_path = 'ut_ug_m' # Es el nombre del archivo que guardamos, en al convensión que usamos pero sin el sufijo '_data.csv'
dataviz.createGraph(group_data=[True], file_path=file_path, variables=['tipoProcedimiento_1_clave'])

# Mostramos la gráfica
plt.show()
```

# Quieres contribuir 🤔
Nosotros somos Dataket y nos puedes contactar por medio de los siguientes correos:
- david.pedroza.segoviano@gmail.com
- missaelgabo@gmail.com
- ge.rodriguezrivera@ugto.mx

''')
