import telebot  # импорт библиотеки для работы с ботом
import re  # импорт библиотеки для проверки ввода(будет понятно, когда рассмотрим функцию)

bot = telebot.TeleBot('6996264013:AAFmWmhw-XThUEG3VcxO-pCzCGvaX-GLYYE');  # создание бота

file = open('Storage.txt', 'w')  # создание файла, в котором будет храниться информация о записи на стрижку
file.close()


def check_time(line):  # функция для проверки, корректно ли введено время
    new_line = line.split(":")
    if len(new_line) != 2 or new_line[0] not in ["10", "11", "12", "13", "14", "15", "16", "17", "18"] or new_line[
        1] != "00":
        return False
    else:
        return True


def check_length(line):  # функция для проверки длины строки, введенной пользователем(чтобы бот не сломался)
    if len(line) > 254:
        return False
    return True


def check_name(line):  # функция для проверки корректности введенных пользователем инициалов
    new_line = line.split(" ")
    if len(new_line) != 2 or any(ch.isdigit() for ch in new_line[0]) or any(ch.isdigit() for ch in new_line[1]):
        return False
    else:
        return True


def check_day(line):  # функция для проверки корректности введенного дня недели пользователем
    new_line = line.lower()
    days = {"понедельник", "вторник", "среда", "четверг", "пятница"}
    if new_line not in days:
        return False
    else:
        return True


# словарь с изначально доступными вариантами записи на стрижку
timetable = {'понедельник': ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"],
             'вторник': ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"],
             'среда': ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"],
             'четверг': ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"],
             'пятница': ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]}


def get_data(): # функция для получения данных из файла и составления нового доступного расписания
    data = []
    time = []
    name = []
    date = []
    with open("Storage.txt", "r") as file:
        for line in file:
            data.append(line.strip())

    for i in range(len(data)):
        if (i + 1) % 2 == 1:
            line = data[i].split(', ')
            date.append(line[0])
            time.append(line[1])
        else:
            name.append(data[i])
    new_timetable = timetable
    if len(time) != 0:
        for i in range(len(date)):
            if time[i] in new_timetable[date[i]]:
                new_timetable[date[i]].remove(time[i])
    return new_timetable


def get_names(): # функция для получения списка имен, которые уже записаны на стрижку
    data = []
    name = []
    with open("Storage.txt", "r") as file:
        for line in file:
            data.append(line.strip())
    for i in range(len(data)):
        if (i + 1) % 2 == 0:
            name.append(data[i])
    return set(name)


def storage(message): # функция для записи информации в файл, хранящий время и список имен
    file = open('Storage.txt', 'a')
    file.write(f'{message.text.lower()}\n')
    file.close()


def log(message): # функция для вывода сообщений пользователя в отдельный файл
    file = open("log.txt", 'a')
    file.write(f'{message.text}\n')
    file.close()


def is_emoji(text): # функция для проверки, является ли текст смайликом
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # Список смайликов и других значков со стандартной раскладки
                               u"\U0001F300-\U0001F5FF"  
                               u"\U0001F680-\U0001F6FF"  
                               u"\U0001F700-\U0001F77F"  
                               u"\U0001F780-\U0001F7FF"  
                               u"\U0001F800-\U0001F8FF"  
                               u"\U0001F900-\U0001F9FF"  
                               u"\U0001FA00-\U0001FA6F"  
                               u"\U0001FA70-\U0001FAFF"  
                               u"\U00002702-\U000027B0"  
                               u"\U000024C2-\U0001F251"  
                               "]+", flags=re.UNICODE)

    return bool(emoji_pattern.search(text))


@bot.message_handler(func=lambda message: True, content_types=['text']) # декоратор, который будет вызывать функции ниже при получении текстового сообщения
def start(message): # функция для обработки начала переписки, т.е когда пользователь пишет /start
    if message.content_type != 'text' or check_length(message.text) == False or is_emoji(message.text): # в этом условии мы проверяем корректность введенных данных пользователем
        bot.send_message(message.from_user.id, "Я вас не понимаю, введите коректные данные, пожалуйста",
                         parse_mode='HTML')
        bot.register_next_step_handler(message, start)
    else:
        log(message) # записываем сообщение пользователя в файл
        if message.text == '/start':
            bot.send_message(message.from_user.id,
                             "Добро пожаловать! Чего желаете? \n1 - записаться на стрижку \n2 - уйти \nВведите число: 1 или 2",
                             parse_mode='HTML') #отправка сообщения ботом в чат
            bot.register_next_step_handler(message, handle_message); # переход к следующему шагу - получения следующего сообщения от пользователя и вызов соответствующей функции для обработки этого сообщения
        else:
            bot.send_message(message.from_user.id, 'Напиши /start', parse_mode='HTML');


