#!/usr/bin/env python
# -*- coding: utf-8 -*-
import PySimpleGUI as sg
from TrabajoFinal import Layouts
from TrabajoFinal.Configuracion import clasificarPalabra
import random, sys, string, json 


BOX_SIZE = 25

def DefinirRango(clave, diccionario, configUsuario):
    """Verifica la cantidad de palabras a encontrar ingresada por el usuario y verifica que no supere el maximo.
    Retorna la cantidad de palabras a encontrar en la grilla."""
    if int(configUsuario[clave]['cantidad']) > len(list(diccionario['clases'][clave].keys())):
        return len(diccionario['clases'][clave])
    else:
        return int(configUsuario[clave]['cantidad'])

def LlenarLista(diccionario, configUsuario):
    """Recibe por parametro el diccionario que contiene el total de palabras y la configuracion de palabras del usuario.
    Segun la cantidad elegida por el usuario, escoge palabras al azar en el diccionario de palabras y conforma una lista.
    Retorna dicha lista de palabras."""
    copia = dict(diccionario.copy())
    listaDePalabrasRandom = []
        
    for clave in diccionario['clases'].keys():
        for i in range(0,DefinirRango(clave, diccionario, configUsuario)):
            aux = random.choice(list(copia['clases'][clave].keys()))
            listaDePalabrasRandom.append(aux)
            del copia['clases'][clave][aux]
            
    return listaDePalabrasRandom

def definirTamanio(configUsuario, diccionario, palabraMasLarga):
    """"Recibe como parametro el diccionario de configuracion y la palabra mas larga, y retorna una tupla que define el tamaño de la interfaz de la grilla."""
    for clase in list(configUsuario.keys()):
        configUsuario[clase]['cantidad'] = DefinirRango(clase, diccionario, configUsuario)
        
        doblePalabras = (configUsuario['NN']['cantidad'] + configUsuario['JJ']['cantidad'] + configUsuario['VB']['cantidad']) * 2
        X, Y = doblePalabras * (BOX_SIZE + 1), palabraMasLarga * (BOX_SIZE + 1)
    
    if (diccionario['orientacion'] == 'horizontal'):
            X, Y = Y, X
            
    return (X, Y)

