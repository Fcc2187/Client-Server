import socket

HOST = "127.0.0.1"
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Servidor aguardando conexões na porta {PORT}...")

conn, addr = server_socket.accept()
print(f"Conexão estabelecida com {addr}")

# Recebendo handshake
handshake_data = conn.recv(1024).decode()
modo_operacao, tamanho_max = handshake_data.split(",")
tamanho_max = int(tamanho_max)

print(f"Modo de operação recebido: {modo_operacao}")
print(f"Tamanho máximo da carga útil: {tamanho_max}")

# Confirmar handshake
conn.sendall(f"HANDSHAKE_OK:{modo_operacao}".encode())

# Dicionário para armazenar pacotes recebidos
mensagem_reconstruida = {}

while True:
    pacote = conn.recv(1024).decode()

    if pacote == "FIM":
        break  # Sinal de que terminou a transmissão

    pacote_id = pacote[:2]  # ID do pacote
    flag = pacote[2]         # Flag (S, P ou E)
    carga = pacote[3:]       # Carga útil

    print(f"Recebido pacote {pacote_id}: Flag={flag}, Carga={carga}")

    if flag == "O":  # Apenas armazenar pacotes corretos
        mensagem_reconstruida[int(pacote_id)] = carga.ljust(tamanho_max)  # Preenche com espaços se necessário

# Remontar a mensagem em ordem correta
mensagem_final = "".join(mensagem_reconstruida[i] for i in sorted(mensagem_reconstruida.keys()))
print(f"Mensagem reconstruída: {mensagem_final}")

# Fechar conexão
conn.close()
server_socket.close()