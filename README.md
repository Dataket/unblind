# Unblind
Protecto para el Datatón anticorrupción 2022 ✨.

# Descripción 📄
Librería en Python 🐍 que ayuda en el tratamiento de datos, creación de visualizaciones, y desarrollo de modelos predictivos, para los datos de la Plataforma Digital Nacional. También se creó una página web dinámica con ayuda de [streamlit](https://streamlit.io/) (Véase la rama de [streamlit](https://github.com/Dataket/unblind/tree/streamlit)).

# Requerimientos para el paquete 📦
- python 3.8+
- python-env

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


# Setup 🛠
Para poder correr el código del paquete y ser capaz de hacer cambios en él, se necesitará seguir los siguientes pasos.

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

# Quieres contribuir 🤔
Nosotros somos Dataket y nos puedes contactar por medio de los siguientes correos:
- david.pedroza.segoviano@gmail.com