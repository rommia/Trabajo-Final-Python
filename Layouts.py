#!/usr/bin/env python
# -*- coding: utf-8 -*-

def Inicio(sg):
    
    inicio = [[sg.Frame('Inicio', layout=[
    [sg.Txt('Bienvenido al juego interactivo...')],
    [sg.ReadButton('Jugar', size = (20,2), key = 'jugar')],
    [sg.ReadButton('Configuracion', size = (20,2), key = 'configuracion')],
    [sg.ReadButton('Salir', size = (20,2), key = 'salir')],
    [sg.Txt('                  ')]])]]
    
    return inicio

def Configuracion(sg, listaPalabras, diccionario):
    columna1 = [[sg.Frame('Ingreso de datos', layout = [
    [sg.Txt('Ingrese las palabras a encontrar en la sopa de letras') ],
    [sg.InputText(key='palabra'), sg.ReadButton('Cargar', key='cargar')],
    [sg.Listbox(values=listaPalabras, size= (15,3), key='lista'), sg.ReadButton('Modificar', key='modificar'), sg.ReadButton('Eliminar', key='eliminar')]])],
    [sg.Frame('Orientación de las palabras', layout=[
        [sg.Radio(group_id = 0, text='Horizontal', key='horizontal', default = diccionario['orientacion'] =='horizontal' )],
        [sg.Radio(group_id = 0, text='Vertical', key='vertical',default = diccionario['orientacion']=='vertical')]]),sg.Frame('Formato', layout=[
        [sg.Radio(group_id = 1, text='Minúsculas', key='minusculas', default =  diccionario['minusculas'])],
        [sg.Radio(group_id = 1, text='Mayúsculas', key='mayusculas', default = not diccionario['minusculas'])]])],
    [sg.Frame('Seleccione el tipo de ayuda que desea brindarle al jugador:', layout=[[sg.Listbox(values=['Sin ayuda', 'Palabras', 'Definiciones'], default_values=('Sin ayuda'), key='listaAyuda', size=(11,3))]])]]
    
    columna2 = [[sg.Frame('Look and feel', layout= [[sg.Txt('Oficina Número: '), sg.Listbox(values=['1','2','3','4','5'], default_values=('1'), key='ofi', size=(11,3))]])],
                [sg.Frame('Seleccione el formato de la grilla:', layout = [
            [sg.Listbox(values=(['Arial','Helvetica', 'Courier', 'Verdana', 'Comic']), enable_events=True, key='fonts', size = (20,5))]])],
                [sg.Text('          ')],
                [sg.Text('           ')],
                [sg.Text('           ')],
                [sg.ReadButton('Guardar', key='guardar'), sg.ReadButton('Volver', key='volver')]]
    
    configuracion = [[sg.Column(columna1), sg.Column(columna2)]]
    
    return configuracion

    
    
    

def Jugar(sg, diccionario):
    canS = 'La cantidad máxima de sustantivos posibles es:'+ str(len(list(diccionario['NN'].keys())))
    canA = 'La cantidad máxima de adjetivos posibles es:'+ str(len(list(diccionario['JJ'].keys())))
    canV = 'La cantidad máxima de verbos posibles es:'+ str(len(list(diccionario['VB'].keys())))
    wjugar = [[sg.Text('Sopa de letras'), sg.Text('', key='_OUTPUT_')],
              [sg.Frame('Defina los colores', layout= [
        [sg.Txt('Sustantivos'), sg.ColorChooserButton('Seleccionar', target=(0,2), key='ColorSustantivos'), sg.InputText('#ffff80', key='auxSustantivos', visible=False)],
        [sg.Txt('Verbos'), sg.ColorChooserButton('Seleccionar', target=(1,2), key='ColorVerbos'), sg.Input('#00ffff',key='auxVerbos', visible=False)],
        [sg.Txt('Adjetivos'), sg.ColorChooserButton('Seleccionar', target=(2,2), key='ColorAdjetivos'), sg.Input('#c0c0c0', key= 'auxAdjetivos', visible=False)]]), sg.Frame('Cantidad de palabras a encontrar', layout= [
        [sg.Txt('Sustantivos'), sg.InputText(str(len(list(diccionario['NN'].keys()))), key='cantSustantivos', size = (10,1)), sg.Txt(canS)], 
        [sg.Txt('Verbos'), sg.InputText(str(len(list(diccionario['VB'].keys()))), key='cantVerbos', size = (10,1)), sg.Txt(canV)],
        [sg.Txt('Adjetivos'), sg.InputText(str(len(list(diccionario['JJ'].keys()))), key='cantAdjetivos', size = (10,1)), sg.Txt(canA)]])],
        [sg.Txt('')],
        [sg.ReadButton('Jugar', key = 'jugando'), sg.ReadButton('Salir', key='fuera')]]
    
    return wjugar

def Jugando (sg, conf, tuplaTamanio, conflictos, colorInterfaz):
    columna = [[sg.Text('Conflictos en el ingreso de palabras:')],
                [sg.Listbox(values=conflictos, size= (30,5))], 
                [sg.ReadButton('Verificar',key='verificar'), sg.ReadButton('Ayuda', key='ayuda')]]
    windowJugando = [[sg.Text('Primero debés seleccionar el color del tipo de palabra que vas a marcar')],
              [sg.Text('Verbos'), sg.Text('', enable_events=True, click_submits=True, size=(5,1), background_color = conf['VB']['color'], key='VB'), sg.Text('Sustantivos'), sg.Text('', enable_events=True, size=(5,1), background_color = conf['NN']['color'], key='NN'),sg.Text('Adjetivos'), sg.Text('', enable_events=True, size=(5,1), key='JJ', background_color = conf['JJ']['color'])],
              [sg.Graph((tuplaTamanio), (0,tuplaTamanio[1]), (tuplaTamanio[0],0), key='_GRAPH_', change_submits=True, drag_submits=False, background_color='white'), sg.Column(columna, background_color=colorInterfaz)],
              [sg.ReadButton('Salir', key='out')]]
    return windowJugando