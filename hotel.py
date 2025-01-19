import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import datetime
conn = sqlite3.connect('client.db')

class AdminLogin(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.db = master.db  # Соединение с базой данных

        tk.Label(self, text="Вход для администратора", font=("Arial", 16)).pack(pady=10)

        # Поле для ввода логина
        tk.Label(self, text="Логин:").pack(pady=5)
        self.login_entry = ttk.Entry(self)
        self.login_entry.pack(pady=5)

        # Поле для ввода пароля
        tk.Label(self, text="Пароль:").pack(pady=5)
        self.password_entry = ttk.Entry(self, show="*")  # Скрываем символы пароля
        self.password_entry.pack(pady=5)

        # Кнопка входа
        ttk.Button(self, text="Войти", command=self.login).pack(pady=10)

        # Кнопка возврата в главное меню
        ttk.Button(self, text="Назад", command=lambda: master.show_frame(MainMenu)).pack(pady=5)

    def login(self):
        """Проверяем логин и пароль"""
        login = self.login_entry.get()
        password = self.password_entry.get()

        # Пример с использованием хардкодированных данных (можно заменить на запрос к базе данных)
        if login == "admin" and password == "12345":  # Здесь можно задать свои тестовые данные
            messagebox.showinfo("Успех", "Вы вошли в систему!")
            self.master.show_frame(AdminPanel)  # Переход в панель администратора
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль!")

class HotelApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Система бронирования отеля')
        self.geometry('600x600')
        self.current_frame = None
        self.show_main_menu()

    def show_frame(self, frame_class):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame_class(self)
        self.current_frame.pack(fill='both', expand=True)

    def show_main_menu(self):
        self.show_frame(MainMenu)

    def on_closing(self):
        # Закрываем соединение с базой данных при закрытии приложения
        self.conn.close()
        self.destroy()


class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Главное меню", font=("Arial", 20)).pack(pady=20)
        ttk.Button(self, text="Регистрация клиента", command=lambda: master.show_frame(ClientRegistration)).pack(pady=5)
        ttk.Button(self, text="Авторизация клиента", command=lambda: master.show_frame(ClientLogin)).pack(pady=5)
        ttk.Button(self, text="Бронирование номера", command=lambda: master.show_frame(Booking)).pack(pady=5)
        ttk.Button(self, text="Заказ услуги", command=lambda: master.show_frame(ServiceOrder)).pack(pady=5)
        ttk.Button(self, text="Оплата", command=lambda: master.show_frame(Payment)).pack(pady=5)
        ttk.Button(self, text="Вход в админ-панель", command=self.admin_login).pack(pady=5)

    def admin_login(self):
        """Простая авторизация для входа в админ-панель"""
        login_window = tk.Toplevel(self)
        login_window.title("Вход в админ-панель")
        login_window.geometry("300x200")

        tk.Label(login_window, text="Введите логин и пароль", font=("Arial", 12)).pack(pady=10)

        tk.Label(login_window, text="Логин:").pack(pady=5)
        login_entry = ttk.Entry(login_window)
        login_entry.pack(pady=5)

        tk.Label(login_window, text="Пароль:").pack(pady=5)
        password_entry = ttk.Entry(login_window, show="*")
        password_entry.pack(pady=5)

        def verify_credentials():
            login = login_entry.get()
            password = password_entry.get()

            # Хардкодированные данные для входа
            if login == "admin" and password == "12345":
                messagebox.showinfo("Успех", "Вы вошли как администратор")
                self.master.show_frame(AdminPanel)
                login_window.destroy()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль!")

        ttk.Button(login_window, text="Войти", command=verify_credentials).pack(pady=10)


class ClientRegistration(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.db = sqlite3.connect("client.db")
        self.cursor = self.db.cursor()

        tk.Label(self, text="Регистрация клиента", font=("Arial", 16)).pack(pady=10)

        # Поля для регистрации
        ttk.Label(self, text="Фамилия:").pack(pady=2)
        self.surname_entry = ttk.Entry(self)
        self.surname_entry.pack(pady=2)

        ttk.Label(self, text="Имя:").pack(pady=2)
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack(pady=2)

        ttk.Label(self, text="Отчество:").pack(pady=2)
        self.patronymic_entry = ttk.Entry(self)
        self.patronymic_entry.pack(pady=2)

        ttk.Label(self, text="Паспорт:").pack(pady=2)
        self.passport_entry = ttk.Entry(self)
        self.passport_entry.pack(pady=2)

        ttk.Label(self, text="Email:").pack(pady=2)
        self.email_entry = ttk.Entry(self)
        self.email_entry.pack(pady=2)

        ttk.Label(self, text="Пароль:").pack(pady=2)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack(pady=2)

        ttk.Button(self, text="Зарегистрироваться", command=self.register).pack(pady=10)
        ttk.Button(self, text="Назад", command=lambda: master.show_frame(MainMenu)).pack(pady=5)

    def register(self):
        surname = self.surname_entry.get()
        name = self.name_entry.get()
        patronymic = self.patronymic_entry.get()
        passport = self.passport_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Проверяем, что все поля заполнены
        if not all([surname, name, passport, email, password]):
            messagebox.showerror("Ошибка", "Все поля, кроме отчества, должны быть заполнены!")
            return

        try:
            # Добавляем нового клиента в базу данных
            self.cursor.execute(
                "INSERT INTO Client (Surname, Name, Patronymic, Passport, Email, Password) VALUES (?, ?, ?, ?, ?, ?)",
                (surname, name, patronymic, passport, email, password))
            self.db.commit()
            messagebox.showinfo("Успех", "Регистрация успешна!")
            self.master.show_frame(MainMenu)  # Возврат в главное меню
        except sqlite3.IntegrityError:
            messagebox.showerror("Ошибка", "Пользователь с таким email или паспортом уже существует!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

class ClientLogin(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.db = sqlite3.connect("client.db")
        self.cursor = self.db.cursor()

        tk.Label(self, text="Авторизация клиента", font=("Arial", 16)).pack(pady=10)

        ttk.Label(self, text="Email:").pack(pady=2)
        self.email_entry = ttk.Entry(self)
        self.email_entry.pack(pady=2)

        ttk.Label(self, text="Пароль:").pack(pady=2)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack(pady=2)

        ttk.Button(self, text="Войти", command=self.login).pack(pady=10)
        ttk.Button(self, text="Назад", command=lambda: master.show_frame(MainMenu)).pack(pady=5)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Проверяем, что поля заполнены
        if not email or not password:
            messagebox.showerror("Ошибка", "Введите email и пароль!")
            return

        try:
            # Проверяем, существует ли пользователь с указанным email
            self.cursor.execute("SELECT Password FROM Client WHERE Email = ?", (email,))
            client = self.cursor.fetchone()

            if client and client[0] == password:
                messagebox.showinfo("Успех", "Вход выполнен!")
                self.master.show_frame(MainMenu)  # Возврат в главное меню
            else:
                messagebox.showerror("Ошибка", "Неверный email или пароль!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

class Booking(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.db = sqlite3.connect("client.db")
        self.cursor = self.db.cursor()

        tk.Label(self, text="Бронирование номера", font=("Arial", 16)).pack(pady=10)

        # Виджеты для ввода данных
        ttk.Label(self, text="Дата заезда (YYYY-MM-DD):").pack(pady=2)
        self.check_in_entry = ttk.Entry(self)
        self.check_in_entry.pack(pady=2)

        ttk.Label(self, text="Дата выезда (YYYY-MM-DD):").pack(pady=2)
        self.check_out_entry = ttk.Entry(self)
        self.check_out_entry.pack(pady=2)

        ttk.Label(self, text="Категория номера:").pack(pady=2)
        self.room_category = tk.StringVar(self)
        room_categories = ["Эконом", "Стандарт", "Полулюкс", "Люкс"]
        self.room_category_dropdown = ttk.Combobox(self, textvariable=self.room_category, values=room_categories)
        self.room_category_dropdown.pack(pady=2)

        ttk.Button(self, text="Забронировать", command=self.book).pack(pady=10)
        ttk.Button(self, text="Назад", command=lambda: master.show_frame(MainMenu)).pack(pady=5)

        # Виджет Treeview для отображения доступных номеров
        self.rooms_tree = ttk.Treeview(self, columns=("ID", "Category", "Status", "Price"), show="headings")
        self.rooms_tree.heading("ID", text="ID")
        self.rooms_tree.heading("Category", text="Категория")
        self.rooms_tree.heading("Status", text="Статус")
        self.rooms_tree.heading("Price", text="Цена")
        self.rooms_tree.pack(pady=10)

        # Заполнение Treeview данными из базы
        self.update_rooms_tree()

    def book(self):
        try:
            # Получаем данные из полей ввода
            check_in_date_str = self.check_in_entry.get()
            check_out_date_str = self.check_out_entry.get()
            room_category = self.room_category.get()

            # Проверка формата дат
            check_in_date = datetime.datetime.strptime(check_in_date_str, '%Y-%m-%d').date()
            check_out_date = datetime.datetime.strptime(check_out_date_str, '%Y-%m-%d').date()

            # Валидация данных
            if check_in_date >= check_out_date:
                raise ValueError("Дата выезда должна быть позже даты заезда.")
            if not room_category:
                raise ValueError("Выберите категорию номера.")

            # Проверяем, выбран ли номер в Treeview
            selected_item = self.rooms_tree.selection()
            if not selected_item:
                raise ValueError("Выберите номер из списка.")

            # Получаем ID выбранного номера
            room_id = self.rooms_tree.item(selected_item[0])["values"][0]

            # Проверка на занятость номера
            self.cursor.execute("""
                SELECT * FROM Booking
                WHERE Id_room = ? AND (
                    (check_in_date <= ? AND check_out_date > ?) OR
                    (check_in_date < ? AND check_out_date >= ?)
                )
            """, (room_id, check_in_date, check_in_date, check_out_date, check_out_date))
            existing_booking = self.cursor.fetchone()
            if existing_booking:
                raise ValueError(f"Номер {room_id} занят на указанные даты.")

            # Бронирование номера
            self.cursor.execute(
                "INSERT INTO Booking (Id_room, check_in_date, check_out_date, booking_status) VALUES (?, ?, ?, ?)",
                (room_id, check_in_date, check_out_date, "Confirmed"))
            self.db.commit()
            messagebox.showinfo("Успех", "Номер успешно забронирован!")
            self.master.show_frame(MainMenu)  # Возврат в главное меню
            self.update_rooms_tree()  # Обновляем отображение свободных/занятых номеров

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    def find_free_room(self, category, check_in_date, check_out_date):
        # Поиск свободного номера по категории и датам
        self.cursor.execute("""
            SELECT Id_room FROM Room
            WHERE Category = ? AND Id_room NOT IN (
                SELECT Id_room FROM Booking
                WHERE (check_in_date <= ? AND check_out_date > ?) OR (check_in_date < ? AND check_out_date >= ?)
            )
            LIMIT 1
        """, (category, check_in_date, check_in_date, check_out_date, check_out_date))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def update_rooms_tree(self):
        # Очистка текущих данных в Treeview
        for item in self.rooms_tree.get_children():
            self.rooms_tree.delete(item)

        # Заполнение Treeview данными из таблицы Room
        self.cursor.execute("SELECT Id_room, Category, Status, Price_per_night FROM Room")
        rooms = self.cursor.fetchall()
        for room in rooms:
            self.rooms_tree.insert("", "end", values=room)

class ViewBookings(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.db = sqlite3.connect("client.db")
        self.cursor = self.db.cursor()

        tk.Label(self, text="Просмотр бронирований", font=("Arial", 16)).pack(pady=10)

        self.bookings_tree = ttk.Treeview(self, columns=("ID", "Клиент", "Номер", "Заезд", "Выезд", "Статус"),
                                          show="headings")
        self.bookings_tree.heading("ID", text="ID")
        self.bookings_tree.heading("Клиент", text="Клиент")
        self.bookings_tree.heading("Номер", text="Номер")
        self.bookings_tree.heading("Заезд", text="Дата заезда")
        self.bookings_tree.heading("Выезд", text="Дата выезда")
        self.bookings_tree.heading("Статус", text="Статус")
        self.bookings_tree.pack(pady=10)

        ttk.Button(self, text="Обновить список", command=self.update_bookings_tree).pack(pady=5)
        ttk.Button(self, text="Назад", command=lambda: master.show_frame(AdminPanel)).pack(pady=5)

        self.update_bookings_tree()

    def update_bookings_tree(self):
        for item in self.bookings_tree.get_children():
            self.bookings_tree.delete(item)

        self.cursor.execute("""
            SELECT b.Id_booking, c.Surname || ' ' || c.Name, r.Category, b.check_in_date, b.check_out_date, b.booking_status
            FROM Booking b
            JOIN Client c ON b.Id_client = c.Id_client
            JOIN Room r ON b.Id_room = r.Id_room
        """)
        bookings = self.cursor.fetchall()
        for booking in bookings:
            self.bookings_tree.insert("", "end", values=booking)
class ManageClients(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.db = sqlite3.connect("client.db")
        self.cursor = self.db.cursor()

        tk.Label(self, text="Управление клиентами", font=("Arial", 16)).pack(pady=10)

        # Таблица для отображения клиентов
        self.clients_tree = ttk.Treeview(self, columns=("ID", "Фамилия", "Имя", "Отчество", "Паспорт", "Email"),
                                         show="headings")
        self.clients_tree.heading("ID", text="ID")
        self.clients_tree.heading("Фамилия", text="Фамилия")
        self.clients_tree.heading("Имя", text="Имя")
        self.clients_tree.heading("Отчество", text="Отчество")
        self.clients_tree.heading("Паспорт", text="Паспорт")
        self.clients_tree.heading("Email", text="Email")
        self.clients_tree.pack(pady=10)
        self.update_clients_tree()

        # Кнопки действий
        ttk.Button(self, text="Удалить клиента", command=self.delete_client).pack(pady=5)
        ttk.Button(self, text="Обновить список", command=self.update_clients_tree).pack(pady=5)
        ttk.Button(self, text="Назад", command=lambda: master.show_frame(AdminPanel)).pack(pady=5)

    def update_clients_tree(self):
        """Обновление данных о клиентах"""
        for item in self.clients_tree.get_children():
            self.clients_tree.delete(item)

        self.cursor.execute("SELECT Id_client, Surname, Name, Patronymic, Passport, Email FROM Client")
        clients = self.cursor.fetchall()
        for client in clients:
            self.clients_tree.insert("", "end", values=client)

    def delete_client(self):
        """Удаление выбранного клиента"""
        selected_item = self.clients_tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите клиента для удаления!")
            return

        client_id = self.clients_tree.item(selected_item[0])["values"][0]
        try:
            self.cursor.execute("DELETE FROM Client WHERE Id_client = ?", (client_id,))
            self.db.commit()
            messagebox.showinfo("Успех", "Клиент удалён!")
            self.update_clients_tree()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить клиента: {e}")

class ViewServices(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.db = sqlite3.connect("client.db")
        self.cursor = self.db.cursor()

        tk.Label(self, text="Просмотр услуг", font=("Arial", 16)).pack(pady=10)

        # Таблица для отображения услуг
        self.services_tree = ttk.Treeview(self, columns=("ID", "Название", "Описание", "Цена"), show="headings")
        self.services_tree.heading("ID", text="ID")
        self.services_tree.heading("Название", text="Название")
        self.services_tree.heading("Описание", text="Описание")
        self.services_tree.heading("Цена", text="Цена")
        self.services_tree.pack(pady=10)
        self.update_services_tree()

        # Кнопки действий
        ttk.Button(self, text="Обновить список", command=self.update_services_tree).pack(pady=5)
        ttk.Button(self, text="Назад", command=lambda: master.show_frame(AdminPanel)).pack(pady=5)

    def update_services_tree(self):
        """Обновление списка услуг"""
        for item in self.services_tree.get_children():
            self.services_tree.delete(item)

        self.cursor.execute("SELECT Id_service, Name, Description, Price FROM Service")
        services = self.cursor.fetchall()
        for service in services:
            self.services_tree.insert("", "end", values=service)

class ViewPayments(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.db = sqlite3.connect("client.db")
        self.cursor = self.db.cursor()

        tk.Label(self, text="Просмотр платежей", font=("Arial", 16)).pack(pady=10)

        # Таблица для отображения платежей
        self.payments_tree = ttk.Treeview(self, columns=("ID", "Бронирование", "Сумма", "Дата", "Способ оплаты"),
                                          show="headings")
        self.payments_tree.heading("ID", text="ID")
        self.payments_tree.heading("Бронирование", text="ID бронирования")
        self.payments_tree.heading("Сумма", text="Сумма")
        self.payments_tree.heading("Дата", text="Дата")
        self.payments_tree.heading("Способ оплаты", text="Способ оплаты")
        self.payments_tree.pack(pady=10)
        self.update_payments_tree()

        # Кнопки действий
        ttk.Button(self, text="Обновить список", command=self.update_payments_tree).pack(pady=5)
        ttk.Button(self, text="Назад", command=lambda: master.show_frame(AdminPanel)).pack(pady=5)

    def update_payments_tree(self):
        """Обновление списка платежей"""
        for item in self.payments_tree.get_children():
            self.payments_tree.delete(item)

        self.cursor.execute("SELECT Id_payment, Id_booking, Sum, Date, Payment_method FROM Payment")
        payments = self.cursor.fetchall()
        for payment in payments:
            self.payments_tree.insert("", "end", values=payment)

class ManageRooms(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.db = sqlite3.connect("client.db")
        self.cursor = self.db.cursor()

        tk.Label(self, text="Управление номерами", font=("Arial", 16)).pack(pady=10)

        # Отображение номеров
        self.rooms_tree = ttk.Treeview(self, columns=("ID", "Category", "Status", "Price"), show="headings")
        self.rooms_tree.heading("ID", text="ID")
        self.rooms_tree.heading("Category", text="Категория")
        self.rooms_tree.heading("Status", text="Статус")
        self.rooms_tree.heading("Price", text="Цена")
        self.rooms_tree.pack(pady=10)
        self.update_rooms_tree()

        # Поля для добавления/редактирования номера
        ttk.Label(self, text="Категория:").pack(pady=2)
        self.category_entry = ttk.Entry(self)
        self.category_entry.pack(pady=2)

        ttk.Label(self, text="Статус:").pack(pady=2)
        self.status_entry = ttk.Entry(self)
        self.status_entry.pack(pady=2)

        ttk.Label(self, text="Цена за ночь:").pack(pady=2)
        self.price_entry = ttk.Entry(self)
        self.price_entry.pack(pady=2)

        ttk.Button(self, text="Добавить номер", command=self.add_room).pack(pady=5)
        ttk.Button(self, text="Удалить номер", command=self.delete_room).pack(pady=5)
        ttk.Button(self, text="Обновить список", command=self.update_rooms_tree).pack(pady=5)
        ttk.Button(self, text="Назад", command=lambda: master.show_frame(AdminPanel)).pack(pady=5)

    def update_rooms_tree(self):
        for item in self.rooms_tree.get_children():
            self.rooms_tree.delete(item)

        self.cursor.execute("SELECT Id_room, Category, Status, Price_per_night FROM Room")
        rooms = self.cursor.fetchall()
        for room in rooms:
            self.rooms_tree.insert("", "end", values=room)

    def add_room(self):
        category = self.category_entry.get()
        status = self.status_entry.get()
        price = self.price_entry.get()

        try:
            self.cursor.execute("INSERT INTO Room (Category, Status, Price_per_night) VALUES (?, ?, ?)",
                                (category, status, price))
            self.db.commit()
            messagebox.showinfo("Успех", "Номер добавлен!")
            self.update_rooms_tree()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить номер: {e}")

    def delete_room(self):
        selected_item = self.rooms_tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите номер для удаления!")
            return

        room_id = self.rooms_tree.item(selected_item[0])["values"][0]
        try:
            self.cursor.execute("DELETE FROM Room WHERE Id_room = ?", (room_id,))
            self.db.commit()
            messagebox.showinfo("Успех", "Номер удалён!")
            self.update_rooms_tree()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить номер: {e}")

class AdminPanel(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.db = sqlite3.connect("client.db")
        self.cursor = self.db.cursor()

        tk.Label(self, text="Панель администратора", font=("Arial", 16)).pack(pady=10)

        # Кнопки для управления
        ttk.Button(self, text="Управление номерами", command=self.manage_rooms).pack(pady=5)
        ttk.Button(self, text="Управление клиентами", command=self.manage_clients).pack(pady=5)
        ttk.Button(self, text="Просмотр бронирований", command=self.view_bookings).pack(pady=5)
        ttk.Button(self, text="Просмотр услуг", command=self.view_services).pack(pady=5)
        ttk.Button(self, text="Просмотр платежей", command=self.view_payments).pack(pady=5)
        ttk.Button(self, text="Назад", command=lambda: master.show_frame(MainMenu)).pack(pady=5)

    def manage_rooms(self):
        """Открыть управление номерами"""
        self.master.show_frame(ManageRooms)

    def manage_clients(self):
        """Открыть управление клиентами"""
        self.master.show_frame(ManageClients)

    def view_bookings(self):
        """Просмотр всех бронирований"""
        self.master.show_frame(ViewBookings)

    def view_services(self):
        """Просмотр всех услуг"""
        self.master.show_frame(ViewServices)

    def view_payments(self):
        """Просмотр всех платежей"""
        self.master.show_frame(ViewPayments)

class ServiceOrder(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.db = sqlite3.connect("client.db")
        self.cursor = self.db.cursor()

        tk.Label(self, text="Заказ услуги", font=("Arial", 16)).pack(pady=10)

        ttk.Label(self, text="ID бронирования:").pack(pady=2)
        self.booking_id_entry = ttk.Entry(self)
        self.booking_id_entry.pack(pady=2)

        ttk.Label(self, text="ID услуги:").pack(pady=2)
        self.service_id_entry = ttk.Entry(self)
        self.service_id_entry.pack(pady=2)

        ttk.Label(self, text="Выберите услугу:").pack(pady=2)
        services = [("Уборка", 0), ("Массаж", 1000), ("Завтрак в номер", 500), ("Прачечная", 300), ("Трансфер", 1500)]
        self.service_var = tk.StringVar(self)
        for name, price in services:
            ttk.Radiobutton(self, text=f"{name} - {price}р.", variable=self.service_var, value=name).pack()

        ttk.Button(self, text="Заказать услугу", command=self.order_service).pack(pady=10)
        ttk.Button(self, text="Назад", command=lambda: master.show_frame(MainMenu)).pack(pady=5)

        # Вывод списка услуг
        self.services_tree = ttk.Treeview(self, columns=("ID", "Name", "Description", "Price"), show="headings")
        self.services_tree.heading("ID", text="ID")
        self.services_tree.heading("Name", text="Название")
        self.services_tree.heading("Description", text="Описание")
        self.services_tree.heading("Price", text="Цена")
        self.services_tree.pack(pady=10)
        self.update_services_tree()

    def order_service(self):
        try:
            booking_id = int(self.booking_id_entry.get())
            service_name = self.service_var.get()
            if service_name == "":
                raise ValueError("Выберите услугу!")

            self.cursor.execute("SELECT Id_service, Price FROM Service WHERE Name = ?", (service_name,))
            service = self.cursor.fetchone()
            if service is None:
                raise ValueError("Ошибка: услуга не найдена")
            service_id, price = service

            self.cursor.execute("INSERT INTO ServiceOrder (booking_id, service_id) VALUES (?, ?)",
                                (booking_id, service_id))
            self.db.commit()
            messagebox.showinfo("Успех", "Услуга успешно заказана!")
            self.master.show_frame(MainMenu)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
        finally:
            self.db.close()

    def update_services_tree(self):
        for item in self.services_tree.get_children():
            self.services_tree.delete(item)

        self.cursor.execute("SELECT Id_service, Name, Description, Price FROM Service")
        services = self.cursor.fetchall()
        for service in services:
            self.services_tree.insert("", "end", values=service)

class Payment(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.db = sqlite3.connect("client.db")
        self.cursor = self.db.cursor()

        tk.Label(self, text="Оплата", font=("Arial", 16)).pack(pady=10)

        ttk.Label(self, text="ID бронирования:").pack(pady=2)
        self.booking_id_entry = ttk.Entry(self)
        self.booking_id_entry.pack(pady=2)

        ttk.Label(self, text="Сумма:").pack(pady=2)
        self.sum_entry = ttk.Entry(self)
        self.sum_entry.pack(pady=2)

        ttk.Label(self, text="Способ оплаты:").pack(pady=2)
        self.payment_method_entry = ttk.Entry(self)
        self.payment_method_entry.pack(pady=2)

        ttk.Button(self, text="Оплатить", command=self.make_payment).pack(pady=10)
        ttk.Button(self, text="Назад", command=lambda: master.show_frame(MainMenu)).pack(pady=5)

    def make_payment(self):
        try:
            booking_id = int(self.booking_id_entry.get())
            sum = float(self.sum_entry.get())
            payment_method = self.payment_method_entry.get()
            self.cursor.execute("INSERT INTO Payment (Id_booking, Sum, Date, Payment_method) VALUES (?, ?, ?, ?)",
                                (booking_id, sum, datetime.date.today(), payment_method))
            self.db.commit()
            messagebox.showinfo("Успех", "Оплата успешно проведена!")
            self.master.show_frame(MainMenu)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
        finally:
            self.db.close()

app = HotelApp()
app.mainloop()
