import telebot


# 1723068705:AAG2vZ92MLYJNaJpcWwi-**YWdq43h1Q3wA
bot = telebot.TeleBot("1723068705:AAG2vZ92MLYJNaJpcWwi-**YWdq43h1Q3wA")

# RA
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 "Привет, я чат-бот, который умеет подбирать аналоги стали, напищи в чат /analog, чтобы подобрать аналог")


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "По всем вопросам обращайтесь к оператору поддержки чат-бота @troppppr")


def find_value(look_value, df):
    for i in df.keys():
        if look_value.upper() in df[i]:
            for j in df.keys():
                for count, element in enumerate(df[j]):
                    if element == look_value.upper():
                        return (i, count)
    return ('-', '-')


def osnova(fin, df, message):
    col, row = find_value(fin, df)
    fin = fin.upper()
    if fin in df['СНГ (ГОСТ)']:
        bot.send_message(message.from_user.id, 'Найдено!')

        if df['Аналог РФ'][row] != '-':
            answer = 'Аналог СНГ: ' + df['Аналог РФ'][row]
            bot.send_message(message.from_user.id, answer)
        answer = 'Аналог США (AISI): ' + df['США (AISI)'][row]
        bot.send_message(message.from_user.id, answer)

    elif fin in df['США (AISI)']:
        bot.send_message(message.from_user.id, 'Найдено!')

        if df['Аналог РФ'][row] != '-':
            answer = 'Аналог СНГ: ' + df['Аналог РФ'][row]
            bot.send_message(message.from_user.id, answer)
        answer = 'Аналог СНГ: ' + df['СНГ (ГОСТ)'][row]
        bot.send_message(message.from_user.id, answer)

    elif fin in df['Аналог РФ']:
        bot.send_message(message.from_user.id, 'Найдено!')

        if df['Аналог РФ'][row] != '-':
            answer = 'Аналог СНГ: ' + df['СНГ (ГОСТ)'][row]
            bot.send_message(message.from_user.id, answer)
        answer = 'Аналог США (AISI): ' + df['США (AISI)'][row]
        bot.send_message(message.from_user.id, answer)

    elif col == '-' and row == '-':
        bot.send_message(message.from_user.id, 'Не найдено, поиск пока в разработке')


@bot.message_handler(commands=['analog'])
def analog(message):
    bot.reply_to(message, 'Введите маркировку стали')
    bot.register_next_step_handler(message, mark)


def mark(message):
    with open("E:\\Study\\Testbot\\dataset.csv", "r", encoding="MacCyrillic") as input_file:
        fin = message.text
        df = {}
        counter = 0
        rawdata = input_file.readlines()

        rawheader = rawdata[0].strip('\n').split(';')

        for col in rawheader:
            df[col] = []

        for header in rawheader:
            for line in rawdata[1:]:
                new_row = line.strip('\n').split(';')
                df[header].append(new_row[counter])
            counter += 1

        if df['']:
            del df['']

        osnova(fin, df, message)


@bot.message_handler(commands=['info'])
def info(message):
    bot.reply_to(message, 'Введите маркировку стали для получения информации о составе')
    bot.register_next_step_handler(message, informaciya)


def informaciya(message):
    with open("E:\\Study\\Testbot\\dataset.csv", "r", encoding="MacCyrillic") as input_file:
        df = {}
        counter = 0
        rawdata = input_file.readlines()

        rawheader = rawdata[0].strip('\n').split(';')

        for col in rawheader:
            df[col] = []

        for header in rawheader:
            for line in rawdata[1:]:
                new_row = line.strip('\n').split(';')
                df[header].append(new_row[counter])
            counter += 1

        if df['']:
            del df['']
        headers = []
        for i in df.keys():
            headers.append(i)
        fin = message.text
        col, row = find_value(fin, df)
        if col == '-' and row == '-':
            bot.send_message(message.from_user.id, 'Маркировка не найдена')
        else:
            bot.send_message(message.from_user.id, 'Найдено!')
            answer = 'В стандарте ' + col
            bot.send_message(message.from_user.id, answer)
            answer = ''
            bord = []

            bot.send_message(message.from_user.id, 'Содержание химических элементов: ')
            for i in range(1, 10, 2):
                if df[headers[i]][row] == '-':
                    continue
                else:
                    bord.append(df[headers[i]][row])
                    bord.append(df[headers[i + 1]][row])

                    answer = 'Cодержание ' + str(headers[i])[:-3] + bord[0] + '% < > ' + bord[1] + '%'

                    bot.send_message(message.from_user.id, answer)
                    answer = ''
                    bord = []


bot.polling()