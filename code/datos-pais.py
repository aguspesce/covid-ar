#!/usr/bin/env python
# coding: utf-8

# # Graficas sobre la evolucion del COVID-19 en Argentina

# In[1]:


from pathlib import Path
import os

import numpy as np
import pandas as pd

import plotly.express as px


# In[2]:


# Path para guardar las graficas
plots_dir =  Path(os.path.realpath(__file__)).absolute().parent.parent / "web" / "plots"

# Direccion a los datos
URL = "https://docs.google.com/spreadsheets/d/16-bnsDdmmgtSxdWbVMboIHo5FRuz76DBxsz_BbsEVWA/export?format=csv&id=16-bnsDdmmgtSxdWbVMboIHo5FRuz76DBxsz_BbsEVWA&gid=0"

RENAME_COLUMNS = {
    "nue_casosconf_diff": "casos_diarios",
    "nue_fallecidos_diff": "fallecidos_diarios",
}
PROVINCIAS = [
    'CABA', 'Indeterminado', 'Buenos Aires', 'San Luis', 'Chaco',
    'Río Negro', 'Santa Fe', 'Tierra del Fuego', 'Córdoba', 'Jujuy',
    'Salta', 'Entre Ríos', 'Santa Cruz', 'Tucumán', 'Corrientes',
    'Neuquén', 'Santiago del Estero', 'Mendoza', 'La Pampa',
    'Misiones', 'San Juan', 'La Rioja', 'Chubut', 'Formosa',
    'Catamarca'
]

def fetch_covid_data_argentina(province=None):
    """
    Fetch data de números de infectados de COVID
    
    Parameters
    ----------
    province : str or None (optional)
        Provincia de la cual quiero los datos. Si es None, devuelve
        datos de toda la Argentina.
        
    Returns
    -------
    df : pandas.DataFrame
    """
    df = pd.read_csv(URL, parse_dates=["fecha"], dayfirst=True)
    if province is None:
        df = df.groupby("fecha").sum()
    else:
        df = df.loc[df.osm_admin_level_4 == province]
        df = df.set_index("fecha")
    df = df[list(RENAME_COLUMNS.keys())]
    df = df.rename(columns=RENAME_COLUMNS)
    return df


# In[3]:


datos_arg = fetch_covid_data_argentina()
datos_arg.head()


# ## Datos diarios
# 
# Hago un promedio con una ventana de 7 dias

# In[4]:


datos_arg_mean = datos_arg.rolling(window=pd.to_timedelta(7, unit="D")).mean()


# In[29]:


# Nuevos casos
fig = px.line(
    datos_arg_mean, 
    y="casos_diarios", 
    title="Nuevos casos diarios en Argentina", 
    height=500, 
    width=700,
    labels=dict(casos_diarios="Número de casos", fecha="Fecha", color=""), 
    color=px.Constant("Casos promediados a 7 dias")
)

fig.add_bar(
    x=datos_arg.index,
    y=datos_arg.casos_diarios, 
    name="Nuevos casos",
)

fig.update_layout(
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    )
)

fig.update_xaxes(
    dtick="M1",
    #tickformat="%b\n%Y",
)

fig.write_html((plots_dir / "casos_diarios.html").as_posix())
fig.show()


# In[25]:


fig = px.line(
    datos_arg_mean, 
    y="fallecidos_diarios", 
    title="Muertes diarias en Argentina", 
    height=500, 
    width=700,
    labels=dict(fallecidos_diarios="Número de fallecidos", fecha="Fecha", color=""),
    color=px.Constant("Casos promediados a 7 dias")
)

fig.add_bar(
    x=datos_arg.index,
    y=datos_arg.fallecidos_diarios, 
    name="Casos diarios"      
)

fig.update_xaxes(
    dtick="M1",
    #tickformat="%b\n%Y",
)

fig.update_layout(
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    )
)

fig.write_html((plots_dir / "fallecidos_diarios.html").as_posix())
fig.show()


# ## Total acumulados diarios

# In[21]:


# Total de casos diarios
fig = px.line(
    y=datos_arg.casos_diarios.cumsum(), 
    x=datos_arg.index,
    title="Cantidad de casos nuevos acumulados", 
    height=500, 
    width=700,
    labels=dict(y="Número de casos", x="Fecha"),
)
fig.update_xaxes(
    dtick="M1",
    #tickformat="%b\n%Y",
    
)
fig.update_layout(showlegend=False, )
fig.write_html((plots_dir / "casos_acumulados.html").as_posix())
fig.show()


# In[22]:


# Total de Fallecido diarios
fig = px.line(
    y=datos_arg.fallecidos_diarios.cumsum(), 
    x=datos_arg.index,
    title="Cantidad acumulada de fallecidos", 
    height=500, 
    width=700,
    labels=dict(y="Número de fallecidos", x="Fecha"),
)
fig.update_xaxes(
    dtick="M1",
    #tickformat="%b\n%Y",
    
)
fig.update_layout(showlegend=False, )
fig.write_html((plots_dir / "fallecidos_acumulados.html").as_posix())
fig.show()


# In[ ]:




