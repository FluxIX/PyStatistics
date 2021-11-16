__version__ = r"1.0"

from .statistics_tester import StatisticsTester

def main( args = [] ):
    return StatisticsTester().run()