def DibujarGrilla(g, diccionario, coordenadas, dicSeleccion, configUsuario):
    """Calcula el largo de la palabra m�s extensa y la cantidad de palabras.
    Se determina el ancho y el largo de la grilla seg�n la cantidad palabras, la palabra m�s extensa y configuraci�n de la sopa de letras (horizontal/vertical)
    Dibuja todos los casilleros de la grilla. luego escribe sobre cada fila o columna las palabras a encontrar y rellena los recuadros faltantes con letras al azar.
    Va completando un diccionario que asocia cada casillero con un elemento del mismo, seg�n su coordenada, con los siguientes atributos:
    letra = guarda la letra del casillero.
    color = define el color del casillero.
    habilitado = guarda un booleano que define si un casillero est� habilitado para seleccionarse o no.
    seleccionado = guarda un booleano que define si un casillero est� seleccionado o no."""
    orientacion = diccionario['orientacion']
    minus = diccionario['minusculas']
    cantidadTotal = configUsuario['NN']['cantidad'] + configUsuario['JJ']['cantidad'] + configUsuario['VB']['cantidad']
    
    listaDePalabrasRandom = LlenarLista(diccionario, configUsuario)
    palabraMasLarga = len(max(listaDePalabrasRandom, key=len))
    
    for filas in range(palabraMasLarga):
        for columnas in range(cantidadTotal*2):
            if orientacion == 'horizontal':
                x = filas
                y = columnas
            else:
                x = columnas 
                y = filas
            coordenadas[(x, y)] = {'letra': '', 'color': '', 'casillero' : g.DrawRectangle((x * BOX_SIZE + 5, y * BOX_SIZE + 3), (x * BOX_SIZE + BOX_SIZE + 5, y * BOX_SIZE + BOX_SIZE + 3), line_color='black'), 'habilitado':True, 'seleccionado':False }
            
    posiblesFilas = list(range(0,cantidadTotal*2))
    for elemento in listaDePalabrasRandom:
                        
        filaRandom = int(random.choice(posiblesFilas)) 
        r = int(random.randrange((1+(palabraMasLarga)-len(elemento))))

        for pos in range(0,r): 
            if orientacion == 'vertical':
                x = filaRandom
                y = pos
            else:
                x = pos
                y = filaRandom
            if minus:
                letraRandom = random.choice(string.ascii_lowercase)
            else:
                letraRandom =random.choice(string.ascii_uppercase)
            g.DrawText('{}'.format(letraRandom), (x * BOX_SIZE + 13, (y * BOX_SIZE + 20)), font=diccionario['font'])
            coordenadas[(x, y)]['letra'] = letraRandom            
        
        listaTuplas = []
        for letra in range(0,len(elemento)):
            if orientacion == 'vertical':
                x = filaRandom
                y = (r + letra)
            else:
                x = (r + letra)
                y = filaRandom
            if minus:    
                g.DrawText((elemento[letra].lower()), (x * BOX_SIZE + 13, (y * BOX_SIZE + 20)), font=diccionario['font'])
            else:
                g.DrawText((elemento[letra].upper()), (x * BOX_SIZE + 13, (y * BOX_SIZE + 20)), font=diccionario['font'])
            coordenadas[(x, y)]['letra'] = elemento[letra]
            listaTuplas.append((x, y))
        
        dicSeleccion[clasificarPalabra(elemento)]['palabras'].append(listaTuplas)

        for pos in range((r+len(elemento)), (palabraMasLarga)):
            if orientacion == 'vertical':
                x = filaRandom
                y = pos
            else:
                x = pos
                y = filaRandom
            if minus:
                letraRandom = random.choice(string.ascii_lowercase)
            else:
                letraRandom = random.choice(string.ascii_uppercase)
            g.DrawText('{}'.format(letraRandom), (x * BOX_SIZE + 13, (y * BOX_SIZE + 20)), font=diccionario['font'])
            coordenadas[(x, y)]['letra'] = letraRandom
                  
        posiblesFilas.remove(filaRandom)
        
    for fila in range(0,palabraMasLarga):
        for pos in posiblesFilas:
            if orientacion == 'vertical':
                x = pos
                y = fila
            else:
                x = fila
                y = pos
            if minus:
                letraRandom = random.choice(string.ascii_lowercase)
            else:
                letraRandom = random.choice(string.ascii_uppercase)
            g.DrawText('{}'.format(letraRandom), (x * BOX_SIZE + 13, (y * BOX_SIZE + 20)), font=diccionario['font'])                
            coordenadas[(x, y)]['letra'] = letraRandom
            
def cuadradoHabilitado(coordenadas, tuplaClave):
    """Retorna un booleano que indica si el casillero est� habilitado para seleccionarse o no."""
    return (coordenadas[tuplaClave]['habilitado'])

def Seleccionar(coordenadas, tuplaClave):
    """Verifica si un casillero est� seleccionado o no, para realizar la acci�n contraria.
    Retorna un booleano que indica su nuevo valor."""
    if (not coordenadas[tuplaClave]['seleccionado']):
        coordenadas[tuplaClave]['seleccionado'] = True
        return True
    
    coordenadas[tuplaClave]['seleccionado'] = False
    return False

def verificarPalabras(coordenadas, dicSeleccion):
    """Recibe el diccionario que contiene todos los casilleros con sus respectivos atributos, junto al diccionario que contiene una lista de listas de casilleros que conforman las palabras a encontrar.
    Verifica si los casilleros se encuentran seleccionados y con el color correspondiente, en caso de ser as� deshabilita todos los casilleros correspondientes y elimina la palabra de la lista de palabras a encontrar."""
    listaEliminacion = []
    for clases in dicSeleccion.keys():
        for lista in dicSeleccion[clases]['palabras']:
            listaTuplas = []
            for tuplas in lista:
               if (coordenadas[tuplas]['seleccionado']) and (coordenadas[tuplas]['color'] == dicSeleccion[clases]['color']):
                   listaTuplas.append(tuplas)
            if (lista == listaTuplas):
                listaEliminacion.append(listaTuplas)
                auxStr = ''
                for letra in listaTuplas:
                    coordenadas[letra]['habilitado'] = False
                    auxStr = auxStr + coordenadas[letra]['letra']
                    
    if (len(listaEliminacion) != 0):
        for clases in dicSeleccion.keys():
            for indice in listaEliminacion:
                if (indice in dicSeleccion[clases]['palabras']):
                    dicSeleccion[clases]['palabras'].remove(indice)
                
