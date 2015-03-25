from multiprocessing import Queue, Process, JoinableQueue, cpu_count
import urllib2

tasks_queue = JoinableQueue()
results_queue = Queue()
processor_num = cpu_count()

class ResourceGetter(Process):
    def __init__(self, task_queue, result_queue):
        Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        while True:
            proc_name = self.name
            task = self.task_queue.get()
            if task is None:
                print "%s is exiting" % proc_name
                self.task_queue.task_done()
                break
            try:
                result = task().read()
            except Exception, e:
                result = e
            self.result_queue.put(result)
            self.task_queue.task_done()

class HtmlTask(object):
    def __init__(self, url):
        assert url is not None, "url cant be None"
        self.url = url

    def __call__(self):
        return urllib2.urlopen(self.url)

def start():
    for _ in range(processor_num):
        ResourceGetter(tasks_queue, results_queue).start()

def terminate():
    for _ in range(processor_num):
        tasks_queue.put(None)
    tasks_queue.join()

def register(tasks):
    for task in tasks:
        tasks_queue.put(task)
  
if __name__ == "__main__":
    start()
    tasks = [HtmlTask('http://www.example.com')]
    register(tasks)
    terminate()
    jobs_num = len(tasks)
    while jobs_num:
        result = results_queue.get()
        print result
        jobs_num -= 1

