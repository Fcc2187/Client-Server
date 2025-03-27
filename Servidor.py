import socket

HOST = "127.0.0.1"
PORT = 5001

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Servidor aguardando conexões na porta {PORT}...")

conn, addr = server_socket.accept()
print(f"Conexão estabelecida com {addr}")

# Recebendo handshake
modo_operacao, tamanho_max = conn.recv(1024).decode().split(",")
print(f"Modo de operação: {modo_operacao}\nTamanho máximo por pacote: {tamanho_max}")

# Confirmar handshake
conn.sendall(f"HANDSHAKE_OK:{modo_operacao}".encode())

# Dicionário para armazenar pacotes recebidos
mensagem_reconstruida = {}

while True:
    pacote = conn.recv(1024).decode()

    if pacote == "FIM":
        break  # Finaliza ao receber "FIM"

    if len(pacote) < 3:  # Validação única
        print(f"Pacote inválido: '{pacote}'")
        continue

    pacote_id, flag, carga = int(pacote[:2]), pacote[2], pacote[3:]
    print(f"Recebido pacote {pacote_id}: Flag={flag}, Carga={carga}")

    if flag == "S":
        mensagem_reconstruida[pacote_id] = carga  # Apenas armazenar pacotes seguros

# Reconstrução da mensagem na ordem correta
print(f"Mensagem reconstruída: {''.join(mensagem_reconstruida[i] for i in sorted(mensagem_reconstruida))}")

conn.close()
server_socket.close()