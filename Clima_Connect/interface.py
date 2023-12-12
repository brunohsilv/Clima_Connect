import tkinter as tk
import subprocess

monitoramento_iniciado = False

def iniciar_monitoramento(caminho_main, status_label, iniciar_button, finalizar_button):
    global monitoramento_iniciado
    
    status_label.config(text="Em monitoramento")
    iniciar_button.config(state=tk.DISABLED)
    finalizar_button.config(state=tk.NORMAL, bg="red")  # Altera a cor para vermelho
    monitoramento_iniciado = True

    # Inicia a execução do main.py
    subprocess.Popen(["python3", caminho_main])

def finalizar_monitoramento(status_label, iniciar_button, finalizar_button):
    global monitoramento_iniciado
    
    status_label.config(text="Monitoramento finalizado")
    iniciar_button.config(state=tk.NORMAL)
    finalizar_button.config(state=tk.DISABLED, bg="gray")  # Volta para a cor cinza
    monitoramento_iniciado = False
    
    # Encerra a execução do main.py
    subprocess.Popen(["pkill", "-f", "main.py"])

root = tk.Tk()
root.title("Monitoramento de Banco de Dados")
root.geometry("400x400")

empresa_label = tk.Label(root, text="Clima Connect")
empresa_label.pack()

# Carrega a imagem do logo
logo_image = tk.PhotoImage(file="/home/gustavo/DocumentosProgramação/Clima_Connect/Clima_Connect/ClimaConnect-Logo.png")
# Redimensiona a imagem do logo
logo_image_resized = logo_image.subsample(5, 5)  # Substitua os números para redimensionar a imagem conforme necessário
logo_label = tk.Label(root, image=logo_image_resized)
logo_label.image = logo_image_resized  # Mantém uma referência à imagem para que ela não seja descartada pelo garbage collector
logo_label.pack(side=tk.TOP, pady=10)

status_label = tk.Label(root, text="Monitoramento não iniciado")
status_label.pack()

iniciar_button = tk.Button(root, text="Iniciar Monitoramento", command=lambda: iniciar_monitoramento("/home/gustavo/DocumentosProgramação/Clima_Connect/Clima_Connect/main.py", status_label, iniciar_button, finalizar_button), bg="green")
iniciar_button.pack()

finalizar_button = tk.Button(root, text="Finalizar Monitoramento", command=lambda: finalizar_monitoramento(status_label, iniciar_button, finalizar_button), bg="gray", state=tk.DISABLED)
finalizar_button.pack()

terminal_frame = tk.Frame(root)
terminal_frame.pack()

terminal_label = tk.Label(terminal_frame, text="Terminal:")
terminal_label.pack()

# Widget Text para exibir a saída do terminal
terminal_text = tk.Text(terminal_frame, height=10, width=50)
terminal_text.pack()

root.mainloop()
