import multiprocessing
import time

total = 100000000
count_processes = 4


def calculate_sum(start, end):
    local_sum = 0
    for i in range(start, end + 1):
        local_sum += i
    return local_sum

if __name__ == "__main__":

    pool = multiprocessing.Pool(processes=count_processes)

    chunk_size = total // count_processes
    tasks = []

    for i in range(count_processes):
        start_num = i * chunk_size + 1

        if i == count_processes - 1:
            end_num = total
        else:
            end_num = (i + 1) * chunk_size

        tasks.append((start_num, end_num))

    start_time = time.time()

    results = pool.starmap(calculate_sum, tasks)

    final_sum = sum(results)

    end_time = time.time()

    print(f"Сумма: {final_sum}")
    print(f"Время выполнения multiprocessing: {end_time - start_time:.2f} секунд")