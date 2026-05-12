import asyncio
import time

total = 100000000
count_task = 4


async def calculate_sum(start, end):
    local_sum = 0

    for i in range(start, end + 1):
        local_sum += i

        if i % 1_000_000 == 0:
            await asyncio.sleep(0)

    return local_sum


async def main():

    chunk_size = total // count_task
    tasks = []

    for i in range(count_task):
        start_num = i * chunk_size + 1

        if i == count_task - 1:
            end_num = total
        else:
            end_num = (i + 1) * chunk_size

        tasks.append(
            asyncio.create_task(
                calculate_sum(start_num, end_num)
            )
        )

    results = await asyncio.gather(*tasks)

    return sum(results)


start_time = time.time()

final_sum = asyncio.run(main())

end_time = time.time()

print(f"Сумма: {final_sum}")
print(f"Время выполнения async: {end_time - start_time:.2f} секунд")