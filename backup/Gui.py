# gui.py - Interfaz gráfica de la calculadora
import tkinter as tk
from tkinter import Label, Button, Frame, Entry, messagebox, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class Style:
    """Clase para definir el estilo de la aplicación"""
    PRIMARY = "#2563eb"
    PRIMARY_HOVER = "#1d4ed8"
    SECONDARY = "#f1f5f9"
    BG = "#292929"
    CARD_BG = "#292929"
    TEXT = "#1e293b"
    TEXT_SECONDARY = "#64748b"
    ACCENT = "#10b981"
    ERROR = "#ef4444"
    BORDER = "#e2e8f0"
    FONT = "Segoe UI"
    FONT_MONO = "Consolas"

    ENTRY = {
        "font": (FONT, 12),
        "bg": "#ffffff",
        "fg": TEXT,
        "relief": "solid",
        "bd": 1,
        "highlightthickness": 2,
        "highlightbackground": BORDER,
        "highlightcolor": PRIMARY,
        "insertbackground": TEXT
    }

    BUTTON_PRIMARY = {
        "font": (FONT, 11, "bold"),
        "bg": PRIMARY,
        "fg": "#ffffff",
        "activebackground": PRIMARY_HOVER,
        "activeforeground": "#ffffff",
        "relief": "flat",
        "bd": 0,
        "padx": 15,
        "pady": 8,
        "cursor": "hand2"
    }

    BUTTON_SECONDARY = {
        "font": (FONT, 10),
        "bg": SECONDARY,
        "fg": TEXT,
        "activebackground": "#e2e8f0",
        "activeforeground": TEXT,
        "relief": "flat",
        "bd": 0,
        "padx": 8,
        "pady": 6,
        "cursor": "hand2"
    }

    BUTTON_CALC = {
        "font": (FONT, 10),
        "bg": "#ffffff",
        "fg": TEXT,
        "activebackground": SECONDARY,
        "activeforeground": TEXT,
        "relief": "solid",
        "bd": 1,
        "padx": 8,
        "pady": 6,
        "cursor": "hand2"
    }

