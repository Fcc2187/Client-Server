import socket
import random

HOST = "127.0.0.1"
PORT = 5001

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Servidor aguardando conexões na porta {PORT}...")

conn, addr = server_socket.accept()
print(f"Conexão estabelecida com {addr}")

try:
    # Recebendo handshake
    dados_handshake = conn.recv(1024).decode()
    modo_operacao, tamanho_max = dados_handshake.split(",")
    tamanho_max = int(tamanho_max)
    print(f"Modo de operação: {modo_operacao}\nTamanho máximo por pacote: {tamanho_max}")

    # Confirmar handshake
    conn.sendall(f"HANDSHAKE_OK:{modo_operacao}".encode())

    # Dicionário para armazenar pacotes recebidos
    mensagem_reconstruida = {}

    while True:
        pacote = conn.recv(1024).decode()

        if pacote == "FIM":
            break  # Finaliza ao receber "FIM"

        if len(pacote) < 3:
            print(f"Pacote inválido: '{pacote}'")
            continue

        pacote_id, flag, carga = int(pacote[:2]), pacote[2], pacote[3:]
        
        # Simulação de perda de pacotes
        if modo_operacao == "2" and random.random() < 0.2:  # 20% de chance de perda
            print(f"Pacote {pacote_id} perdido!")
            continue
        
        # Simulação de erro nos pacotes
        if modo_operacao == "3" and random.random() < 0.2:  # 20% de chance de erro
            carga = "X" * len(carga)  # Corrompe os dados
            print(f"Pacote {pacote_id} corrompido!")
        
        # Verifica se o tamanho do pacote é maior que o permitido
        if len(carga) > tamanho_max:
            print(f"Erro: Pacote {pacote_id} excede o tamanho máximo permitido ({tamanho_max} bytes). Ignorado.")
            continue

        print(f"Recebido pacote {pacote_id}: Flag={flag}, Carga={carga}")

        if flag == "S":
            mensagem_reconstruida[pacote_id] = carga  # Apenas armazenar pacotes seguros

    # Reconstrução da mensagem na ordem correta
    mensagem_final = "".join(mensagem_reconstruida[i] for i in sorted(mensagem_reconstruida))
    print(f"Mensagem reconstruída: {mensagem_final}")

except Exception as e:
    print(f"Erro no servidor, tente novamente: {e}")
finally:
    conn.close()
    server_socket.close()
