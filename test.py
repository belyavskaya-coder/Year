word = input("Введите слово: ")

length = len(word)
mid_index = length // 2

if length % 2 == 0:
    result = word[mid_index - 1: mid_index + 1]
else:  # Если длина нечётная
    result = word[mid_index]

print("Результат:", result)