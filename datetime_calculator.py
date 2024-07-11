from datetime import datetime
import sys

print(sys.argv)

def convert_seconds_to_hhmmss(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:01}:{seconds:02}"

# start time
start_time = sys.argv[1]
end_time = sys.argv[2]

# convert time string to datetime
t1 = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
print('Start time:', t1.time())

t2 = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
print('End time:', t2.time())

# get difference
delta = t2 - t1

# time difference in seconds
print(f"Time difference is {delta.total_seconds()} seconds")

print(f"Total time difference is {convert_seconds_to_hhmmss(delta.total_seconds())} seconds")