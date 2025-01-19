import sqlite3


def setup_database():
    conn = sqlite3.connect('client.db')
    cursor = conn.cursor()

    # Таблица клиентов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Client (
            Id_client INTEGER PRIMARY KEY AUTOINCREMENT,
            Surname TEXT NOT NULL,
            Name TEXT NOT NULL,
            Patronymic TEXT,
            Passport TEXT UNIQUE NOT NULL,
            Email TEXT UNIQUE NOT NULL,
            Password TEXT NOT NULL
        )
    ''')

    # Таблица номеров
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Room (
            Id_room INTEGER PRIMARY KEY AUTOINCREMENT,
            Category TEXT NOT NULL,
            Status TEXT DEFAULT 'Free',
            Price REAL NOT NULL
        )
    ''')

    # Таблица бронирований
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Booking (
            Id_booking INTEGER PRIMARY KEY AUTOINCREMENT,
            Id_room INTEGER NOT NULL,
            Id_client INTEGER NOT NULL,
            check_in_date DATE NOT NULL,
            check_out_date DATE NOT NULL,
            booking_status TEXT NOT NULL,
            FOREIGN KEY (Id_room) REFERENCES Room(Id_room),
            FOREIGN KEY (Id_client) REFERENCES Client(Id_client)
        )
    ''')

    # Таблица услуг
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Service (
            Id_service INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Description TEXT,
            Price REAL NOT NULL
        )
    ''')

    # Таблица заказов услуг
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ServiceOrder (
            Id_order INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER NOT NULL,
            service_id INTEGER NOT NULL,
            FOREIGN KEY (booking_id) REFERENCES Booking(Id_booking),
            FOREIGN KEY (service_id) REFERENCES Service(Id_service)
        )
    ''')

    # Таблица платежей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Payment (
            Id_payment INTEGER PRIMARY KEY AUTOINCREMENT,
            Id_booking INTEGER NOT NULL,
            Sum REAL NOT NULL,
            Date DATE NOT NULL,
            Payment_method TEXT NOT NULL,
            FOREIGN KEY (Id_booking) REFERENCES Booking(Id_booking)
        )
    ''')

    conn.commit()
    conn.close()