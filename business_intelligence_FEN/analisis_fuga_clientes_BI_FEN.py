import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

#config de la app
st.set_page_config(layout='wide')

#Agora tem que conseguir puxar o banco lá do Drive com a PyDrive e depois copiar as células que plotam os gráficos
#Read dataset
df_fuga = pd.read_excel('https://github.com/EnzoGolfetti/praticas_python/blob/main/business_intelligence_FEN/BASEFUGA-1.xlsx?raw=true', 
                    sheet_name= 'BASE GENERAL', thousands='.')
df_fuga.columns = df_fuga.columns.str.lower().str.strip()


#Título del sitio e introducción
st.title('App de soporte para análisis de Fuga de clientes')

st.subheader('Business Intelligence FEN Otoño/22')
st.subheader('Esta APP es una solución interactiva para complementar la análisis del PDF del proyecto.')

st.write('Acá están disponibilizados de forma interactiva los gráficos contenidos en la análisis por PDF.')
st.write("""Hay también gráficos no exibidos en la análisis más sucinta, pero que están a disposición 
            para mayores exploraciones y para responder preguntas futuras que pueden surgir en la lectura
            del proyecto.
        """)

#Una mirada y recuerdo del dataset
st.header('Un recuerdo supe el diseño de los datos')

st.write('Disposición de las observaciones:')
st.dataframe(df_fuga.head())

#describe
#Describe dividido
df_fuga_describe_cat = df_fuga.describe(include='all')
df_fuga_describe_cat = df_fuga_describe_cat.loc[:, [ 'genero', 'niv_educ', 'e_civil', 'ciudad', 'seguro', 'fuga' ]]

idx = pd.IndexSlice
slice_genero = idx[idx['top'], idx['genero']]
slice_educ = idx[idx['top'], idx['niv_educ']]
slice_seguro = idx[idx['top'], idx['seguro']]
slice_ciudad = idx[idx['top'], idx['ciudad']]
slice_edad = idx[idx['mean'], idx['edad']]

st.write('Principales estadísticas descritivas de las variables categóricas:')
st.dataframe(df_fuga_describe_cat.style.set_properties(**{'background-color': '#A619D4'}, subset=slice_genero)\
                                  .set_properties(**{'background-color': '#A619D4'}, subset=slice_educ)\
                                  .set_properties(**{'background-color': '#A619D4'}, subset=slice_ciudad)\
                                  .set_properties(**{'background-color': '#A619D4'}, subset=slice_seguro))

st.header('Gráficos de la análisis univariada')

#Mirando la columna de Edad
df_edad_aux = df_fuga['edad'].value_counts().to_frame().reset_index(drop=False).rename(columns={'index':'edad','edad':'count'}).astype({'edad':'int64'})
df_edad_aux['coluna_auxiliar_color'] = 'color'
fig = px.bar(df_edad_aux, x='edad', y='count', title='Distribución de clientes por edad', text_auto=True,
             labels=dict(edad='Edad',count='Cantidad de Clientes'), color='coluna_auxiliar_color', color_discrete_sequence=['#7328EB'])
fig.update_layout(width=1200,
                  height=500,
                  margin=dict(l=1,r=20,t=32,b=1), 
                  paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#FFFFFF',  showlegend=False, 
                  title_x=0.5, title_font_family='Open Sans', font_family='Open Sans', font_size=15
                  )
fig.update_yaxes(gridcolor='#CCCCCC')
st.plotly_chart(fig)

#Mirando la columna de género
df_genero_aux = df_fuga.copy()
df_genero_aux['genero'] = df_genero_aux['genero'].str.replace('F','Femenino').str.replace('M','Masculino')
df_genero_aux = df_genero_aux.groupby(['genero']).count()
df_genero_aux['coluna_auxiliar_color'] = 'color'
fig_2 = px.bar(df_genero_aux, x=df_genero_aux.index, y='id', title='Distribución de clientes por género', text_auto=True,
             labels=dict(genero='Género', id='Cantidad de Clientes'), color='coluna_auxiliar_color', color_discrete_sequence=['#00266C'])
fig_2.update_layout(width=1200, 
                    height=500,
                    margin=dict(l=1,r=20,t=32,b=1), 
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#FFFFFF', showlegend=False,
                    title_x=0.5, title_font_family='Open Sans', font_family='Open Sans', font_size=15
                    )