class IntegralCalculatorGUI:
    """Clase principal para la interfaz gráfica"""
    
    def __init__(self, calculator):
        self.calculator = calculator
        self.root = None
        self.func_entry = None
        self.lower_limit_entry = None
        self.upper_limit_entry = None
        self.result_label = None
        self.ax = None
        self.canvas = None
        
    def create_gui(self):
        """Crea y configura la interfaz gráfica"""
        self.root = tk.Tk()
        self.root.title("Calculadora de Integrales Definidas")
        self.root.configure(bg=Style.BG)
        self.root.geometry("1400x800")
        self.root.minsize(1200, 700)
        
        # Configurar grid principal
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Crear panel izquierdo (calculadora)
        self._create_left_panel()
        
        # Crear panel derecho (gráfica)
        self._create_right_panel()
        
        return self.root
    
    def _create_left_panel(self):
        """Crea el panel izquierdo con la calculadora"""
        left_panel = Frame(self.root, bg=Style.BG, padx=20, pady=20)
        left_panel.grid(row=0, column=0, sticky="nsew")
        
        # Título
        title_label = Label(left_panel, text="Calculadora de Integrales", 
                           bg=Style.BG, fg=Style.TEXT, 
                           font=(Style.FONT, 18, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Frame de entrada con estilo de tarjeta
        self._create_input_card(left_panel)
        
        # Separador
        separator = Frame(left_panel, height=2, bg=Style.BORDER)
        separator.pack(fill="x", pady=20)
        
        # Frame de botones calculadora
        self._create_calculator_section(left_panel)
        
        # Frame de resultados
        self._create_result_section(left_panel)
    
    def _create_input_card(self, parent):
        """Crea la tarjeta de entrada de datos"""
        card_frame = Frame(parent, bg=Style.CARD_BG, relief="solid", bd=1)
        card_frame.pack(fill="x", pady=10)
        
        # Padding interno
        inner_frame = Frame(card_frame, bg=Style.CARD_BG)
        inner_frame.pack(fill="x", padx=15, pady=15)
        
        # Campo para la función
        Label(inner_frame, text="Función f(x):", bg=Style.CARD_BG, fg=Style.TEXT, 
              font=(Style.FONT, 12, "bold")).pack(anchor="w")
        self.func_entry = Entry(inner_frame, **Style.ENTRY)
        self.func_entry.pack(fill="x", pady=(5, 15))
        
        # Frame para límites
        limits_frame = Frame(inner_frame, bg=Style.CARD_BG)
        limits_frame.pack(fill="x")
        
        # Límite inferior
        left_limit_frame = Frame(limits_frame, bg=Style.CARD_BG)
        left_limit_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        Label(left_limit_frame, text="Límite inferior (a):", bg=Style.CARD_BG, fg=Style.TEXT, 
              font=(Style.FONT, 11, "bold")).pack(anchor="w")
        self.lower_limit_entry = Entry(left_limit_frame, **Style.ENTRY)
        self.lower_limit_entry.pack(fill="x", pady=(5, 0))
        
        # Límite superior
        right_limit_frame = Frame(limits_frame, bg=Style.CARD_BG)
        right_limit_frame.pack(side="left", fill="x", expand=True)
        
        Label(right_limit_frame, text="Límite superior (b):", bg=Style.CARD_BG, fg=Style.TEXT, 
              font=(Style.FONT, 11, "bold")).pack(anchor="w")
        self.upper_limit_entry = Entry(right_limit_frame, **Style.ENTRY)
        self.upper_limit_entry.pack(fill="x", pady=(5, 0))
        
        # Botones de acción
        button_frame = Frame(inner_frame, bg=Style.CARD_BG)
        button_frame.pack(fill="x", pady=(20, 0))
        
        calc_btn = Button(button_frame, text="📊 Calcular Integral", 
                         command=self.calculate_integral, **Style.BUTTON_PRIMARY)
        calc_btn.pack(side="left", padx=(0, 10))
        
        clear_btn = Button(button_frame, text="🗑️ Limpiar", 
                          command=self.clear_input, **Style.BUTTON_SECONDARY)
        clear_btn.pack(side="left")
    
    def _create_calculator_section(self, parent):
        """Crea la sección de botones de calculadora"""
        calc_label = Label(parent, text="Teclado Matemático", bg=Style.BG, fg=Style.TEXT, 
                          font=(Style.FONT, 14, "bold"))
        calc_label.pack(pady=(0, 10))
        
        calc_frame = Frame(parent, bg=Style.CARD_BG, relief="solid", bd=1)
        calc_frame.pack(fill="x", pady=10)
        
        # Padding interno
        inner_calc = Frame(calc_frame, bg=Style.CARD_BG)
        inner_calc.pack(padx=15, pady=15)
        
        buttons = [
            ['sin(', 'cos(', 'tan(', 'ln(', 'sqrt('],
            ['7', '8', '9', '(', ')'],
            ['4', '5', '6', '+', '-'],
            ['1', '2', '3', '*', '/'],
            ['0', '.', 'x', '^', 'π'],
            ['e', 'exp(', 'log(', '∞', '⌫']
        ]

        for i, row in enumerate(buttons):
            row_frame = Frame(inner_calc, bg=Style.CARD_BG)
            row_frame.pack(fill="x", pady=2)
            
            for j, val in enumerate(row):
                if val == '⌫':
                    btn = Button(row_frame, text=val, width=8, 
                               command=self.backspace, **Style.BUTTON_CALC)
                else:
                    btn = Button(row_frame, text=val, width=8, 
                               command=lambda v=val: self.insert_text(v), **Style.BUTTON_CALC)
                btn.pack(side="left", padx=2)
    
    def _create_result_section(self, parent):
        """Crea la sección de resultados"""
        result_label = Label(parent, text="Resultado", bg=Style.BG, fg=Style.TEXT, 
                            font=(Style.FONT, 14, "bold"))
        result_label.pack(pady=(20, 10))
        
        result_frame = Frame(parent, bg=Style.CARD_BG, relief="solid", bd=1)
        result_frame.pack(fill="both", expand=True, pady=10)
        
        # Padding interno
        inner_result = Frame(result_frame, bg=Style.CARD_BG)
        inner_result.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.result_label = Label(inner_result, text="Ingresa una función y presiona 'Calcular Integral'", 
                                 bg=Style.CARD_BG, fg=Style.TEXT_SECONDARY, 
                                 font=(Style.FONT_MONO, 10), justify="left", wraplength=350)
        self.result_label.pack(fill="both", expand=True)
    
    def _create_right_panel(self):
        """Crea el panel derecho con la gráfica"""
        right_panel = Frame(self.root, bg=Style.BG, padx=20, pady=20)
        right_panel.grid(row=0, column=1, sticky="nsew")
        
        # Título de la gráfica
        graph_title = Label(right_panel, text="Visualización Gráfica", 
                           bg=Style.BG, fg=Style.TEXT, 
                           font=(Style.FONT, 18, "bold"))
        graph_title.pack(pady=(0, 15))
        
        # Frame para la gráfica con estilo de tarjeta
        graph_frame = Frame(right_panel, bg=Style.CARD_BG, relief="solid", bd=1)
        graph_frame.pack(fill="both", expand=True)
        
        # Crear área de graficación
        self._create_plot_area(graph_frame)
    
    def _create_plot_area(self, parent):
        """Crea el área de graficación"""
        # Padding interno
        plot_container = Frame(parent, bg=Style.CARD_BG)
        plot_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Configurar matplotlib con estilo moderno
        plt_style = {
            'figure.facecolor': Style.CARD_BG,
            'axes.facecolor': '#ffffff',
            'axes.edgecolor': Style.BORDER,
            'axes.labelcolor': Style.TEXT,
            'axes.axisbelow': True,
            'xtick.color': Style.TEXT_SECONDARY,
            'ytick.color': Style.TEXT_SECONDARY,
            'grid.color': Style.BORDER,
            'grid.alpha': 0.6,
            'text.color': Style.TEXT
        }
        
        fig = Figure(figsize=(8, 6), dpi=100, facecolor=Style.CARD_BG)
        fig.patch.set_facecolor(Style.CARD_BG)
        
        self.ax = fig.add_subplot(111)
        self._setup_empty_plot()

        self.canvas = FigureCanvasTkAgg(fig, master=plot_container)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.draw()
    
    def _setup_empty_plot(self):
        """Configura una gráfica vacía con estilo moderno"""
        self.ax.set_facecolor('#ffffff')
        self.ax.grid(True, linestyle="-", alpha=0.3, color=Style.BORDER)
        self.ax.axhline(0, color=Style.TEXT_SECONDARY, linewidth=0.8, alpha=0.7)
        self.ax.axvline(0, color=Style.TEXT_SECONDARY, linewidth=0.8, alpha=0.7)
        self.ax.set_title("Gráfica de f(x)", fontsize=14, color=Style.TEXT, pad=20)
        self.ax.set_xlabel("x", fontsize=12, color=Style.TEXT)
        self.ax.set_ylabel("y", fontsize=12, color=Style.TEXT)
        
        # Configurar colores de los ejes
        self.ax.tick_params(colors=Style.TEXT_SECONDARY, which='both')
        for spine in self.ax.spines.values():
            spine.set_color(Style.BORDER)
    
    def backspace(self):
        """Elimina el último carácter del campo de función"""
        current_text = self.func_entry.get()
        if current_text:
            self.func_entry.delete(len(current_text)-1, tk.END)
        self.func_entry.focus()
    
    def insert_text(self, value):
        """Inserta texto en el campo de función"""
        # Mapear símbolos especiales
        symbol_map = {
            'π': 'pi',
            '∞': 'oo'
        }
        
        actual_value = symbol_map.get(value, value)
        self.func_entry.insert(tk.INSERT, actual_value)
        self.func_entry.focus()
    
    def calculate_integral(self):
        """Calcula la integral y actualiza la interfaz"""
        try:
            # Obtener valores de los campos
            func_str = self.func_entry.get().strip()
            lower_limit_str = self.lower_limit_entry.get().strip()
            upper_limit_str = self.upper_limit_entry.get().strip()
            
            # Validar campos vacíos
            if not func_str:
                messagebox.showwarning("Advertencia", "Por favor, ingresa una función.")
                return
            if not lower_limit_str or not upper_limit_str:
                messagebox.showwarning("Advertencia", "Por favor, ingresa ambos límites de integración.")
                return
            
            # Calcular usando la lógica
            result_def, result_indef, func, a, b = self.calculator.calculate_definite_integral(
                func_str, lower_limit_str, upper_limit_str
            )
            
            # Mostrar resultado con formato mejorado
            result_text = self._format_result_display(result_def, result_indef, a, b, func_str)
            self.result_label.config(text=result_text, fg=Style.TEXT)
            
            # Actualizar gráfica
            self._plot_function(func, a, b)
            
        except Exception as e:
            error_msg = str(e)
            if "Error en el cálculo" in error_msg:
                messagebox.showerror("Error de Cálculo", f"No se pudo calcular la integral:\n{error_msg}")
            else:
                messagebox.showerror("Error", f"Error inesperado:\n{error_msg}")
            
            # Mostrar error en el resultado
            self.result_label.config(text="❌ Error en el cálculo", fg=Style.ERROR)
    
    def _format_result_display(self, result_def, result_indef, a, b, func_str):
        """Formatea el resultado para una mejor visualización"""
        try:
            # Formatear el resultado numérico
            if abs(float(result_def)) < 1e-10:
                result_num = "0"
            elif abs(float(result_def)) > 1e6:
                result_num = f"{float(result_def):.2e}"
            else:
                result_num = f"{float(result_def):.6f}".rstrip('0').rstrip('.')
            
            result_text = f"✅ RESULTADO\n\n"
            result_text += f"Función: f(x) = {func_str}\n"
            result_text += f"Límites: [{a}, {b}]\n\n"
            result_text += f"∫ f(x) dx = {result_num}\n\n"
            result_text += f"Integral indefinida:\n∫ f(x) dx = {result_indef} + C"
            
            return result_text
            
        except Exception:
            return f"✅ RESULTADO\n\n∫ de {a} a {b} f(x) dx = {result_def}\n\nIntegral indefinida:\n∫ f(x) dx = {result_indef} + C"
    
    def _plot_function(self, func, a, b):
        """Grafica la función y el área bajo la curva con estilo moderno"""
        try:
            self.ax.clear()
            
            # Obtener valores para graficar
            x_vals, y_vals = self.calculator.get_function_values(func, a, b)
            
            # Configurar colores
            line_color = Style.PRIMARY
            fill_color = Style.ACCENT
            
            # Graficar función principal
            self.ax.plot(x_vals, y_vals, label="f(x)", color=line_color, linewidth=2.5, alpha=0.9)
            
            # Llenar área bajo la curva
            mask = (x_vals >= float(a)) & (x_vals <= float(b))
            self.ax.fill_between(x_vals, y_vals, where=mask, 
                               color=fill_color, alpha=0.3, label="Área integrada", 
                               interpolate=True)
            
            # Marcar límites de integración
            y_min, y_max = self.ax.get_ylim()
            self.ax.axvline(float(a), color=Style.ERROR, linestyle='--', alpha=0.8, linewidth=2, label=f'x = {a}')
            self.ax.axvline(float(b), color=Style.ERROR, linestyle='--', alpha=0.8, linewidth=2, label=f'x = {b}')
            
            # Configurar gráfica
            self._setup_plot_style()
            
            # Leyenda con estilo
            legend = self.ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)
            legend.get_frame().set_facecolor('#ffffff')
            legend.get_frame().set_alpha(0.9)
            
            # Actualizar canvas
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Error de Graficación", f"No se pudo graficar la función:\n{str(e)}")
            # Mostrar gráfica vacía en caso de error
            self.ax.clear()
            self._setup_empty_plot()
            self.canvas.draw()
    
    def _setup_plot_style(self):
        """Aplica estilo moderno a la gráfica"""
        self.ax.set_facecolor('#ffffff')
        self.ax.grid(True, linestyle="-", alpha=0.3, color=Style.BORDER)
        self.ax.axhline(0, color=Style.TEXT_SECONDARY, linewidth=0.8, alpha=0.7)
        self.ax.axvline(0, color=Style.TEXT_SECONDARY, linewidth=0.8, alpha=0.7)
        
        # Títulos y etiquetas
        self.ax.set_title("Gráfica de f(x) e Integral Definida", fontsize=14, color=Style.TEXT, pad=20)
        self.ax.set_xlabel("x", fontsize=12, color=Style.TEXT)
        self.ax.set_ylabel("f(x)", fontsize=12, color=Style.TEXT)
        
        # Configurar colores de los ejes
        self.ax.tick_params(colors=Style.TEXT_SECONDARY, which='both')
        for spine in self.ax.spines.values():
            spine.set_color(Style.BORDER)
    
    def clear_input(self):
        """Limpia todos los campos de entrada y la gráfica"""
        self.func_entry.delete(0, tk.END)
        self.lower_limit_entry.delete(0, tk.END)
        self.upper_limit_entry.delete(0, tk.END)
        self.result_label.config(text="Ingresa una función y presiona 'Calcular Integral'", 
                                fg=Style.TEXT_SECONDARY)
        # Limpiar gráfica
        self.ax.clear()
        self._setup_empty_plot()
        self.canvas.draw()
        # Enfocar el campo de función
        self.func_entry.focus()
    
    def run(self):
        """Inicia la aplicación"""
        if self.root:
            self.root.mainloop()