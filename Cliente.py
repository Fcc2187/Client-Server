import socket
import random
import hashlib

HOST = "127.0.0.1"
PORT = 5001

def calcular_checksum(dados):
    return hashlib.md5(dados.encode()).hexdigest()[:8]

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
gbn_rs = input("Digite:\n1 - Go back N\n2 - Repetição Seletiva\n--> ")
operacao = input("Digite:\n1 - Modo Seguro\n2 - Modo com perda de pacotes\n3 - Modo com erro nos pacotes\n--> ")
try:
    if operacao not in ["1", "2", "3"]:
        print("Erro: Modo de operação inválido!")
        client_socket.close()
        exit()
    else:
        tamanho_max_mensagem = int(input("Digite o tamanho máximo da mensagem: "))
        mensagem = input("Digite a mensagem a ser enviada: ")

        if len(mensagem) > tamanho_max_mensagem:
            print("Erro: A mensagem excede o tamanho máximo permitido!")
        else:
            client_socket.sendall(f"{operacao},3".encode())
            print(f"Resposta do servidor: {client_socket.recv(1024).decode()}")

            tamanho_pacote = 3
            for i, carga in enumerate([mensagem[j:j+tamanho_pacote] for j in range(0, len(mensagem), tamanho_pacote)], start=1):
                if operacao == "2" and random.random() < 0.4:
                    print(f"Pacote {i:02d} perdido!")
                    continue
                
                if operacao == "3" and random.random() < 0.4:
                    carga = "X" * len(carga)
                    print(f"Pacote {i:02d} corrompido!")
                
                checksum = calcular_checksum(carga)
                pacote = f"{i:02d} - S - {carga} - {checksum}"
                client_socket.sendall(pacote.encode())
                print(f"Enviado pacote: {pacote}")

            client_socket.sendall("FIM".encode())

except ValueError:
    print("Erro: Tamanho máximo inválido!")
finally:
    client_socket.close()