from Modulo1 import cargar_procesos, admitir_nuevos
import os

"""Se busca la ruta del archivo 'procesos_ejemplo.csv' en la misma carpeta que este script."""
carpeta = os.path.dirname(os.path.abspath(__file__)) 
ruta = os.path.join(carpeta, "procesos_ejemplo.txt") # Aca solo cambien la extension del archivo a (.txt o .csv) segun el archivo que tengan en la carpeta.

procesos, errores = cargar_procesos(ruta)
cola_nuevos = []

clock = int(input("Ingrese el instante de clock: ")) # Aca va a tener que estar sincrozado con el modulo que se encarga de aumentar el clock.


admitidos = admitir_nuevos(procesos, cola_nuevos, clock)

"""Imprime los procesos admitidos en ese instante de clock."""
print(f"Admitidos en clock {clock}:")
for p in admitidos:
    print(p)

if errores:
    print(f"\n Se generaron los siguientes errores al cargar el archivo:")
    for error in errores:
        print(f"\n {error}")