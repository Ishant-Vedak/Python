import sys

nums = {}

try:
    user_input = int(input('Write the highest number: '))

    for i in range(1, user_input + 1):
        nums[i] = []

        for j in range(1, i + 1):
            if i % j == 0:
                nums[i].append(j)

    max_key = max(nums, key=lambda k: len(nums[k]))
    print(max_key, nums[max_key])
except:
    sys.exit("Provide a number value")

