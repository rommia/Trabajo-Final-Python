#!/usr/bin/env python
# -*- coding: utf-8 -*-
import PySimpleGUI as sg
from TrabajoFinal import Jugar, Configuracion, Layouts
import json, sys

windowInicio = sg.Window('Bienvenido').Layout(Layouts.Inicio(sg))


while True:
    event, values = windowInicio.Read()
    
    try:
        archivoConfig = open('archivoDeConfiguracion.json', 'r', encoding="utf8")
        dicConfig = json.load(archivoConfig)
        archivoConfig.close()
    except FileNotFoundError:
        dicConfig = {"clases": {"JJ":{}, "VB": {}, "NN": {}}, "orientacion": "horizontal", "ayuda": {'activa':False, 'tipo':'palabras'}, "minusculas": False, "font": 'Helvetica', 'oficina':0}

    if event is None or event == 'salir':    
        sys.exit()
    elif event == 'jugar':
        Jugar.__init__(dicConfig)
    elif event == 'configuracion':
        Configuracion.__init__(dicConfig)