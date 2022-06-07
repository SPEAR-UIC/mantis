"""
Module to handle all components configuring Mantis Monitor

Author: Melanie Cornelius
This code is licensed under LGPL v 2.1
See LICENSE for details
"""

import pprint
import logging
import yaml
import subprocess
import os

#TODO how do I make sure all the logs go to the same place? Just reuse the name?
logging.basicConfig(filename='testing.log', encoding='utf-8', format='%(levelname)s:%(message)s', level=logging.DEBUG)

class Configuration:
    """
    Outer-most object to control Configuration elements
    """
    def __init__(self, location=None):
        """The config file used during this invocation of mantis-monitor"""
        self.location = location
        """Config file location, a string"""
        if location and os.path.exists(location):
            self.contents = yaml.safe_load(open(location))
            logging.info("Read config yaml at %s", location)
        elif location:
            logging.error("A config file was provided but could not be found")
            raise ValueError("Config file not found")
        else:
            self.contents = generate_default_config()

        self.set_all_contents()
        check_perf()
        check_nvidia()

    def set_all_contents(self):
        self.collector_modes = self.contents["collection_modes"]
        self.benchmarks = self.contents["benchmarks"]
        self.formatter_modes = self.contents["formatter_modes"]
        self.perf_counters = self.contents["perf_counters"]

        self.log = self.contents["log"]

        self.test_name = self.contents["test_name"]
        self.iterations = self.contents["iterations"]
        self.timescale = self.contents["time_count"]

    def print_all(self):
        pprint.pprint(self.contents)


def generate_default_config():
    """Helper function to generate a new default configuration
    """
    # Get possible perf counters and search for default counters
    selected_counters = get_default_counters(get_available_perf())

    # Build default yaml
    default_yaml = {
        'benchmarks': {
            'TestBench': {
                'runner': "TestBench",
                'waittimes': [1, 4, 8],
            },
        },
        'collection_modes': {
            'perf': {
                'pmu_count': 4,
            },
            'memory': None,
            #'memory': {
            #    'modes': ['high_watermark', 'memory_over_time'],
            #},
            #'nvidia': {
            #    'modes': ['api_trace', 'gpu_trace', 'power_over_time', 'power_summary'],
            #    'gen': 'sm_80',
            #},
        },
        'formatter_modes': ['PandasPickle', 'CSV'],
        'perf_counters': selected_counters,

        'iterations': 1,
        'time_count': 1000,
        'log': True,
        #'debug': True,
        'test_name': 'DEFAULT',
    }

    return default_yaml

def get_default_counters(all_counters):
    """Function to do string closest-matching on perf counter names
    Early implementation should ignore case
    Add more match strings here for better fuzzy matching on new architectures
    If this becomes unwieldy or enormous, move to fuzzy string matching, but it would be overkill
    in the current implementation
    """
    match_strings = {
        "instructions": ["instructions"],
        "cycles": ["cycles", "cpu-cycles"],
        "LLC stores": ["LLC-stores"],
        "page faults": ["page-faults"],
        "major faults": ["major-faults"],
        #"memory BW": ["DRAM_BW_Use"],
        #"cpu power": ["Average_Frequency"],
        #"cpu utilization": ["CPU_Utilization"],
    }

    matched_counters = []
    for match_string_category, match_string_list in match_strings.items():
        # Want to ensure we only add a matched string once per category and once per
        # matching against that category, hence the use of the below temp variable
        # This is relatively inefficient, but for a small number of default values,
        # it should not be too expensive, only about 1,000 string match operations
        matched_counter_string = None
        for match_string in match_string_list:
            for counter_string in all_counters:
                if match_string.lower() == counter_string.lower():
                    matched_counter_string = counter_string

        if matched_counter_string:
            matched_counters.append(matched_counter_string)

    return matched_counters

def dump_default_yaml(location):
    config = generate_yaml()
    with open(location, 'w') as yamlfile:
        yaml.dump(contents, yamlfile)
        logging.info("Dumped new yaml file at %s", location)


def check_perf():
    perf_overall = subprocess.run("perf", capture_output=True)
    if not perf_overall:
        logging.info("Uh-oh, it looks like there's an issue using perf!")
    else:
        logging.info("Perf outputs")

def get_available_perf():
    """Helper function to query perf and return all available counters
    """
    perf_list_raw = subprocess.run(["perf", "list", "--raw-dump"], capture_output=True, text=True)
    return list(set(perf_list_raw.stdout.split()))

def check_nvidia():
    """Helper function to ensure nvidia systems function on this architecture, TODO
    """
    pass

if __name__ == "__main__":
    #dump_default_yaml("../config.yaml")
    c = Configuration()
    print(c.contents)
