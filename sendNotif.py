import telepot

class Notification():
    def __init__(self):
        self.bot = telepot.Bot(token="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        self.chat_id = XXXXXXXXX

    def sendNotification(self, images):
        self.bot.sendMessage(chat_id=self.chat_id, text="Vous avez une personne devant la porte")
        for image in images:
            self.bot.sendPhoto(chat_id=self.chat_id, photo=open(image, 'rb'))
        print("Notification sent")
