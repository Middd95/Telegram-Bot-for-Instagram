import csv,math,random,time
from unicodedata import name
from xml.dom.minidom import Document
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from turtle import update
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.conversationhandler import ConversationHandler
from telegram.ext.filters import Filters

updater = Updater("5050655709:AAHTkXokWGz5VHO0DSHdKFfk2TlzUOZq1uQ",
				use_context=True)

# ---------- defining states ---------
userpassword = ''
ONE , TWO = range(2)

def start(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Hello sir, Welcome to the Bot.Please write\
		/help to see the commands available.")

def help(update: Update, context: CallbackContext):
	update.message.reply_text("""Available Commands :-\
    /InstagramBot - To know about your followers
	/meet - To Meet""")

def InstagramBot(update: Update, context: CallbackContext):
	update.message.reply_text("""
	This bot helps in knowing your unfollower list(Those
	whom you follow but they don't follow back)
	To Continue with InstagramBot please Enter UserName """)
	return ONE

def got_username(update: Update, context: CallbackContext):
     chat_id = update.message.chat_id
     name = update.message.text # now we got the name
     context.user_data["name"] = name # to use it later (in next func)
     update.message.reply_text("thanks " + name + " ! please enter your password")
     return TWO

def got_password(update: Update, context: CallbackContext):
     chat_id = update.message.chat_id
     userpassword = update.message.text 
     name = context.user_data["name"] # we had the name , remember ?!
     update.message.reply_text("Completed ! Please wait for few mins for the unfollowers list")
     return login_credential(name, userpassword,update,context)


def login_credential(name, userpassword,update,context):
		driver = webdriver.Chrome(executable_path=r'D:\webdrivers\chromedriver.exe')
		driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
		time.sleep(3)
		username = driver.find_element_by_name("username")
		username.send_keys(name)
		time.sleep(2)
		password = driver.find_element_by_name("password")
		password.send_keys(userpassword)
		time.sleep(2)
		login_data = driver.find_element_by_css_selector("button[type='submit']")
		login_data.click()
		time.sleep(3)
		return user_id(name,driver,update,context)

def user_id(name,driver,update,context):
	driver.get("https://www.instagram.com/"+name+"/")
	time.sleep(3)
	Follower1 = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
	time.sleep(2)
	Follower2 = Follower1.text
	Follower2 = Follower2.split()
	Follower2 = int(Follower2[0])
	Follower1.click()
	time.sleep(3)
	data = driver.find_element_by_class_name('isgrP') 
	time.sleep(3)
	i = 0
	while i < Follower2:
		foqllist = []
		foqllist = data.find_elements_by_class_name('Pkbci')
		driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", data)
		time.sleep(random.randint(500,1000)/1000)
		i = len(foqllist) + 1
	dataList = data.find_elements_by_class_name('d7ByH')
	FollowersList = []
	count = 0
	a = 0
	b = ''
	for item in dataList:
		if 'Follow' in item.text:
			a = len(item.text)
			b = item.text[0:a-9]
			FollowersList.append(b)
		else:
			FollowersList.append(item.text)
			count = count + 1
	time.sleep(5)
	driver.get("https://www.instagram.com/"+name+"/")
	time.sleep(3)
	following1 = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a')
	following2 = following1.text
	following2 = following2.split()
	following2 = int(following2[0])
	following1.click()
	time.sleep(5)
	data = driver.find_element_by_class_name('isgrP') 
	time.sleep(10)
	for i in range(math.ceil(following2/4)):
		driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", data)
		time.sleep(random.randint(500,1000)/1000)
	dataList = data.find_elements_by_class_name('d7ByH')
	FollowingList = []
	count = 0
	a = 0
	b = ''
	for item in dataList:
		if 'Verified' in item.text:
			a = len(item.text)
			b = item.text[0:a-9]
			FollowingList.append(b)
		else:
			FollowingList.append(item.text)
			count = count + 1
	out = []
	for ele in FollowingList:
		if ele not in FollowersList:
			out.append(ele)
	res = []
	for el in out:
		sub = el.split(', ')
		res.append(sub)
	file = open('Unfollowers.csv', 'w+', newline ='')
	with file:
		write = csv.writer(file)
		write.writerows(res)
	return send_details(update,context)

def send_details(update: Update, context: CallbackContext):
	chat_id = update.message.chat_id
	document = open('Unfollowers.csv', 'rb')
	context.bot.send_document(chat_id, document)

def cancel(update: Update, context: CallbackContext):
     chat_id = update.message.chat_id
     update.message.reply_text("process canceled !")
     return ConversationHandler.END

def meet(update: Update, context: CallbackContext):
    update.message.reply_text("Call me at - 1111111111 dummy code")

def unknown(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Sorry '%s' is not a valid command" % update.message.text)

def unknown_text(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Sorry I can't recognize you , you said '%s'" % update.message.text)


# ---------- conversation handler ---------
CH = ConversationHandler(entry_points = [CommandHandler('InstagramBot', InstagramBot)],
     states = {ONE : [MessageHandler(Filters.text , got_username)],
     TWO : [MessageHandler(Filters.text , got_password)]
     },
	 fallbacks = [MessageHandler(Filters.regex('cancel'), cancel)],
	 allow_reentry = True)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('meet', meet))
updater.dispatcher.add_handler(CH)
updater.dispatcher.add_handler(MessageHandler(
	Filters.command, unknown)) # Filters out unknown commands
# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))
updater.start_polling()


