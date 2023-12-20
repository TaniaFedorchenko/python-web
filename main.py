import pickle
import re
from datetime import datetime


class Contact:
    def __init__(self, name, phone, birthday, email):
        self.name = name
        self.phone = phone
        self.birthday = birthday
        self.email = email


class AddressBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, contact):
        self.contacts.append(contact)

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.contacts, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.contacts = pickle.load(file)
        except FileNotFoundError:
            pass

    def search_contacts(self, search_term):
        results = []
        for contact in self.contacts:
            if (search_term.lower() in contact.name.lower()) or (search_term in contact.phone):
                results.append(contact)
        return results

    def display_all_contacts(self):
        if self.contacts:
            print("Список користувачів:")
            for index, contact in enumerate(self.contacts):
                print(
                    f"{index + 1}. Ім'я: {contact.name}, Телефон: {contact.phone}, День народження: {contact.birthday}, Пошта: {contact.email}")
        else:
            print("Адресна книга порожня.")

    def edit_contact(self, index, name, phone, birthday, email):
        if 0 <= index < len(self.contacts):
            self.contacts[index].name = name
            self.contacts[index].phone = phone
            self.contacts[index].birthday = birthday
            self.contacts[index].email = email
            self.save_to_file('address_book.pkl')
            print("Контакт відредаговано!")

    def delete_contact(self, index):
        if 0 <= index < len(self.contacts):
            deleted_contact = self.contacts.pop(index)
            self.save_to_file('address_book.pkl')
            print(f"Контакт {deleted_contact.name} видалено!")

    def upcoming_birthdays(self, days):
        today = datetime.today()
        upcoming = []

        for contact in self.contacts:
            if contact.birthday:
                # Перетворюємо дату народження у вірний формат ('день.місяць.рік' -> 'рік-місяць-день')
                parts = contact.birthday.split('.')
                formatted_birthday = f'{parts[2]}-{parts[1]}-{parts[0]}'
                birthday = datetime.strptime(formatted_birthday, '%Y-%m-%d')
                days_until_birthday = (birthday - today).days
                if 0 <= days_until_birthday <= days:
                    upcoming.append((contact, days_until_birthday))

        return upcoming


# Перевірка правильності формату номеру телефону
def is_valid_phone(phone):
    return bool(re.match(r'^\+380\d{9}$', phone))


# Перевірка правильності формату пошти
def is_valid_email(email):
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))


# Основна частина програми
def main():
    address_book = AddressBook()

    try:
        address_book.load_from_file('address_book.pkl')
    except FileNotFoundError:
        pass

    while True:
        print("1. Додати контакт")
        print("2. Знайти контакт")
        print("3. Вивести список всіх контактів")
        print("4. Редагувати контакт")
        print("5. Видалити контакт")
        print("6. Перевірити дні народження")
        print("7. Вийти")

        choice = input("Виберіть дію: ")

        if choice == '1':
            name = input("Введіть ім'я контакту: ")
            phone = input("Введіть номер телефону контакту (+380xxxxxxxxx): ")
            while not is_valid_phone(phone):
                print("Невірний формат номеру телефону. Введіть ще раз (+380xxxxxxxxx).")
                phone = input("Введіть номер телефону контакту: ")

            birthday = input("Введіть день народження контакту (рік-місяць-день): ")
            email = input("Введіть пошту контакту: ")
            while not is_valid_email(email):
                print("Невірний формат пошти. Введіть ще раз.")
                email = input("Введіть пошту контакту: ")

            contact = Contact(name, phone, birthday, email)
            address_book.add_contact(contact)
            address_book.save_to_file('address_book.pkl')
            print("Контакт додано!")

        elif choice == '2':
            search_term = input("Введіть рядок для пошуку: ")
            results = address_book.search_contacts(search_term)
            if results:
                print("Знайдені контакти:")
                for index, contact in enumerate(results):
                    print(
                        f"{index + 1}. Ім'я: {contact.name}, Телефон: {contact.phone}, День народження: {contact.birthday}, Пошта: {contact.email}")
            else:
                print("Контакти не знайдені.")

        elif choice == '3':
            address_book.display_all_contacts()

        elif choice == '4':
            try:
                index = int(input("Введіть номер контакту для редагування: ")) - 1
                if 0 <= index < len(address_book.contacts):
                    name = input("Введіть нове ім'я контакту: ")
                    phone = input("Введіть новий номер телефону контакту (+380xxxxxxxxx): ")
                    while not is_valid_phone(phone):
                        print("Невірний формат номеру телефону. Введіть ще раз (+380xxxxxxxxx).")
                        phone = input("Введіть новий номер телефону контакту: ")
                    birthday = input("Введіть новий день народження контакту (рік-місяць-день): ")
                    email = input("Введіть нову пошту контакту: ")
                    while not is_valid_email(email):
                        print("Невірний формат пошти. Введіть ще раз.")
                        email = input("Введіть нову пошту контакту: ")
                    address_book.edit_contact(index, name, phone, birthday, email)
                else:
                    print("Номер контакту недійсний.")
            except ValueError:
                print("Неправильний формат вводу!")

        elif choice == '5':
            try:
                index = int(input("Введіть номер контакту для видалення: ")) - 1
                if 0 <= index < len(address_book.contacts):
                    address_book.delete_contact(index)
                else:
                    print("Номер контакту недійсний.")
            except ValueError:
                print("Неправильний формат вводу!")

        elif choice == '6':
            try:
                days = int(input("Скільки днів до дня народження перевірити: "))
            except ValueError:
                print("Неправильний формат вводу!")
                continue  # Перейти на наступну ітерацію циклу

            upcoming = address_book.upcoming_birthdays(days)
            if upcoming:
                print(f"Контакти з днями народження, які настають протягом наступних {days} днів:")
                for contact, days_until_birthday in upcoming:
                    print(
                        f"Ім'я: {contact.name}, День народження: {contact.birthday}, Днів до народження: {days_until_birthday}")
            else:
                print("Немає контактів з наближеними днями народження.")

        elif choice == '7':
            break


if __name__ == "__main__":
    main()

