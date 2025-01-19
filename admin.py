import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class AdminPanel(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.db = master.db  # Передаём соединение с базой данных из главного приложения

        tk.Label(self, text="Панель администратора", font=("Arial", 16)).pack(pady=10)

        # Кнопки для управления
        ttk.Button(self, text="Управление номерами", command=self.manage_rooms).pack(pady=5)
        ttk.Button(self, text="Управление клиентами", command=self.manage_clients).pack(pady=5)
        ttk.Button(self, text="Просмотр бронирований", command=self.view_bookings).pack(pady=5)
        ttk.Button(self, text="Просмотр услуг", command=self.view_services).pack(pady=5)
        ttk.Button(self, text="Просмотр платежей", command=self.view_payments).pack(pady=5)
        ttk.Button(self, text="Назад", command=lambda: master.show_frame(MainMenu)).pack(pady=5)

    def manage_rooms(self):
        self.master.show_frame(ManageRooms)

    def manage_clients(self):
        self.master.show_frame(ManageClients)

    def view_bookings(self):
        self.master.show_frame(ViewBookings)

    def view_services(self):
        self.master.show_frame(ViewServices)

    def view_payments(self):
        self.master.show_frame(ViewPayments)


class ManageRooms(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.db = master.db
        self.cursor = self.db.cursor()

        tk.Label(self, text="Управление номерами", font=("Arial", 16)).pack(pady=10)

        # Таблица для номеров
        self.rooms_tree = ttk.Treeview(self, columns=("ID", "Категория", "Статус", "Цена"), show="headings")
        self.rooms_tree.heading("ID", text="ID")
        self.rooms_tree.heading("Категория", text="Категория")
        self.rooms_tree.heading("Статус", text="Статус")
        self.rooms_tree.heading("Цена", text="Цена")
        self.rooms_tree.pack(pady=10)

        ttk.Button(self, text="Обновить", command=self.update_tree).pack(pady=5)
        ttk.Button(self, text="Назад", command=lambda: master.show_frame(AdminPanel)).pack(pady=5)

        self.update_tree()

    def update_tree(self):
        """Обновить данные таблицы номеров"""
        for item in self.rooms_tree.get_children():
            self.rooms_tree.delete(item)

        self.cursor.execute("SELECT Id_room, Category, Status, Price_per_night FROM Room")
        for room in self.cursor.fetchall():
            self.rooms_tree.insert("", "end", values=room)


class ManageClients(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.db = master.db
        self.cursor = self.db.cursor()

        tk.Label(self, text="Управление клиентами", font=("Arial", 16)).pack(pady=10)

        # Таблица для клиентов
        self.clients_tree = ttk.Treeview(self, columns=("ID", "Фамилия", "Имя", "Email"), show="headings")
        self.clients_tree.heading("ID", text="ID")
        self.clients_tree.heading("Фамилия", text="Фамилия")
        self.clients_tree.heading("Имя", text="Имя")
        self.clients_tree.heading("Email", text="Email")
        self.clients_tree.pack(pady=10)

        ttk.Button(self, text="Обновить", command=self.update_tree).pack(pady=5)
        ttk.Button(self, text="Назад", command=lambda: master.show_frame(AdminPanel)).pack(pady=5)

        self.update_tree()

    def update_tree(self):
        """Обновить данные таблицы клиентов"""
        for item in self.clients_tree.get_children():
            self.clients_tree.delete(item)

        self.cursor.execute("SELECT Id_client, Surname, Name, Email FROM Client")
        for client in self.cursor.fetchall():
            self.clients_tree.insert("", "end", values=client)


class ViewBookings(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.db = master.db
        self.cursor = self.db.cursor()

        tk.Label(self, text="Просмотр бронирований", font=("Arial", 16)).pack(pady=10)

        # Таблица для бронирований
        self.bookings_tree = ttk.Treeview(self, columns=("ID", "Клиент", "Номер", "Дата заезда", "Дата выезда"),
                                          show="headings")
        self.bookings_tree.heading("ID", text="ID")
        self.bookings_tree.heading("Клиент", text="Клиент")
        self.bookings_tree.heading("Номер", text="Номер")
        self.bookings_tree.heading("Дата заезда", text="Дата заезда")
        self.bookings_tree.heading("Дата выезда", text="Дата выезда")
        self.bookings_tree.pack(pady=10)

        ttk.Button(self, text="Обновить", command=self.update_tree).pack(pady=5)
        ttk.Button(self, text="Назад", command=lambda: master.show_frame(AdminPanel)).pack(pady=5)

        self.update_tree()

    def update_tree(self):
        """Обновить данные таблицы бронирований"""
        for item in self.bookings_tree.get_children():
            self.bookings_tree.delete(item)

        self.cursor.execute("""
            SELECT b.Id_booking, c.Surname || ' ' || c.Name, r.Category, b.check_in_date, b.check_out_date
            FROM Booking b
            JOIN Client c ON b.Id_client = c.Id_client
            JOIN Room r ON b.Id_room = r.Id_room
        """)
        for booking in self.cursor.fetchall():
            self.bookings_tree.insert("", "end", values=booking)