"""Наповнення бази даних тестовими даними.

Запуск:  python3 seed.py
Скрипт видаляє всі дані й створює базу заново.
"""

from app import create_app
from database import db
from models import Counterparty, Product, Supplier, User

SUPPLIERS = [
    ("ТОВ «Офіс-Постач»", "+380 44 123 45 67", "sales@office-postach.ua", "м. Київ, вул. Січових Стрільців, 21"),
    ("ТОВ «ПаперЛюкс»", "+380 32 245 11 22", "info@paperlux.ua", "м. Львів, вул. Городоцька, 120"),
    ("ТОВ «ТехноСвіт»", "+380 57 700 30 40", "order@technosvit.ua", "м. Харків, просп. Науки, 14"),
    ("ФОП Коваленко О. М.", "+380 67 555 12 34", "kovalenko.om@gmail.com", "м. Вінниця, вул. Соборна, 5"),
    ("ТОВ «Електрон-Трейд»", "+380 48 799 88 77", "trade@electron.ua", "м. Одеса, вул. Дерибасівська, 9"),
]

COUNTERPARTIES = [
    ("ТОВ «Школа майбутнього»", "client", "+380 44 333 22 11", "office@school-future.ua"),
    ("Бібліотека ЛНУ ім. І. Франка", "client", "+380 32 239 41 00", "library@lnu.edu.ua"),
    ("ТОВ «Бізнес-Центр Плаза»", "client", "+380 32 297 00 00", "admin@plaza-bc.ua"),
    ("ФОП Мельник І. В. (магазин «Канцелярія»)", "partner", "+380 98 123 45 67", "melnyk.shop@ukr.net"),
]

# (назва, артикул, ціна, мінімальний запас, номер постачальника у списку SUPPLIERS)
PRODUCTS = [
    ("Папір офісний A4, 500 арк.", "PAP-A4-500", 245.00, 20, 1),
    ("Папір офісний A3, 500 арк.", "PAP-A3-500", 520.00, 5, 1),
    ("Зошит 48 арк., клітинка", "ZOS-48-KL", 32.50, 30, 1),
    ("Блокнот A5, 80 арк.", "BLK-A5-80", 68.00, 15, 1),
    ("Ручка кулькова синя", "RUC-KUL-BL", 12.00, 50, 0),
    ("Ручка гелева чорна", "RUC-GEL-BK", 18.50, 40, 0),
    ("Олівець простий HB", "OLV-HB", 7.00, 50, 0),
    ("Маркер текстовий жовтий", "MRK-TXT-YL", 24.00, 20, 0),
    ("Степлер №24/6", "STP-24-6", 145.00, 5, 3),
    ("Скоби для степлера №24/6, 1000 шт.", "SKB-24-6", 22.00, 25, 3),
    ("Папка-реєстратор A4, 75 мм", "PPK-REG-75", 89.00, 10, 3),
    ("Файли A4, 100 шт.", "FAJ-A4-100", 115.00, 10, 3),
    ("Калькулятор настільний", "KLK-NST-12", 380.00, 3, 2),
    ("Мишка комп'ютерна USB", "MSH-USB", 299.00, 5, 2),
    ("Клавіатура USB", "KLV-USB", 549.00, 3, 2),
    ("Флеш-накопичувач 32 ГБ", "FLS-32GB", 259.00, 10, 4),
    ("Картридж для принтера HP 85A", "KRT-HP-85A", 1250.00, 2, 4),
    ("Батарейки AA, 4 шт.", "BAT-AA-4", 95.00, 15, 4),
    ("Подовжувач 5 розеток, 3 м", "POD-5R-3M", 420.00, 3, 4),
    ("Лампа настільна LED", "LMP-LED", 690.00, 2, 2),
]

# (логін, пароль, роль)
USERS = [
    ("admin", "admin123", "admin"),
    ("manager", "manager123", "manager"),
    ("keeper", "keeper123", "keeper"),
]


def seed():
    db.drop_all()
    db.create_all()

    suppliers = [Supplier(name=n, phone=p, email=e, address=a) for n, p, e, a in SUPPLIERS]
    db.session.add_all(suppliers)

    db.session.add_all(
        Counterparty(name=n, kind=k, phone=p, email=e) for n, k, p, e in COUNTERPARTIES
    )

    # Кількість на старті 0: товари потраплять на склад лише через
    # прибуткові накладні — так кожна одиниця товару має документ.
    db.session.add_all(
        Product(name=n, sku=s, price=pr, min_quantity=mq, quantity=0, supplier=suppliers[i])
        for n, s, pr, mq, i in PRODUCTS
    )

    for username, password, role in USERS:
        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)

    db.session.commit()


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed()
        print(f"Готово: {len(SUPPLIERS)} постачальників, {len(COUNTERPARTIES)} контрагентів, "
              f"{len(PRODUCTS)} товарів, {len(USERS)} користувачі.")