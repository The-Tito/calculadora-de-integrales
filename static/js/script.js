// static/js/script.js

document.addEventListener('DOMContentLoaded', () => {
    // Referencias a elementos del DOM
    const formulario = document.getElementById('calculadora-form');
    const resultadoDiv = document.getElementById('resultado');
    const graficaPlaceholder = document.getElementById('graph-placeholder');
    const statusMessage = document.getElementById('status-message');
    const navItems = document.querySelectorAll('.nav-item');
    const pageSections = document.querySelectorAll('.page-section');
    const historyList = document.getElementById('history-list');

    const clearHistoryBtn = document.getElementById('clear-history-btn');
    // Nueva referencia al botón de PDF
    const downloadPdfBtn = document.getElementById('download-pdf-btn');

    // Función para actualizar el estado en la barra inferior
    function updateStatus(message) {
        statusMessage.textContent = message;
    }

    // --- Funciones para manejar el Historial ---

    // Cargar historial desde localStorage
    function loadHistory() {
        const history = JSON.parse(localStorage.getItem('integralHistory')) || [];
        renderHistory(history);
    }

    // Guardar nuevo cálculo en el historial y en localStorage
    function saveToHistory(calculation) {
        const history = JSON.parse(localStorage.getItem('integralHistory')) || [];
        history.unshift(calculation); // Agregar al inicio del array
        localStorage.setItem('integralHistory', JSON.stringify(history));
        renderHistory(history);
    }

    // Renderizar el historial en la página
    function renderHistory(history) {
        historyList.innerHTML = ''; // Limpiar el contenido anterior

        if (history.length === 0) {
            historyList.innerHTML = '<p class="empty-message">Aún no hay operaciones en el historial.</p>';
            return;
        }

        history.forEach((item, index) => {
            const historyItem = document.createElement('div');
            historyItem.classList.add('history-item');
            historyItem.innerHTML = `
                <div class="history-content">
                    <p class="history-formula">∫(${item.funcion}) dx de ${item.limiteInferior} a ${item.limiteSuperior}</p>
                    <p class="history-result">${item.resultado}</p>
                </div>
                <div class="history-actions">
                    <button class="repeat-btn" data-index="${index}"><i class="fas fa-redo-alt"></i></button>
                    <button class="delete-btn" data-index="${index}"><i class="fas fa-trash-alt"></i></button>
                </div>
            `;
            historyList.appendChild(historyItem);
        });

        document.querySelectorAll('.repeat-btn').forEach(button => {
            button.addEventListener('click', (e) => repeatCalculation(e.target.dataset.index));
        });
        document.querySelectorAll('.delete-btn').forEach(button => {
            button.addEventListener('click', (e) => deleteHistoryItem(e.target.dataset.index));
        });
    }

    function repeatCalculation(index) {
        const history = JSON.parse(localStorage.getItem('integralHistory'));
        const itemToRepeat = history[index];

        document.getElementById('funcion').value = itemToRepeat.funcion;
        document.getElementById('limite_inferior').value = itemToRepeat.limiteInferior;
        document.getElementById('limite_superior').value = itemToRepeat.limiteSuperior;

        showSection('#calculator-section');
        document.querySelector('.nav-item.active-nav-item').classList.remove('active-nav-item');
        document.querySelector('a[href="#calculator-section"]').classList.add('active-nav-item');

        formulario.requestSubmit();
    }

    function deleteHistoryItem(index) {
        const history = JSON.parse(localStorage.getItem('integralHistory'));
        history.splice(index, 1);
        localStorage.setItem('integralHistory', JSON.stringify(history));
        renderHistory(history);
    }

    function clearHistory() {
        if (confirm('¿Estás seguro de que quieres borrar todo el historial?')) {
            localStorage.removeItem('integralHistory');
            renderHistory([]);
            updateStatus('Historial borrado.');
        }
    }
    
    // --- NUEVA FUNCIÓN PARA GENERAR EL PDF ---
    async function generatePdf() {
    updateStatus('Generando PDF...');
    
    try {
        // Crear un contenedor temporal para el PDF
        const pdfContainer = document.createElement('div');
        pdfContainer.style.cssText = `
            position: absolute;
            top: -9999px;
            left: 0;
            width: 800px;
            background: white;
            padding: 30px;
            font-family: 'Poppins', sans-serif;
            color: #34495e;
        `;
        
        // Obtener los datos actuales
        const funcion = document.getElementById('funcion').value;
        const limiteInferior = document.getElementById('limite_inferior').value;
        const limiteSuperior = document.getElementById('limite_superior').value;
        const resultadoContent = document.getElementById('resultado').innerHTML;
        const graficaImg = document.querySelector('#graph-placeholder img');
        
        // Crear el contenido del PDF
        pdfContainer.innerHTML = `
            <div style="text-align: center; margin-bottom: 30px; border-bottom: 2px solid #3498db; padding-bottom: 20px;">
                <h1 style="color: #2c3e50; margin: 0; font-size: 28px;">
                    <i class="fas fa-calculator" style="color: #3498db; margin-right: 10px;"></i>
                    Calculadora de Integrales
                </h1>
                <p style="color: #7f8c8d; margin: 10px 0 0 0;">Resultado del cálculo</p>
            </div>
            
            <div style="margin-bottom: 25px;">
                <h3 style="color: #2c3e50; margin-bottom: 15px; font-size: 18px;">Datos de entrada:</h3>
                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #3498db;">
                    <p style="margin: 5px 0;"><strong>Función:</strong> f(x) = ${funcion}</p>
                    <p style="margin: 5px 0;"><strong>Límite inferior:</strong> a = ${limiteInferior}</p>
                    <p style="margin: 5px 0;"><strong>Límite superior:</strong> b = ${limiteSuperior}</p>
                </div>
            </div>
            
            <div style="margin-bottom: 25px;">
                <h3 style="color: #2c3e50; margin-bottom: 15px; font-size: 18px;">Resultado:</h3>
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; font-family: 'Roboto Mono', monospace; white-space: pre-wrap; line-height: 1.6;">
                    ${resultadoContent}
                </div>
            </div>
            
            ${graficaImg ? `
                <div style="margin-bottom: 25px;">
                    <h3 style="color: #2c3e50; margin-bottom: 15px; font-size: 18px;">Gráfica:</h3>
                    <div style="text-align: center; background: #f8f9fa; padding: 20px; border-radius: 8px;">
                        <img src="${graficaImg.src}" style="max-width: 100%; height: auto; border-radius: 8px; border: 1px solid #dfe6e9;" />
                    </div>
                </div>
            ` : ''}
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #dfe6e9; text-align: center; color: #7f8c8d; font-size: 12px;">
                <p>Generado el ${new Date().toLocaleString('es-ES')}</p>
            </div>
        `;
        
        // Agregar el contenedor al body temporalmente
        document.body.appendChild(pdfContainer);
        
        // Esperar un momento para que se renderice
        await new Promise(resolve => setTimeout(resolve, 100));
        
        // Capturar el contenido con html2canvas
        const canvas = await html2canvas(pdfContainer, {
            scale: 2,
            useCORS: true,
            allowTaint: true,
            backgroundColor: '#ffffff',
            width: 800,
            height: pdfContainer.scrollHeight
        });
        
        // Remover el contenedor temporal
        document.body.removeChild(pdfContainer);
        
        const imgData = canvas.toDataURL('image/png');
        
        // Crear el documento PDF con jsPDF
        const { jsPDF } = window.jspdf;
        const pdf = new jsPDF('p', 'mm', 'a4');
        
        // Calcular dimensiones para ajustar al PDF
        const imgProps = pdf.getImageProperties(imgData);
        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pdfHeight = pdf.internal.pageSize.getHeight();
        const imgWidth = pdfWidth - 20; // Margen de 10mm a cada lado
        const imgHeight = (imgProps.height * imgWidth) / imgProps.width;
        
        // Si la imagen es más alta que la página, ajustar y crear múltiples páginas si es necesario
        if (imgHeight > pdfHeight - 20) {
            const ratio = (pdfHeight - 20) / imgHeight;
            const finalWidth = imgWidth * ratio;
            const finalHeight = imgHeight * ratio;
            pdf.addImage(imgData, 'PNG', 10, 10, finalWidth, finalHeight);
        } else {
            pdf.addImage(imgData, 'PNG', 10, 10, imgWidth, imgHeight);
        }
        
        // Generar nombre de archivo con timestamp
        const timestamp = new Date().toISOString().slice(0, 10);
        const filename = `integral_${timestamp}.pdf`;
        
        // Descargar el archivo
        pdf.save(filename);
        updateStatus('PDF descargado exitosamente.');
        
    } catch (error) {
        console.error('Error al generar el PDF:', error);
        updateStatus('Error al generar el PDF. Por favor, inténtalo de nuevo.');
    }
}
    // --- Lógica de la Calculadora ---
    formulario.addEventListener('submit', async (e) => {
        e.preventDefault();

        resultadoDiv.innerHTML = '';
        graficaPlaceholder.innerHTML = '<p>Calculando...</p>';
        updateStatus('Calculando la integral...');
        downloadPdfBtn.style.display = 'none'; // Ocultar el botón al iniciar un nuevo cálculo

        const funcion = document.getElementById('funcion').value;
        const limiteInferior = document.getElementById('limite_inferior').value;
        const limiteSuperior = document.getElementById('limite_superior').value;

        if (!funcion || !limiteInferior || !limiteSuperior) {
            resultadoDiv.innerHTML = `<h3 class="error">Error de Validación</h3><p>Todos los campos son obligatorios.</p>`;
            graficaPlaceholder.innerHTML = '<p>La gráfica aparecerá aquí.</p>';
            updateStatus('Error: Campos incompletos.');
            return;
        }

        try {
            const response = await fetch('/calcular', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ funcion, limite_inferior: limiteInferior, limite_superior: limiteSuperior }),
            });

            const data = await response.json();

            if (data.exito) {
                resultadoDiv.innerHTML = data.resultado_texto;
                graficaPlaceholder.innerHTML = `<img src="${data.grafica_url}" alt="Gráfica de la función">`;
                updateStatus('Cálculo completado exitosamente.');
                downloadPdfBtn.style.display = 'block'; // Mostrar el botón si el cálculo es exitoso

                saveToHistory({
                    funcion: funcion,
                    limiteInferior: limiteInferior,
                    limiteSuperior: limiteSuperior,
                    resultado: data.resultado_texto.replace(/<[^>]*>?/gm, '').trim()
                });

            } else {
                resultadoDiv.innerHTML = `<h3 class="error">Error en el Cálculo</h3><p>${data.error}</p>`;
                graficaPlaceholder.innerHTML = '<p>La gráfica no se pudo generar debido a un error.</p>';
                updateStatus('Error en el cálculo: ' + data.error);
                downloadPdfBtn.style.display = 'none'; // Ocultar el botón si hay un error
            }
        } catch (error) {
            console.error('Error al enviar la solicitud:', error);
            resultadoDiv.innerHTML = `<h3 class="error">Error del Servidor</h3><p>No se pudo conectar con el servidor. Por favor, inténtalo de nuevo más tarde.</p>`;
            graficaPlaceholder.innerHTML = '<p>La gráfica no se pudo generar debido a un error.</p>';
            updateStatus('Error de conexión.');
            downloadPdfBtn.style.display = 'none'; // Ocultar el botón si hay un error de conexión
        }
    });

    // --- Lógica de Navegación ---
    function showSection(sectionId) {
        pageSections.forEach(section => {
            section.classList.remove('active-section');
        });
        const targetSection = document.querySelector(sectionId);
        if (targetSection) {
            targetSection.classList.add('active-section');
            if (sectionId === '#history-section') {
                loadHistory();
            }
        }
    }

    navItems.forEach(item => {
        item.addEventListener('click', (event) => {
            event.preventDefault();
            navItems.forEach(nav => nav.classList.remove('active-nav-item'));
            item.classList.add('active-nav-item');
            const sectionId = item.getAttribute('href');
            showSection(sectionId);
        });
    });

    if (clearHistoryBtn) {
        clearHistoryBtn.addEventListener('click', clearHistory);
    }
    
    // --- Event listener para el botón de PDF ---
    if (downloadPdfBtn) {
        downloadPdfBtn.addEventListener('click', generatePdf);
    }
    
    // Cargar historial al inicio
    loadHistory();
});