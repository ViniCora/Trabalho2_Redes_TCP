import socket
import hashlib
CAMINHO_ARQUIVO_RECEBER = "D:/Faculdade/Redes/Teste_Recebido/"

def receive_file(client_socket):
    caminho = client_socket.recv(1024).decode().split(": ")[1]
    partes = caminho.split('/')
    nome_arquivo = partes[-1]
    print("nome arquivo: " + nome_arquivo)
    client_socket.send("Nome recebido".encode())

    size = int(client_socket.recv(1024).decode().split(": ")[1])
    client_socket.send("Tamanho recebido".encode())

    file_hash = client_socket.recv(1024).decode().split(": ")[1]
    client_socket.send("Hash recebido".encode())

    file_data = b""
    while len(file_data) < size:
        file_data += client_socket.recv(1024)

    client_socket.send("Dados recebidos".encode())

    status = client_socket.recv(1024).decode()
    print(status)

    if status == "Status: OK":
        with open(CAMINHO_ARQUIVO_RECEBER + nome_arquivo, "wb") as f:
            f.write(file_data)
        if hashlib.sha256(file_data).hexdigest() == file_hash:
            print("Arquivo recebido com integridade.")
        else:
            print("Erro na integridade do arquivo.")
    else:
        print("Erro ao receber arquivo.")


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 12345))

    while True:
        command = input("Digite a requisição (Sair, Arquivo <nome>, Chat): ")
        client.send(command.encode())

        if command.lower() == "sair":
            response = client.recv(1024).decode()
            print(response)
            break

        elif command.startswith("Arquivo"):
            receive_file(client)

        elif command.lower() == "chat":
            while True:
                chat_msg = input("Você: ")
                client.send(chat_msg.encode())
                if chat_msg.lower() == "sair":
                    response = client.recv(1024).decode()
                    print(response)
                    break
                response = client.recv(1024).decode()
                print(f"Servidor: {response}")

        else:
            response = client.recv(1024).decode()
            print(response)

    client.close()


if __name__ == "__main__":
    main()
