from datadog import initialize, api
from datetime import datetime
from orbi import orbi
import os
import time

REPORT_INTERVAL=5 # seconds

def metrics_from_stats(stats_dict):
    return [{'metric': k, 'points': v} for k, v in stats_dict.iteritems()]

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

orbi_username = os.environ['ORBI_USERNAME']
orbi_password = os.environ['ORBI_PASSWORD']

datadog_options = {
    'api_key': os.environ['DATADOG_API_KEY'],
    'app_key': os.environ['DATADOG_APP_KEY']
}

initialize(**datadog_options)

while True:
    first_stats_dict = orbi.statistics(orbi_username, orbi_password)
    first_numbers_dict = {k: float(v) for k, v in first_stats_dict.iteritems() if is_number(v)}

    time.sleep(1)
    second_stats_dict = orbi.statistics(orbi_username, orbi_password)
    second_numbers_dict = {k: float(v) for k, v in second_stats_dict.iteritems() if is_number(v)}

    diff_dict = {k: (second_numbers_dict[k] - first_numbers_dict[k]) for k, v in first_numbers_dict.iteritems()}

    print "tick @ %s" % datetime.now()

    try:
        api.Metric.send(metrics_from_stats(diff_dict))
    except Exception, e:
        print "Got an exception while contacting the Datadog API: %s" % e
        pass

    time.sleep(REPORT_INTERVAL)
