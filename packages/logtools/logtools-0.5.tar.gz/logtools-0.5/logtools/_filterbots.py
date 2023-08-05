#!/usr/bin/env python
#
#  Licensed under the Apache License, Version 2.0 (the "License"); 
#  you may not use this file except in compliance with the License. 
#  You may obtain a copy of the License at 
#  
#      http://www.apache.org/licenses/LICENSE-2.0 
#     
#  Unless required by applicable law or agreed to in writing, software 
#  distributed under the License is distributed on an "AS IS" BASIS, 
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
#  See the License for the specific language governing permissions and 
#  limitations under the License. 
"""
logtools._filterbots
Filter bots from logrows based on an ip/host and useragent blacklists.
"""
import re
import sys
import logging
from itertools import imap
from functools import partial
from optparse import OptionParser

from _config import logtools_config, interpolate_config, AttrDict

__all__ = ['filterbots_parse_args', 'filterbots', 
           'filterbots_main', 'parse_bots_ua', 'is_bot_ua']

def filterbots_parse_args():
    usage = "%prog " \
          "-u <useragents_blacklist_file> " \
          "-i <ips_blacklist_file> " \
          "-r <ip_useragent_regexp>"
    parser = OptionParser(usage=usage)

    parser.add_option("-u", dest="bots_ua", default=None, 
                      help="Bots useragents blacklist file")
    parser.add_option("-i", dest="bots_ips", default=None, 
                      help="Bots ips blacklist file")
    parser.add_option("-r", dest="ip_ua_re", default=None, 
                      help="Regular expression to match IP/useragent fields." \
                      "Should have an 'ip' and 'ua' named groups")
    parser.add_option("-p", "--print", dest="printlines", action="store_true",
                      help="Print non-filtered lines")
    parser.add_option("-t", "--pattern", dest="pattern", action="store_true",
                      help="Use pattern analysis to filter bots (See documentation for details)")    
    parser.add_option("-R", "--reverse", dest="reverse", action="store_true",
                      help="Reverse filtering")

    parser.add_option("-P", "--profile", dest="profile", default='filterbots',
                      help="Configuration profile (section in configuration file)")

    options, args = parser.parse_args()

    # Interpolate from configuration and open filehandle
    options.bots_ua  = open(interpolate_config(options.bots_ua, 
                                               options.profile, 'bots_ua'), "r")
    options.bots_ips = open(interpolate_config(options.bots_ips, 
                                               options.profile, 'bots_ips'), "r")
    options.ip_ua_re  = interpolate_config(options.ip_ua_re, 
                                           options.profile, 'ip_ua_re')  
    options.pattern   = interpolate_config(options.pattern, 
                                           options.profile, 'pattern', default=False, type=bool)    
    options.reverse   = interpolate_config(options.reverse, 
                                           options.profile, 'reverse', default=False, type=bool)
    options.printlines  = interpolate_config(options.printlines, 
                                             options.profile, 'print', default=False, type=bool) 

    return AttrDict(options.__dict__), args

def parse_bots_ua(bots_ua):
    """Parse the bots useragents blacklist
    and produce a dictionary for exact match
    and set of regular expressions if any"""
    bots_ua_dict = {}
    bots_ua_prefix_dict = {}
    bots_ua_suffix_dict = {}
    bots_ua_re   = []

    for line in imap(lambda x: x.strip(), bots_ua):
        if line.startswith("#"):
            # Comment line
            continue
        if line.startswith("r'"):
            # Regular expression
            bots_ua_re.append(re.compile(eval(line, {}, {})))
        elif line.startswith("p'"):
            bots_ua_prefix_dict[line[2:-1]] = True
        elif line.startswith("s'"):
            bots_ua_suffix_dict[line[2:-1]] = True
        else:
            # Exact match
            bots_ua_dict[line] = True

    return bots_ua_dict, bots_ua_prefix_dict, \
           bots_ua_suffix_dict, bots_ua_re


def is_bot_ua(useragent, bots_ua_dict, bots_ua_prefix_dict, bots_ua_suffix_dict, bots_ua_re):
    """Check if user-agent string is blacklisted as a bot, using
    given blacklist dictionaries for exact match, prefix, suffix, and regexp matches"""
    if not useragent:
        return False

    if useragent in bots_ua_dict:
        # Exact match hit for host or useragent
        return True
    else:
        # Try prefix matching on user agent
        for prefix in bots_ua_prefix_dict:
            if useragent.startswith(prefix):
                return True
        else:
            # Try suffix matching on user agent
            for suffix in bots_ua_suffix_dict:
                if useragent.endswith(suffix):
                    return True
            else:
                # Try Regular expression matching on user agent
                for ua_re in bots_ua_re:
                    if ua_re.match(useragent):
                        return True
    return False


def filterbots(fh, ip_ua_re, bots_ua, bots_ips, reverse, **kwargs):
    """Filter bots from a log stream using
    ip/useragent blacklists"""
    bots_ua_dict, bots_ua_prefix_dict, bots_ua_suffix_dict, bots_ua_re = \
                parse_bots_ua(bots_ua)
    bots_ips = dict.fromkeys([l.strip() for l in bots_ips \
                              if not l.startswith("#")])
    #reverse = options.reverse
    ua_ip_re = re.compile(ip_ua_re)

    is_bot_ua_func = partial(is_bot_ua, bots_ua_dict=bots_ua_dict, 
                             bots_ua_prefix_dict=bots_ua_prefix_dict, 
                             bots_ua_suffix_dict=bots_ua_suffix_dict, 
                             bots_ua_re=bots_ua_re)

    num_lines=0
    num_filtered=0
    for line in imap(lambda x: x.strip(), fh):
        match = ua_ip_re.match(line)
        if not match:
            logging.warn("No match for line: %s", line)
            continue

        matchgroups = match.groupdict()
        is_bot = False

        ua = matchgroups.get('ua', None)
        is_bot = is_bot_ua_func(ua)        

        if not is_bot and matchgroups.get('ip', None) in bots_ips:
            # IP Is blacklisted
            is_bot = True

        if is_bot ^ reverse:
            logging.debug("Filtering line: %s", line)
            num_filtered+=1
            continue

        num_lines+=1
        yield line

    logging.info("Number of lines after filtering: %s", num_lines)
    logging.info("Number of lines filtered: %s", num_filtered)            

    return

def filterbots_main():
    """Console entry-point"""
    options, args = filterbots_parse_args()
    if options.printlines:
        for line in filterbots(fh=sys.stdin, *args, **options):
            print line
    else:
        for line in filterbots(fh=sys.stdin, *args, **options): 
            pass

    return 0

