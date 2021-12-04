#AddressBook
from collections import UserDict
from typing import Optional, List
from datetime import datetime, date


class Field:
    """Fields of records in contact book : name , phone/phones , etc."""

    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    pass


class Phone(Field):
    """Phone of the contact"""

    def __eq__(self, other: Field) -> bool:
        return self.value == other.value

    def __str__(self):
        return f"Phone:{self.value}"

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value: str) -> None:
        if value[0] != '+':
            raise ValueError("Phone number must starts from +")
        number = value[1:]
        if len(number) != 12 or not number.isalnum():
            raise ValueError("Phone must contain only 12 digits")
        self.__value = value


class Birthday(Field):
    """Date of birth of contact"""

    @property
    def value(self) -> datetime:
        return self.__value

    @value.setter
    def value(self, value) -> None:
        try:
            self.__value = datetime.strptime(value, '%d %m %Y')
        except (ValueError, TypeError):
            raise ValueError("Data must match pattern '%d %m %Y'")


class Record:
    """Records(contacts) in users contact book.
    Only one name , but it can be more than one phone"""

    def __init__(self, name: str, phone: List[str] = None, birthday: Birthday = None) -> None:
        if phone is None:
            self.phone = []
        else:
            self.phone = [Phone(p) for p in phone]
        self.name = Name(name)
        self.birthday = birthday

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
            self.phone.remove(phone_to_remove) if phone_to_remove else None
            self.phone.append(new_phone)

    def days_to_birthday(self) -> Optional[int]:
        if self.birthday and self.birthday.value:
            value = self.birthday.value
            today = date.today()

            delta1 = date(today.year, value.month, value.day)
            delta2 = date(today.year + 1, value.month, value.day)

            delta = delta2 if delta1 < today else delta1
            return (delta - today).days

    def __str__(self):
        return f"Record of {self.name.value}, phones {[p.value for p in self.phone]}"

    def __repr__(self):
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

    def iterator(self, n):
        values = list(self.data.values())
        while values:
            yield values[:n]
            values = values[n:]

    def __str__(self):
        return str(self.data)

book = AddressBook()
book.add_record(['Yehor', "+380674889977"])
book.add_record(['Liza', "+380674889277"])
book.add_record(['Andrew', "+380674889277"])

record_iterator = book.iterator(2)

print(next(record_iterator))