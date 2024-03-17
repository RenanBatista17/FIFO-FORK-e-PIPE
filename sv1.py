import socket
import threading
import os

# Definindo os dados de cada servidor
SERVERS = {
    'Server1': ('127.0.0.1', 8001, 'String de exemplo para Server1')
}

# Função para lidar com a conexão de um cliente
def handle_client_connection(client_socket, server_address, server_string):
    response = f"Data from {server_address}: {server_string}"
    client_socket.send(response.encode())
    client_socket.close()

# Função principal para iniciar o servidor
def start_server(server_name, server_address, server_string):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_address[0], server_address[1]))
    server_socket.listen(5)  # Número máximo de conexões pendentes

    print(f"Server {server_name} listening on {server_address}")

    # Criar FIFO
    caminho_fifo = f"/home/vm-trabalho-01/Desktop/{server_name}_fifo"
    if not os.path.exists(caminho_fifo):
        os.mkfifo(caminho_fifo)

    pid = os.fork()

    if pid == 0:  # Processo filho
        fifo = os.open(caminho_fifo, os.O_RDONLY)  # Abrir FIFO para leitura
        
        # Ler dados do FIFO
        dados = os.read(fifo, 1024).decode()
        print(f"Dados recebidos do FIFO em {server_name}: {dados}")
        
        # Fechar FIFO após a leitura
        os.close(fifo)
        
    else:  # Processo pai
        while True:
            cliente_soquete, endereco_cliente = server_socket.accept()
            print(f"Conexão aceita de {endereco_cliente}")
            manipulador_cliente = threading.Thread(
                target=handle_client_connection,
                args=(cliente_soquete, server_address, server_string)
            )
            manipulador_cliente.start()
            
            # Abrir FIFO para escrita
            fifo = os.open(caminho_fifo, os.O_WRONLY)
            
            # Escrever dados no FIFO
            os.write(fifo, server_string.encode())
            
            # Fechar FIFO após a escrita
            os.close(fifo)

# Iniciar os servidores
if __name__ == "__main__":
    for server_name, server_info in SERVERS.items():
        start_server(server_name, server_info[:2], server_info[2])
