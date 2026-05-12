import threading
import time

total = 100000000
count_threads = 14

results = [0] * count_threads


def calculate_sum(start, end, index):
    local_sum = 0
    for i in range(start, end + 1):
        local_sum += i
    results[index] = local_sum


threads = []
chunk_size = total // count_threads

start_time = time.time()

for i in range(count_threads):
    start_num = i * chunk_size + 1

    if i == count_threads - 1:
        end_num = total
    else:
        end_num = (i + 1) * chunk_size

    thread = threading.Thread(
        target=calculate_sum,
        args=(start_num, end_num, i)
    )

    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

final_sum = sum(results)

end_time = time.time()

print(f"Сумма: {final_sum}")
print(f"Время выполнения threading: {end_time - start_time:.2f} секунд")