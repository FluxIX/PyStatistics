#!/usr/bin/env python

from statistics_tester import run as entry_point

def run( args = [] ):
    return entry_point( args )

if __name__ == "__main__":
    import sys

    run( sys.argv )
