from src import FutBot
import time

def main():

    bot = FutBot.FutBot()
    
    while True:
        bot.update()
        time.sleep(FutBot.SLEEP_TIME)

if __name__ == "__main__":
    main()