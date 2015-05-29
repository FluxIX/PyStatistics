#!/usr/bin/env python

from statistics_tester import StatisticsTester

def run( args = [] ):
    StatisticsTester().run()

if __name__ == "__main__":
    import sys

    run( sys.argv )
