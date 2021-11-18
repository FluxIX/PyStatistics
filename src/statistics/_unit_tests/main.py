__version__ = r"1.0"

from .statistics_tester import run as main_entry

def main( args = [], **kwargs ):
    return main_entry( args, **kwargs )
