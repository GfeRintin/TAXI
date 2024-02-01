import sqlite3
import datetime

class SQLighter:
    def __init__(self,database_file):
        """ Констуктор """
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def add_subscriber(self, user_id, username, first_name, last_name):
        """Добавляем нового подписчика"""
        if not last_name:
            last_name = False
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO users (user_id, username,first_name,last_name) VALUES(?,?,?,?)",
                (user_id, username, first_name, last_name))

    def subscriber_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()

    def update_UserName(self, user_id, username):
        """Изменяем имя пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE users SET username = ?  WHERE user_id = ?",
                                       (username, user_id,))
    
    def all_admin(self):
        """Получаем всех администраторов"""
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM users WHERE admin = 1 ").fetchall()
    
    def new_order(self, address, create_order, phone, user_id):
        """Создаем новый заказ"""
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO orders (create_order, address, number_phone, user_id) VALUES(?,?,?,?)",
                (create_order, address, phone, user_id))
        
    def add_message_chat(self, message_chat, order_id):
        """Добавляю к заказу сообщение в чате"""
        with self.connection:
            return self.cursor.execute("UPDATE orders SET message_chat = ?  WHERE id = ?",
                                       (message_chat, order_id,))
        
    def add_message_client(self, message_client, order_id):
        """Добавляю к заказу сообщение клиента"""
        with self.connection:
            return self.cursor.execute("UPDATE orders SET message_client = ?  WHERE id = ?",
                                       (message_client, order_id,))
    
    def get_message_chat(self, user_id):
        """Получаем сообщение заказа в чате"""
        with self.connection:
            return self.cursor.execute("""SELECT message_chat FROM orders
                                        WHERE user_id = ?""" , (user_id,)).fetchall()[-1][0]
    
    def get_message_client(self, user_id):
        """Получаем сообщение заказа в чате"""
        with self.connection:
            return self.cursor.execute("""SELECT message_client FROM orders
                                        WHERE user_id = ?""" , (user_id,)).fetchall()[-1][0]
    
    def get_order_last(self):
        """Получаем последний заказ в базе"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM orders WHERE id = (select max(id) from orders)").fetchall()

    def add_phone(self, phone, user_id):
        """Добавляем номер телефона"""
        with self.connection:
            return self.cursor.execute("UPDATE users SET number_phone = ?  WHERE user_id = ?",
                                       (phone, user_id,))
        
    def get_order(self, order_id, username):
        """Добавляем водителя и время к заказу"""
        with self.connection:
            return self.cursor.execute("""UPDATE orders
                                        SET get_order = ?, who_get_order = ?
                                        WHERE id = ?""",
                                       (datetime.datetime.now().strftime("%d/%m/%y %H:%M"), username, order_id,))

    def add_number_car(self, number_car, user_id):
        """Добавляем номер машины"""
        with self.connection:
            return self.cursor.execute("""UPDATE users
                                        SET number_car = ?
                                        WHERE user_id = ?""",
                                       (number_car, user_id))
    
    def add_driver(self, user_id, orders_left):
        """Добавляем Водителя"""
        # orders_left = 20
        with self.connection:
            return self.cursor.execute("""UPDATE users
                                        SET driver = 1, orders_left = ?
                                        WHERE user_id = ?""",
                                       (orders_left, user_id))
    
    def driver_exists(self, user_id):
        """Проверяем, водитель ли юзер"""
        with self.connection:
            return self.cursor.execute("""SELECT * FROM users
                                        WHERE user_id = ? AND driver = 1""" , (user_id,)).fetchall()
        
    def orders_left(self, user_id):
        """Проверяем, сколько можно ещё взять заказов"""
        with self.connection:
            return self.cursor.execute("""SELECT orders_left FROM users
                                        WHERE user_id = ?""" , (user_id,)).fetchone()[0]
        
    def give_number_car(self, user_id):
        """Получаем номер машины водителя"""
        with self.connection:
            return self.cursor.execute("""SELECT number_car FROM users
                                        WHERE user_id = ?""" , (user_id,)).fetchone()[0]
     
    def order_exists(self, id_order):
        """Получаем заказ по его id"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM orders WHERE id = ?", (id_order,)).fetchone()

    def order_who_get_order__exists(self, id_order):
        """Получаем водителя заказа по его id"""
        with self.connection:
            return self.cursor.execute("SELECT who_get_order FROM orders WHERE id = ?", (id_order,)).fetchone()[0]

        
    def add_arrived_order(self, order_id):
        """Добавляем водителя и время к заказу"""
        with self.connection:
            return self.cursor.execute("""UPDATE orders
                                        SET arrived = ?
                                        WHERE id = ?""",
                                       (datetime.datetime.now().strftime("%d/%m/%y %H:%M"), order_id,))

    def add_finish_order(self, order_id):
        """Добавляем время финиша к заказу"""
        with self.connection:
            return self.cursor.execute("""UPDATE orders
                                        SET finish_order = ?
                                        WHERE id = ?""",
                                       (datetime.datetime.now().strftime("%d/%m/%y %H:%M"), order_id,))
        
    def add_finish_order_diver(self, user_id):
        """Отнимаем один заказ и добавляем к общей сумме поездок"""
        with self.connection:
            return self.cursor.execute("""UPDATE users
                                        SET orders_left = (orders_left - 1), all_trip_driver = (all_trip_driver + 1)
                                        WHERE user_id = ?""",
                                       (user_id,))
    
    def add_finish_order_client(self, user_id):
        """Добавлем к сумме поездок"""
        with self.connection:
            return self.cursor.execute("""UPDATE users
                                        SET all_trip = (all_trip + 1)
                                        WHERE user_id = ?""",
                                       (user_id,))

    def get_orders_left(self, user_id):
        """Колличество оставшихся заказов"""
        with self.connection:
            return self.cursor.execute("SELECT orders_left FROM users WHERE user_id = ?", (user_id,)).fetchone()

    def order_finish__exists(self, user_driver_username):
        """Проверяем есть ли не завершённые заказы"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM orders WHERE who_get_order = ? AND finish_order is null ", (user_driver_username,)).fetchone()
    
    def order_finish__exists_client(self, user_id):
        """Проверяем есть ли не завершённые заказы"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM orders WHERE user_id = ? AND finish_order is null ", (user_id,)).fetchone()

