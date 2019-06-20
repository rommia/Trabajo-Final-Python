#!/usr/bin/env python
# -*- coding: utf-8 -*-
import PySimpleGUI as sg
from TrabajoFinal import Layouts
import json
from pattern.web import Wiktionary
from pattern.es import conjugate, attributive, parse, split, INFINITIVE, NEUTRAL

def guardarArchivo (dic):
    """Abre el archivo de configuracion en modo escritura y lo guarda."""
    archivoPalabras = open('archivoDeConfiguracion.json', 'w', encoding="utf8")
    json.dump(dic, archivoPalabras)
    archivoPalabras.close()

def modificarPalabra(dicPalabras, palabraActual):
    """Abre una interfaz en la que permite modificar
    la palabra seleccionada, que es enviada por parametro. Si es modificada
    se elimina la palabra anterior y se inserta la nueva palabra."""
    
    palabraModificada = sg.PopupGetText('Modificar nombre: ', default_text = palabraActual)
    if (palabraModificada != palabraActual):
        if (ingresarPalabra(dicPalabras, palabraModificada)):
            eliminarPalabra(dicPalabras, palabraActual)
        return True
    return False    
def eliminarPalabra(dicPalabras, palabra):
    """Verifica la clasificacion de la palabra
    y la remueve de la lista correspondiente."""
    
    if (palabra in list(dicPalabras['NN'].keys())):
        del dicPalabras['NN'][palabra]
    elif (palabra in list(dicPalabras['JJ'].keys())):
        del dicPalabras['JJ'][palabra]
    elif (palabra in list(dicPalabras['VB'].keys())):
        del dicPalabras['VB'][palabra]
            
def esPalabraValida (palabra):
    """Verifica que la palabra sea valida dentro de Wiktionary."""
    if (Wiktionary().search(palabra) == None):
        return False
    else:
        return True
def GenerarReporte(texto):
    """Abre el archivo de reporte y escribe un texto enviado por parametro.
    si el archivo no existe, se crea en modo escritura."""
    
    try:
        archivoReporte = open('ArchivoReporte.txt', 'a')
    except FileNotFoundError:
        archivoReporte = open('ArchivoReporte.txt', 'w')
    
    archivoReporte.write(texto + "\n")
    archivoReporte.close()
    
def ingresarPalabra(dicPalabras, text):
    """Verifica que la palabra sea v�lida tanto en Wiktionary como en Pattern.
     la palabra existe, la clasifica en verbo/sustantivo/adjetivo y la agrega a la lista de palabras.
    Caso contrario, genera el reporte con una descripcion del error.
    Retorna verdadero o falso dependiendo si la palabra se inserto correctamente o no."""
    try:
        clasificacion = parse(text).split('/')[1][0:2]
        
        if esPalabraValida(text):                        
                if (clasificacion == 'VB'):      
                    enInfinitivo = conjugate(text, INFINITIVE)
                    articulo = Wiktionary(language='es').search(enInfinitivo)
                elif (clasificacion == 'JJ'):
                    adjetivo = attributive(text, gender=NEUTRAL)
                    articulo = Wiktionary(language='es').search(adjetivo)
                elif (clasificacion == 'NN'):
                    articulo = Wiktionary(language='es').search(text)
                aux = str(articulo.sections)
                if 'ADJ' in aux.upper() and clasificacion == 'JJ':
                    print('La palabra es un adjetivo') 
                elif 'VERB' in aux.upper() and clasificacion == 'VB':
                    print('La palabra es un verbo')
                elif 'SUST' in aux.upper() and clasificacion == 'NN':
                    print('La palabra es un sustantivo')
                
                if (clasificacion != 'JJ' and clasificacion != 'NN' and clasificacion != 'VB'):
                    GenerarReporte('La palabra ' + text + ' no existe en pattern.')
                    
                dicPalabras[clasificacion][text] = buscarDefinicion(text)
                return True
        else:
            if (clasificacion == 'JJ' or clasificacion == 'NN' or clasificacion == 'VB'):
                GenerarReporte('La palabra ' + text + ' no fue encontrada en Wiktionary pero si en pattern siendo un ' + clasificacion + '. Se ha agregado esta situacion en un reporte llamado ArchivoReporte.txt.')
                dicPalabras[clasificacion][text] = sg.PopupGetText('Definicion: ')
                return True
            else:
                GenerarReporte('La palabra ' + text + ' no fue encontrada en Wiktionary y tampoco en pattern.')
                sg.Popup('La palabra ingresada no es valida. Se ha agregado esta situacion en un reporte llamado ArchivoReporte.txt.')
    except:
            GenerarReporte('La palabra ' + text + ' no es valida.')
            sg.Popup('La palabra ingresada no es valida. Se ha agregado esta situacion en un reporte ArchivoReporte.txt.')
        
    
    return False
    
