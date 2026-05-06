import math
import matplotlib.pyplot as plt
import numpy as np

def solve_task1():
    print("\nЗавдання 1")
    x_nodes = np.array([0.2 * i for i in range(6)])
    y_nodes = np.exp(-x_nodes)

    def lagrange_interpolation(x, x_pts, y_pts):
        n = len(x_pts)
        total_sum = 0
        for i in range(n):
            li = 1
            for j in range(n):
                if i != j:
                    li *= (x - x_pts[j]) / (x_pts[i] - x_pts[j])
            total_sum += y_pts[i] * li
        return total_sum

    x_val = 0.5
    y_interp = lagrange_interpolation(x_val, x_nodes, y_nodes)
    y_exact = math.exp(-x_val)

    print(f"Обчислення в точці x = {x_val}:")
    print(f"Наближене L(x): {y_interp:.6f}")
    print(f"Точне f(x):    {y_exact:.6f}")
    print(f"Похибка:        {abs(y_exact - y_interp):.2e}")

    x_range = np.linspace(0, 1, 100)
    y_exact_range = np.exp(-x_range)
    y_lagrange_range = [lagrange_interpolation(xi, x_nodes, y_nodes) for xi in x_range]

    plt.figure(figsize=(8, 4))
    plt.plot(x_range, y_exact_range, 'r-', label='Точна функція exp(-x)')
    plt.plot(x_range, y_lagrange_range, 'b--', label='Поліном Лагранжа')
    plt.scatter(x_nodes, y_nodes, color='black', label='Вузли (x_i)')
    plt.title("Завдання 1: Інтерполяція")
    plt.legend()
    plt.grid(True)
    plt.show()


def solve_task2():
    print("\nЗавдання 2")
    x = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    y = np.array([1.25, 1.48, 1.75, 2.01, 2.22, 2.50, 2.78, 3.05, 3.29, 3.55])

    # Лінійна апроксимація y = ax + b
    a, b = np.polyfit(x, y, 1)

    print(f"Отримана модель: y = {a:.4f} * x + {b:.4f}")

    # Прогноз для наступної точки
    x_next = 1.1
    y_pred = a * x_next + b
    print(f"Прогноз для x = {x_next}: y = {y_pred:.4f}")

    plt.figure(figsize=(8, 4))
    plt.scatter(x, y, color='green', label='Дані (таблиця)')
    plt.plot(x, a * x + b, 'r-', label=f'Лінія МНК: {a:.2f}x + {b:.2f}')
    plt.title("Завдання 2")
    plt.legend()
    plt.grid(True)
    plt.show()

def solve_task3():
    print("\nЗавдання 3")

    # Інтегруємо f(x) = 1 / (1 + x^2) на [0, 1]
    def f(x):
        return 1 / (1 + x ** 2)

    a, b = 0, 1
    n = 10
    h = (b - a) / n

    integral = (f(a) + f(b)) / 2.0
    for i in range(1, n):
        integral += f(a + i * h)
    integral *= h

    exact_value = math.pi / 4
    print(f"Метод трапецій (n={n}): {integral:.6f}")
    print(f"Точне значення (pi/4): {exact_value:.6f}")
    print(f"Різниця: {abs(exact_value - integral):.2e}")


if __name__ == "__main__":
    #solve_task1()
    #solve_task2()
    solve_task3()