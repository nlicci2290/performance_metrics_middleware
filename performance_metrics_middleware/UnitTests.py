from performance_metrics_middleware.PerformanceMetrics import PerformanceMetricsMiddleware as pmm
import os
import threading
import json
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpRequest

settings.configure()

TEST_CONTENT = b"test string"
TEST_CONTENT_MD5 = "6f8db599de986fab7a21625b7916589c"
OUTPUT_FILE = os.getcwd() + "test.csv"
CSV_HEADER_ROW = "REQUEST_PATH,REQUEST TIME,RESPONSE TIME,PARAMETER LIST,MD5 HASH,PROCESS ID,THREAD ID"

def get_response(request):
    # Content is the only attribute the middleware cares about in the response
	return HttpResponse(content = TEST_CONTENT)

def test_metric_log():
    mock_http_req = HttpRequest()
    mock_http_req.GET = { "q": "5" }
    mock_http_req.method = "GET"
    mock_http_req.path = "/"

    thread_id = str(threading.current_thread().ident)
    pid = str(os.getpid())
    metrics_file = None
    metrics_data_row = None

    # Need to ensure the middleware creates a brand new file
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    middleware = pmm(get_response, OUTPUT_FILE)

    # We should get a response since we give it a none null response
    assert(middleware.__call__(mock_http_req) != None)

    # Now we check to see if output file exists
    assert(os.path.exists(OUTPUT_FILE) == True)

    # Read all data from file into a list
    # Sample file for reference:
    # "REQUEST_PATH", "REQUEST TIME", "RESPONSE TIME", "PARAMETER LIST", "MD5 HASH", "PROCESS ID", "THREAD ID"
    #
    # /,2019-11-11 19:02:25.684578,2019-11-11 19:02:25.739542,,D8F1200C1C02C1322B58EFAF70FA9903,13184,15080
    with open(OUTPUT_FILE, "r") as output_file: 
        # remove all empty lines 
        metrics_file = list(filter(lambda line: len(line.strip()) > 0, output_file.readlines()))

    # Verify we have 2 lines of data (header row, data row)
    assert (len(metrics_file) == 2)

    # Verify first line is the header
    assert (metrics_file[0].strip() == CSV_HEADER_ROW)

    # Verify we have the correct number of entries in data row
    metrics_data_row = metrics_file[1].split(",")
    assert (len(metrics_data_row) == len(pmm.CSV_HEADER))

    # Verify we have the correct path logged
    assert(metrics_data_row[0] == mock_http_req.path)

    # We skip entry 1 and 2 because we have no way of getting the exact time logged

    # Verify request params are correct
    assert(metrics_data_row[3] == '"{""q"": ""5""}"')

    # Verify md5 is correct
    assert(metrics_data_row[4].lower() == TEST_CONTENT_MD5)

    # Verify proc id
    assert(metrics_data_row[5] == pid)

    # Verify thread id
    assert(metrics_data_row[6].strip() == thread_id)
