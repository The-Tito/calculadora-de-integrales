# calculadora_logica.py - Lógica de cálculo de integrales
import numpy as np
from sympy import symbols, sympify, lambdify, integrate, latex, pi, exp, sin, cos, tan, log, sqrt, oo
import matplotlib.pyplot as plt
import os
import uuid

# Definir símbolo matemático
x = symbols('x')

# Diccionario de funciones matemáticas
math_dict = {
    'pi': pi,
    'π': pi,
    'e': exp(1),
    'E': exp(1),
    'exp': exp,
    'sin': sin,
    'cos': cos,
    'tan': tan,
    'ln': log,
    'log': log,
    'sqrt': sqrt,
    'oo': oo,
    '∞': oo,
    'x': x
}

class IntegralCalculator:
    """Clase para manejar los cálculos de integrales"""
    
    def __init__(self):
        self.x = x
        self.math_dict = math_dict
    
    def parse_function(self, func_str):
        """Convierte una cadena de texto a una función simbólica"""
        func_str = func_str.strip().replace("^", "**")
        return sympify(func_str, locals=self.math_dict)
    
    def parse_limit(self, limit_str):
        """Convierte una cadena de texto a un límite numérico"""
        return sympify(limit_str.strip(), locals=self.math_dict)
    
    def calculate_definite_integral(self, func_str, lower_limit_str, upper_limit_str):
        """
        Calcula la integral definida de una función
        
        Args:
            func_str: Función como cadena de texto
            lower_limit_str: Límite inferior como cadena
            upper_limit_str: Límite superior como cadena
            
        Returns:
            tuple: (resultado_definida, integral_indefinida, función_parseada, límite_a, límite_b)
        """
        try:
            # Parsear función y límites
            func = self.parse_function(func_str)
            a = self.parse_limit(lower_limit_str)
            b = self.parse_limit(upper_limit_str)
            
            # Calcular integrales
            result_def = integrate(func, (self.x, a, b)).evalf()
            result_indef = integrate(func, self.x)
            
            return result_def, result_indef, func, a, b
            
        except Exception as e:
            raise Exception(f"Error en el cálculo: {e}")
    
    def get_function_values(self, func, a, b, num_points=1000):
        """
        Obtiene valores numéricos de la función para graficar
        
        Args:
            func: Función simbólica
            a: Límite inferior
            b: Límite superior
            num_points: Número de puntos para la gráfica
            
        Returns:
            tuple: (x_vals, y_vals)
        """
        try:
            f = lambdify(self.x, func, modules=["numpy"])
            
            # Crear rango extendido para mejor visualización
            x_start = float(a) - 2 if float(a) != -oo else float(b) - 5
            x_end = float(b) + 2 if float(b) != oo else float(a) + 5
            
            x_vals = np.linspace(x_start, x_end, num_points)
            y_vals = f(x_vals)
            
            # Reemplazar valores infinitos o NaN con un valor seguro
            y_vals = np.nan_to_num(y_vals, posinf=np.max(y_vals) if np.isfinite(np.max(y_vals)) else 100, neginf=np.min(y_vals) if np.isfinite(np.min(y_vals)) else -100)
            
            return x_vals, y_vals
            
        except Exception as e:
            raise Exception(f"Error al generar valores de la función: {e}")
    
    def generate_integral_plot(self, func, a, b, img_dir, num_points=1000):
        """
        Genera y guarda una gráfica de la función y su integral.

        Args:
            func: Función simbólica de SymPy.
            a: Límite inferior de la integral.
            b: Límite superior de la integral.
            img_dir: Directorio donde se guardará la imagen.
            num_points: Número de puntos para la curva.

        Returns:
            La ruta del archivo de imagen si se genera con éxito, None en caso contrario.
        """
        try:
            # Eliminar gráficas antiguas para evitar saturación del servidor
            if os.path.exists(img_dir):
                for filename in os.listdir(img_dir):
                    if filename.endswith(".png"):
                        os.remove(os.path.join(img_dir, filename))

            f_numpy = lambdify(self.x, func, modules=["numpy"])
            
            # Definir un rango de x para la gráfica completa
            x_range = np.linspace(float(a)-1, float(b)+1, num_points)
            y_range = f_numpy(x_range)
            
            # Definir un rango de x para el área de la integral
            x_integral = np.linspace(float(a), float(b), num_points)
            y_integral = f_numpy(x_integral)
            
            # Crear la gráfica
            plt.figure(figsize=(8, 6))
            
            # Graficar la función completa
            plt.plot(x_range, y_range, label=f'$f(x) = {latex(func)}$', color='#3498db')
            
            # Rellenar el área bajo la curva
            plt.fill_between(x_integral, y_integral, color='#3498db', alpha=0.3, label='Área de la integral')
            
            # Límites de la integral
            plt.axvline(x=a, color='red', linestyle='--', label=f'x = {a}')
            plt.axvline(x=b, color='red', linestyle='--', label=f'x = {b}')
            
            plt.title('Gráfica de la función y área de la integral')
            plt.xlabel('x')
            plt.ylabel('f(x)')
            plt.grid(True, linestyle=':', alpha=0.6)
            plt.legend()
            
            # Generar un nombre de archivo único
            filename = f"graph_{uuid.uuid4().hex}.png"
            filepath = os.path.join(img_dir, filename)
            
            # Guardar la imagen
            plt.savefig(filepath)
            plt.close()

            return f"/static/img/{filename}"

        except Exception as e:
            print(f"Error al generar la gráfica: {e}")
            return None

    # (El resto de la clase permanece igual)
    def format_result(self, result_def, result_indef, a, b):
        return f"∫ de {a} a {b} de f(x) dx = {result_def}\nIntegral indefinida: ∫f(x)dx = {latex(result_indef)} + C"

    def pretty_print_expression(self, expr):
        try:
            expr_str = str(expr)
            replacements = {
                'pi': 'π', 'E': 'e', 'exp(': 'e^(', 'sqrt(': '√(', 'oo': '∞', '**': '^',
                '*': '·', 'log(': 'ln(', 'I': 'i', 'Abs(': '|', 'asin(': 'arcsin(',
                'acos(': 'arccos(', 'atan(': 'arctan(', 'sinh(': 'senh(', 'cosh(': 'cosh(', 'tanh(': 'tanh(',
            }
            formatted_expr = expr_str
            for old, new in replacements.items():
                formatted_expr = formatted_expr.replace(old, new)
            formatted_expr = self._format_exponentials(formatted_expr)
            formatted_expr = self._format_fractions(formatted_expr)
            return formatted_expr
        except Exception:
            return str(expr)

    def _format_exponentials(self, expr_str):
        import re
        expr_str = re.sub(r'e\^\(([^)]+)\)', r'e^{\1}', expr_str)
        expr_str = re.sub(r'x\^(\d+)', r'x^{\1}', expr_str)
        return expr_str
    
    def _format_fractions(self, expr_str):
        import re
        fraction_map = {
            r'\b1/2\b': '½', r'\b1/3\b': '⅓', r'\b2/3\b': '⅔', r'\b1/4\b': '¼', r'\b3/4\b': '¾',
            r'\b1/5\b': '⅕', r'\b2/5\b': '⅖', r'\b3/5\b': '⅗', r'\b4/5\b': '⅘', r'\b1/6\b': '⅙',
            r'\b5/6\b': '⅚', r'\b1/8\b': '⅛', r'\b3/8\b': '⅜', r'\b5/8\b': '⅝', r'\b7/8\b': '⅞',
        }
        for pattern, replacement in fraction_map.items():
            expr_str = re.sub(pattern, replacement, expr_str)
        return expr_str
    
    def format_result_pretty(self, result_def, result_indef, a, b, func_str):
        try:
            func_formatted = self.pretty_print_expression(sympify(func_str, locals=self.math_dict))
            a_formatted = self.pretty_print_expression(a)
            b_formatted = self.pretty_print_expression(b)
            if isinstance(result_def, (int, float, complex)):
                if abs(float(result_def)) < 1e-12:
                    result_def_formatted = "0"
                elif abs(float(result_def)) > 1e6:
                    result_def_formatted = f"{float(result_def):.4e}"
                else:
                    result_def_formatted = f"{float(result_def):.8f}".rstrip('0').rstrip('.')
            else:
                result_def_formatted = self.pretty_print_expression(result_def)
            
            result_indef_formatted = self.pretty_print_expression(result_indef)
            
            result_text = f"✅ RESULTADO DE LA INTEGRACIÓN\n\n"
            result_text += f"Función: f(x) = {func_formatted}\n"
            result_text += f"Límites: [{a_formatted}, {b_formatted}]\n\n"
            result_text += f"∫[{a_formatted} → {b_formatted}] f(x) dx = {result_def_formatted}\n\n"
            result_text += f"Integral indefinida:\n"
            result_text += f"∫ f(x) dx = {result_indef_formatted} + C"
            
            return result_text
            
        except Exception as e:
            return f"∫ de {a} a {b} de f(x) dx = {result_def}\nIntegral indefinida: ∫f(x)dx = {result_indef} + C"