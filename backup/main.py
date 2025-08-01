

from calculadora_logica import IntegralCalculator
from backup.Gui import IntegralCalculatorGUI

def main():
    """Función principal que inicia la aplicación"""
    try:
        # Crear instancia del calculador
        calculator = IntegralCalculator()
        
        # Crear instancia de la interfaz gráfica
        app = IntegralCalculatorGUI(calculator)
        
        # Crear y mostrar la GUI
        app.create_gui()
        
        # Mostrar mensaje de bienvenida en consola
        print("=" * 50)
        print("CALCULADORA DE INTEGRALES DEFINIDAS")
        print("=" * 50)
        print("Funciones soportadas:")
        print("- Funciones básicas: +, -, *, /, ^")
        print("- Funciones trigonométricas: sin, cos, tan")
        print("- Funciones logarítmicas: ln, log")
        print("- Funciones exponenciales: exp, e")
        print("- Raíz cuadrada: sqrt")
        print("- Constantes: pi, e, oo (infinito)")
        print("- Variable: x")
        print("\nEjemplos de uso:")
        print("- f(x) = x^2")
        print("- f(x) = sin(x)")
        print("- f(x) = exp(x)")
        print("- f(x) = ln(x)")
        print("=" * 50)
        print("¡La aplicación está lista para usar!")
        print("Cierra esta ventana para salir del programa.")
        print("=" * 50)
        
        # Ejecutar la aplicación
        app.run()
        
    except ImportError as e:
        print(f"Error: No se pudieron importar las dependencias necesarias: {e}")
        print("Asegúrate de tener instalados:")
        print("- tkinter (incluido con Python)")
        print("- matplotlib: pip install matplotlib")
        print("- numpy: pip install numpy") 
        print("- sympy: pip install sympy")
        
    except Exception as e:
        print(f"Error inesperado: {e}")
        print("Por favor, reporta este error al desarrollador.")

if __name__ == "__main__":
    main()