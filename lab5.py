import itertools

def solve_task1():
    print("\nЗавдання 1")
    slots = range(5)
    all_variants = list(itertools.permutations(slots, 3))
    valid_count = 0

    for p in all_variants:
        pos_py, pos_math, pos_stat = p
        # Умова 1: Python не в першому слоті
        # Умова 2: Math не одразу після Stats
        if pos_py != 0 and pos_math != pos_stat + 1:
            valid_count += 1
            if valid_count <= 3:
                print(f"Варіант {valid_count}: Python:{pos_py + 1}, Math:{pos_math + 1}, Stats:{pos_stat + 1}")
    print(f"Всього допустимих варіантів: {valid_count}")


def solve_task2():
    print("\nЗавдання 2")
    candidates = [
        {"name": "Anna", "skills": {"python", "sql"}},
        {"name": "Bohdan", "skills": {"excel", "sql"}},
        {"name": "Iryna", "skills": {"python", "statistics"}},
        {"name": "Maksym", "skills": {"excel", "presentation"}},
        {"name": "Olha", "skills": {"statistics", "sql"}}
    ]
    required = {"python", "sql", "statistics", "excel"}

    for r in range(1, len(candidates) + 1):
        for team in itertools.combinations(candidates, r):
            current_skills = set().union(*(c["skills"] for c in team))
            if required.issubset(current_skills):
                names = [c["name"] for c in team]
                print(f"Мінімальна команда ({len(names)} чол.): {', '.join(names)}")
                return


def solve_task3():
    print("\nЗавдання 3")
    allowed = {("A", "B"), ("B", "A"), ("A", "C"), ("C", "A"),
               ("B", "D"), ("D", "B"), ("C", "D"), ("D", "C"),
               ("D", "E"), ("E", "D")}

    def check(route):
        return all((route[i], route[i + 1]) in allowed for i in range(len(route) - 1))

    routes = [["A", "B", "D", "E"], ["A", "E"]]
    for r in routes:
        print(f"Маршрут {r}: {'Валідний' if check(r) else 'Невалідний'}")


def solve_task4():
    """Задача про монети (жадібний алгоритм vs перебір)."""
    print("\n Завдання 4")
    coins = [4, 3, 1]
    target = 6

    # Жадібний
    greedy_res = []
    temp_target = target
    for c in coins:
        while temp_target >= c:
            temp_target -= c
            greedy_res.append(c)

    print(f"Жадібний алгоритм: {greedy_res} (кількість: {len(greedy_res)})")
    print("Жадібний алгоритм не завжди оптимальний, як у цьому випадку.")


def main():
    solve_task1()
    solve_task2()
    solve_task3()
    solve_task4()

if __name__ == "__main__":
    main()