import socket
import hashlib

HOST = "127.0.0.1"
PORT = 5001

MODOS_OPERACAO = {
    "1": "Seguro",
    "2": "Com Perda",
    "3": "Com Erro"
}

def calcular_checksum(dados):
    return hashlib.md5(dados.encode()).hexdigest()[:8]  # Usando os primeiros 8 caracteres do hash

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Servidor aguardando conexões na porta {PORT}...")

conn, addr = server_socket.accept()
print(f"Conexão estabelecida com {addr}")

try:
    dados_handshake = conn.recv(1024).decode()
    modo_operacao, tamanho_max = dados_handshake.split(",")
    tamanho_max = int(tamanho_max)
    nome_modo = MODOS_OPERACAO.get(modo_operacao, "Desconhecido")
    print(f"Modo de operação: {nome_modo}\nTamanho máximo por pacote: {tamanho_max}")

    conn.sendall(f"HANDSHAKE_OK:{nome_modo}".encode())

    mensagem_reconstruida = {}

    while True:
        pacote = conn.recv(1024).decode()
        
        if pacote:
            if pacote == "FIM":
                break

            partes = pacote.split(" - ")
            if len(partes) != 4:
                print(f"Pacote inválido: '{pacote}'")
                continue

            pacote_id, flag, carga, checksum_recebido = partes
            pacote_id = int(pacote_id)

            checksum_calculado = calcular_checksum(carga)
            if checksum_calculado != checksum_recebido:
                print(f"Erro: Checksum inválido para pacote {pacote_id}. Pacote ignorado.")
                continue
            
            if len(carga) > tamanho_max:
                print(f"Erro: Pacote {pacote_id} excede o tamanho máximo permitido ({tamanho_max} bytes). Ignorado.")
                continue

            print(f"Recebido pacote {pacote_id}: Flag={flag}, Carga={carga}, Checksum={checksum_recebido}")

            if flag == "S":
                mensagem_reconstruida[pacote_id] = carga

    mensagem_final = "".join(mensagem_reconstruida[i] for i in sorted(mensagem_reconstruida))
    print(f"Mensagem reconstruída: {mensagem_final}")

except Exception as e:
    print(f"Erro no servidor, tamanho da mensagem máxima menor que o tamanho do pacote.")
finally:
    conn.close()
    server_socket.close()
    print("Conexão encerrada.")