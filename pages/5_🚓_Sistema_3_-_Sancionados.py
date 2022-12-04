import streamlit as st
import unblind.dataviz as dv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import py7zr

st.markdown('''
# 🚓 Sistema 3: Sansionados
-----
''')

# Select a type
subsystem = st.selectbox('Selecciona el subsistema a utilizar', ['s3s', 's3p'])

s3 = pd.read_csv('data/process_data/'+subsystem+'/ut_ug_m_data.csv')

if st.checkbox('Mostrar datos completos 🤔'):
    st.write(s3)

st.markdown('## 📊 Gráficos')

# Source: https://seaborn.pydata.org/generated/seaborn.set_theme.html
sns.set_theme(context='talk', style='darkgrid', palette='colorblind')

# Parameters
root_path = 'data/process_data/'
pdn_system = subsystem

file_path, list_of_variables = dv.give_viable_features(root_path=root_path,
                                                    system=pdn_system,
                                                    aggregated_data=True,
                                                    thresh=5)

def remove_variable_if_contains(variables, string, exact=False):
    if exact:
        return [x for x in variables if string != x]
    else:
        return [x for x in variables if string not in x]

if subsystem == 's3s':
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string='id', exact = True)
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string='unique_id', exact = True)
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string='curp')
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string='rfc')
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string='observaciones', exact = True)
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string="causaMotivoHechos", exact = True)
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string="fechaCaptura", exact = True)
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string="expediente", exact = True)
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string="descripcion")
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string="autoridadSancionadora", exact = True)
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string="resolucion_url", exact = True)
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string='documentos')
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string='moneda')
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string='nombre')
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string='fecha')
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string='Apellido')
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string="institucionDependencia")

else:
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string='autoridad')
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string='id', exact = True)
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string='unique_id', exact = True)
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string='causaMotivoHechos', exact = True)
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string='expediente', exact = True)
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string='observaciones', exact = True)
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string="particularSancionado_nombreRazonSocial", exact = True)
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string="responsableSancion_nombres", exact = True)
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string='fecha')
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string="institucionDependencia")

#st.write(list_of_variables)
# Sort list of variables
if subsystem == 's3s':
    list_of_variables.sort()

st.write('### 👀 Gráficas para una variable')

st.write('Primero, tenemos una gráfica de pastel 🎂 para ver la distribución de los datos de una variable (ya que se están _agrupando_ las opciones).')

left_column, right_column = st.columns(2)

with left_column:
    variable = st.selectbox('Seleccione una variable para la gráfica de pastel', list_of_variables)

with right_column:
    fig = plt.figure(figsize=(10, 8))
    dv.graph_features(root_path=root_path, system=pdn_system,
                group_data=[True], file_path='ut_ug_m', variables=[variable])
    st.write(fig)

if subsystem == 's3s':

    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string='Responsabilidad')
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string='Area')
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string='estado_declarante')
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string='valor')
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string='Responsabilidad')
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string='servidorPublico')
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string='multa_monto', exact = True)
    list_of_variables = remove_variable_if_contains(variables=list_of_variables, string="tipoSancion_1__id", exact = True)

    st.write('### 😎 Gráficas para dos variables')

    st.write('Podemos crear un scatter plot 📈 para ver la relación entre dos variables. (esto sin agrupar, para ver valores únicos')

    left_column, right_column = st.columns(2)

    with left_column:
        variable_x = st.selectbox('Seleccione una variable para el eje x', list_of_variables)
        # Remove variable from list
        temp_list = list_of_variables.copy()
        temp_list.remove(variable_x)
        variable_y = st.selectbox('Seleccione una variable para el eje y', temp_list)

    with right_column:
        fig = plt.figure(figsize=(10, 8))
        dv.graph_features(root_path=root_path, system=pdn_system,
                    group_data=[False, False], file_path='ut_ug_m', variables=[variable_x, variable_y])
        st.write(fig)
