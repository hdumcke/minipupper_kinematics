import threading
import queue

q = queue.Queue()

def worker():
    while True:
        item = q.get()
        print('Working on {%s}' % item['item'])
        print('Finished {%s}' % item['item'])
        q.task_done()

# Turn-on the worker thread.
threading.Thread(target=worker, daemon=True).start()

# Send thirty task requests to the worker.
for item in range(30):
    q.put({'item': item})

# Block until all tasks are done.
q.join()
print('All work completed')
