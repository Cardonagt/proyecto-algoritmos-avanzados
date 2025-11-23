"""
Módulo de utilidades para manejo de grafos.

Este módulo proporciona funciones auxiliares para cargar grafos desde archivos CSV
y visualizar resultados usando NetworkX y Matplotlib.

Complejidad: O(E) para lectura, donde E es el número de aristas.
"""

import csv
import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Tuple


def leer_grafo_csv(archivo: str) -> List[Tuple[str, str, int]]:
    """
    Lee un grafo desde un archivo CSV.
    
    Args:
        archivo: Ruta al archivo CSV con formato: nodo1,nodo2,peso
    
    Returns:
        Lista de tuplas (nodo1, nodo2, peso) representando las aristas
    
    Complejidad: O(E) donde E es el número de aristas
    """
    aristas = []
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            lector = csv.reader(f)
            for fila in lector:
                if len(fila) >= 3:
                    nodo1 = fila[0].strip()
                    nodo2 = fila[1].strip()
                    peso = int(fila[2].strip())
                    aristas.append((nodo1, nodo2, peso))
        print(f"✓ Grafo cargado: {len(aristas)} aristas")
        return aristas
    except FileNotFoundError:
        print(f"✗ Error: No se encontró el archivo {archivo}")
        return []
    except Exception as e:
        print(f"✗ Error al leer el grafo: {e}")
        return []


def crear_grafo_networkx(aristas: List[Tuple[str, str, int]]) -> nx.Graph:
    """
    Crea un grafo de NetworkX a partir de una lista de aristas.
    
    Args:
        aristas: Lista de tuplas (nodo1, nodo2, peso)
    
    Returns:
        Grafo de NetworkX
    
    Complejidad: O(E) donde E es el número de aristas
    """
    G = nx.Graph()
    for nodo1, nodo2, peso in aristas:
        G.add_edge(nodo1, nodo2, weight=peso)
    return G


def visualizar_grafo(G: nx.Graph, aristas_resaltadas: List[Tuple] = None, 
                     titulo: str = "Grafo", archivo_salida: str = "grafo.png",
                     nodo_origen: str = None):
    """
    Visualiza un grafo usando Matplotlib y lo guarda como PNG.
    
    Args:
        G: Grafo de NetworkX
        aristas_resaltadas: Lista de aristas a resaltar en rojo
        titulo: Título del gráfico
        archivo_salida: Nombre del archivo PNG de salida
        nodo_origen: Nodo origen a resaltar (opcional)
    
    Complejidad: O(V + E) donde V es vértices y E es aristas
    """
    plt.figure(figsize=(12, 8))
    
    # Usar spring_layout en lugar de graphviz_layout
    pos = nx.spring_layout(G, seed=42, k=2, iterations=50)
    
    # Dibujar todas las aristas en gris claro
    nx.draw_networkx_edges(G, pos, edge_color='lightgray', width=2, alpha=0.6)
    
    # Dibujar aristas resaltadas
    if aristas_resaltadas:
        nx.draw_networkx_edges(G, pos, edgelist=aristas_resaltadas, 
                                edge_color='red', width=3)
    
    # Dibujar nodos
    node_colors = []
    for node in G.nodes():
        if nodo_origen and node == nodo_origen:
            node_colors.append('gold')
        else:
            node_colors.append('lightblue')
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                           node_size=700, edgecolors='black', linewidths=2)
    
    # Dibujar etiquetas de nodos
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    
    # Dibujar pesos de aristas
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=10)
    
    plt.title(titulo, fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(archivo_salida, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ Imagen guardada: {archivo_salida}")