import timeit
from typing import Callable


def benchmark(func: Callable, input_sum, coins):
    setup_code = f"from __main__ import {func.__name__}"
    stmt = f"{func.__name__}(input_sum, coins)"
    return timeit.timeit(stmt=stmt, setup=setup_code,
                         globals={"input_sum": input_sum,
                                  "coins": coins}, number=10)


def find_coins_greedy(suma, coins):
    count_coins = {}
    for coin in coins:
        count = suma // coin
        if count > 0:
            count_coins[coin] = count
        suma = suma - coin*count
    return count_coins


def find_min_coins(suma, coins):
    count_coins = {}
    # використаємо індекс у якості суми
    # мінімальна кількість потрібних монет
    min_coins_req = [0] + [float("inf")] * suma
    # остання монета для цієї суми
    last_coin_usage = [0] * (suma + 1)

    for s in range(1, suma + 1):
        for coin in coins:
            if s >= coin and min_coins_req[s - coin] + 1 < min_coins_req[s]:
                min_coins_req[s] = min_coins_req[s - coin] + 1
                last_coin_usage[s] = coin
    current_sum = suma
    while current_sum > 0:
        coin = last_coin_usage[current_sum]
        count_coins[coin] = count_coins.get(coin, 0) + 1
        current_sum = current_sum - coin
    return count_coins


if __name__ == "__main__":
    root = None
    input_sum = 11545
    monety = [50, 25, 10, 5, 2, 1]
    results = []
    print("Решта жадібним алгоритмом = ", find_coins_greedy(input_sum, monety))
    print("Решта динамічнім програмуванням = ", find_min_coins(input_sum,
                                                               monety))
    time = benchmark(find_coins_greedy, input_sum, monety)
    results.append((find_coins_greedy.__name__, time))
    time = benchmark(find_min_coins, input_sum, monety)
    results.append((find_min_coins.__name__, time))
    title = f"{'Функція':<30} | {'Час виконання, секунди'}"
    print("-" * len(title))
    print(title)
    print("-" * len(title))
    for result in results:
        print(f"{result[0]:<30} | {result[1]}")
