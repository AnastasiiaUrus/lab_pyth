import socket
import threading
import sys


def listen(sock):
    buf = ""
    try:
        while True:
            data = sock.recv(1024).decode()
            if not data: break
            buf += data
            while "\n" in buf:
                line, buf = buf.split("\n", 1)
                # Виводимо повідомлення від сервера і повертаємо символ запрошення >
                print(f"\r{line}\n> ", end="", flush=True)
    except:
        pass
    print("\nDisconnected.")
    sys.exit()


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('127.0.0.1', 12345))
    except:
        print("Server is offline.")
        return

    # Вивід інструкції при вході
    print("=" * 30)
    print("TASK CLIENT")
    print("Команди:")
    print("  /nick <name>      - змінити ім'я")
    print("  /who              - хто онлайн")
    print("  /add <text>       - нове завдання")
    print("  /list             - всі завдання")
    print("  /my               - мої завдання")
    print("  /done <id>        - виконати")
    print("  /delete <id>      - видалити")
    print("  /msg <name> <msg> - приват")
    print("  /quit             - вихід")
    print("  <text>            - загальний чат")

    threading.Thread(target=listen, args=(s,), daemon=True).start()

    try:
        while True:
            msg = input("> ")
            if msg:
                s.sendall((msg + "\n").encode())
            if msg.strip().lower() == '/quit':
                break
    except:
        pass
    finally:
        s.close()


if __name__ == "__main__":
    main()