def ganarJuego(dicSeleccion):
    """Recibe como parametro el diccionario que contiene la lista de palabras a encontrar y corrobora la cantidad de palabras faltantes.
    Retorna la cantidad de palabras que a�n no se han encontrado en la sopa de letras."""
    palabrasFaltantes = 0
    for clases in dicSeleccion.keys():
        for lista in dicSeleccion[clases]['palabras']:
            palabrasFaltantes = palabrasFaltantes + 1
    
    return palabrasFaltantes

def definirColor(cantUbicaciones):
    """Recibe como parametro la cantidad total de oficinas y calcula el promedio de temperaturas de una oficina al azar.
    Retorna el color de la interfaz dependiendo de la temperatura promedio."""
    try:
        ubicacion = random.choice(range(0, cantUbicaciones))
        archivoTemperaturas = open('temperatura_' + str(ubicacion) + '.json', 'r')
        lista_temperaturas = json.load(archivoTemperaturas)
        
        cantTotal = 0
        cantTemperatura = 0
        for dic in lista_temperaturas:
            cantTemperatura = cantTemperatura + dic['temperatura']
            cantTotal = cantTotal + 1
        
        if ((cantTemperatura / cantTotal) < 15):
            return 'blue'
        else:
            return 'red'
    except:
        return 'blue'
            

