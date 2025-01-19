import sqlite3
def reset_room_table():
    conn = sqlite3.connect('client.db')
    cursor = conn.cursor()

    # Удаляем таблицу Room, если она существует
    cursor.execute("DROP TABLE IF EXISTS Room")
    conn.commit()
    conn.close()


reset_room_table()

print("База данных и таблицы успешно созданы!")