# import time

# print("task started")
# time.sleep(1)
# print("processing...")
# time.sleep(1)
# print("task finished")




import time

print("task started", flush=True)
time.sleep(1)

for i in range(1, 31):
    print(f"processing line {i}", flush=True)
    time.sleep(0.3)

print("task finished", flush=True)