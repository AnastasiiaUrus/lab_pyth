import socket
import threading
import queue
from dataclasses import dataclass

HOST, PORT = '127.0.0.1', 12345

@dataclass
class Task:
    id: int
    author: str
    text: str
    status: str = "OPEN"

class TaskServer:
    def __init__(self):
        # Створюємо TCP сокет (AF_INET - IPv4, SOCK_STREAM - TCP)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Це щоб не чекати 2 хв, поки порт звільниться після перезапуску
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((HOST, PORT))
        self.server.listen(5)

        self.clients = {}  # Словник {сокет: нікнейм}
        self.tasks = []    # Наш список завдань у пам'яті
        self.task_id_seq = 1
        # черга для синхронізації, щоб різні потоки не побили дані
        self.events = queue.Queue()

    def broadcast(self, msg, skip_sock=None):
        """Розсилка всім. Важливо: додаємо \n, бо клієнт читає рядками"""
        data = (msg.strip() + "\n").encode()
        for sock in list(self.clients.keys()):
            if sock != skip_sock:
                try:
                    sock.sendall(data)
                except:
                    self.remove_client(sock)

    def remove_client(self, sock):
        if sock in self.clients:
            nick = self.clients.pop(sock)
            sock.close()
            self.events.put(('msg', f"User {nick} left"))

    def client_handler(self, sock, addr):
        """Потік для кожного клієнта. Тільки читає дані з сокета"""
        nick = f"User_{addr[1]}"
        self.clients[sock] = nick
        self.events.put(('msg', f"New user: {nick}"))

        buf = "" # Буфер, бо TCP може розбити одне повідомлення на шматки
        try:
            while True:
                data = sock.recv(1024).decode()
                if not data: break
                buf += data
                while "\n" in buf: # Обробляємо по одному рядку
                    line, buf = buf.split("\n", 1)
                    self.events.put(('cmd', sock, line.strip()))
        except:
            pass
        finally:
            self.events.put(('exit', sock))

    def manager(self):
        """Головний потік-менеджер"""
        while True:
            ev = self.events.get() # Чекаємо на подію з черги (блокуючий виклик)
            if ev[0] == 'msg':
                self.broadcast(ev[1])
            elif ev[0] == 'exit':
                self.remove_client(ev[1])
            elif ev[0] == 'cmd':
                self.execute(ev[1], ev[2])

    def execute(self, sock, line):
        """Логіка команд. Тут парсимо рядок після символа /"""
        nick = self.clients.get(sock)
        if not line.startswith('/'):
            self.broadcast(f"[{nick}]: {line}", sock)
            return

        parts = line.split(maxsplit=2)
        cmd = parts[0].lower()
        args = parts[1:]

        try:
            if cmd == '/nick' and args:
                if args[0] in self.clients.values():
                    sock.sendall(b"Error: Nick taken\n")
                else:
                    old = self.clients[sock]
                    self.clients[sock] = args[0]
                    self.broadcast(f"{old} -> {args[0]}")
            elif cmd == '/who':
                sock.sendall(f"Online: {', '.join(self.clients.values())}\n".encode())
            elif cmd == '/add' and args:
                t = Task(self.task_id_seq, nick, " ".join(args))
                self.tasks.append(t)
                sock.sendall(f"Task #{t.id} added\n".encode())
                self.task_id_seq += 1
            elif cmd == '/list':
                # Генераторний вираз для формування списку
                out = "\n".join([f"#{t.id} [{t.status}] {t.author}: {t.text}" for t in self.tasks])
                sock.sendall((out + "\n").encode() if out else b"Empty\n")
            elif cmd == '/done' and args:
                for t in self.tasks:
                    if t.id == int(args[0]): t.status = "DONE"
                sock.sendall(b"Ok\n")
            elif cmd == '/delete' and args:
                # Видаляємо через list comprehension (фільтрація)
                self.tasks = [t for t in self.tasks if t.id != int(args[0])]
                sock.sendall(b"Ok\n")
            elif cmd == '/my':
                out = "\n".join([f"#{t.id} [{t.status}] {t.text}" for t in self.tasks if t.author == nick])
                sock.sendall((out + "\n").encode() if out else b"No tasks\n")
            elif cmd == '/msg' and len(args) >= 2:
                # Пошук сокета за нікнеймом через next()
                target = next((s for s, n in self.clients.items() if n == args[0]), None)
                if target: target.sendall(f"DM from {nick}: {args[1]}\n".encode())
                else: sock.sendall(b"Error: User not found\n")
            elif cmd == '/quit':
                sock.sendall(b"Bye\n")
                self.remove_client(sock)
            else:
                sock.sendall(b"Unknown command\n")
        except:
            sock.sendall(b"Command error\n")

    def run(self):
        # Запускаємо менеджер подій в окремому фоновому (daemon) потоці
        threading.Thread(target=self.manager, daemon=True).start()
        while True:
            # Чекаємо нових підключень (основний цикл)
            c, a = self.server.accept()
            threading.Thread(target=self.client_handler, args=(c, a), daemon=True).start()

if __name__ == "__main__":
    TaskServer().run()