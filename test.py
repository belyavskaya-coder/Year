word = input("Введите слово: ")  # Запрашиваем слово у пользователя

length = len(word)  # Определяем длину слова
mid_index = length // 2  # Находим средний индекс

if length % 2 == 0:  # Если длина чётная
    result = word[mid_index - 1: mid_index + 1]  # Извлекаем две средние буквы
else:  # Если длина нечётная
    result = word[mid_index]  # Извлекаем одну среднюю букву

print("Результат:", result)  # Выводим результат