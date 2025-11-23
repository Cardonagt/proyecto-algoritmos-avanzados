"""
Implementación del Algoritmo de Huffman para codificación óptima.

El algoritmo de Huffman construye un árbol de codificación óptimo basado
en las frecuencias de los caracteres, asignando códigos más cortos a
caracteres más frecuentes.

Complejidad: O(n log n) donde n = número de caracteres únicos
"""

import heapq
from typing import Dict, Tuple, Optional
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx


class NodoHuffman:
    """
    Nodo del árbol de Huffman.
    
    Cada nodo contiene una frecuencia y puede tener un carácter (nodos hoja)
    o dos hijos (nodos internos).
    """
    
    def __init__(self, caracter: Optional[str], frecuencia: int, 
                 izquierdo: Optional['NodoHuffman'] = None, 
                 derecho: Optional['NodoHuffman'] = None):
        """
        Inicializa un nodo del árbol de Huffman.
        
        Args:
            caracter: Carácter que representa (None para nodos internos)
            frecuencia: Frecuencia del carácter o suma de frecuencias
            izquierdo: Hijo izquierdo
            derecho: Hijo derecho
        """
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierdo = izquierdo
        self.derecho = derecho
    
    def __lt__(self, otro):
        """Comparador para el heap (por frecuencia)."""
        return self.frecuencia < otro.frecuencia
    
    def es_hoja(self) -> bool:
        """Verifica si el nodo es una hoja."""
        return self.izquierdo is None and self.derecho is None


def calcular_frecuencias(texto: str) -> Dict[str, int]:
    """
    Calcula la frecuencia de cada carácter en el texto.
    
    Args:
        texto: Texto a analizar
    
    Returns:
        Diccionario con las frecuencias de cada carácter
    
    Complejidad: O(m) donde m = longitud del texto
    """
    return dict(Counter(texto))


def construir_arbol_huffman(frecuencias: Dict[str, int]) -> Optional[NodoHuffman]:
    """
    Construye el árbol de Huffman a partir de las frecuencias.
    
    Args:
        frecuencias: Diccionario con frecuencias de caracteres
    
    Returns:
        Raíz del árbol de Huffman
    
    Complejidad: O(n log n) donde n = número de caracteres únicos
    """
    if not frecuencias:
        return None
    
    # Crear heap con nodos hoja
    # Complejidad: O(n log n)
    heap = [NodoHuffman(char, freq) for char, freq in frecuencias.items()]
    heapq.heapify(heap)
    
    # Construir árbol combinando nodos de menor frecuencia
    # Complejidad: O(n log n)
    while len(heap) > 1:
        izq = heapq.heappop(heap)
        der = heapq.heappop(heap)
        
        # Crear nodo padre con suma de frecuencias
        padre = NodoHuffman(None, izq.frecuencia + der.frecuencia, izq, der)
        heapq.heappush(heap, padre)
    
    return heap[0] if heap else None