def clasificarPalabra(palabra):
    """Clasifica la palabra segun sea verbo/sustantivo/adjetivo/etc."""
    return parse(palabra).split('/')[1][0:2]    

def buscarDefinicion(palabra):
    """Recibe por parametro una palabra, busca su definicion en Wiktionary y retorna un string con dicha definicion."""    
    try:
        articulo = Wiktionary(language="es").search(palabra)
        for elemento in articulo.sections:
            if "Etimolog" in elemento.title:
                if "Si puedes," in elemento.content:
                    definicion = palabra.title()
                else:
                    definicion = elemento.content.split("[editar]")[1].split("\n\n")[1]
                    if "[" in elemento.content.split("[editar]")[1].split("\n\n")[1]:
                        definicion = definicion.split("[")[0]
                break
            else:
                definicion = palabra.title()
    except:
        definicion = palabra.title()
        
    return definicion

def __init__(dicConfig): 
    listaPalabras = list(dicConfig['clases']['VB'].keys()) + list(dicConfig['clases']['JJ'].keys()) + list(dicConfig['clases']['NN'].keys())           
    windowConfig = sg.Window('Configuracion').Layout(Layouts.Configuracion(sg, listaPalabras, dicConfig))
        
    while True:            
        e, v = windowConfig.Read()
            
        if e is None:
            break
        if e == 'volver':
            windowConfig.Hide()
            break
        elif e == 'cargar':
            try:
                if (ingresarPalabra(dicConfig['clases'], v['palabra'])):
                    listaPalabras.append(v['palabra'])                    
                    windowConfig.FindElement('palabra').Update('')
                    windowConfig.FindElement('lista').Update(values=listaPalabras)
                    guardarArchivo(dicConfig)
            except IndexError:
                sg.Popup('No escribiste ninguna palabra.')
        elif e == 'fonts':
            dicConfig['font'] = v['fonts'][0]
        elif e == 'modificar':
            try:
                if (modificarPalabra(dicConfig['clases'], v['lista'][0])):
                    listaPalabras = list(dicConfig['clases']['VB'].keys()) + list(dicConfig['clases']['JJ'].keys()) + list(dicConfig['clases']['NN'].keys())
                    windowConfig.FindElement('lista').Update(values=listaPalabras)
                    guardarArchivo(dicConfig)
            except IndexError:
                sg.Popup('Debes seleccionar una palabra.')
        elif e == 'eliminar':
            try:
                eliminarPalabra(dicConfig['clases'], v['lista'][0])
                listaPalabras.remove(v['lista'][0])
                windowConfig.FindElement('lista').Update(values=listaPalabras)
                guardarArchivo(dicConfig)
            except IndexError:
                sg.Popup('Debes seleccionar una palabra.')
        elif e == 'guardar':
            if v['horizontal']:
                dicConfig['orientacion'] = 'horizontal'
            else:
                dicConfig['orientacion'] = 'vertical'
                    
            dicConfig['ayuda']['activa'] = v['si']
            
            if (dicConfig['ayuda']['activa']):
                try:
                    dicConfig['ayuda']['tipo'] = v['listaAyuda'][0]
                except:
                    sg.Popup('Seleccione el tipo de ayuda que desea otorgarle al jugador.')
                    
            dicConfig['minusculas'] = v['minusculas']
            dicConfig['oficina'] = windowConfig.FindElement('oficinaEligida').Get()
            guardarArchivo(dicConfig)