def handle_message(message): # функция для начала записи пользователя на стрижку
    if message.content_type != 'text' or check_length(message.text) == False or is_emoji(message.text):
        bot.send_message(message.from_user.id, "Я вас не понимаю, введите коректные данные, пожалуйста",
                         parse_mode='HTML')
        bot.register_next_step_handler(message, handle_message)
    else:
        log(message)
        if message.text == 'записаться на стрижку' or message.text == '1':
            formatted_text = "<b>Доступное время и дата для записи:</b>\n" # создание строки, в которую добавим словарь с доступным расписанием
            new_timetable = get_data()
            for key, values in new_timetable.items():
                formatted_text += f"<b>{key}:</b> "
                formatted_text += ", ".join(str(value) for value in values) + "\n"
            bot.send_message(message.chat.id, formatted_text, parse_mode='HTML')
            bot.send_message(message.from_user.id,
                             "Напишите день недели и время для записи, через запятую и пробел\nПример: понедельник, 15:00",
                             parse_mode='HTML')
            bot.register_next_step_handler(message, register_user_by_time)
        elif message.text == 'уйти' or message.text == '2':
            bot.send_message(message.from_user.id, "Всего хорошего!", parse_mode='HTML')
        else:
            bot.send_message(message.from_user.id, "Я Вас не понимаю, пожалуйста введите, что вы хотите из списка",
                             parse_mode='HTML')
            bot.register_next_step_handler(message, handle_message)


def register_user_by_time(message): # функция для продолжения записи пользователя и определения времени и дня недели, на которые пользователь хочет записаться
    if message.content_type != 'text' or check_length(message.text) == False or is_emoji(message.text):
        bot.send_message(message.from_user.id, "Я вас не понимаю, введите коректные данные, пожалуйста",
                         parse_mode='HTML')
        bot.register_next_step_handler(message, register_user_by_time)
    else:
        log(message)
        new_m = message.text.split(', ')
        new_m[0] = new_m[0].lower()
        if len(new_m) != 2:
            bot.send_message(message.from_user.id, "Вы неверно ввели день недели и(или) время", parse_mode='HTML')
            bot.send_message(message.from_user.id, "Введите данные коректно", parse_mode='HTML')
            bot.register_next_step_handler(message, register_user_by_time)
        elif check_day(new_m[0]) == False or check_time(new_m[1]) == False:
            bot.send_message(message.from_user.id, "Вы неверно ввели день недели и(или) время", parse_mode='HTML')
            bot.send_message(message.from_user.id, "Введите данные коректно", parse_mode='HTML')
            bot.register_next_step_handler(message, register_user_by_time)
        else:
            new_timetable = get_data() #получаем новое расписание и далее проверяем свободно ли место для записи
            if new_m[1] not in new_timetable[new_m[0]]:
                bot.send_message(message.from_user.id,
                                 "Это время уже забронировано\nПожалуйста, выберите свободное время", parse_mode='HTML')
                bot.register_next_step_handler(message, register_user_by_time)
            else:
                storage(message)
                bot.send_message(message.from_user.id, "Введите свои имя и фамилию через пробел", parse_mode='HTML')
                bot.register_next_step_handler(message, register_user_by_name)


def register_user_by_name(message): # функция для определения имени пользователя
    if message.content_type != 'text' or check_length(message.text) == False or is_emoji(message.text):
        bot.send_message(message.from_user.id, "Я вас не понимаю, введите коректные данные, пожалуйста",
                         parse_mode='HTML')
        bot.register_next_step_handler(message, register_user_by_name)
    else:
        log(message)
        if not check_name(message.text):
            bot.send_message(message.from_user.id, "Фамилия и(или) имя введены неправильно. \nВведите данные коректно",
                             parse_mode='HTML')
            bot.register_next_step_handler(message, register_user_by_name)
        else:
            name = get_names() # тут получаем уже записанных пользователей
            if message.text in name and len(name) != 0: # если пользователь есть в списке, то записанное время перед этим надо удалить из файла
                bot.send_message(message.from_user.id, "Вы уже записаны на стрижку!", parse_mode='HTML')
                with open('Storage.txt', 'r') as file:
                    lines = file.readlines()
                lines.pop()
                with open('Storage.txt', 'w') as file:
                    for line in lines:
                        file.write(line)
            else: # если пользователь не записан на стрижку, то сохраняем имя в файл в строчке ниже
                storage(message)
                with open('Storage.txt', 'r') as file: # для вывода записи пользователя считываем последние 2 строчки из файла с информацией
                    lines = file.readlines()[-2:]

                for i in range(2):
                    lines[i] = lines[i][0:len(lines[i]) - 1]
                lines[0] = lines[0].split(',')
                lines[1] = lines[1].split(' ')
                lines[1][0] = lines[1][0].capitalize()
                lines[1][1] = lines[1][1].capitalize()

                if lines[0][
                    0] == "среда":  # проверяем дни недели, т.к. у двух дней надо будет вручную изменить окончания для правильного вывода
                    bot.send_message(message.from_user.id,
                                     f'{lines[1][0]} {lines[1][1]}, спасибо за запись. Будем ждать Вас в среду в{lines[0][1]}',
                                     parse_mode='HTML')
                elif lines[0][0] == "пятница":
                    bot.send_message(message.from_user.id,
                                     f'{lines[1][0]} {lines[1][1]}, спасибо за запись. Будем ждать Вас в пятницу в{lines[0][1]}',
                                     parse_mode='HTML')
                elif lines[0][0] == "вторник":
                    bot.send_message(message.from_user.id,
                                     f'{lines[1][0]} {lines[1][1]}, спасибо за запись. Будем ждать Вас во вторник в{lines[0][1]}',
                                     parse_mode='HTML')
                else:
                    bot.send_message(message.from_user.id,
                                     f'{lines[1][0]} {lines[1][1]}, спасибо за запись. Будем ждать Вас в {lines[0][0]} в{lines[0][1]}',
                                     parse_mode='HTML')


bot.polling(none_stop=True) # функция, чтобы бот продолжал работу, независимо от возможных ошибок со стороны Telegram-а
