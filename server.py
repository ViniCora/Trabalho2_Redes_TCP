import socket
import threading
import os
import hashlib
CAMINHO_ARQUIVO = "D:/Faculdade/Redes/"

def handle_client(client_socket):
    while True:
        request = client_socket.recv(1024).decode()

        if request.lower() == "sair":
            client_socket.send("Conexão encerrada.".encode())
            break

        elif request.startswith("Arquivo"):
            file_name = CAMINHO_ARQUIVO + request.split()[1]
            print(file_name)
            if os.path.isfile(file_name):
                file_size = os.path.getsize(file_name)
                with open(file_name, "rb") as f:
                    file_data = f.read()
                file_hash = hashlib.sha256(file_data).hexdigest()

                client_socket.send(f"Nome: {file_name}".encode())
                client_socket.recv(1024)  # Aguardar confirmação

                client_socket.send(f"Tamanho: {file_size}".encode())
                client_socket.recv(1024)  # Aguardar confirmação

                client_socket.send(f"Hash: {file_hash}".encode())
                client_socket.recv(1024)  # Aguardar confirmação

                client_socket.send(file_data)
                client_socket.recv(1024)  # Aguardar confirmação

                client_socket.send("Status: OK".encode())
            else:
                client_socket.send("Status: Arquivo inexistente".encode())

        elif request.lower() == "chat":
            while True:
                chat_msg = client_socket.recv(1024).decode()
                if chat_msg.lower() == "sair":
                    client_socket.send("Chat encerrado.".encode())
                    break
                print(f"Cliente: {chat_msg}")
                server_msg = input("Servidor: ")
                client_socket.send(server_msg.encode())

        else:
            client_socket.send("Comando inválido.".encode())

    client_socket.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 12345))
    server.listen(5)
    print("Servidor aguardando conexões...")

    while True:
        client_socket, addr = server.accept()
        print(f"Conexão aceita de {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    main()