fig_2.update_yaxes(gridcolor='#CCCCCC')
st.plotly_chart(fig_2)


#Mirando la columna de educación
df_educacion_aux = df_fuga.copy()
df_educacion_aux['niv_educ'] = df_educacion_aux['niv_educ'].str.replace('BAS','Basica').str.replace('MED','Média').str.replace('TEC','Técnica').str.replace('UNV','Universitaria')
df_educacion_aux = df_educacion_aux.groupby(['niv_educ']).count()
df_educacion_aux['coluna_auxiliar_color'] = 'color'
fig_3 = px.bar(df_educacion_aux, x=df_educacion_aux.index, y='id', title='Distribución de clientes por nivel educacional', text_auto=True,
             labels=dict(niv_educ='Nivel Educacional', id='Cantidad de Clientes'), color='coluna_auxiliar_color', color_discrete_sequence=['#1B19D4'])
fig_3.update_layout(width=1200,
                    height=500,
                    margin=dict(l=1,r=20,t=32,b=1), 
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#FFFFFF', showlegend=False, 
                    title_x=0.5, title_font_family='Open Sans', font_family='Open Sans', font_size=15
                    )
fig_3.add_annotation(xref='x', 
                    yref='y',
                    x=0,
                    y=20,
                    text="Valores no especificos",
                    font_family='Open Sans',
                    font_color='#00266C',
                    showarrow=True,
                    arrowhead=1,
                    arrowcolor='#00266C',
                    arrowwidth=2,
                    ax=30,
                    ay=-70
                    )
fig_3.update_yaxes(gridcolor='#CCCCCC')
st.plotly_chart(fig_3)

#Mirando Estado Civil
df_e_civil_aux = df_fuga.copy()
df_e_civil_aux['e_civil'] = df_e_civil_aux['e_civil'].str.replace('CAS','Casado').str.replace('SEP','Separado').str.replace('SOL','Soltero').str.replace('VIU','Viuvo')
df_e_civil_aux = df_e_civil_aux.groupby(['e_civil']).count()
df_e_civil_aux['coluna_auxiliar_color'] = 'color'
fig_4 = px.bar(df_e_civil_aux, x=df_e_civil_aux.index, y='id', title='Distribución de clientes por Estado Civil', text_auto=True,
             labels=dict(e_civil='Estado Civil', id='Cantidad de Clientes'), 
             color='coluna_auxiliar_color', color_discrete_sequence=['#7328EB'])
fig_4.update_layout(width=1200,
                    height=500, 
                    margin=dict(l=1,r=20,t=32,b=1), 
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='#FFFFFF', 
                    showlegend=False, 
                    title_x=0.5, title_font_family='Open Sans', font_family='Open Sans', font_size=15)
fig_4.update_yaxes(gridcolor='#CCCCCC')
st.plotly_chart(fig_4)

#Visualizando columns de renta
df_renta_aux = df_fuga.copy()
df_renta_aux['renta'] = df_renta_aux['renta'] / 100000
df_renta_aux['coluna_auxiliar_color'] = 'color'
fig_5 = px.histogram(df_renta_aux, x='renta', nbins=100, title='Distribución de la renta', 
                    labels=dict(renta='Renta (en millones de pesos chilenos)'), 
                   color='coluna_auxiliar_color', color_discrete_sequence=['#1B19D4'])
fig_5.update_layout(width=1200,
                    height=500, 
                    margin=dict(l=1,r=20,t=32,b=1), 
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='#FFFFFF', 
                    showlegend=False, 
                    title_x=0.5, title_font_family='Open Sans', font_family='Open Sans', font_size=15)
fig_5.update_xaxes(nticks=20)
fig_5.update_yaxes(gridcolor='#CCCCCC')
st.plotly_chart(fig_5)

st.write("""Abajo se puede interactivamente selecionar cuál de los meses de deudas 
            se desea mirar en detalles.
        """)
#Caja de selección
mes_deuda = st.selectbox('Seleccione el més de interés:',
                        ['Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre'])
mes_df = f'd_{mes_deuda.lower()}'
df_aux_deuda = df_fuga.copy()
df_aux_deuda['coluna_auxiliar_color'] = 'color'

