__version__ = r"1.0"

# Cannot use a relative import here.
from statistics._unit_tests.main import main as entry_point

if __name__ == '__main__':
    import sys
    ret_value = entry_point( sys.argv, has_prog_name = True )

    sys.exit( ret_value )
