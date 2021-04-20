#!/usr/bin/env python

import os
import csv
import sys
import json
import time
import datetime
import socket
import requests
import statistics


def blah(thing):
    print(type(thing))


def timeit(method):
    def timed(*args, **kw):
        hostname = socket.gethostname()
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        sys.stderr.write('%r,%r,%r,%r,%2.2f' % \
              (hostname, method.__name__, ts, te,  te-ts))
        return result
    return timed


@timeit
def generate_job_data_url(job_name):
    try:
       return 'http://localhost:8080/job/{}/api/json'.format(job_name)
    except:
        raise


@timeit
def do_jenkins_request(url, user, jenkins_api_token):
    try:
        return requests.get(url, auth=(user, jenkins_api_token))
    except:
        raise

@timeit
def main():
    """A quick and dirty script to pull job statistics out ouf jenkins"""
    user = os.environ['USER']
    # A jenkins api token looks like '79b08af21ff820673a2e68f6de4a0a9d'
    # Get it buy clicking on your user and Show API Token"
    jenkins_api_token=os.environ['JENKINS_API_TOKEN']


    ts = time.time()
    isodate='2015-01-01'
    report = []
    report_filename = 'jenkins-job-status-report-{isodate}-{ts}.csv'.format(ts=ts, isodate=isodate)

    jobs_of_interest = [
                        'priority 1 (should jump queue)',
                       ]

    # These "interesting_things" are what we want to grab from the json
    things_to_extract = [
                           #'fullDisplayName',
                           'number',
                           'builtOn',
                           'duration',
                           'result',
                           'timestamp',
                         ]


    for job_name in jobs_of_interest:
       url = generate_job_data_url(job_name)
       r = do_jenkins_request(url, user, jenkins_api_token)
       j = json.loads(r.text)
       job_report = []
       for build in j['builds']:
          build_url = '{}/api/json'.format(build['url'])
          b = do_jenkins_request(build_url, user, jenkins_api_token)
          x = json.loads(b.text)
          # if you add/remove interesting things then remember to update teh writer.writerow for the CSV header
          # in the report
          tootle = [ job_name ]

          for thing in things_to_extract:
              tootle.append(x[thing])

          report.append(tootle)


       hosts_used_for_build = []
       durations = list(( x[3] for x in report))
       successful_durations = list(( x[3] for x in report if x[4] == 'SUCCESS'))
       hosts_used_for_build = list(( x[2] for x in report))
       successful_builds  = list((x for x in report if x[4] == 'SUCCESS'))
       failed_builds = list((x for x in report if x[4] == 'FAILURE'))

       print
       print


       count_successful = len(successful_builds)
       count_failed = len(failed_builds)
       set_of_hosts_used = set(hosts_used_for_build)
       number_of_hosts_used = len(set(hosts_used_for_build))
       total_durations = 0

       for n in durations:
           total_durations += n

       total_successful_durations = 0
       for n in successful_durations:
           total_successful_durations += n


       avg_duration_s = ( total_durations / len(durations) / 1000 )
       max_duration_s = (max(durations) / 1000 )
       min_duration_s = (min(durations) / 1000 )


       avg_sduration_s = ( total_successful_durations / len(successful_durations) / 1000 )
       max_s_duration_s = (max(successful_durations) / 1000 )
       min_s_duration_s = (min(successful_durations) / 1000 )



       print('All Builds: {}'.format(job_name))
       print('==========')
       print('                                   date/time = {date}'.format(date=time.strftime('%c')))
       print('                                   timestamp = {:>10}'.format(ts))
       print
       print('                            number of builds = {:>10}'.format(len(durations)))
       print('               mean build duration (seconds) = {:>10}'.format(int(statistics.mean(durations)/1000)))
       print('             median build duration (seconds) = {:>10}'.format(int(statistics.median(durations)/1000)))
       print('                max build duration (seconds) = {:>10}'.format(max_duration_s))
       print('                min build duration (seconds) = {:>10}'.format(min_duration_s))

       print
       print

       print('Successful Builds: {}'.format(job_name))
       print('=================')
       print('                            number of builds = {:>10}'.format(len(successful_durations)))
       print('               mean build duration (seconds) = {:>10}'.format(int(statistics.mean(successful_durations)/1000)))
       print('             median build duration (seconds) = {:>10}'.format(int(statistics.median(successful_durations)/1000)))
       print('                max build duration (seconds) = {:>10}'.format(max_s_duration_s))
       print('                min build duration (seconds) = {:>10}'.format(min_s_duration_s))

       print
       print
       print('set of hosts used = {}'.format(set_of_hosts_used))
       print('number of hosts used = {}'.format(number_of_hosts_used))
       print('count of successful builds = {}'.format(count_successful))
       print('count of failure builds = {}'.format(count_failed))

    # Chuck the data out to a CSV for the excel obsessed
    with open(report_filename, 'wb') as result:
        writer = csv.writer(result, dialect='excel')
        writer.writerow(things_to_extract)
        writer.writerows(report)

    """
    Q. Does excluding failed builds make sense? I say not because failed builds still consume time.
       To waste time is the greatest sin because lost time cannot be recovered.
    """


if __name__ == "__main__":
    main()

