#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Get Zabbix configuration data from the Zazbbix Rest API """


import os
import sys
import json
from collections import defaultdict
from zbx_admin.zbx_conf import zabbix_conf
from zabbix_api import ZabbixAPI, ZabbixAPIException
from argparse import ArgumentParser, RawDescriptionHelpFormatter


HELP_MESSAGE = """
    This script get the configuration data from a Zabbix Server.
    The output format is in XML format that is the default to import on Zabbix Web.
    The option --format accept JSON format that can be used with the Rest API.
    If the number of host, groups or template be to much huge, increase --timeout_seconds.

    To use some environment vars is necessary, so export than all:
        > export ZABBIX_USER=zabbix_web_user
        > export ZABBIX_PASS=zabbix_user_password
        > export ZABBIX_HOST=hostname_or_ip_of_zabbix_server
"""



def config_args():
    """ Parse args to run the config backup process """

    _parser = ArgumentParser(description=HELP_MESSAGE, formatter_class=RawDescriptionHelpFormatter)

    _parser.add_argument("-p", "--path", action="store", default=".",
                         help="Get path to save the output files. Default.")
    _parser.add_argument("-t", "--type", action="store", default="all",
                         help="Get path to save the output files. Default.")
    _parser.add_argument("-v", "--verbose", action="store_true", default=False,
                         help="Print verbose data.")
    _parser.add_argument("-s", "--timeout_seconds", action="store", default=10,
                         help="Time in seconds to timeout request in the Zabbix API.")
    _parser.add_argument("-f", "--format", action="store", default="xml",
                         help="Format of output data, default is XML.")

    return _parser.parse_args()

def get_opts():
    """ Get opts to get config from Zabbix API """

    _opts = defaultdict(lambda: False)
    
    for env in ['ZABBIX_USER', 'ZABBIX_PASS', 'ZABBIX_HOST']:
        if env in os.environ.keys():
            _opts[env] = os.environ[env]
        else:
            print((f"\nThe env var {env} was not found!\nPlease, set the var in your bash_profile.\n"
                   "Exiting...\n"))
            sys.exit(0)

    _args = config_args()

    _opts['path'] = _args.path
    _opts['type'] = _args.type
    _opts['verbose'] = _args.verbose
    _opts['timeout'] = _args.timeout_seconds
    _opts['format'] = _args.format
    _opts['help'] = HELP_MESSAGE

    return _opts

def main():
    opts = get_opts()
    get_conf = zabbix_conf(opts)
    get_conf.run()

if __name__ == "__main__":
    main()