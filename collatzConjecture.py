import time
import decimal


def collatz(num):
    """
    :type num: int;
    :param num: start number, any positive integer;
    :return [start number, [following_numbers], steps, time];
    """
    num_original = num
    following_nums = []
    step = 0
    start = time.time()
    while num != 1:
        # print(str(num))
        if (num % 2) == 0:  # Even
            num = int(num / 2)  # n/2
            following_nums.append(num)
            step += 1
        else:  # Odd
            num = int(3 * num + 1)  # 3n+1
            following_nums.append(num)
            step += 1
    end = time.time()
    elapsed = decimal.getcontext().create_decimal(decimal.Decimal(end - start))
    return [num_original, following_nums, step, round(elapsed, 10)]
