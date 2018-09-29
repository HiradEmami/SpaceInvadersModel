import time
past =0
for i in range(0,10):
    time.sleep(1)
    now =time.time()
    print (now -past)
    past = now