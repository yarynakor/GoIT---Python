from collections import UserDict
from typing import Optional, List


class Field:
    """Fields of records in contact book : name , phone/phones , etc."""

    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    """Phone of the contact"""

    def __eq__(self, other: object) -> bool:
        return self.value == other.value

    def __str__(self):
        return f"Phone:{self.value}"


class Record:
    """Records(contacts) in users contact book.
    Only one name , but it can be more than one phone"""

    def __init__(self, name: str, phone: List[str] = None) -> None:
        if phone is None:
            self.phone = []
        else:
            self.phone = [Phone(p) for p in phone]
        self.name = Name(name)

    def add_phone(self, phone_number: str) -> None:
        phone = Phone(phone_number)
        if phone not in self.phone:
            self.phone.append(phone)

    def find_phone(self, phone: str) -> Optional[Phone]:
        for p in self.phone:
            if p.value == phone:
                return p

    def delete_phone(self, phone: str) -> None:
        phone_to_delete = self.find_phone(phone)
        self.phone.remove(phone_to_delete) if phone_to_delete else None

    def edit_phone(self, old_phone, new_phone) -> None:
        new_phone = Phone(new_phone)
        phone_to_remove = self.find_phone(old_phone)
        if phone_to_remove:
            self.phone.remove()
            self.phone.append(new_phone)

    def __str__(self):
        return f"Record of {self.name.value}, phones {[p.value for p in self.phone]}"


class AddressBook(UserDict):
    """All contacts data"""

    def add_record(self, record: list) -> None:
        new_record = Record(record[0], record[1:])
        self.data[new_record.name.value] = new_record

    def find_record(self, value: str) -> Optional[Record]:
        return self.data.get(value)

    def delete_record(self, value: str) -> None:
        self.data.pop(value)

    def __str__(self):
        return str(self.data)


def main():
    book = AddressBook()
    book.add_record(["Yehor", "063 666 99 66", "048 722 22 22"])
    book.add_record(["Pavel", "063 666 66 66", "048 222 22 22"])

    record = book.find_record("Pavel")
    book.delete_record("Yehor")

    print("#" * 10)
    print(book)
    print(record)
    print("\n")
    print("#" * 10)
    record.delete_phone("048 222 22 22")
    record.edit_phone("095 666 66 66", "067 666 66 66")
    print(record)


main()