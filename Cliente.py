import socket

HOST = "127.0.0.1"
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Handshake inicial
operacao = int(input("Digite:\n1 - Modo Seguro\n2 - Modo com perda de pacotes\n3 - Modo com erro nos pacotes\n--> "))
modos = {1: "SEGURO", 2: "PERDA", 3: "ERRO"}
modo_operacao = modos.get(operacao, "SEGURO")

handshake_message = f"{modo_operacao},3"
client_socket.sendall(handshake_message.encode())

# Esperando resposta do servidor
response = client_socket.recv(1024).decode()
print(f"Resposta do servidor: {response}")

# Entrada da mensagem completa a ser enviada
mensagem = input("Digite a mensagem a ser enviada: ")

# Quebrar a mensagem em pacotes de 3 caracteres
tamanho_pacote = 3
pacotes = [mensagem[i:i+tamanho_pacote] for i in range(0, len(mensagem), tamanho_pacote)]

# Enviar pacotes com ID e FLAG
for i, carga in enumerate(pacotes, start=1):
    pacote_id = f"{i:02d}"  # ID com 2 dígitos (01, 02, 03...)
    flag = "O"  # "O" (OK), "P" (Perdido), "E" (Erro)
    
    pacote = f"{pacote_id}{flag}{carga.ljust(3)}"  # Garante que tenha 3 caracteres
    client_socket.sendall(pacote.encode())
    print(f"Enviado pacote: {pacote}")

# Enviar sinal de fim da transmissão
client_socket.sendall("FIM".encode())

# Fechar conexão
client_socket.close()