"""
    This django middleware gets the time that the request enters the middleware, the time that it leaves the middleware, request path, the parameter list, 
    the MD5 hash value of the rendered output, and the current thread and process ids.

    External requirments:
        cryptohashpy
"""

import json
import threading
import os                   
import cryptohashpy                 # C extension module for calcuating md5 sum
from django.conf import settings    # Configurable output file MIDDLEWARE_PERFORMANCE_METRICS_FILE
import datetime                     # Get time request enters/leaves middleware
import csv

class PerformanceMetricsMiddleware(object):
    CSV_HEADER = ["REQUEST_PATH", "REQUEST TIME", "RESPONSE TIME", "PARAMETER LIST", "MD5 HASH", "PROCESS ID", "THREAD ID"]

    def get_current_time():
        return str(datetime.datetime.now())

    def __init__(self, get_response, output_file = None):
        self.get_response = get_response
        self.file_write_lock = threading.Lock()
        self.output_file = output_file

        if hasattr(settings, "MIDDLEWARE_PERFORMANCE_METRICS_FILE"):
            self.output_file = settings.MIDDLEWARE_PERFORMANCE_METRICS_FILE 

        if self.output_file and not os.path.exists(self.output_file):
            self.mk_output_dir()
            self.csv_write_row(PerformanceMetricsMiddleware.CSV_HEADER)

    def mk_output_dir(self):
        dir = os.path.dirname(self.output_file)

        if not os.path.exists(dir):
            try:
                os.makedirs(dir)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

    def csv_write_row(self, row):
        if self.output_file:
            with self.file_write_lock:
                with open(self.output_file, 'a') as csvfile:
                    metrics_writer = csv.writer(csvfile)
                    metrics_writer.writerow(row)

    def __call__(self, request):
        # Cant attach request_sent_time to a class member because a single PerformanceMetricsMiddleware instance is shared
        # between threads
        request.request_sent_time = PerformanceMetricsMiddleware.get_current_time()

        response = self.get_response(request)

        response_rec_time = PerformanceMetricsMiddleware.get_current_time()
        md5_hash = "N/A"
        param_list = ""
        response_content = response.content

        if response_content:
            md5_hash = cryptohashpy.md5(response_content)

        if request.method == 'GET' and request.GET:
            param_list = json.dumps(request.GET)
        elif request.method == 'POST' and request.POST:
            param_list = json.dumps(request.POST)

        csv_row = [request.path, request.request_sent_time, 
                   response_rec_time, param_list, md5_hash, 
                   str(os.getpid()), str(threading.get_ident())]

        self.csv_write_row(csv_row)

        return response
