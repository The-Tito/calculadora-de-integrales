# app.py
from flask import Flask, render_template, request, jsonify
from calculadora_logica import IntegralCalculator
import os

app = Flask(__name__)
# Instanciamos tu clase de lógica una sola vez
calculadora = IntegralCalculator()

# Crear la carpeta de imágenes si no existe
img_dir = os.path.join(app.root_path, 'static', 'img')
os.makedirs(img_dir, exist_ok=True)

# --- Rutas de la aplicación ---

@app.route('/')
def home():
    """Sirve la página principal de la calculadora."""
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    """
    Endpoint de la API para calcular la integral.
    Recibe los datos del formulario y devuelve el resultado.
    """
    try:
        data = request.get_json()
        
        # Extracción de datos del request
        funcion_str = data.get('funcion')
        limite_inferior_str = data.get('limite_inferior')
        limite_superior_str = data.get('limite_superior')
        
        # Verificar que los datos no estén vacíos
        if not all([funcion_str, limite_inferior_str, limite_superior_str]):
            return jsonify({'error': 'Todos los campos son requeridos.', 'exito': False}), 400

        # Usar tu lógica de cálculo
        result_def, result_indef, func, a, b = calculadora.calculate_definite_integral(
            funcion_str, limite_inferior_str, limite_superior_str
        )
        
        # Formatear el resultado para el frontend
        resultado_formateado = calculadora.format_result_pretty(result_def, result_indef, a, b, funcion_str)

        # Generar la gráfica y obtener la ruta
        grafica_url = calculadora.generate_integral_plot(func, a, b, img_dir)

        # Enviar el resultado y la URL de la gráfica en el JSON
        return jsonify({
            'resultado_texto': resultado_formateado,
            'grafica_url': grafica_url,
            'exito': True,
        })

    except Exception as e:
        # Manejar errores de forma elegante
        return jsonify({'error': str(e), 'exito': False}), 500

if __name__ == '__main__':
    app.run(debug=True)