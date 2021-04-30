import FutBot
import time

def main():

    bot = FutBot.FutBot()
    
    while True:
        bot.update_bot()
        time.sleep(FutBot.SLEEP_TIME)

if __name__ == "__main__":
    main()