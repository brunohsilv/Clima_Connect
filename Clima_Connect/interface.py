import tkinter as tk
import subprocess

monitoramento_iniciado = False

def iniciar_monitoramento(caminho_main, status_label, iniciar_button, finalizar_button, Alertas_text):
    global monitoramento_iniciado
    
    status_label.config(text="Em monitoramento...")
    iniciar_button.config(state=tk.DISABLED)
    finalizar_button.config(state=tk.NORMAL, bg="red")  
    monitoramento_iniciado = True

    # Lê o conteúdo do arquivo PyWhatKit_DB.txt e exibe no campo de Alertas
    with open("PyWhatKit_DB.txt", "r") as arquivo:
        conteudo = arquivo.read()
        Alertas_text.insert(tk.END, conteudo)

    # Inicia a execução do main.py
    subprocess.Popen(["python3", caminho_main])

def finalizar_monitoramento(status_label, iniciar_button, finalizar_button, Alertas_text):
    global monitoramento_iniciado
    
    status_label.config(text="Monitoramento finalizado.")
    iniciar_button.config(state=tk.NORMAL)
    finalizar_button.config(state=tk.DISABLED, bg="gray")
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
logo_image_resized = logo_image.subsample(5, 5)  
logo_label = tk.Label(root, image=logo_image_resized)
logo_label.image = logo_image_resized  
logo_label.pack(side=tk.TOP, pady=10)

status_label = tk.Label(root, text="Monitoramento não iniciado.")
status_label.pack()

iniciar_button = tk.Button(root, text="Iniciar Monitoramento", command=lambda: iniciar_monitoramento("/home/gustavo/DocumentosProgramação/Clima_Connect/Clima_Connect/main.py", status_label, iniciar_button, finalizar_button, Alertas_text), bg="green")
iniciar_button.pack()

finalizar_button = tk.Button(root, text="Finalizar Monitoramento", command=lambda: finalizar_monitoramento(status_label, iniciar_button, finalizar_button, Alertas_text), bg="gray", state=tk.DISABLED)
finalizar_button.pack()

Alertas_frame = tk.Frame(root)
Alertas_frame.pack()

Alertas_label = tk.Label(Alertas_frame, text="Alertas de monitoramento:")
Alertas_label.pack()

# Widget Text para exibir a saída do Alertas
Alertas_text = tk.Text(Alertas_frame, height=20, width=160)
Alertas_text.pack()

root.mainloop()
