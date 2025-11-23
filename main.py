"""
Programa Principal - Proyecto Final de Análisis de Algoritmos.

Este programa implementa y visualiza los algoritmos:
- Prim (Árbol de Expansión Mínima)
- Kruskal (Árbol de Expansión Mínima)
- Dijkstra (Caminos más cortos)
- Huffman (Codificación óptima)

Autor: [Tu Nombre]
Carnet: [Tu Carnet]
Universidad Da Vinci de Guatemala
Fecha: Diciembre 2024
"""

import os
import sys
from src.prim import ejecutar_prim
from src.kruskal import ejecutar_kruskal
from src.dijkstra import ejecutar_dijkstra
from src.huffman import ejecutar_huffman


def limpiar_pantalla():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_banner():
    """Muestra el banner del programa."""
    print("=" * 70)
    print(" " * 10 + "PROYECTO FINAL - ANÁLISIS DE ALGORITMOS")
    print(" " * 15 + "Implementación de Algoritmos Avanzados")
    print("=" * 70)
    print("\n  Algoritmos disponibles:")
    print("    • Prim - Árbol de Expansión Mínima")
    print("    • Kruskal - Árbol de Expansión Mínima")
    print("    • Dijkstra - Caminos más cortos")
    print("    • Huffman - Codificación óptima")
    print("\n" + "=" * 70 + "\n")


def mostrar_menu():
    """Muestra el menú principal."""
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║              MENÚ PRINCIPAL DE ALGORITMOS                  ║")
    print("╠════════════════════════════════════════════════════════════╣")
    print("║  1. Algoritmo de Prim (MST)                                ║")
    print("║  2. Algoritmo de Kruskal (MST)                             ║")
    print("║  3. Algoritmo de Dijkstra (Caminos más cortos)             ║")
    print("║  4. Algoritmo de Huffman (Codificación)                    ║")
    print("║  5. Ejecutar todos los algoritmos                          ║")
    print("║  6. Salir                                                  ║")
    print("╚════════════════════════════════════════════════════════════╝")


def verificar_archivos():
    """Verifica que existan las carpetas necesarias."""
    carpetas = ['data', 'output', 'docs', 'docs/evidencias']
    
    for carpeta in carpetas:
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
            print(f"✓ Carpeta creada: {carpeta}")


def ejecutar_todos():
    """Ejecuta todos los algoritmos en secuencia."""
    print("\n" + "🚀" * 30)
    print(" " * 15 + "EJECUTANDO TODOS LOS ALGORITMOS")
    print("🚀" * 30)
    
    # Prim
    ejecutar_prim()
    input("\nPresione Enter para continuar...")
    
    # Kruskal
    ejecutar_kruskal()
    input("\nPresione Enter para continuar...")
    
    # Dijkstra (con nodo origen predeterminado)
    ejecutar_dijkstra(nodo_origen='A')
    input("\nPresione Enter para continuar...")
    
    # Huffman
    ejecutar_huffman()
    
    print("\n" + "✅" * 30)
    print(" " * 10 + "TODOS LOS ALGORITMOS EJECUTADOS EXITOSAMENTE")
    print("✅" * 30)


def main():
    """Función principal del programa."""
    # Verificar estructura de carpetas
    verificar_archivos()
    
    # Mostrar banner inicial
    limpiar_pantalla()
    mostrar_banner()
    
    while True:
        mostrar_menu()
        
        try:
            opcion = input("\n➤ Seleccione una opción (1-6): ").strip()
            
            if opcion == '1':
                ejecutar_prim()
                input("\nPresione Enter para continuar...")
                limpiar_pantalla()
                mostrar_banner()
            
            elif opcion == '2':
                ejecutar_kruskal()
                input("\nPresione Enter para continuar...")
                limpiar_pantalla()
                mostrar_banner()
            
            elif opcion == '3':
                ejecutar_dijkstra()
                input("\nPresione Enter para continuar...")
                limpiar_pantalla()
                mostrar_banner()
            
            elif opcion == '4':
                ejecutar_huffman()
                input("\nPresione Enter para continuar...")
                limpiar_pantalla()
                mostrar_banner()
            
            elif opcion == '5':
                ejecutar_todos()
                input("\nPresione Enter para continuar...")
                limpiar_pantalla()
                mostrar_banner()
            
            elif opcion == '6':
                print("\n" + "=" * 70)
                print(" " * 20 + "¡Gracias por usar el programa!")
                print(" " * 15 + "Universidad Da Vinci de Guatemala")
                print("=" * 70 + "\n")
                sys.exit(0)
            
            else:
                print("\n❌ Opción inválida. Por favor seleccione 1-6.")
                input("Presione Enter para continuar...")
                limpiar_pantalla
                mostrar_banner()
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Programa interrumpido por el usuario.")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            input("Presione Enter para continuar...")
            limpiar_pantalla()
            mostrar_banner()


if __name__ == "__main__":
    main()