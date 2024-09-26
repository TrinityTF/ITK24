import datetime
import time

schedule = [
    ("09:00", "10:20"),
    ("10:30", "11:50"),
    ("12:00", "12:40"),
    ("13:20", "14:00"),
    ("14:10", "15:30"),
    ("15:40", "17:00"),
    ("17:10", "18:30"),
]
def is_pause_time(now):
    current_minutes = now.hour * 60 + now.minute


    for start, end in schedule:
        start_minutes = int(start.split(":")[0]) * 60 + int(start.split(":")[1])
        end_minutes = int(end.split(":")[0]) * 60 + int(end.split(":")[1])

        if current_minutes < start_minutes:
            break  # Before the first class starts

        if current_minutes < end_minutes:
            return False  # It's class time

    return True  # It's pause time


try:
    while True:
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f"Aeg: {current_time}", end="\r")

        if is_pause_time(now):
            print(f"Aeg: {current_time} - Nüüd on paus!")  # Print pause message

        time.sleep(1)

except KeyboardInterrupt:
    print("\nProgrammi katkestamine.")
