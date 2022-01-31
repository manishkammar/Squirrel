#import config
import telegram
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import datetime
import logging
from telegram.ext import Updater
from telegram.ext import  CommandHandler
from telegram import  ReplyKeyboardRemove
from telegram.ext import CallbackQueryHandler
import config


# Enable logging
import telegramcalendar
import Validate
global leave_date


def start(bot,update):
    print("In start")
    user=update.message.from_user

    if Validate.get_info(str(user['id']))==False:
        contact_keyboard = telegram.KeyboardButton(text="/Register", request_contact=True)
        custom_keyboard = [[contact_keyboard]]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        update.message.reply_text('Register',
                                  reply_markup=reply_markup)
    else:
        print( "In start else" )
        all( bot, update )


def Register(bot,update):
    contact_keyboard = telegram.KeyboardButton(text="send_contact", request_contact=True)
    custom_keyboard = [[contact_keyboard]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text('send',
                              reply_markup=reply_markup)

def CheckIn(bot,update):
    contact_keyboard = telegram.KeyboardButton(text="send_location", request_location=True)
    custom_keyboard = [[contact_keyboard]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text('Check in',
                              reply_markup=reply_markup)

def CheckOut(bot, update):
    contact_keyboard = telegram.KeyboardButton(text="send_location", request_location=True)
    custom_keyboard = [[contact_keyboard]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text('Check out',
                              reply_markup=reply_markup)

def LocationCallabck(bot, update):
    if Validate.in_range(update.message.location.latitude, update.message.location.longitude)==True:
        print("in range")
        date = datetime.datetime.today().strftime( '%d-%m-%Y' )
        time = datetime.datetime.now().strftime( '%H:%M' )
        user = update.message.from_user
        fname = user.first_name
        id = user['id']
        print(date,id,time)
        if Validate.check_in(str(date), str(id))==True:
            print("check in is true")
            if Validate.fetch(str(id), str(date), str(time))==0:
                print( "early" )
                reply_keyboard = [
                    ['Personal Issue', 'Transport Issue', 'Health Issue', 'Todays Target Achieved', 'Others']]
                update.message.reply_text( 'Please select the reason for early check out',
                                           reply_markup=ReplyKeyboardMarkup( reply_keyboard, one_time_keyboard=True ) )
            else:
                update.message.reply_text("Checked out")
                all( bot, update )
        else:
            print("recording jusin")
            Validate.jusin(id, date, time)
            update.message.reply_text("Checked in")
            all( bot, update )

    else:
        update.message.reply_text("You are out of range")


def ContactCallabck(bot, update):

    ph_no=update.message.contact.phone_number
    name=update.message.contact.first_name
    id=update.message.contact.user_id
    uname='None'
    Validate.register(str(id), str(name), str(uname), str(ph_no))
    update.message.reply_text("You have been registered successfully")
    all(bot,update)


def Get_Weekly_Attendance_Report(bot,update):

    bot.send_photo(update.message.chat_id, open('pluto.jpg', 'rb'))
    all(bot,update)

def all(bot,update):
    print("in all")
    id=update.message.from_user.id
    date = datetime.datetime.today().strftime( '%d-%m-%Y' )
    print(date)
    Check_In = telegram.KeyboardButton( text="Check In", request_location=True )
    Check_Out = telegram.KeyboardButton( text="Check Out", request_location=True )
    if Validate.check_in(str(date), str(id))==True:

        reply_keyboard = [
        [Check_Out], ['/Get_Weekly_Attendance_Report', '/Get_Monthly_Attendance_Report'], ['/Leave_Status',
         '/Apply_Leave']]
    else:
        reply_keyboard = [
            [Check_In], ['/Get_Weekly_Attendance_Report', '/Get_Monthly_Attendance_Report'],
            ['/Leave_Status',
             '/Apply_Leave']]
    update.message.reply_text('Thank You, What you want to do? ',
                             reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


def Get_Montly_Attendance_Report(bot, update):

    bot.send_photo(update.message.chat_id, open('pluto.jpg', 'rb'))
    all(bot,update)

def Leave_Status(bot,update):
    update.message.reply_text('some Leave status')
    all(bot,update)

def Apply_Leave(bot,update):
    calendar_handler(bot,update)

def calendar_handler(bot,update):
    update.message.reply_text("Please select the date",
                        reply_markup=telegramcalendar.create_calendar())

def inline_handler(bot,update):
    global leave_date
    print("in line handler")
    selected,date = telegramcalendar.process_calendar_selection(bot, update)
    if selected:
        print("In selecvted")
        bot.send_message(chat_id=update.callback_query.from_user.id,
                        text="You selected %s    /Confirm" % (date.strftime("%d/%m/%Y")),
                         reply_keyboard=['1','2']
                        )
        leave_date = date.strftime("%d/%m/%Y")


def reason(bot,update):
    print("in reason")
    print(update.message[-1])

def leave_reason(bot,update,user_data):
    reply_keyboard = [
        ['Sick Leave', 'Personal Work'],
        ['On Site Work',
         'Other Reasons']]
    update.message.reply_text( 'Please select the Reason? ',
                               reply_markup=ReplyKeyboardMarkup( reply_keyboard, one_time_keyboard=True ) )



def leave_app(bot,update):
    print("Bantu")
    print(update)
    global leave_date
    print(update.message.chat.id)
    print(update.message.text)
    print(leave_date)

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(config.SNE_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    dp.add_handler(
        CommandHandler('start', start))# Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    dp.add_handler(
        CommandHandler('Register', Register))
    dp.add_handler(CommandHandler('CheckIn',CheckIn))
    dp.add_handler(CommandHandler('CheckOut',CheckOut))
    dp.add_handler(MessageHandler(Filters.location,LocationCallabck))
    dp.add_handler(MessageHandler(Filters.contact, ContactCallabck))
    dp.add_handler(CommandHandler('Get_Weekly_Attendance_Report',Get_Weekly_Attendance_Report))
    dp.add_handler(CommandHandler('Get_Monthly_Attendance_Report', Get_Montly_Attendance_Report))
    dp.add_handler(CommandHandler('Apply_Leave',Apply_Leave))
    dp.add_handler(CommandHandler('Leave_Status',Leave_Status))
    #dp.add_handler(CommandHandler('Confirm', leave_reason))
    dp.add_handler(CommandHandler('all',all))
    dp.add_handler(RegexHandler('^(Personal Issue|Transport Issue|Health Issue|Todays Target Achieved|Others)$',
                                    reason
                                    ))
    dp.add_handler(CallbackQueryHandler(inline_handler))
    dp.add_handler(CommandHandler('Confirm', leave_reason, pass_user_data=True) )
    dp.add_handler( CommandHandler( 'all1', calendar_handler ) )
    dp.add_handler(RegexHandler('^(Sick Leave|Personal Work|On Site Work|Other Reasons)$',
                               leave_app))
#    dp.add_handler(RegexHandler('^(Sick Leave|Transport Issue|Other)$', leave_app))


    # log all errors
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
