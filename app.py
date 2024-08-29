import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import cv2
import pytesseract
import pdfplumber
from PIL import Image, ImageTk

# Função para carregar o arquivo e realizar OCR
def carregar_arquivo():
    filepath = filedialog.askopenfilename(
        filetypes=[("PDF Files", "*.pdf"), ("PNG Files", "*.png"), ("All Files", "*.*")]
    )
    if not filepath:
        return

    if filepath.lower().endswith('.png'):
        processar_png(filepath)
    elif filepath.lower().endswith('.pdf'):
        processar_pdf(filepath)
    else:
        messagebox.showerror("Erro", "Formato de arquivo não suportado.")

# Função para processar arquivos PNG
def processar_png(filepath):
    # Carregar a imagem com OpenCV
    img = cv2.imread(filepath)
    if img is None:
        messagebox.showerror("Erro", "Falha ao carregar a imagem.")
        return
    
    # Apontar para o executável do Tesseract
    pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\Gabriel\\Desktop\\Tessaret_new\\Tesseract.exe"
    
    # Realizar OCR
    resultado = pytesseract.image_to_string(img)
    
    # Exibir o resultado na interface
    resultado_text.delete(1.0, tk.END)
    resultado_text.insert(tk.END, resultado)
    
    # Mostrar a imagem carregada
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(image=img_pil)
    imagem_label.config(image=img_tk)
    imagem_label.image = img_tk  # Manter referência para evitar que a imagem seja destruída pelo garbage collector

# Função para processar arquivos PDF em blocos
def processar_pdf(filepath, paginas_por_bloco=50):
    try:
        with pdfplumber.open(filepath) as pdf:
            total_paginas = len(pdf.pages)
            texto_extraido = ""
            
            for i in range(0, total_paginas, paginas_por_bloco):
                bloco_paginas = pdf.pages[i:i+paginas_por_bloco]
                for pagina in bloco_paginas:
                    texto_extraido += pagina.extract_text() + "\n"
                
                # Atualiza a interface após cada bloco (opcional)
                resultado_text.delete(1.0, tk.END)
                resultado_text.insert(tk.END, texto_extraido)
                root.update_idletasks()  # Atualiza a interface gráfica

        if not texto_extraido:
            messagebox.showinfo("Aviso", "Nenhum texto encontrado no PDF.")
        else:
            resultado_text.delete(1.0, tk.END)
            resultado_text.insert(tk.END, texto_extraido)

    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao ler o PDF: {str(e)}")

# Criar a janela principal
root = tk.Tk()
root.title("Leitor de Texto de Imagens e PDFs (OCR)")

# Botão para carregar o arquivo
carregar_btn = tk.Button(root, text="Carregar Arquivo", command=carregar_arquivo)
carregar_btn.pack(pady=10)

# Label para exibir a imagem carregada
imagem_label = tk.Label(root)
imagem_label.pack()

# Área de texto para exibir o resultado
resultado_text = tk.Text(root, height=20, width=80)
resultado_text.pack(pady=10)

# Iniciar o loop principal da interface
root.mainloop()
