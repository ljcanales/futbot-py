from futbot import Bot
from time import sleep

#sleeping time
SLEEP_TIME = 300

def main():

    bot = Bot()
    
    while True:
        bot.update()
        sleep(SLEEP_TIME)

if __name__ == "__main__":
    main()