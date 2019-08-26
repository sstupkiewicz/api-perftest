import requests
import threading
import sys
from datetime import datetime

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

class Test(object):
    def __init__(self, url, client_id, burst, threads_n):
        self.url = url
        self.burst = burst
        self.n = threads_n
        self.cid = client_id
        

    def test(self):
        head = { "X-IBM-Client-ID": self.cid }
        r = requests.get(self.url, headers = head, verify = False)
        if r.status_code == 200:
            sys.stdout.write(".")
        else:
            sys.stdout.write("!")
    
    def run(self):
        overall_perf = []
        for i in range(self.burst):
            sys.stdout.write("Starting run {}/{}: ".format(i+1, self.burst))
            start_time = datetime.now()
            for t in range(self.n):
                thread = threading.Thread(target = self.test)
                thread.start()
            
            main_thread = threading.currentThread()

            for t in threading.enumerate():
                if t is not main_thread:
                    t.join()
            end_time = datetime.now()
            elapsed = end_time - start_time
            c_elapsed = float("{:d}.{:d}".format(elapsed.seconds, elapsed.microseconds))
            performance = self.n / c_elapsed
            overall_perf.append(performance)
            print(" {:.2f} API Calls/s ({} s)".format(performance, c_elapsed))
        print("Completed runs: {}. Average performance: {:.2f} API Calls/s.".format(self.burst, sum(overall_perf)/float(len(overall_perf))))