import datetime
import time as t

today = datetime.date.today()
quarterly_done = False

def main():
    global today, quarterly_done
    while True:
        now = datetime.datetime.now()
        if today.day != now.day:
            today = datetime.date.today()
            print("date updated")
        if now.minute % 15 == 0 and not quarterly_done:
            print("quarterly update")
            quarterly_done = True
        if now.minute % 15 == 1 and quarterly_done:
            print("reset quarter")
            quarterly_done = False

        print(now)       
        t.sleep(1) 

if __name__ == "__main__":
    main()