def generar_codigos(raiz: Optional[NodoHuffman], codigo: str = "", 
                    codigos: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """
    Genera los códigos de Huffman mediante recorrido del árbol.
    
    Args:
        raiz: Raíz del árbol de Huffman
        codigo: Código actual (para recursión)
        codigos: Diccionario de códigos (para recursión)
    
    Returns:
        Diccionario con los códigos de cada carácter
    
    Complejidad: O(n) donde n = número de nodos
    """
    if codigos is None:
        codigos = {}
    
    if raiz is None:
        return codigos
    
    # Si es hoja, guardar código
    if raiz.es_hoja():
        codigos[raiz.caracter] = codigo if codigo else "0"
        return codigos
    
    # Recorrer subárbol izquierdo (agregar '0')
    generar_codigos(raiz.izquierdo, codigo + "0", codigos)
    
    # Recorrer subárbol derecho (agregar '1')
    generar_codigos(raiz.derecho, codigo + "1", codigos)
    
    return codigos


def representacion_textual_arbol(raiz: Optional[NodoHuffman], prefijo: str = "", 
                                 es_izquierdo: bool = True) -> str:
    """
    Genera representación textual del árbol de Huffman.
    
    Args:
        raiz: Raíz del árbol
        prefijo: Prefijo para la indentación
        es_izquierdo: Si es hijo izquierdo
    
    Returns:
        String con la representación del árbol
    
    Complejidad: O(n) donde n = número de nodos
    """
    if raiz is None:
        return ""
    
    resultado = ""
    
    # Símbolo de conexión
    conector = "├── " if es_izquierdo else "└── "
    
    # Representar nodo actual
    if raiz.es_hoja():
        char_repr = repr(raiz.caracter) if raiz.caracter != ' ' else "' '"
        resultado += f"{prefijo}{conector}[{char_repr}: {raiz.frecuencia}]\n"
    else:
        resultado += f"{prefijo}{conector}[{raiz.frecuencia}]\n"
    
    # Actualizar prefijo para hijos
    nuevo_prefijo = prefijo + ("│   " if es_izquierdo else "    ")
    
    # Recorrer hijos
    if raiz.izquierdo:
        resultado += representacion_textual_arbol(raiz.izquierdo, nuevo_prefijo, True)
    if raiz.derecho:
        resultado += representacion_textual_arbol(raiz.derecho, nuevo_prefijo, False)
    
    return resultado


def visualizar_arbol_huffman(raiz: Optional[NodoHuffman], archivo_salida: str = "output/huffman_tree.png"):
    """
    Visualiza el árbol de Huffman usando NetworkX y Matplotlib.
    
    Args:
        raiz: Raíz del árbol de Huffman
        archivo_salida: Nombre del archivo PNG de salida
    
    Complejidad: O(n) donde n = número de nodos
    """
    if raiz is None:
        return
    
    G = nx.DiGraph()
    etiquetas = {}
    contador = [0]  # Para IDs únicos de nodos
    
    def agregar_nodos(nodo, id_nodo=0):
        """Agrega nodos al grafo de forma recursiva."""
        if nodo is None:
            return
        
        # Etiqueta del nodo
        if nodo.es_hoja():
            char_repr = repr(nodo.caracter) if nodo.caracter != ' ' else "' '"
            etiquetas[id_nodo] = f"{char_repr}\n{nodo.frecuencia}"
        else:
            etiquetas[id_nodo] = str(nodo.frecuencia)
        
        # Agregar hijos
        if nodo.izquierdo:
            contador[0] += 1
            id_izq = contador[0]
            G.add_edge(id_nodo, id_izq, label='0')
            agregar_nodos(nodo.izquierdo, id_izq)
        
        if nodo.derecho:
            contador[0] += 1
            id_der = contador[0]
            G.add_edge(id_nodo, id_der, label='1')
            agregar_nodos(nodo.derecho, id_der)
    
    agregar_nodos(raiz)
    
    # Crear visualización
    plt.figure(figsize=(14, 10))
    
    # Usar hierarchical_layout para árbol
    pos = nx.spring_layout(G, k=3, iterations=50)
    
    # Dibujar nodos
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                           node_size=1500, edgecolors='black', linewidths=2)
    
    # Dibujar aristas
    nx.draw_networkx_edges(G, pos, edge_color='gray', 
                           width=2, arrowsize=20, arrowstyle='->')
    
    # Dibujar etiquetas de nodos
    nx.draw_networkx_labels(G, pos, etiquetas, font_size=10, font_weight='bold')
    
    # Dibujar etiquetas de aristas
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=9, font_color='red')
    
    plt.title("Árbol de Huffman", fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(archivo_salida, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ Árbol guardado: {archivo_salida}")


def visualizar_frecuencias(frecuencias: Dict[str, int], archivo_salida: str = "output/huffman_freq.png"):
    """
    Visualiza las frecuencias de caracteres en un gráfico de barras.
    
    Args:
        frecuencias: Diccionario con frecuencias de caracteres
        archivo_salida: Nombre del archivo PNG de salida
    
    Complejidad: O(n log n) por el ordenamiento
    """
    # Ordenar por frecuencia descendente
    items = sorted(frecuencias.items(), key=lambda x: x[1], reverse=True)
    caracteres = [repr(char) if char != ' ' else "' '" for char, _ in items]
    freqs = [freq for _, freq in items]
    
    # Crear gráfico
    plt.figure(figsize=(12, 6))
    bars = plt.bar(range(len(caracteres)), freqs, color='skyblue', edgecolor='black')
    
    # Agregar valores sobre las barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=9)
    
    plt.xlabel('Caracteres', fontsize=12, fontweight='bold')
    plt.ylabel('Frecuencia', fontsize=12, fontweight='bold')
    plt.title('Frecuencia de Caracteres', fontsize=14, fontweight='bold')
    plt.xticks(range(len(caracteres)), caracteres, rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(archivo_salida, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ Frecuencias guardadas: {archivo_salida}")


def ejecutar_huffman(archivo_txt: str = "data/texto.txt"):
    """
    Ejecuta el algoritmo de Huffman completo y genera visualizaciones.
    
    Args:
        archivo_txt: Ruta al archivo de texto
    
    Complejidad: O(m + n log n) donde m = longitud texto, n = caracteres únicos
    """
    print("\n" + "="*60)
    print("ALGORITMO DE HUFFMAN - CODIFICACIÓN ÓPTIMA")
    print("="*60)
    
    # Leer texto
    try:
        with open(archivo_txt, 'r', encoding='utf-8') as f:
            texto = f.read()
        print(f"✓ Texto cargado: {len(texto)} caracteres")
    except FileNotFoundError:
        print(f"✗ Error: No se encontró el archivo {archivo_txt}")
        return
    except Exception as e:
        print(f"✗ Error al leer el texto: {e}")
        return
    
    # Calcular frecuencias
    frecuencias = calcular_frecuencias(texto)
    print(f"✓ Caracteres únicos: {len(frecuencias)}")
    
    # Construir árbol de Huffman
    raiz = construir_arbol_huffman(frecuencias)
    
    # Generar códigos
    codigos = generar_codigos(raiz)
    
    # Mostrar tabla de códigos
    print(f"\n Tabla de Códigos de Huffman:")
    print(f"{'Carácter':<12} {'Frecuencia':<12} {'Código'}")
    print("-" * 45)
    for char, freq in sorted(frecuencias.items(), key=lambda x: x[1], reverse=True):
        char_repr = repr(char) if char != ' ' else "' '"
        codigo = codigos.get(char, "")
        print(f"{char_repr:<12} {freq:<12} {codigo}")
    
    # Representación textual del árbol
    print(f"\n🌳 Estructura del Árbol de Huffman:")
    print(representacion_textual_arbol(raiz))
    
    # Calcular tamaño original vs comprimido
    bits_original = len(texto) * 8
    bits_comprimido = sum(len(codigos[char]) * freq for char, freq in frecuencias.items())
    tasa_compresion = (1 - bits_comprimido / bits_original) * 100
    
    print(f"\n Estadísticas de Compresión:")
    print(f"   Bits originales: {bits_original}")
    print(f"   Bits comprimidos: {bits_comprimido}")
    print(f"   Tasa de compresión: {tasa_compresion:.2f}%")
    
    # Generar visualizaciones
    visualizar_arbol_huffman(raiz)
    visualizar_frecuencias(frecuencias)
    
    print(f"\n✓ Proceso completado exitosamente")
    print("="*60 + "\n")


if __name__ == "__main__":
    ejecutar_huffman()