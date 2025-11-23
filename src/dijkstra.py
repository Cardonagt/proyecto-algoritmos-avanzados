"""
Implementación del Algoritmo de Dijkstra para caminos más cortos.

El algoritmo de Dijkstra encuentra las rutas más cortas desde un nodo origen
a todos los demás nodos en un grafo con pesos no negativos.

Complejidad: O((V + E) log V) con heap binario
"""

import heapq
from typing import List, Tuple, Dict, Set
from src.graph_utils import leer_grafo_csv, crear_grafo_networkx, visualizar_grafo


def dijkstra(aristas: List[Tuple[str, str, int]], nodo_origen: str) -> Tuple[Dict[str, int], Dict[str, str]]:
    """
    Implementa el algoritmo de Dijkstra para encontrar caminos más cortos.
    
    Args:
        aristas: Lista de tuplas (nodo1, nodo2, peso)
        nodo_origen: Nodo desde donde calcular las distancias
    
    Returns:
        Tupla con (distancias desde origen, predecesores para reconstruir rutas)
    
    Complejidad: O((V + E) log V) con heap binario
    """
    # Construir lista de adyacencia
    # Complejidad: O(E)
    grafo: Dict[str, List[Tuple[str, int]]] = {}
    for nodo1, nodo2, peso in aristas:
        if nodo1 not in grafo:
            grafo[nodo1] = []
        if nodo2 not in grafo:
            grafo[nodo2] = []
        grafo[nodo1].append((nodo2, peso))
        grafo[nodo2].append((nodo1, peso))
    
    # Verificar que el nodo origen existe
    if nodo_origen not in grafo:
        print(f"✗ Error: El nodo '{nodo_origen}' no existe en el grafo")
        return {}, {}
    
    # Inicializar distancias y predecesores
    distancias: Dict[str, float] = {nodo: float('inf') for nodo in grafo}
    distancias[nodo_origen] = 0
    predecesores: Dict[str, str] = {}
    visitados: Set[str] = set()
    
    # Heap de prioridad: (distancia, nodo)
    # Complejidad de heappush/heappop: O(log V)
    heap = [(0, nodo_origen)]
    
    # Procesar nodos
    # Complejidad total: O((V + E) log V)
    while heap:
        distancia_actual, nodo_actual = heapq.heappop(heap)
        
        # Si ya visitamos este nodo, continuar
        if nodo_actual in visitados:
            continue
        
        visitados.add(nodo_actual)
        
        # Revisar vecinos
        for vecino, peso in grafo[nodo_actual]:
            if vecino in visitados:
                continue
            
            # Calcular nueva distancia
            nueva_distancia = distancia_actual + peso
            
            # Si encontramos un camino más corto, actualizar
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                predecesores[vecino] = nodo_actual
                heapq.heappush(heap, (nueva_distancia, vecino))
    
    return distancias, predecesores


def reconstruir_ruta(predecesores: Dict[str, str], nodo_origen: str, nodo_destino: str) -> List[str]:
    """
    Reconstruye la ruta más corta desde origen hasta destino.
    
    Args:
        predecesores: Diccionario de predecesores
        nodo_origen: Nodo de inicio
        nodo_destino: Nodo de destino
    
    Returns:
        Lista de nodos en la ruta (de origen a destino)
    
    Complejidad: O(V) en el peor caso
    """
    if nodo_destino not in predecesores and nodo_destino != nodo_origen:
        return []  # No hay ruta
    
    ruta = []
    nodo_actual = nodo_destino
    
    while nodo_actual != nodo_origen:
        ruta.append(nodo_actual)
        if nodo_actual not in predecesores:
            return []  # No hay ruta
        nodo_actual = predecesores[nodo_actual]
    
    ruta.append(nodo_origen)
    ruta.reverse()
    return ruta


def ejecutar_dijkstra(archivo_csv: str = "data/grafo.csv", nodo_origen: str = None):
    """
    Ejecuta el algoritmo de Dijkstra completo y genera la visualización.
    
    Args:
        archivo_csv: Ruta al archivo CSV con el grafo
        nodo_origen: Nodo origen para calcular distancias
    
    Complejidad: O((V + E) log V) dominado por Dijkstra
    """
    print("\n" + "="*60)
    print("ALGORITMO DE DIJKSTRA - CAMINOS MÁS CORTOS")
    print("="*60)
    
    # Leer grafo
    aristas = leer_grafo_csv(archivo_csv)
    if not aristas:
        return
    
    # Obtener nodos disponibles
    nodos = set()
    for n1, n2, _ in aristas:
        nodos.add(n1)
        nodos.add(n2)
    
    # Si no se especifica nodo origen, pedir al usuario
    if nodo_origen is None:
        print(f"\n Nodos disponibles: {sorted(nodos)}")
        nodo_origen = input("Ingrese el nodo origen: ").strip()
    
    # Ejecutar Dijkstra
    distancias, predecesores = dijkstra(aristas, nodo_origen)
    
    if not distancias:
        return
    
    # Mostrar resultados
    print(f"\n Distancias mínimas desde '{nodo_origen}':")
    for nodo in sorted(distancias.keys()):
        dist = distancias[nodo]
        if dist == float('inf'):
            print(f"   {nodo_origen} → {nodo}: ∞ (no alcanzable)")
        else:
            print(f"   {nodo_origen} → {nodo}: {dist}")
    
    print(f"\n  Rutas completas:")
    aristas_rutas = []
    for nodo_destino in sorted(nodos):
        if nodo_destino == nodo_origen:
            continue
        
        ruta = reconstruir_ruta(predecesores, nodo_origen, nodo_destino)
        if ruta:
            ruta_str = " → ".join(ruta)
            print(f"   {ruta_str} (distancia: {distancias[nodo_destino]})")
            
            # Agregar aristas de esta ruta para visualización
            for i in range(len(ruta) - 1):
                aristas_rutas.append((ruta[i], ruta[i+1]))
        else:
            print(f"   {nodo_origen} → {nodo_destino}: No hay ruta")
    
    # Crear visualización
    G = crear_grafo_networkx(aristas)
    visualizar_grafo(G, aristas_rutas, 
                     titulo=f"Algoritmo de Dijkstra - Caminos más cortos desde '{nodo_origen}'",
                     archivo_salida="output/dijkstra_paths.png",
                     nodo_origen=nodo_origen)
    
    print(f"\n✓ Proceso completado exitosamente")
    print("="*60 + "\n")


if __name__ == "__main__":
    ejecutar_dijkstra()