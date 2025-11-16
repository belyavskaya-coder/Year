documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
]

directories = {
    '1': ['2207 876234', '11-2'],
    '2': ['10006'],
    '3': []
}


def get_owner(doc_number):
    for doc in documents:
        if doc["number"] == doc_number:
            return doc["name"]
    return None


def get_shelf(doc_number):
    for shelf, docs in directories.items():
        if doc_number in docs:
            return shelf
    return None


def main():
    command = input("Введите команду:\n").strip()
    if command == "p":
        doc_num = input("Введите номер документа:\n").strip()
        owner = get_owner(doc_num)
        print(f"Владелец документа: {owner}" if owner else "Документ не найден")
    elif command == "s":
        doc_num = input("Введите номер документа:\n").strip()
        shelf = get_shelf(doc_num)
        print(f"Документ хранится на полке: {shelf}" if shelf else "Документ не найден")
    else:
        print("Неизвестная команда")


if __name__ == '__main__':
    main()