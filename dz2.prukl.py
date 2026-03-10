import random
import matplotlib.pyplot as plt

def simulate_stadium(N, m, t, t1):
    arrivals = [random.uniform(-t, 0) for _ in range(N)]
    arrivals.sort()

    # кожен елемент - це час, коли турнікет звільниться
    # На початку всі турнікети вільні з моменту відкриття (-t)
    turnstiles = [-t] * m

    for arrival in arrivals:
        # Кожна людина обирає турнікет, який звільниться найшвидше
        turnstiles.sort()

        # Початок обслуговування: або коли людина підійшла, або коли звільнився турнікет
        # (якщо турнікет уже вільний, то беремо час приходу людини)
        start_service = max(turnstiles[0], arrival)
        duration = random.uniform(1, t1)
        turnstiles[0] = start_service + duration

    return max(turnstiles)


print("Моделювання черги на стадіоні")
N = int(input("Кількість глядачів: "))
m = int(input("Кількість турнікетів: "))
t = float(input("За скільки хв до матчу відкривають вхід (t): "))
t1 = float(input("Макс. час на одну людину (t1): "))

iterations = 1000
results = [simulate_stadium(N, m, t, t1) for _ in range(iterations)]
# Сортуємо всі 1000 результатів від кращого до гіршого
results.sort()

#900-й результат, ймовірність 0.9
p90_time = results[int(0.9 * iterations)]

print(f"\nЗ імовірністю 0.9 останній глядач зайде о {p90_time:.2f} хв.")




plt.figure(figsize=(10, 6))
# гістограма розподілу результатів
plt.hist(results, bins=40, color='skyblue', edgecolor='black', alpha=0.7)

# Позначено вертикальними лініями важливі точки
plt.axvline(0, color='green', linestyle='-', label='Старт матчу (0 хв)')
plt.axvline(p90_time, color='red', linestyle='--', label=f'90% поріг: {p90_time:.2f} хв')

plt.title(f"Результати для N={N}, m={m}")
plt.xlabel("Час відносно початку матчу (хв)")
plt.ylabel("Кількість матчів")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()