#!/usr/bin/env python3
"""
Minimización de Autómatas Finitos Deterministas (AFD)
=====================================================

Este programa implementa el algoritmo de minimización de AFD usando el método
de tabla de distingibilidad. El objetivo es encontrar pares de estados equivalentes
que pueden ser combinados para minimizar el autómata.

Autor: [Jose Miguel Muñoz Rios]
Fecha: [05/08/2025]
"""

import sys
from typing import List, Tuple, Optional


def leer_archivo_entrada(nombre_archivo: str) -> List[str]:
    """
    Lee el archivo de entrada y retorna las líneas como lista.
    
    Args:
        nombre_archivo: Nombre del archivo a leer
        
    Returns:
        Lista de líneas del archivo
        
    Raises:
        FileNotFoundError: Si el archivo no existe
        IOError: Si hay problemas al leer el archivo
    """
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            return f.read().splitlines()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{nombre_archivo}'")
        print("Asegúrate de que el archivo 'input.txt' esté en el mismo directorio que este script.")
        sys.exit(1)
    except IOError as e:
        print(f"Error al leer el archivo '{nombre_archivo}': {e}")
        sys.exit(1)


def validar_entrada(estados: int, estados_finales: List[int], transiciones: List[List[int]]) -> bool:
    """
    Valida que los datos de entrada sean consistentes.
    
    Args:
        estados: Número total de estados
        estados_finales: Lista de estados finales
        transiciones: Matriz de transiciones
        
    Returns:
        True si la entrada es válida, False en caso contrario
    """
    # Validar número de estados
    if estados <= 0:
        print("Error: El número de estados debe ser positivo")
        return False
    
    # Validar estados finales
    for estado in estados_finales:
        if estado < 0 or estado >= estados:
            print(f"Error: Estado final {estado} fuera de rango [0, {estados-1}]")
            return False
    
    # Validar matriz de transiciones
    if len(transiciones) != estados:
        print(f"Error: Número de filas en transiciones ({len(transiciones)}) no coincide con estados ({estados})")
        return False
    
    for i, fila in enumerate(transiciones):
        for j, destino in enumerate(fila):
            if destino < 0 or destino >= estados:
                print(f"Error: Transición inválida en estado {i}, símbolo {j}: destino {destino} fuera de rango")
                return False
    
    return True


def crear_tabla_distinguibilidad(estados: int, estados_finales: List[int], 
                                transiciones: List[List[int]]) -> List[List[bool]]:
    """
    Crea la tabla de distinguibilidad usando el algoritmo de minimización de AFD.
    
    El algoritmo funciona de la siguiente manera:
    1. Inicializa la tabla marcando como distinguibles los pares donde uno es final y otro no
    2. Itera hasta que no haya más cambios, aplicando la regla de propagación:
       Si dos estados tienen transiciones que llevan a estados distinguibles, 
       entonces estos estados también son distinguibles.
    
    Args:
        estados: Número total de estados
        estados_finales: Lista de estados finales
        transiciones: Matriz donde transiciones[i][j] = estado destino desde i con símbolo j
        
    Returns:
        Matriz triangular donde tabla[i][j] = True indica que los estados i y j son distinguibles
    """
    # Inicializar tabla triangular (solo la mitad superior)
    tabla = [[False for _ in range(estados)] for _ in range(estados)]
    
    # Paso 1: Marcar como distinguibles los pares donde uno es final y otro no
    for i in range(estados):
        for j in range(i + 1, estados):
            # Si uno es final y otro no, son distinguibles
            if (i in estados_finales) != (j in estados_finales):
                tabla[i][j] = True
    
    # Paso 2: Aplicar algoritmo iterativo de propagación
    cambiado = True
    iteracion = 0
    while cambiado:
        cambiado = False
        iteracion += 1
        
        # Revisar todos los pares de estados
        for i in range(estados):
            for j in range(i + 1, estados):
                # Solo procesar pares que aún no están marcados como distinguibles
                if not tabla[i][j]:
                    # Verificar todas las transiciones posibles
                    for simbolo in range(len(transiciones[i])):
                        # Verificar que el símbolo existe en ambos estados
                        if simbolo >= len(transiciones[j]):
                            continue
                        
                        # Obtener estados destino para este símbolo
                        p = transiciones[i][simbolo]  # Destino desde estado i
                        q = transiciones[j][simbolo]  # Destino desde estado j
                        
                        # Asegurar que accedemos a la parte triangular de la tabla
                        if p > q:
                            p, q = q, p
                        
                        # Si los destinos son distinguibles, entonces i y j también lo son
                        if tabla[p][q]:
                            tabla[i][j] = True
                            cambiado = True
                            break
    
    return tabla


