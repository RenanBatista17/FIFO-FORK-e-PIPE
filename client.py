import socket
import os

# Definindo os dados de cada servidor
SERVERS = {
    'Server1': ('127.0.0.1', 8001),
    'Server2': ('127.0.0.1', 8002),
    'Server3': ('127.0.0.1', 8003)
}

# Função para consultar todos os servidores
def query_all_servers(pipe_escrita):
    for server_name, server_address in SERVERS.items():
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(server_address)
        client_socket.send(b"QueryAll")
        response = client_socket.recv(4096).decode()
        os.write(pipe_escrita, response.encode())  # Escreve no pipe
        client_socket.close()

# Função para buscar uma informação específica em um servidor
def query_specific_server(search_string, pipe_escrita):
    found = False
    for server_name, server_address in SERVERS.items():
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(server_address)
        client_socket.send(search_string.encode())
        response = client_socket.recv(4096).decode()
        if search_string in response: # Verifica se a resposta contém a string de busca
            print(f"String '{search_string}' found in {server_name}: {response}")
            found = True
            os.write(pipe_escrita, f"String '{search_string}' found in {server_name}: {response}".encode())  # Escreve no pipe
            break
        client_socket.close()
    
    if not found:
        print(f"String '{search_string}' not found in any server.")
        os.write(pipe_escrita, f"String '{search_string}' not found in any server.".encode())  # Escreve no pipe

if __name__ == "__main__":
     # Cria o pipe
    pipe_leitura, pipe_escrita = os.pipe()

    # Cria um novo processo
    pid = os.fork()

    if pid == 0:  # Processo filho
        os.close(pipe_escrita)  # Fecha a extremidade de escrita do pipe no processo filho
        # Lê as mensagens do pipe e imprime
        while True:
            mensagem = os.read(pipe_leitura, 4096).decode()
            if mensagem == "":
                break
            print("Processo filho recebeu:", mensagem)
        os.close(pipe_leitura)  # Fecha a extremidade de leitura do pipe no processo filho
    else:  # Processo pai
        os.close(pipe_leitura)  # Fecha a extremidade de leitura do pipe no processo pai
        query_all_servers(pipe_escrita)  # Chama a função com o argumento pipe_escrita
        query_specific_server('eae blz', pipe_escrita)  # Buscar uma string específica em todos os servidores
        os.close(pipe_escrita)  # Fecha a extremidade de escrita do pipe no processo pai
