import config
import logging
import datetime
import numpy as np

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler,
    CallbackContext,
)


patient = {}

token = config.token_prod

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
MODE, HIEGHT, WEIGHT, AGE, TEMP, FINISH, SUMMARY = range(7)

id = 0


def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [['Женщина'], ['Мужчина']]
    id = 0
    update.message.reply_text(
        'Новый пациент {} \n'.format(id),
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
            input_field_placeholder='gender'
        ),
    )
    patient = {}

    return MODE


def mode(update: Update, context: CallbackContext) -> int:
    logger.info("gender: %s", update.message.text)
    logger.info("date: %s",  datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    patient['date'] = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    patient['gender'] = update.message.text
    reply_keyboard = [['Постельный'], ['Палатный'], ['Общий']]
    update.message.reply_text('Режим: ', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, resize_keyboard=True),)

    return TEMP


def temp(update: Update, context: CallbackContext) -> int:
    logger.info("mode  %s", update.message.text)
    patient['mode'] = update.message.text
    reply_keyboard = [['нет'], ['38'], ['39'], ['40'], ['41']]
    update.message.reply_text('Teмпература [С]:', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True),)

    return HIEGHT


def hieght(update: Update, context: CallbackContext) -> int:
    logger.info("temp: %s", update.message.text)
    patient['temp'] = update.message.text
    update.message.reply_text('Рocт [см]: ')
    return WEIGHT


def weight(update: Update, context: CallbackContext) -> int:
    logger.info("hieght  %s", update.message.text)
    patient['hieght'] = update.message.text
    update.message.reply_text('Bec [кг]: ')
    return AGE


def age(update: Update, context: CallbackContext) -> int:
    logger.info("weight  %s", update.message.text)
    patient['weight'] = update.message.text
    update.message.reply_text('Boзраст: ')
    return SUMMARY




def _float(st:str):
    if ',' in st:
        return float(st.replace(',','.'))
    else:
        return float(st)

def summary(update: Update, context: CallbackContext) -> int:
    logger.info("age  %s", update.message.text)
    patient['age'] = update.message.text
    print(patient)
    list_ = ['Дата: ', 'Пол: ', 'Режим: ', 'Температура [C]: ', 'Рост [см]: ',
             'Возраст: ',
             'Масса тела [кг]: ',]

    text = 'Отчет:  '+'\n'+'\n'
    for name, label in zip(list_, patient):
        text += name+str(patient[label])+'\n'
    print(text)
    output=0
    print(patient['gender'])
    error=''
    try: 
        if patient['gender'] == 'Мужчина':
            print('mt', (13.7 *_float(patient['weight'])))
            print('h', (5*_float(patient['hieght'])))
            print('a', (6.8*_float(patient['age'])))
            output = 66+(13.7 * \
                _float(patient['weight']))+(5*_float(patient['hieght'])) - \
                (6.8*_float(patient['age']))
        elif patient['gender'] == 'Женщина':
            output = 655+(9.6*_float(patient['weight']) )+ \
                (1.8*_float(patient['hieght']))-(4.5*_float(patient['age']))
            print('mt', (9.6 * _float(patient['weight'])))
            print('h', (1.8*_float(patient['hieght'])))
            print('a', (4.5*_float(patient['age'])))
        else:
            error+='unkown gender'
        print(output)
        save=output
        if patient['mode'] == 'Постельный':
            output = output *1.1
        elif patient['mode'] == 'Палатный':
            output = output *1.2
        elif patient['mode'] == 'Общий':
            output = output *1.3
        else:
            error += 'unkown mode'
        print(output,output/save)
        save2=output
        temp_dict = {'нет':1.0,'38': 1.1, '39': 1.2,'40': 1.3, '41': 1.4 }
        output =output * temp_dict[patient['temp']]
        print(output/save2)
        update.message.reply_text(text)
        update.message.reply_text(
        'Действительные расходы энергии (ДРЭ)) = '+str(np.round(output,2))+" ккал/сут")
    # update.message.reply_text(comment)
        update.message.reply_text('Всем спасибо')
    except:
        output=0
        update.message.reply_text('Что-то пошло не так, попробуйте еще раз')
    # comment ="""
    # -----------------------------
    # Расчет произведен по формуле:
    # ДРЭ = ОЭО*ФА*TФ.
    # ОЭО - основной энергитический обмен;
    # ТФ - температурный фактор;
    # ФА - фактор активности;
    # -----------------------------
    # """


    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END



def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MODE: [MessageHandler(Filters.text, mode)],
            TEMP: [MessageHandler(Filters.text, temp)],
            HIEGHT: [MessageHandler(Filters.text & ~Filters.command, hieght)],
            WEIGHT: [MessageHandler(Filters.text, weight)],
            AGE: [MessageHandler(Filters.text, age)],
            SUMMARY: [MessageHandler(Filters.text, summary)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        # per_message=True
    )


    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