def encontrar_pares_equivalentes(estados: int, tabla: List[List[bool]]) -> List[Tuple[int, int]]:
    """
    Encuentra todos los pares de estados equivalentes basándose en la tabla de distinguibilidad.
    
    Args:
        estados: Número total de estados
        tabla: Tabla de distinguibilidad
        
    Returns:
        Lista de tuplas (i, j) donde i y j son estados equivalentes
    """
    pares_equivalentes = []
    
    # Recorrer la tabla triangular
    for i in range(estados):
        for j in range(i + 1, estados):
            # Si NO están marcados como distinguibles, son equivalentes
            if not tabla[i][j]:
                pares_equivalentes.append((i, j))
    
    return pares_equivalentes


def procesar_caso_prueba() -> Optional[List[Tuple[int, int]]]:
    """
    Procesa un caso de prueba completo.
    
    Returns:
        Lista de pares equivalentes, o None si hay error en la entrada
    """
    try:
        # Leer número de estados
        estados = int(input().strip())
        if estados <= 0:
            print("Error: El número de estados debe ser positivo")
            return None
        
        # Leer alfabeto (no se usa en el algoritmo pero es parte del formato)
        alfabeto = input().strip().split()
        
        # Leer estados finales
        linea_finales = input().strip()
        estados_finales = []
        if linea_finales:  # Si no está vacía
            estados_finales = list(map(int, linea_finales.split()))
        
        # Leer matriz de transiciones
        transiciones = []
        for _ in range(estados):
            fila = list(map(int, input().strip().split()))
            transiciones.append(fila)
        
        # Validar entrada
        if not validar_entrada(estados, estados_finales, transiciones):
            return None
        
        # Ejecutar algoritmo de minimización
        tabla = crear_tabla_distinguibilidad(estados, estados_finales, transiciones)
        pares_equivalentes = encontrar_pares_equivalentes(estados, tabla)
        
        return pares_equivalentes
        
    except ValueError as e:
        print(f"Error en formato de entrada: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None


def formatear_salida(pares_equivalentes: List[Tuple[int, int]]) -> str:
    """
    Formatea la salida de los pares equivalentes.
    
    Args:
        pares_equivalentes: Lista de pares equivalentes
        
    Returns:
        String formateado con los pares equivalentes
    """
    if not pares_equivalentes:
        return "None"
    
    # Ordenar pares para salida consistente
    pares_ordenados = sorted(pares_equivalentes)
    return " ".join(f"({i},{j})" for i, j in pares_ordenados)


def main():
    """
    Función principal que ejecuta el programa de minimización de AFD.
    
    Lee múltiples casos de prueba desde el archivo input.txt y procesa cada uno,
    mostrando los pares de estados equivalentes encontrados.
    """
    # Leer archivo de entrada
    lines = leer_archivo_entrada("input.txt")
    
    # Configurar función input para usar las líneas del archivo
    def input():
        if not lines:
            raise EOFError("Se acabaron las líneas del archivo")
        return lines.pop(0)
    
    # Hacer input() disponible globalmente
    import builtins
    builtins.input = input
    
    try:
        # Leer número de casos de prueba
        casos = int(input().strip())
        if casos <= 0:
            print("Error: El número de casos debe ser positivo")
            return
        
        print(f"Procesando {casos} caso(s) de prueba...")
        print("=" * 50)
        
        # Procesar cada caso
        for caso in range(1, casos + 1):
            print(f"\nCaso {caso}:")
            print("-" * 20)
            
            pares_equivalentes = procesar_caso_prueba()
            
            if pares_equivalentes is None:
                print("Error en el procesamiento del caso")
                continue
            
            # Mostrar resultados
            resultado = formatear_salida(pares_equivalentes)
            print(f"Pares de estados equivalentes: {resultado}")
            
            if pares_equivalentes:
                print(f"Total de pares equivalentes: {len(pares_equivalentes)}")
            else:
                print("No se encontraron estados equivalentes")
        
        print("\n" + "=" * 50)
        print("Procesamiento completado.")
        
    except EOFError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error en formato de entrada: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")


if __name__ == "__main__":
    main()
