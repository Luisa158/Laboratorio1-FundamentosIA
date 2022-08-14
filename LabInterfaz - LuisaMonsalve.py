# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 18:14:55 2022

@author: user
"""

### paquetes de impotacion y manejo de datos
import pandas as pd
import numpy as np

### paquetes de graficos
import matplotlib.pyplot as plot
from scipy import stats

#####   paquetes de interfaz grafica
from tkinter import *
import tkinter as tk
from tkinter import ttk


def IdentificarAtipicos(df, ft, valorAlfa):
    q1 = df[ft].quantile(0.25)
    q3 = df[ft].quantile(0.75)
    iqr = q3 - q1
    
    bigote_inferior = q1 - valorAlfa * iqr
    bigote_superior = q3 + valorAlfa * iqr
    
    ls = df.index[(df[ft]<bigote_inferior) | (df[ft] > bigote_superior)]
    return ls

def eliminar(df, index):
    index = sorted(set(index))
    df = df.drop(index)
    return df

def histo(df,col):
    plot.title( " - Histograma")
    plot.hist(df[col])
    plot.show()

def bigotes(df, col):
    plot.title(col + " - Diagrama de Caja")
    plot.boxplot(df[col])
    plot.show()

def norma(df, col):
    fig=plot.figure()
    ax=fig.add_subplot(111)
    res=stats.probplot(df[col],dist=stats.norm,plot=ax)
    plot.show()

def disper(df,col1,col2):
    plot.scatter((df[col1]), (df[col2]))
    plot.xlabel(col1)
    plot.ylabel(col2)
    plot.show()

def corre(df,col1,col2):
    plot.xcorr(df[col1], df[col2])
    plot.xlabel(col1)
    plot.ylabel(col2)
    plot.show()
    
    
def selec():
    
    graf = graficas.get()
    columna = colum.get()
    lista = datos

    tipo = tip.get()
    
    if(tipo=='Sin atipicos'):
        valor_alpha = float(num.get())
        if(valor_alpha<0):
            tk.messagebox.showinfo(message="El valor debe ser mayor que cero ", title="ALERTA!!")
            
        elif(valor_alpha>=0):
            index_list = []
            for i in aux:
                index_list.extend(IdentificarAtipicos(lista, i,valor_alpha))
            final_index_list = []
            for index in index_list:
                if index not in final_index_list:
                    final_index_list.append(index)
    
            lista = eliminar(lista,index_list)
            lista.columns=columnas
    else:
        lista = datos
        
    if (graf=='Histograma'):
        histo(lista, columna)
    elif (graf=='Cajas y Bigotes'):
        bigotes(lista, columna)
    elif (graf=='Normalización'):
        norma(lista, columna)
    elif (graf=='Dispersión'):
         columna2= colum2.get()
         disper(lista, columna, columna2)
    elif (graf=='Correlación'):
        columna2= colum2.get()
        corre(lista, columna, columna2)
    else:
        tk.messagebox.showinfo(message="Faltar seleccionar algo ", title="ALERTA!!")

    graf.set("")
    columna.set("")
    colum2.set("")
    colum2["state"]="disable"

def validacion(event):
    if graficas.get() == 'Dispersión':
        colum2["state"]="readonly"
        
    elif graficas.get() == 'Correlación':
        colum2["state"]="readonly"
    
    else:
        colum2["state"]="disabled" 
        
def validacion_2(event):
    if tip.get() == "Sin atipicos":
        num['state'] = "normal"
    else:
        num['state'] = "disabled"

    
    
archivo='abalone.csv'
 
datos=pd.read_csv(archivo)
columnas=['sex', 'length',
'Diameter',
'Height',
'Whole weight',
'Shucked weight',
'Viscera weight',
'Shell weight',
'Rings' ]
datos.columns=columnas

tipo =['Con atipicos', 'Sin atipicos']
graf =['Histograma', 'Cajas y Bigotes','Normalización', 'Dispersión','Correlación']
 
aux = ['length',
'Diameter',
'Height',
'Whole weight',
'Shucked weight',
'Viscera weight',
'Shell weight',
'Rings' ]

index_list = []
for i in aux:
    index_list.extend(IdentificarAtipicos(datos, i,1.5))
final_index_list = []
for index in index_list:
    if index not in final_index_list:
        final_index_list.append(index)

new_df = eliminar(datos,index_list)
new_df.columns=columnas


# Creating tkinter window
window = tk.Tk()
window.geometry('520x480')
# Label

num = tk.Entry(window,bg="White",fg="black",state="disabled")
num.grid(padx=10, pady=10, row=1, column=4)



#GRAFICAS
ttk.Label(window, text = "Grafica: ", 
        font = ("Times New Roman", 10)).grid(column = 0, 
        row = 15, padx = 10, pady = 25)
  
n = tk.StringVar()
graficas = ttk.Combobox(window, width = 27, textvariable = n)
# Adding combobox drop down list
graficas['values'] = graf
  
graficas.grid(column = 1, row = 15)
graficas['state'] = "readonly"
graficas.set("")
graficas.bind("<<ComboboxSelected>>", validacion)
#COLUMNAS
ttk.Label(window, text = "Columna: ", 
        font = ("Times New Roman", 10)).grid(column = 0, 
        row = 25, padx = 15, pady = 28)
    
  
n = tk.StringVar()
colum = ttk.Combobox(window, width = 27, textvariable = n)

colum['values'] = aux
colum['state'] = "readonly"

colum.grid(column = 1, row = 25)
colum.set(2)
#COLUMNA 2
ttk.Label(window, text = "Columna 2: ", 
        font = ("Times New Roman", 10)).grid(column = 0, 
        row = 27, padx = 18, pady = 30)
n = tk.StringVar()
colum2 = ttk.Combobox(window, width = 27, textvariable = n)

colum2['values'] = aux
colum2['state'] = "disabled"

colum2.grid(column = 1, row = 27)
colum2.set("")

#TIPO
ttk.Label(window, text = "Con o sin Atipicos: ", 
        font = ("Times New Roman", 10)).grid(column = 0, 
        row = 32, padx = 30, pady = 40)
n = tk.StringVar()
tip = ttk.Combobox(window, width = 27, textvariable = n)
# Adding combobox drop down list
tip['values'] = tipo
tip['state'] = "readonly"
tip.grid(column = 1, row = 32)
tip.bind("<<ComboboxSelected>>", validacion_2)



button = ttk.Button(window,text='Graficar!',command= selec)
button.grid()
window.mainloop()





