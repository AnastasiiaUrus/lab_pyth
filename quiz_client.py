import socket

HOST = '127.0.0.1'
PORT = 65432


def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print("--- ПІДКЛЮЧЕНО ---")
            while True:
                user_input = input("> ")
                if not user_input: continue

                s.sendall((user_input + "\n").encode('utf-8'))
                data = s.recv(1024)
                if not data: break

                print(data.decode('utf-8').strip())

                if "END" in data.decode('utf-8') or user_input.upper() == "QUIT":
                    break
        except ConnectionRefusedError:
            print("Помилка: Запусти спочатку сервер!")


if __name__ == "__main__":
    start_client()