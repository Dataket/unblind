# Unblind + Streamlit = Visualización de datos en tiempo real, ¡sin programar! 😎
En esta página web se podrán obtener gráficos dinámicos de su interés, y obtener archivos en excel con la información que se necesite en cuestión de minutos.

# Requerimientos para el paquete 📦
- Python 3.8.x (estable, por ejemplo: Python 3.8.10)
- python-env

# Estructura de carpetas 📁
A continuación ser verá la estructura de carpetas utilizada en nuestro proyecto así como las descripciones de cada uno de los archivos.

```
.
.
├── data
│   └── process_data
├── pages
│   ├── 1_👀_Quienes_somos.py
│   ├── 2_🐍_Unblind_Python_package.py
│   ├── 3_💸_Sistema_1_-_Declaraciones.py
│   ├── 4_🏗️_Sistema_2_-_Contrataciones.py
│   └── 5_🚓_Sistema_3_-_Sancionados.py
├── 1_❤️‍🔥_Unblind.py
├── README.md
└── requirements.txt
```

- data: Carpeta que guarda todos los datos que son utilizados para los análisis y graficas.
	- process_data: Los datos de la __PDN__ procesados por nuestro módulo **unblind**. 
- pages: Carpeta donde se albergan todas las páginas hechas con streamlit.
- 1_❤️‍🔥_Unblind.py: script de Python que contiene la vista principal de nuestro proyecto.


# Setup 🛠
Para poder correr el código del paquete y ser capaz de hacer cambios en él, se necesitará seguir los siguientes pasos.

1. [¡Haz fork al repositorio!](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/about-forks)

2. Clona tu repositorio y accede a la rama correcta(sustituye la URL de abajo por la URL de tu fork)
```bash
git clone https://github.com/Dataket/unblind.git

cd unblind

git checkout streamlit
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

5. Para correr la página localmente en tu computadora debese de hacer:
```bash
streamlit run 1_❤️‍🔥_Unblind.py
```

# Quieres contribuir 🤔
Nosotros somos Dataket y nos puedes contactar por medio de los siguientes correos:
- david.pedroza.segoviano@gmail.com
