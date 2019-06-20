from numpy.distutils.misc_util import default_text
def Inicio(sg):
    
    inicio = [[sg.Frame('Inicio', layout=[
    [sg.Txt('Bienvenido al juego interactivo...')],
    [sg.ReadButton('Jugar', size = (20,2), key = 'jugar')],
    [sg.ReadButton('Configuracion', size = (20,2), key = 'configuracion')],
    [sg.ReadButton('Salir', size = (20,2), key = 'salir')],
    [sg.Txt('                  ')]])]]
    
    return inicio

def Configuracion(sg, listaPalabras, diccionario):
    configuracion = [[sg.Frame('Ingreso de datos', layout = [
    [sg.Txt('Ingrese las palabras a encontrar en la sopa de letras') ],
    [sg.InputText(key='palabra'), sg.ReadButton('Cargar', key='cargar')],
    [sg.Listbox(values=listaPalabras, size= (15,3), key='lista'), sg.ReadButton('Modificar', key='modificar'), sg.ReadButton('Eliminar', key='eliminar')]]), sg.Frame('Seleccione el formato de la grilla:', layout = [
            [sg.Listbox(values=(['Arial','Helvetica', 'Courier', 'Verdana', 'Comic']), enable_events=True, key='fonts', size = (20,5))]])],
    [sg.Frame('Orientacion de las palabras', layout=[
        [sg.Radio(group_id = 0, text='Horizontal', key='horizontal', default = diccionario['orientacion'] =='horizontal' )],
        [sg.Radio(group_id = 0, text='Vertical', key='vertical',default = diccionario['orientacion']=='vertical')]]),sg.Frame('Formato', layout=[
        [sg.Radio(group_id = 1, text='Minusculas', key='minusculas', default =  diccionario['minusculas'])],
        [sg.Radio(group_id = 1, text='Mayusculas', key='mayusculas', default = not diccionario['minusculas'])]]), sg.Txt('Oficina Numero: '), sg.InputText(default_text = diccionario['oficina'], key='oficinaEligida')],
        [sg.Frame('Seleccione si desea brindarle ayuda al jugador:', layout=[[sg.Listbox(values=['palabras', 'definiciones'], key='listaAyuda', size=(11,2))], [sg.Radio(group_id=2, text='Si', key='si', default = diccionario['ayuda']['activa'])], [sg.Radio(group_id =2, text='No', key='no', default = not diccionario['ayuda']['activa'])]])],
        [sg.ReadButton('Guardar', key='guardar'), sg.ReadButton('Volver', key='volver')]]
    
    return configuracion
    

def Jugar(sg, diccionario):
    canS = 'La cantidad maxima de sustantivos posibles es:'+ str(len(list(diccionario['NN'].keys())))
    canA = 'La cantidad maxima de adjetivos posibles es:'+ str(len(list(diccionario['JJ'].keys())))
    canV = 'La cantidad maxima de verbos posibles es:'+ str(len(list(diccionario['VB'].keys())))
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

def Jugando (sg, cantFilas, mayor, diccionario, conf, ayuda, tuplaTamanio):
    
    windowJugando = [[sg.Text('Primero debes seleccionar el color de la palabra que vas a marcar')],
              [sg.Text('Verbos'), sg.Text('', enable_events=True, click_submits=True, size=(5,1), background_color = conf['VB']['color'], key='VB'), sg.Text('Sustantivos'), sg.Text('', enable_events=True, size=(5,1), background_color = conf['NN']['color'], key='NN'),sg.Text('Adjetivos'), sg.Text('', enable_events=True, size=(5,1), key='JJ', background_color = conf['JJ']['color'])],
              [sg.Graph((tuplaTamanio), (0,tuplaTamanio[1]), (tuplaTamanio[0],0), key='_GRAPH_', change_submits=True, drag_submits=False, background_color='white'), sg.ReadButton('Verificar',key='verificar'), sg.ReadButton('Ayuda', key='ayuda') ],
              [sg.ReadButton('Salir', key='out')]]
    return windowJugando