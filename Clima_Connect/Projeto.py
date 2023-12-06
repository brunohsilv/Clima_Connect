from rethinkdb import RethinkDB
import time
import smtplib
from email.mime.text import MIMEText
import pywhatkit as kit

r = RethinkDB()

# Informações de acesso ao servidor RethinkDB
host = '200.17.86.19'
port = 58015
db = 'santa_rosa'
user = 'gustavo.drews@sou.unijui.edu.br'
password = 'fwe43f34S&2'

# Informações para o e-mail
smtp_server = 'smtp.office365.com'
smtp_port = 587
smtp_username = 'email_do_remetente_tem_que_ser_outlook'
smtp_password = 'senha_do_email_do_remetente'
sender_email = 'email_do_remetente_tem_que_ser_outlook'
receiver_email = 'email_do_destinatario'

# Números fictícios (substitua pelos números reais)
seu_numero = "+5555991160246"
numero_destino = "+5555991844457"

# Mensagem a ser enviada
mensagem_whatsapp = "Banco sem Sinal"

try:
    # Tente conectar ao banco de dados RethinkDB
    conn = r.connect(
        host=host,
        port=port,
        db=db,
        user=user,
        password=password
    ).repl()

    # Se a conexão for bem-sucedida, imprima uma mensagem
    print("Conexão ao RethinkDB bem-sucedida!")

    tempo_maximo = 30  # Tempo máximo em segundos
    tempo_passado = 0
    tempo_inicio = time.time()

    # Obtenha o timestamp inicial da última atualização
    ultimo_timestamp = None

    while tempo_passado < tempo_maximo:
        # Registrar o tempo no início do loop
        tempo_inicio_loop = time.time()

        # Realizar uma consulta para verificar se o banco está atualizando
        resultado = list(r.table('estacoes_metereologicas').run(conn))

        # Obter o timestamp mais recente da tabela
        novo_timestamp = resultado[0].get('timestamp') if resultado else None

        # Verificar se houve uma nova informação desde a última verificação
        if novo_timestamp != ultimo_timestamp:
            # Calcular o tempo levado para receber uma nova informação
            tempo_atualizacao = time.time() - tempo_inicio_loop
            print(f"Conectado! Novo dado recebido. Tempo: {tempo_atualizacao:.2f} segundos")
            # Atualizar o timestamp mais recente
            ultimo_timestamp = novo_timestamp
        else:
            # Atualizar o tempo total passado
            tempo_passado += (time.time() - tempo_inicio_loop)

            # Verificar se o tempo total é maior que 0.10 segundos antes de imprimir "Desconectado"
            if tempo_passado > 0.10:
                print(f"Desconectado! Tempo: {tempo_passado:.2f} segundos")

                # Enviar e-mail se o tempo for maior que 0.10 segundos
                msg = MIMEText("Banco de dados sem sinal")
                msg['Subject'] = 'Alerta de Banco de Dados'
                msg['From'] = sender_email
                msg['To'] = receiver_email

                try:
                    with smtplib.SMTP(smtp_server, smtp_port) as server:
                        server.starttls()
                        server.login(smtp_username, smtp_password)
                        server.sendmail(sender_email, [receiver_email], msg.as_string())
                        print("E-mail enviado com sucesso!")
                except Exception as e:
                    print(f"Erro ao enviar e-mail: {e}")

                # Enviar mensagem por WhatsApp
                kit.sendwhatmsg_instantly(numero_destino, mensagem_whatsapp, wait_time=10)
                print("Mensagem de WhatsApp enviada!")

                break
            else:
                print(f"Conectado! Tempo: {tempo_passado:.2f} segundos")

        # Esperar 1 segundo antes da próxima verificação
        time.sleep(1)

    # Imprimir o tempo total
    print(f"Tempo total: {tempo_passado:.2f} segundos")

except r.errors.ReqlDriverError as e:
    # Se ocorrer um erro de conexão, imprima a mensagem de erro
    print(f"Erro de conexão ao RethinkDB: {e}")

finally:
    # Feche a conexão, independentemente do resultado
    if conn.is_open():
        conn.close()
        print("Conexão fechada.")
