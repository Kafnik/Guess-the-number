
TELEGRAM_TOKEN = '8452848990:AAFOP3-0wBMMrD-vtUqgn2_mndkOeWPQIW0'

#User_name администраторов
ADMIN_USER = 'Kafnik'

 # Функция проверки администратора
def is_admin(message):
    message.from_user.first_name == ADMIN_USER
    return