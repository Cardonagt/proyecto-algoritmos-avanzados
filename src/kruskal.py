"""
Implementación del Algoritmo de Kruskal para Árbol de Expansión Mínima (MST).

El algoritmo de Kruskal construye un MST ordenando las aristas por peso
y agregándolas si no forman ciclos, usando Union-Find para detección de ciclos.

Complejidad: O(E log E) donde E = número de aristas
"""

from typing import List, Tuple, Dict
from src.graph_utils import leer_grafo_csv, crear_grafo_networkx, visualizar_grafo


class UnionFind:
    """
    Estructura de datos Union-Find (Disjoint Set Union) con compresión de ruta.
    
    Utilizada para detectar ciclos eficientemente en el algoritmo de Kruskal.
    
    Complejidad: O(α(n)) por operación, donde α es la inversa de Ackermann (casi constante)
    """
    
    def __init__(self, nodos: List[str]):
        """
        Inicializa Union-Find con cada nodo en su propio conjunto.
        
        Args:
            nodos: Lista de nodos del grafo
        
        Complejidad: O(V) donde V = número de vértices
        """
        self.padre: Dict[str, str] = {nodo: nodo for nodo in nodos}
        self.rango: Dict[str, int] = {nodo: 0 for nodo in nodos}
    
    def encontrar(self, nodo: str) -> str:
        """
        Encuentra el representante del conjunto con compresión de ruta.
        
        Args:
            nodo: Nodo a buscar
        
        Returns:
            Representante del conjunto
        
        Complejidad: O(α(n)) amortizado
        """
        if self.padre[nodo] != nodo:
            self.padre[nodo] = self.encontrar(self.padre[nodo])  # Compresión de ruta
        return self.padre[nodo]
    
    def unir(self, nodo1: str, nodo2: str) -> bool:
        """
        Une dos conjuntos usando unión por rango.
        
        Args:
            nodo1: Primer nodo
            nodo2: Segundo nodo
        
        Returns:
            True si se unieron (estaban en conjuntos diferentes), False si ya estaban unidos
        
        Complejidad: O(α(n)) amortizado
        """
        raiz1 = self.encontrar(nodo1)
        raiz2 = self.encontrar(nodo2)
        
        if raiz1 == raiz2:
            return False  # Ya están en el mismo conjunto (formarían ciclo)
        
        # Unión por rango
        if self.rango[raiz1] < self.rango[raiz2]:
            self.padre[raiz1] = raiz2
        elif self.rango[raiz1] > self.rango[raiz2]:
            self.padre[raiz2] = raiz1
        else:
            self.padre[raiz2] = raiz1
            self.rango[raiz1] += 1
        
        return True


def kruskal(aristas: List[Tuple[str, str, int]]) -> Tuple[List[Tuple], int]:
    """
    Implementa el algoritmo de Kruskal para encontrar el MST.
    
    Args:
        aristas: Lista de tuplas (nodo1, nodo2, peso)
    
    Returns:
        Tupla con (lista de aristas del MST, peso total del MST)
    
    Complejidad: O(E log E) dominado por el ordenamiento
    """
    if not aristas:
        return [], 0
    
    # Obtener todos los nodos únicos
    # Complejidad: O(E)
    nodos = set()
    for nodo1, nodo2, _ in aristas:
        nodos.add(nodo1)
        nodos.add(nodo2)
    
    # Ordenar aristas por peso
    # Complejidad: O(E log E)
    aristas_ordenadas = sorted(aristas, key=lambda x: x[2])
    
    # Inicializar Union-Find
    uf = UnionFind(list(nodos))
    
    mst_aristas: List[Tuple[str, str, int]] = []
    peso_total = 0
    
    # Procesar aristas en orden de peso
    # Complejidad: O(E * α(V))
    for nodo1, nodo2, peso in aristas_ordenadas:
        # Si unir estos nodos no forma ciclo, agregar al MST
        if uf.unir(nodo1, nodo2):
            mst_aristas.append((nodo1, nodo2, peso))
            peso_total += peso
            
            # Si ya tenemos V-1 aristas, terminamos
            if len(mst_aristas) == len(nodos) - 1:
                break
    
    return mst_aristas, peso_total


def ejecutar_kruskal(archivo_csv: str = "data/grafo.csv"):
    """
    Ejecuta el algoritmo de Kruskal completo y genera la visualización.
    
    Args:
        archivo_csv: Ruta al archivo CSV con el grafo
    
    Complejidad: O(E log E) dominado por el algoritmo de Kruskal
    """
    print("\n" + "="*60)
    print("ALGORITMO DE KRUSKAL - ÁRBOL DE EXPANSIÓN MÍNIMA")
    print("="*60)
    
    # Leer grafo
    aristas = leer_grafo_csv(archivo_csv)
    if not aristas:
        return
    
    # Ejecutar Kruskal
    mst_aristas, peso_total = kruskal(aristas)
    
    # Mostrar resultados
    print(f"\n📊 Resultados del MST (Kruskal):")
    print(f"   Aristas en el MST: {len(mst_aristas)}")
    print(f"   Peso total: {peso_total}")
    print(f"\n🌳 Aristas seleccionadas (en orden):")
    for nodo1, nodo2, peso in mst_aristas:
        print(f"   {nodo1} -- {nodo2} : {peso}")
    
    # Crear visualización
    G = crear_grafo_networkx(aristas)
    aristas_mst = [(n1, n2) for n1, n2, _ in mst_aristas]
    visualizar_grafo(G, aristas_mst, 
                     titulo=f"Algoritmo de Kruskal - MST (Peso Total: {peso_total})",
                     archivo_salida="output/kruskal_mst.png")
    
    print(f"\n✓ Proceso completado exitosamente")
    print("="*60 + "\n")


if __name__ == "__main__":
    ejecutar_kruskal()