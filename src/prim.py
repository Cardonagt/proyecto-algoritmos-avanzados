"""
Implementación del Algoritmo de Prim para Árbol de Expansión Mínima (MST).

El algoritmo de Prim construye un MST seleccionando aristas de menor peso
que conectan el árbol en construcción con vértices no visitados.

Complejidad: O(E log V) con heap binario, donde E = aristas, V = vértices
"""

import heapq
from typing import List, Tuple, Dict, Set
from src.graph_utils import leer_grafo_csv, crear_grafo_networkx, visualizar_grafo


def prim(aristas: List[Tuple[str, str, int]], nodo_inicial: str = None) -> Tuple[List[Tuple], int]:
    """
    Implementa el algoritmo de Prim para encontrar el MST.
    
    Args:
        aristas: Lista de tuplas (nodo1, nodo2, peso)
        nodo_inicial: Nodo desde donde iniciar (opcional)
    
    Returns:
        Tupla con (lista de aristas del MST, peso total del MST)
    
    Complejidad: O(E log V) usando heap binario
    """
    if not aristas:
        return [], 0
    
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
    
    # Inicializar
    if nodo_inicial is None:
        nodo_inicial = list(grafo.keys())[0]
    
    visitados: Set[str] = {nodo_inicial}
    mst_aristas: List[Tuple[str, str, int]] = []
    peso_total = 0
    
    # Heap con aristas candidatas: (peso, nodo1, nodo2)
    # Complejidad de heappush/heappop: O(log E)
    heap = []
    for vecino, peso in grafo[nodo_inicial]:
        heapq.heappush(heap, (peso, nodo_inicial, vecino))
    
    # Mientras haya aristas candidatas
    # Complejidad total del bucle: O(E log E) = O(E log V)
    while heap and len(visitados) < len(grafo):
        peso, nodo1, nodo2 = heapq.heappop(heap)
        
        # Si el nodo destino ya fue visitado, saltar
        if nodo2 in visitados:
            continue
        
        # Agregar arista al MST
        visitados.add(nodo2)
        mst_aristas.append((nodo1, nodo2, peso))
        peso_total += peso
        
        # Agregar nuevas aristas candidatas
        for vecino, peso_arista in grafo[nodo2]:
            if vecino not in visitados:
                heapq.heappush(heap, (peso_arista, nodo2, vecino))
    
    return mst_aristas, peso_total


def ejecutar_prim(archivo_csv: str = "data/grafo.csv"):
    """
    Ejecuta el algoritmo de Prim completo y genera la visualización.
    
    Args:
        archivo_csv: Ruta al archivo CSV con el grafo
    
    Complejidad: O(E log V) dominado por el algoritmo de Prim
    """
    print("\n" + "="*60)
    print("ALGORITMO DE PRIM - ÁRBOL DE EXPANSIÓN MÍNIMA")
    print("="*60)
    
    # Leer grafo
    aristas = leer_grafo_csv(archivo_csv)
    if not aristas:
        return
    
    # Ejecutar Prim
    mst_aristas, peso_total = prim(aristas)
    
    # Mostrar resultados
    print(f"\n Resultados del MST (Prim):")
    print(f"   Aristas en el MST: {len(mst_aristas)}")
    print(f"   Peso total: {peso_total}")
    print(f"\n Aristas seleccionadas:")
    for nodo1, nodo2, peso in mst_aristas:
        print(f"   {nodo1} -- {nodo2} : {peso}")
    
    # Crear visualización
    G = crear_grafo_networkx(aristas)
    aristas_mst = [(n1, n2) for n1, n2, _ in mst_aristas]
    visualizar_grafo(G, aristas_mst, 
                     titulo=f"Algoritmo de Prim - MST (Peso Total: {peso_total})",
                     archivo_salida="output/prim_mst.png")
    
    print(f"\n✓ Proceso completado exitosamente")
    print("="*60 + "\n")


if __name__ == "__main__":
    ejecutar_prim()