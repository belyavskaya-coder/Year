documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
]


def get_owner_by_doc_number(doc_number: str) -> str:
    for doc in documents:
        if doc["number"] == doc_number:
            return doc["name"]
    return None


def main():
    command = input("Введите команду:\n").strip()
    if command == "p":
        doc_number = input("Введите номер документа:\n").strip()
        owner = get_owner_by_doc_number(doc_number)
        if owner:
            print(f"Владелец документа: {owner}")
        else:
            print("Документ не найден")
    else:
        print("Неизвестная команда")


if __name__ == '__main__':
    main()