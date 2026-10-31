"""
Módulo 1: Validación, carga y orden de procesos.

Formato esperado del archivo (.txt o .csv), separado por comas:
    #id, TA, TI, TAM
    1, 0, 5, 150
    2, 0, 6, 15

- Las líneas vacías y las que empiezan con '#' se ignoran.
- Cada proceso válido se guarda como diccionario:
    {"id": int, "TA": int, "TI": int, "TAM": int}
"""

import os

EXTENSIONES_VALIDAS = (".txt", ".csv")
MAX_PROCESOS = 10
TAM_MAX_USUARIO = 450  # K disponibles para trabajos de usuario

"""Chequea extensión y existencia."
   Devuelve (bool, mensaje). """
def validar_extension(ruta):
    
    if not ruta.lower().endswith(EXTENSIONES_VALIDAS):
        return False, "El archivo debe tener extensión .txt o .csv"
    if not os.path.isfile(ruta):
        return False, f"El archivo '{ruta}' no existe"
    return True, ""


"""Valida los campos de una línea ya separada.
    
    Devuelve (bool, mensaje_error). """
def validar_linea(campos, ids_vistos):

    if len(campos) != 4:
        return False, f"se esperaban 4 campos {{#id, TA, TI, TAM}} y hay {len(campos)}"
    else:
        if any(campo == "" for campo in campos):
            return False, "hay campos vacíos"

        try:
            id_proc, ta, ti, tam = (int(c) for c in campos)
        except ValueError:
            return False, "todos los campos deben ser números enteros"

        if id_proc in ids_vistos:
            return False, f"el id {id_proc} está repetido"
        if ta < 0:
            return False, "TA no puede ser negativo"
        if ti <= 0:
            return False, "TI debe ser mayor que 0"
        if tam <= 0:
            return False, "TAM debe ser mayor que 0"
        if tam > TAM_MAX_USUARIO:
            return False, f"TAM ({tam}K) supera los {TAM_MAX_USUARIO}K de memoria de usuario"

        return True, ""

"""
    Lee el archivo y devuelve (procesos_validos, errores).
    (errores) es una lista de strings indica el numero de linea y el motivo del error.
    """
def leer_archivo(ruta):
    
    procesos = []
    errores = []
    ids_vistos = set()

    with open(ruta, "r") as archivo:
         for numero, linea in enumerate(archivo, start=1):
            linea = linea.strip()
            if linea == "" or linea.startswith("#"):
                continue

            campos = [c.strip() for c in linea.split(",")]
            es_valida, mensaje = validar_linea(campos, ids_vistos)

            if not es_valida:
                errores.append(f"Línea {numero}: {mensaje} -> '{linea}'")
                continue

            id_proc, ta, ti, tam = (int(c) for c in campos)
            ids_vistos.add(id_proc)
            procesos.append({"id": id_proc, "TA": ta, "TI": ti, "TAM": tam})

            if len(procesos) == MAX_PROCESOS:
                break  # ya hay 10 procesos validos

    return procesos, errores

"""Ordena por TA (menor a mayor)."""
def obtener_ta(proc):
    return proc["TA"]

def ordenar_procesos(procesos):
    return sorted(procesos, key=obtener_ta)


def cargar_procesos(ruta):
    """
    Función principal del módulo.
    Devuelve (procesos, errores):
      - (proceso) es una lista ordenada por TA, con máximo MAX_PROCESOS elementos
      - (errores) es una lista de mensajes (líneas rechazadas, exceso de procesos, etc.)
    Si el archivo no es válido, devuelve ([], [mensaje]).
    """
    es_valida, mensaje = validar_extension(ruta)
    if not es_valida:
        return [], [mensaje]

    procesos, errores = leer_archivo(ruta)
    procesos = ordenar_procesos(procesos)

    if not procesos:
        errores.append("No se cargó ningún proceso válido")

    return procesos, errores


def admitir_nuevos(procesos, cola_nuevos, clock):
    """
    Pasa de la lista 'procesos' a 'cola_nuevos' todo proceso con TA <= clock.
    Agrega 'tiempo_rest' (= TI)  en la lista nuevo, para no modificar TI original.
    Devuelve la lista de procesos admitidos en ese clock.
    """
    admitidos = []
    while procesos and procesos[0]["TA"] <= clock:
        proc= procesos.pop(0)
        nuevo = {"id": proc["id"], "TA": proc["TA"], "TI": proc["TI"], "TAM": proc["TAM"], "tiempo_rest": proc["TI"],}
        cola_nuevos.append(nuevo)
        admitidos.append(nuevo)
    return admitidos


if __name__ == "__main__":
    # Prueba aislada: python Modulo1.py
    import sys

    ruta_archivo = sys.argv[1] if len(sys.argv) > 1 else "procesos_ejemplo.csv"
    lista_procesos, lista_errores = cargar_procesos(ruta_archivo)

    for error in lista_errores:
        print("[AVISO]", error)

    print("\nProcesos cargados:")
    for p in lista_procesos:
        print(p)

    cola_nuevos = []
    clock = 0
    while lista_procesos:
        for p in admitir_nuevos(lista_procesos, cola_nuevos, clock):
            print(f"clock={clock}: llegó el proceso {p['id']}")
        clock += 1