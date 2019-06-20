# -*- coding: utf-8 -*-
import time
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT
import os
import json
import time
import RPi.GPIO as GPIO
import Adafruit_DHT

"""
A0  --> pin 7
VCC --> pin 2
GND --> pin 6
D0  --> pin 15 (BCM22)
"""

class Matriz:
    def __init__(self, numero_matrices=2, orientacion=0, rotacion=0, ancho=16, alto=8):
        self.font = [CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT]
        self.serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(self.serial, width=ancho, height=alto, cascaded=numero_matrices, rotate=rotacion)

    def mostrar_mensaje(self, msg, delay=0.1, font=1):
        show_message(self.device, msg, fill="white",
                     font=proportional(self.font[font]),
                     scroll_delay=delay)

    def dibujar(self, msg):
        with canvas(self.device) as draw:
            text(draw, (0, 0), chr(msg), fill="white")
            self.device.contrast(10 * 16)

class Temperatura:

 def __init__(self, pin=17, sensor=Adafruit_DHT.DHT11):
                # Usamos el DHT11 que es compatible con el DHT12
                self._sensor = sensor
                self._data_pin = pin
def datos_sensor(self):
                """ Devuelve un diccionario con la temperatura y humedad y fecha"""
                humedad, temperatura = Adafruit_DHT.read_retry(self._sensor, self._data_pin)
                return {'temperatura': temperatura, 'humedad': humedad, "fecha": time.asctime(time.localtime(time.time()))}
class Sonido:

    def __init__(self, canal=22):
        self._canal = canal
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._canal, GPIO.IN)
        # Desactivo las warnings por tener más de un circuito en la GPIO
        GPIO.setwarnings(False)
        GPIO.add_event_detect(self._canal, GPIO.RISING)

    def evento_detectado(self, funcion):
        if GPIO.event_detected(self._canal):
            funcion()
            
def leer_temp():
    info_temperatura = temperatura.datos_sensor()
    info_temperatura.update({"fecha": time.asctime(time.localtime(time.time()))})
    return info_temperatura

def imprimirdatos():
    tem=Temperatura()
    dict=tem.datos_sensor()
    text=('Temperatura = {0:0.1f}°C  Humedad = {1:0.1f}%'.format(datos['temperatura'], datos['humedad']))
    matri=Matriz()
    matri.mostrar_mensaje( text, delay=1, font=3)


def guardar_temp(dict,ubicacion):
    info=()
    for key, value in dict():
        temp = [key, value]
        info.append(temp)
        
    with open(os.path.join("archivos_texto", ubicacion + ".json"), "r") as log_file:
        try:
            lista_de_temperaturas = json.load(log_file)
        except Exception:
            lista_de_temperaturas = []
            
    lista_de_temperaturas.append(info)
    with open(os.path.join("archivos_texto", ubicacion + ".json"), "w") as log_file:
        json.dump(lista_de_temperaturas, log_file, indent=4)

 if __name__ == "__main__":
            ubi=input("ingrese la ubicacion donde se encuentra:")
            son=Sonido()
            temp = Temperatura()
            mat= Matriz()
            while True:
                son.evento_detectado(imprimirdatos())
                time.spleet(0.1)
                diction=temp.datos_sensor()
                guardar_temp(diction, ubi)
                time.sleep(60)