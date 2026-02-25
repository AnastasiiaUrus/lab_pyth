import socket

# адреса сама на себе та порт однаковий з клієнтом
HOST = '127.0.0.1'
PORT = 65432

# список словників, діставатимемо по індексу
QUESTIONS = [
    {"id": 1, "text": "Чи отримаю я відмінний бал за це ДЗ?", "options": "A:Так; B:Ні; C:Забагато бажаєш; D:Можливо",
     "correct": "A"},
    {"id": 2, "text": "Скільки ніг у кота?", "options": "A:2; B:4; C:6; D:8", "correct": "B"},
    {"id": 3, "text": "Найкращий факультет КНУ?", "options": "A:Мех-мат; B:Економічний; C:Історичний; D:Хімічний",
     "correct": "A"},
    {"id": 4, "text": "Що найсмачніше у буфеті на мехматі?",
     "options": "A:Бургер; B:Булочка з журавлиною; C:З маком; D:Сосиска в тісті", "correct": "B"},
    {"id": 5, "text": "Скільки буде 2 + 2?", "options": "A:2; B:3; C:4; D:5", "correct": "C"}
]


def start_server():
    #with, щоб сокет автоматично закривався після роботи
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Дозволяємо повторне використання порту, щоб не чекати хвилину після перезапуску
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((HOST, PORT))
            s.listen()
            print("Сервер запущено...")

            # Чекаємо на клієнта. conn — з'єднання
            conn, addr = s.accept()
            with conn:
                # Змінні для збереження стану (хто грає, які бали, чи дана відповідь)
                user_name = None
                quiz_started = False
                current_q_idx = 0
                score = 0
                answered = False

                while True:
                    data = conn.recv(1024)
                    if not data: break

                    request = data.decode('utf-8').strip()
                    parts = request.split(' ')
                    command = parts[0].upper()

                    # 1. ЕТАП ЛОГІНУ (поки user_name порожній, далі не пускаємо)
                    if user_name is None:
                        if command == "LOGIN" and len(parts) > 1:
                            user_name = parts[1]
                            response = f" Welcome {user_name}! (Підказка: напиши START)"
                        else:
                            response = "ERR Спочатку введи команду: LOGIN твоє_ім'я"

                    # 2. ЕТАП СТАРТУ
                    elif not quiz_started:
                        if command == "START":
                            quiz_started = True
                            response = " квіз розпочато! (Підказка: напиши Q щоб отримати питання)"
                        elif command == "QUIT":
                            conn.sendall(" goodbye\n".encode('utf-8'))
                            break
                        else:
                            response = "ERR Квіз не запущено. Напиши START"

                    # 3. ЕТАП ГРИ
                    else:
                        # Якщо введено A, B, C, D — це вважаємо відповіддю
                        if command in ["A", "B", "C", "D"]:
                            if answered:
                                response = "ERR Ти вже відповів. (Підказка: напиши NEXT)"
                            else:
                                # Перевірка чи збігається ввід з полем 'correct' у QUESTIONS
                                if command == QUESTIONS[current_q_idx]["correct"]:
                                    score += 1
                                    response = " Правильно! (Підказка: напиши NEXT для наступного питання)"
                                else:
                                    response = f" Неправильно. Правильна відповідь: {QUESTIONS[current_q_idx]['correct']}. (Підказка: напиши NEXT)"
                                answered = True # Блокуємо повторну відповідь на це ж питання

                        elif command == "Q":
                            q = QUESTIONS[current_q_idx]
                            # Складаємо рядок питання
                            response = f"Q {q['id']}; {q['text']}; {q['options']} (Підказка: введи букву відповіді A, B, C, D)"

                        elif command == "NEXT":
                            if not answered:
                                response = "ERR Спочатку дай відповідь на питання! (Введи букву)"
                            else:
                                current_q_idx += 1
                                answered = False
                                # Перевіряємо чи не закінчилися питання
                                if current_q_idx >= len(QUESTIONS):
                                    response = f" Твій результат: {score}/{len(QUESTIONS)}. Гру завершено!"
                                    conn.sendall((response + "\n").encode('utf-8'))
                                    break
                                response = " Наступне питання готове. (Підказка: напиши Q)"

                        elif command == "QUIT":
                            conn.sendall(" goodbye\n".encode('utf-8'))
                            break
                        else:
                            response = "ERR Невідома команда. Спробуй Q, NEXT або вибери букву A, B, C чи D"

                    # Відправляємо відповідь назад клієнту, додаючи \n в кінці
                    conn.sendall((response + "\n").encode('utf-8'))
        except Exception as e:
            print(f"Помилка: {e}")


if __name__ == "__main__":
    start_server()