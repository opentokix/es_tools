#!/usr/bin/env python2
"""Nagios compatible plugin to check elasticsearch."""

import requests
import sys
import getopt


def usage(message=None, signal=0):
    """Usage of this plugin.

    Returns nagios compatible exit code and information about the checks
    Default runs against 127.0.0.1 and 9200 port, can be optionally configured with:

    -H host
    -P port

    There is no warning or critical settings, since it looks for the elasticsearch
    internal health code green, yellow and red. Will return critical if the check
    times out.
    """
    print usage.__doc__
    if message is not None:
        print "Error: %s" % message
    sys.exit(signal)


def get_cluster_health(host, port):
    """Get the json output from elasticsearch."""
    try:
        uri = "http://%s:%d/_cluster/health" % (host, port)
        r = requests.get(uri)
    except requests.exceptions.RequestException as e:
        usage(e, 255)
    try:
        return r.json()
    except (IndexError, ValueError), e:
        usage(e, 255)


def analyze_data(json_data):
    """Analyze the json output, and send messages and signals."""
    warning = False
    message = "Status is %s, %s unassigned shards " % (json_data['status'],
                                                       json_data['unassigned_shards'])
    message = message + "active_shards: %s, active_primary_shards: %s" % (json_data['active_shards'],
                                                                          json_data['active_primary_shards'])
    if json_data['status'] != 'green':
        if json_data['status'] == 'yellow':
            warning = True
        else:
            exit_with_signal(message, 2)
    elif json_data['timed_out'] is not False:
        print json_data['timed_out']
        exit_with_signal('Timeout', 2)
    else:
        exit_with_signal(message, 0)
    if warning:
        exit_with_signal(message, 1)


def exit_with_signal(message, signal):
    """Exit with nagios standard message and signal."""
    if signal == 0:
        print "OK: %s" % message
        sys.exit(signal)
    elif signal == 1:
        print "WARNING: %s" % message
        sys.exit(signal)
    elif signal == 2:
        print "CRITICAL: %s" % message
        sys.exit(signal)
    elif signal == 3:
        print "UNKNOWN: %s" % message
        sys.exit(signal)
    else:
        print "UNKNOWN: %s, %d" % (message, signal)
        sys.exit(signal)


def main(argv):
    """Main function, and options parsing."""
    # Default values
    host = "127.0.0.1"
    port = 9200
    try:
        opts, args = getopt.getopt(argv, 'hH:P:')
    except getopt.GetoptError:
        usage("Unknown option", 255)

    for opt, arg in opts:
        if opt in ('-H'):
            host = arg
        elif opt in ('-P'):
            port = int(arg)
        elif opt in ('-h'):
            usage(None, 0)

    json_data = get_cluster_health(host, port)
    analyze_data(json_data)

if __name__ == '__main__':
    main(sys.argv[1:])
