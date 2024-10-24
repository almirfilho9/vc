import os
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, Text
import sys

def convert_video(input_file, output_file, progress_text=None):
    command = ['ffmpeg', '-i', input_file, output_file]

    # Inicializa o subprocesso
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Lê a saída em tempo real
    while True:
        output = process.stderr.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            if progress_text:
                progress_text.insert(tk.END, output.strip() + "\n")  # Adiciona a nova saída
                progress_text.see(tk.END)  # Rola para o final do texto
            else:
                print(output.strip())  # Exibe no console

    process.wait()  # Aguarda a conclusão do processo
    if process.returncode == 0:
        if progress_text:
            progress_text.insert(tk.END, "Conversão concluída.\n")
            messagebox.showinfo("Sucesso", f"Arquivo convertido para: {output_file}")
        else:
            print("Conversão concluída.")
    else:
        if progress_text:
            messagebox.showerror("Erro", "Erro durante a conversão do vídeo.")
        else:
            print("Erro durante a conversão do vídeo.")

def convert_and_show_progress(input_file, output_file, progress_text):
    threading.Thread(target=run_conversion, args=(input_file, output_file, progress_text)).start()

def run_conversion(input_file, output_file, progress_text):
    convert_video(input_file, output_file, progress_text)

def select_input_file():
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Todos os Arquivos", "*.*"),
            ("Vídeo", "*.mp4;*.avi;*.mkv;*.mov;*.webm;*.flv;*.wmv;*.mpeg;*.mts;*.dv;*.vob"),
            ("Áudio", "*.mp3;*.wav;*.aac;*.ogg;*.flac;*.wma;*.m4a"),
            ("Imagem", "*.jpg;*.jpeg;*.png;*.bmp;*.gif;*.tiff")
        ]
    )
    input_entry.delete(0, tk.END)
    input_entry.insert(0, file_path)

def select_output_file():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".mp4", 
        filetypes=[
            ("Todos os Arquivos", "*.*"),
            ("Vídeo", "*.mp4;*.avi;*.mkv;*.mov;*.webm;*.flv;*.wmv;*.mpeg"),
            ("Áudio", "*.mp3;*.wav;*.aac;*.ogg;*.flac;*.wma;*.m4a"),
            ("Imagem", "*.jpg;*.jpeg;*.png;*.bmp;*.gif;*.tiff")
        ]
    )
    output_entry.delete(0, tk.END)
    output_entry.insert(0, file_path)

def start_conversion():
    input_file = input_entry.get()
    output_file = output_entry.get()
    if input_file and output_file:
        progress_text.delete(1.0, tk.END)  # Limpa a área de texto antes da conversão
        progress_text.insert(tk.END, "Processando...\n")  # Mensagem inicial
        convert_and_show_progress(input_file, output_file, progress_text)
    else:
        messagebox.showwarning("Aviso", "Por favor, selecione arquivos de entrada e saída.")

def main_gui():
    # Configuração da interface gráfica
    app = tk.Tk()
    app.title("Conversor de Vídeo - Estilo Hacker")
    app.configure(bg="black")
    app.geometry("600x400")

    # Estilo de fonte
    font_style = ("Courier", 12)

    # Frame para o campo de entrada
    input_frame = tk.Frame(app, bg="black")
    input_frame.pack(pady=10)

    global input_entry
    input_entry = tk.Entry(input_frame, width=40, bg="black", fg="green", insertbackground='green', font=font_style)
    input_entry.pack(side=tk.LEFT)

    input_button = tk.Button(input_frame, text="IN", command=select_input_file, bg="black", fg="green", font=font_style)
    input_button.pack(side=tk.LEFT)

    # Frame para o campo de saída
    output_frame = tk.Frame(app, bg="black")
    output_frame.pack(pady=10)

    global output_entry
    output_entry = tk.Entry(output_frame, width=40, bg="black", fg="green", insertbackground='green', font=font_style)
    output_entry.pack(side=tk.LEFT)

    output_button = tk.Button(output_frame, text="OUT", command=select_output_file, bg="black", fg="green", font=font_style)
    output_button.pack(side=tk.LEFT)

    convert_button = tk.Button(app, text="Converter", command=start_conversion, bg="black", fg="green", font=font_style)
    convert_button.pack(pady=20)

    # Área de texto para mostrar o progresso
    global progress_text
    progress_text = Text(app, height=10, width=70, bg="black", fg="green", font=font_style)
    progress_text.pack(pady=10)

    app.mainloop()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        convert_video(input_file, output_file)
    else:
        main_gui()