fig_6 = px.histogram(df_aux_deuda, x=df_aux_deuda[mes_df], nbins=20, 
                    title=f'Distribución de la deuda del més de {mes_deuda}', 
                    #labels=dict(x='Deuda (en pesos chilenos)'), 
                    color='coluna_auxiliar_color', 
                    color_discrete_sequence=['#A61F08']
                    )
fig_6.update_layout(width=1200,
                    height=500, 
                    margin=dict(l=1,r=20,t=32,b=1), 
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='#FFFFFF', 
                    showlegend=False, 
                    title_x=0.5, title_font_family='Open Sans', font_family='Open Sans', font_size=15)
fig_6.update_xaxes(nticks=20, title_font_color='rgba(0,0,0,0)')
fig_6.update_yaxes(gridcolor='#CCCCCC')
st.plotly_chart(fig_6)

#Observando los meses en mora
df_mora = df_fuga['m_moroso'].value_counts().to_frame()
df_mora.index = df_mora.index.astype('int64').astype('str')
df_mora['coluna_auxiliar_color'] = 'color'
fig_7 = px.bar(df_mora, x=df_mora.index, y='m_moroso', 
                labels=dict(index='Meses en Mora', m_moroso='Count'),
                color='coluna_auxiliar_color', color_discrete_sequence=['#7328EB'])
fig_7.update_layout(height=500, 
                    width=1200, 
                    margin=dict(l=1,r=20,t=50,b=1), 
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#FFFFFF', showlegend=False, 
                    title_x=0.5, title_font_family='Open Sans', 
                    font_family='Open Sans', font_size=15, 
                    title_text='Distribución de clientes en Mora')
fig_7.update_xaxes(categoryorder='array', categoryarray=['0','1','2','3'])
fig_7.update_yaxes(gridcolor='#CCCCCC')
st.plotly_chart(fig_7)

#Mirando la distribución de monto preaprobado
df_monto = df_fuga.copy()
df_monto['monto'] = df_monto['monto']/1000000
df_monto['coluna_auxiliar_color'] = 'color'
fig_8 = px.histogram(df_monto, x='monto', nbins=100, 
                    labels=dict(monto='Monto preaprobado (en millones de pesos chilenos)', 
                                count='Count'),
                   color='coluna_auxiliar_color', color_discrete_sequence=['#1B19D4'])
fig_8.update_layout(height=500, 
                    width=1200, 
                    margin=dict(l=1,r=20,t=50,b=1), 
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='#FFFFFF', showlegend=False,
                    title_x=0.5, title_font_family='Open Sans', 
                    font_family='Open Sans', font_size=15, 
                    title_text='Distribución de montos preaprobados'
                    )
fig_8.update_yaxes(gridcolor='#CCCCCC')
st.plotly_chart(fig_8)

st.header('Gráficos de la análisis multivariada')

#tratamiento de edades negativas para no tener un grafico mal diseñado
df_fuga_plot_edad_renta = df_fuga.copy()
for i in df_fuga_plot_edad_renta.loc[:,'edad'].index:
  if df_fuga_plot_edad_renta.loc[i,'edad'] < 0:
    df_fuga_plot_edad_renta.loc[i,'edad'] = df_fuga_plot_edad_renta.loc[i,'edad']*-1

df_fuga_plot_edad_renta['coluna_auxiliar_color'] = 'color'
fig_9 = px.scatter(df_fuga_plot_edad_renta, x='edad', y='renta', labels=dict(edad='Edad', renta='Renta'),
                    color='coluna_auxiliar_color', color_discrete_sequence=['#F514BF'])
fig_9.update_layout(height=500, 
                    width=1200,
                    margin=dict(l=1,r=20,t=50,b=1), 
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#FFFFFF', showlegend=False, 
                    title_x=0.5, title_font_family='Open Sans', font_family='Open Sans', 
                    font_size=15, title_text='Dispersión de la renta por Edad')
fig_9.update_xaxes(nticks=15, gridcolor='#CCCCCC')
st.plotly_chart(fig_9)