def __init__(diccionario):
    try:
        listaDefiniciones = list(diccionario['clases']['NN'].values()) + list(diccionario['clases']['VB'].keys()) + list(diccionario['clases']['JJ'].keys())
        windowJugar = sg.Window('Sopa de letras').Layout(Layouts.Jugar(sg, diccionario['clases'])).Finalize() 
            
        while True:
            eventos, val = windowJugar.Read()

            if (eventos is None):
                break
            elif eventos == 'fuera':
                windowJugar.Hide()
                break
            elif eventos == 'jugando':
                ayudaActiva = (diccionario['ayuda']['tipo'] != 'Sin ayuda')
                tipoAyuda = diccionario['ayuda']['tipo']
                palabras = list(diccionario['clases']['VB'].keys()) + list(diccionario['clases']['JJ'].keys()) + list(diccionario['clases']['NN'].keys())
                    
                if (len(palabras) != 0):
                    cantidadDeFilas = len(palabras)*2
                    palabraMasLarga = len(max(palabras, key=len))
                    configUsuario = {'NN':{'cantidad': int(windowJugar.FindElement('cantSustantivos').Get()), 'color': windowJugar.FindElement('auxSustantivos').Get()}, 'JJ':{'cantidad': int(windowJugar.FindElement('cantAdjetivos').Get()), 'color': windowJugar.FindElement('auxAdjetivos').Get()}, 'VB':{'cantidad': int(windowJugar.FindElement('cantVerbos').Get()), 'color' : windowJugar.FindElement('auxVerbos').Get()}}
                    
                    tuplaTamanio = definirTamanio(configUsuario, diccionario, palabraMasLarga)
                    
                    if (configUsuario['NN']['cantidad'] == 0 and configUsuario['JJ']['cantidad'] == 0 and configUsuario['VB']['cantidad'] == 0):
                        sg.Popup('Debe existir al menos una palabra para buscar en la sopa de letras.')
                    else:
                        colorInterfaz = definirColor(diccionario['oficina'])
                        reporte = open('ArchivoReporte.txt', 'r')
                        conflictos = reporte.read()
                        conflictos = conflictos.split('\n')
                        windowJugando = sg.Window('Sopa de letras', background_color=colorInterfaz, size=(tuplaTamanio[0] + 330, tuplaTamanio[1] + 100),).Layout(Layouts.Jugando(sg, configUsuario, tuplaTamanio, conflictos, colorInterfaz)).Finalize() 
                        
                        g = windowJugando.FindElement('_GRAPH_')
                        coordenadas = {}
                        dicSeleccion = {'NN':{'color': windowJugando.FindElement('NN').BackgroundColor, 'palabras':[]}, 'VB':{'color': windowJugando.FindElement('VB').BackgroundColor, 'palabras':[]}, 'JJ':{'color': windowJugando.FindElement('JJ').BackgroundColor, 'palabras':[]}}
                        DibujarGrilla(g, diccionario, coordenadas, dicSeleccion, configUsuario)

                        while True:
                            e, v = windowJugando.Read() 
                            if e is None or e == 'out':
                                sys.exit()
                                break
                            elif e == 'cancelar':
                                windowJugar.Hide()
                                windowJugando.Hide()
                                break
                            elif e == 'NN' or e == 'VB' or e == 'JJ':
                                colorSel = e
        
                            mouse = v['_GRAPH_']
                                
                            if e == '_GRAPH_':
                                if mouse == (None, None):
                                    continue
                                
                                try:
                                    box_x = mouse[0]//BOX_SIZE
                                    box_y = mouse[1]//BOX_SIZE
                                    tuplaClave = (box_x, box_y)
                                        
                                    if (cuadradoHabilitado(coordenadas, tuplaClave)):
                                        if (Seleccionar(coordenadas, tuplaClave)):   
                                            g.TKCanvas.itemconfig(coordenadas[tuplaClave]['casillero'], fill = dicSeleccion[colorSel]['color']) #pinta el cuadrado
                                            coordenadas[tuplaClave]['color'] = dicSeleccion[colorSel]['color']
                                        else:
                                            g.TKCanvas.itemconfig(coordenadas[tuplaClave]['casillero'], fill = g.BackgroundColor)
                                            coordenadas[tuplaClave]['color'] = g.BackgroundColor
                                except NameError:
                                    sg.Popup('Debés seleccionar un color.')
                                except KeyError:
                                    sg.Popup('Debés seleccionar casilleros dentro de la grilla de sopa de letras.')
                                            
                            elif e == 'verificar':
                                verificarPalabras(coordenadas, dicSeleccion)
                                palabrasFaltantes = ganarJuego(dicSeleccion)
                                
                                if (palabrasFaltantes == 0):
                                    sg.Popup('Felicitaciones', 'Completaste la sopa de letras correctamente.')
                                    sys.exit()
                                else:
                                    sg.Popup('¡Casi!', 'Aún no completaste toda la sopa de letras, falta adivinar ' + str(palabrasFaltantes) + ' palabras.')
                            
                            elif e == 'ayuda':
                                if (ayudaActiva):
                                    if (tipoAyuda == 'Definiciones'):
                                        strAyuda = '\n'.join(listaDefiniciones)
                                        sg.Popup('Definiciones de las palabras: \n' + strAyuda)
                                    else:
                                        strAyuda = '\n'.join(palabras)
                                        sg.Popup('Palabras en la sopa de letras: \n' + strAyuda)
                                else:
                                    sg.Popup('Ayuda','Lo sentimos, la ayuda se encuentra deshabilitada... pero te damos una pista:\nDebés encontrar en total ' + str(configUsuario['NN']['cantidad']) + ' sustantivos, ' + str(configUsuario['VB']['cantidad']) + ' verbos y '+ str(configUsuario['JJ']['cantidad']) + ' adjetivos. \n¡Suerte!')
                else:
                    sg.Popup('No hay ninguna palabra en la sopa de letras, configurala desde el boton "Configuración"')                
    except (FileNotFoundError):
            sg.Popup('No se ha configurado la sopa de letras. Por favor, hágalo clickeando el boton "Configuración"')