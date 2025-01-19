import sqlite3


def seed_data():
    conn = sqlite3.connect('client.db')
    cursor = conn.cursor()

    # Добавление номеров, если их нет
    cursor.execute("SELECT COUNT(*) FROM Room")
    if cursor.fetchone()[0] == 0:
        rooms = [
            ("Эконом", "Free", 1000),
            ("Стандарт", "Free", 1500),
            ("Полулюкс", "Free", 2500),
            ("Люкс", "Free", 3500)
        ]
        cursor.executemany("INSERT INTO Room (Category, Status, Price) VALUES (?, ?, ?)", rooms)

    # Добавление услуг, если их нет
    cursor.execute("SELECT COUNT(*) FROM Service")
    if cursor.fetchone()[0] == 0:
        services = [
            ("Уборка", "Ежедневная уборка номера", 0),
            ("Массаж", "Расслабляющий массаж", 1000),
            ("Завтрак в номер", "Континентальный завтрак", 500),
            ("Прачечная", "Стирка и глажка одежды", 300),
            ("Трансфер", "Трансфер из/в аэропорт", 1500)
        ]
        cursor.executemany("INSERT INTO Service (Name, Description, Price) VALUES (?, ?, ?)", services)

    conn.commit()
    conn.close()