#Boxplot de Fuga x Renta
color_discrete_map = {'NO FUGA':'#009900', 'FUGA':'#A61F08'}
fig_10 = px.box(df_fuga, x='fuga', y='renta', color='fuga', 
            color_discrete_map=color_discrete_map, labels=dict(fuga='Fuga', renta='Renta'))
fig_10.update_layout(height=500, 
                  width=1200,
                  margin=dict(l=1,r=20,t=50,b=2), 
                  paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#FFFFFF', showlegend=False,
                  title_x=0.5, title_font_family='Open Sans', font_family='Open Sans', font_size=15, 
                  title_text="Variable Objetivo 'Fuga' y dispersión por Renta")
fig_10.update_yaxes(gridcolor='#CCCCCC')
st.plotly_chart(fig_10)

#Nivel educacional y Fuga
df_educacion_aux = df_fuga.copy()
df_educacion_aux['niv_educ'] = df_educacion_aux['niv_educ'].str.replace('BAS','Basica').str.replace('MED','Média').str.replace('TEC','Técnica').str.replace('UNV','Universitaria')
color_discrete_map = {'NO FUGA':'#009900', 'FUGA':'#A61F08'}
fig_11 = px.bar(df_educacion_aux.groupby(['niv_educ','fuga']).size().unstack(), 
            labels=dict(niv_educ = 'Nivel Educacional', value = 'Count'), 
            color_discrete_map=color_discrete_map, opacity=.85,
            text_auto=True)
fig_11.add_shape(type='circle', xref='x', yref='y', x0=4.5, y0=1, x1=5.5, y1=1000, line_color='Black')
fig_11.update_layout(height=500, 
                  width=1200,
                  margin=dict(l=1,r=20,t=50,b=2), 
                  paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#FFFFFF', 
                  showlegend=False,
                  title_x=0.5, title_font_family='Open Sans', font_family='Open Sans', font_size=15, 
                  title_text="Fuga X No Fuga por Nivel Educacional")
fig_11.update_yaxes(gridcolor='#CCCCCC')
st.plotly_chart(fig_11)

#Mora y Fuga
df_mora_fuga = df_fuga.copy()
#Para ser posible hacer el grafico sacamos los Nulos
df_mora_fuga = df_mora_fuga.dropna(subset=['m_moroso'])
df_mora_fuga['m_moroso'] = df_mora_fuga['m_moroso'].astype('int64').astype('str')
color_discrete_map = {'NO FUGA':'#009900', 'FUGA':'#A61F08'}
fig_12 = px.bar(df_mora_fuga.groupby(['m_moroso','fuga']).size().unstack(), 
            labels=dict(m_moroso='Meses en mora', value='Count'), 
            text_auto=True, 
            color_discrete_map=color_discrete_map)
fig_12.update_layout(height=500, 
                    width=1200,
                    margin=dict(l=1,r=20,t=50,b=2), 
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#FFFFFF', 
                    showlegend=False,
                    title_x=0.5, title_font_family='Open Sans', font_family='Open Sans', font_size=15, 
                    title_text="Variable Objetivo 'Fuga' y Meses en mora"
                    )
fig_12.update_yaxes(gridcolor='#CCCCCC')
st.plotly_chart(fig_12)

#Ciudades y Fuga
color_discrete_map = {'NO FUGA':'#009900', 'FUGA':'#A61F08'}
df_apoio_ciudades = df_fuga.groupby(['ciudad','fuga']).size().unstack()[df_fuga.groupby(['ciudad','fuga']).size().unstack()['FUGA'].notna()==True]
fig_13 = px.bar(df_apoio_ciudades, 
                labels=dict(ciudad='Ciudades', value='Count'), 
                color_discrete_map=color_discrete_map
              )
fig_13.update_layout(height=500, 
                    width=1200,
                    margin=dict(l=1,r=20,t=50,b=2), 
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#FFFFFF', 
                    showlegend=False,
                    title_x=0.5, title_font_family='Open Sans', font_family='Open Sans', font_size=15, 
                    title_text="Variable Objetivo 'Fuga' y Ciudades")
fig_13.update_yaxes(gridcolor='#CCCCCC')
fig_13.update_xaxes(tickangle=-45)
st.plotly_chart(fig_13)

#Hacer el upload desta primera parte del sitio en GitHub y después Streamlit Nube



