from connection import connect_to_rethinkdb, connect_to_postgresql
import smtplib
from rethinkdb import RethinkDB
from email.mime.text import MIMEText
import time

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

try:
    # Conectar ao banco de dados RethinkDB
    conn_rethink = connect_to_rethinkdb('200.17.86.19', 58015, 'santa_rosa', 'gustavo.drews@sou.unijui.edu.br', 'fwe43f34S&2')
    
    if conn_rethink:
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
            # Substitua a tabela e o campo pela sua tabela e campo reais
            resultado = list(r.table('estacoes_metereologicas').run(conn_rethink))

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
                    send_email(sender_email, receiver_email, smtp_server, smtp_port, smtp_username, smtp_password, "RethinkDB")

                    break
                else:
                    print(f"Conectado! Tempo: {tempo_passado:.2f} segundos")

            # Esperar 1 segundo antes da próxima verificação
            time.sleep(1)

        # Imprimir o tempo total
        print(f"Tempo total: {tempo_passado:.2f} segundos")

    else:
        print("Não foi possível conectar ao RethinkDB.")

    # Conectar ao banco de dados PostgreSQL
    conn_postgresql = connect_to_postgresql('200.17.86.20', 55432, 'santa_rosa', 'gustavo.drews@sou.unijui.edu.br', 'fwe43f34S&2')

    if conn_postgresql:
        print("Conexão ao PostgreSQL bem-sucedida!")

except Exception as e:
    print(f"Erro: {e}")
