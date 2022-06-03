"""
Module containing Mantis base Benchmark class and any basic benchmark helper functions

Author: Melanie Cornelius
This code is licensed under LGPL v 2.1
See LICENSE for details
"""

import logging

logging.basicConfig(filename='testing.log', encoding='utf-8', format='%(levelname)s:%(message)s', level=logging.DEBUG)

class Benchmark():

    implementations = {}

    # Make sure this is unique TODO
    @staticmethod
    def register_benchmark(name, benchmark_class):
        Benchmark.implementations[name] = benchmark_class

    # TODO this is where to change from single to list generation
    @staticmethod
    def get_benchmark(name, arguments):
        return Benchmark.implementations[name](arguments)

    def get_benchmarks(name, arguments):
        # TODO have this thing return a list (or something) of benchmarks with cross-product

    def __init__(self, arguments): #location = "", runscript = "", arguments = "", name = ""):
        self.name = ""
        self.arguments = None

    def setup(self):
        pass

    def get_run_command(self):
        pass

    def teardown(self):
        pass
