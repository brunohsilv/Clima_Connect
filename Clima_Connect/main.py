from connection import connect_to_rethinkdb, connect_to_postgresql
import smtplib
from email.mime.text import MIMEText
import pywhatkit as kit
import time
from rethinkdb import RethinkDB

r = RethinkDB()

# Função para enviar e-mail
def send_email(sender_email, receiver_email, smtp_server, smtp_port, smtp_username, smtp_password, db_type):
    msg = MIMEText(f"Prezado cliente, nosso monitoramento não recebeu nenhum sinal sobre o seu banco de dados {db_type}, verifique se o mesmo está ativo.")
    msg['Subject'] = 'Alerta de Monitoramento de Banco de Dados'
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

# Informações para o e-mail
smtp_server = 'smtp.office365.com'
smtp_port = 587
smtp_username = 'climaconnectremetente@outlook.com'
smtp_password = 'gTV@85qL'
sender_email = 'climaconnectremetente@outlook.com'
receiver_email = 'climaconnectremetente@outlook.com'

# Informações para o envio por WhatsApp
seu_numero = "+5555991667802"
numero_destino = "+5555991667802"

try:
    conn_rethink = connect_to_rethinkdb('200.17.86.19', 58015, 'santa_rosa', 'gustavo.drews@sou.unijui.edu.br', 'fwe43f34S&2')

    if conn_rethink:
        print("Conexão ao RethinkDB bem-sucedida!")

        tempo_maximo = 30
        tempo_passado = 0
        tempo_inicio = time.time()

        ultimo_timestamp = None

        while tempo_passado < tempo_maximo:
            tempo_inicio_loop = time.time()

            resultado = list(r.table('estacoes_metereologicas').run(conn_rethink))

            novo_timestamp = resultado[0].get('timestamp') if resultado else None

            if novo_timestamp != ultimo_timestamp:
                tempo_atualizacao = time.time() - tempo_inicio_loop
                print(f"Conectado! Novo dado recebido. Tempo: {tempo_atualizacao:.2f} segundos")
                ultimo_timestamp = novo_timestamp
            else:
                tempo_passado += (time.time() - tempo_inicio_loop)

                if tempo_passado > 0.10:
                    print(f"Desconectado! Tempo: {tempo_passado:.2f} segundos")

                    # Enviar e-mail se o tempo for maior que 0.10 segundos
                    send_email(sender_email, receiver_email, smtp_server, smtp_port, smtp_username, smtp_password, "RethinkDB")

                    break
                else:
                    print(f"Conectado! Tempo: {tempo_passado:.2f} segundos")

            time.sleep(1)

        print(f"Tempo total: {tempo_passado:.2f} segundos")

    else:
        print("Não foi possível conectar ao RethinkDB.")

except Exception as e:
    print(f"Erro: {e}")

# Verificar condição para enviar mensagem por WhatsApp
if tempo_passado > 0.10:
    print(f"Desconectado! Tempo: {tempo_passado:.2f} segundos")

    # Enviar mensagem por WhatsApp imediatamente
    msg_whatsapp = f"Prezado cliente, nosso monitoramento não recebeu nenhum sinal sobre o seu banco de dados RethinkDB, verifique se o mesmo está ativo."
    kit.sendwhatmsg_instantly(numero_destino, msg_whatsapp)
    print("Mensagem de WhatsApp enviada!")

# Conectar ao banco de dados PostgreSQL
try:
    conn_postgresql = connect_to_postgresql('200.17.86.20', '55432', 'santa_rosa', 'gustavo.drews@sou.unijui.edu.br', 'fwe43f34S&2')

    if conn_postgresql:
        print("Conexão ao PostgreSQL bem-sucedida!")

        while True:
            # Criar um cursor
            cursor = conn_postgresql.cursor()

            # Consulta para verificar o último registro na coluna "time"
            cursor.execute("SELECT MAX(time) FROM nit2xli")
            ultimo_registro = cursor.fetchone()[0]

            cursor.close()

            # Verificar se passaram mais de 2 minutos desde o último registro
            if ultimo_registro and (time.time() - ultimo_registro.timestamp()) > 120:  # 120 segundos = 2 minutos
                print("Não houve novos registros nos últimos 2 minutos! Enviando e-mail e mensagem por WhatsApp...")

                # Enviar e-mail
                send_email(sender_email, receiver_email, smtp_server, smtp_port, smtp_username, smtp_password, "Postgre - Tabela: nit2xli")

                # Enviar mensagem por WhatsApp
                msg_whatsapp = (
                 f"Prezado cliente, não foram encontrados novos registros na tabela nit2xli do seu banco de dados PostgreSQL nos últimos 2 minutos. "
                "Verifique se as estações Unijuí, Aeroporto e Cruzeiro estão funcionando corretamente."
                )
                kit.sendwhatmsg_instantly(numero_destino, msg_whatsapp)
                print("E-mail e mensagem de WhatsApp enviados! - Postgre nit2xli")
            # Aguardar 2 minutos antes da próxima verificação
            time.sleep(120)

except Exception as e:
    print(f"Erro ao conectar ao PostgreSQL: {e}")