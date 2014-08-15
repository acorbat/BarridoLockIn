# importaciones
from lantz.drivers import stanford
from lantz import ureg
from time import sleep
import pylab

from numpy import array
import numpy as np

from lantz import Action, Feat, DictFeat, ureg

# Corregimos una de las funciones del driver de comunicación
class X(stanford.SR830GPIB):
    @Action()
    def measure(self, channels):
        d = {'x': '1', 'y': '2', 'r': '3', 't': '4',
             '1': '5', '2': '6', '3': '7', '4': '8',
             'f': '9', '': 10, '': 11}
        channels = ','.join(d[ch] for ch in channels)
        valores = self.query('SNAP? {}'.format(channels))
        valores = valores.split(',')
        valores = [float(x) for x in valores]
        return valores

#stanford.SR830GPIB('GPIB0::8::INSTR')
lockin = X('GPIB0::8::INSTR')

# Caracteristicas del barrido
inicioBarrido = 200
finalBarrido = 260
paso = 10


# Barrido en frecuencias
frecuencias = np.arange(inicioBarrido, finalBarrido, paso)

# seteo del LockIn
tiempoIntegracion = 0.3
# tiempoIntegracion = lockin.sensitivity 
# la segunda deberia utilizar la sensibilidad seteada pero no estoy seguro si pregunta a cada momento o guarda el valor solicitado la primera vez

frecuencia = []
r = []
theta = []

lockin.initialize() #inicializamos la comunicación
for frecuencia in frecuencias:
    lockin.frequency = frecuencia * ureg.hertz # seteamos la frecuencia
    sleep(tiempoIntegracion*1.5) # le damos un tiempo al lockin para estabilizarse
    valores = lockin.measure('rt') # medimos r y theta del lockin.
    
    r.append(valores[1])
    theta.append(valores[2])
    
lockin.finalize() # finalizamos la comunicación
# print(Tabla) # Esto deberia ser un return, save y/o plot

pylab.plot(array(frecuencias), array(r))
pylab.show()