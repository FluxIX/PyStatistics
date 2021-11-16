__version__ = r"1.0"

from collections import namedtuple
from enum import Enum, unique
from ..utilities.dict import update_if_not_set
from ..utilities.sorting import get_values

PlanValue = namedtuple( "PlanValue", [ "starting_index", "length" ] )

@unique
class PartitionMedianBehavior( Enum ):
    """
    Enumeration of the median behaviors when partitioning a collection of values with an odd-number of values.
    """

    ExcludeBoth = 0
    IncludeLow = 1
    IncludeHigh = 2
    IncludeBoth = IncludeLow | IncludeHigh

    def __contains__( self, value ):
        return ( self.value & value.value ) != self.ExcludeBoth.value

def get_split_plan( value_count, **kwargs ):
    """
    Computes the plan required to split a collection of the given size into two collections, placing the median value according to given a keyword argument value.
    """

    if value_count is None:
        raise ValueError( "Value count cannot be None." )
    else:
        value_count = int( value_count )

        if value_count < 2:
            raise ValueError( "Insufficient number of items so split: {}".format( value_count ) )
        else:
            median_behavior = kwargs.get( "median_behavior", None )
            if median_behavior is None:
                median_behavior = PartitionMedianBehavior.ExcludeBoth

            split_point = value_count // 2

            if value_count % 2 == 0:
                lower_partition = PlanValue( 0, split_point )
                upper_partition = PlanValue( split_point, value_count - split_point )
            else:
                # The split point is the median.

                low_split_point = split_point
                if PartitionMedianBehavior.IncludeLow not in median_behavior:
                    low_split_point -= 1

                upper_split_point = split_point
                if PartitionMedianBehavior.IncludeHigh not in median_behavior:
                    upper_split_point += 1

                lower_partition = PlanValue( 0, low_split_point + 1 )
                upper_partition = PlanValue( upper_split_point, value_count - upper_split_point )

            return lower_partition, upper_partition

def split_values( *values, **kwargs ):
    """
    Partitions the values into two collections of equal size, lower and higher values; values are sorted by default.
    """

    lower_partition, upper_partition = get_split_plan( len( values ), **kwargs )

    keyword_args = update_if_not_set( kwargs, ( "sort", True ), in_place = False )
    data_values = list( get_values( *values, **keyword_args ) )

    starting_index, length = lower_partition
    lower = data_values[ starting_index, starting_index + length - 1 ]

    starting_index, length = upper_partition
    upper = data_values[ starting_index, starting_index + length - 1 ]

    return lower, upper

def get_partition_plan( partitions, value_count, **kwargs ):
    """
    Gets the plan to partition into a number of equally-sized groups.
    """

    if partitions < 1:
        raise ValueError( "Insufficient number of partitions ({}) requested.".format( partitions ) )
    else:
        if value_count < partitions:
            raise ValueError( "Insufficient number of values ({}) into {} partitions.".format( value_count, partitions ) )
        else:
            result = []

            if partitions == 1:
                result.append( PlanValue( 0, value_count ) )
            else:
                partition_fencing_operation = kwargs.get( "partition_fencing_operation", None )
                if partition_fencing_operation is None:
                    partition_fencing_operation = round

                ideal_partion_size = float( value_count ) / partitions
                starting_index = 0
                for partition_division in map( lambda x: x + 1, range( partitions ) ):
                    # The `ending_index` is inclusive.
                    ending_index = int( partition_fencing_operation( float( partition_division ) * ideal_partion_size ) ) - 1
                    partition_size = ending_index - starting_index + 1

                    result.append( PlanValue( starting_index, partition_size ) )

                    starting_index = ending_index + 1

            return tuple( result )

def partition_values( partitions, *values, **kwargs ):
    """
    Partitions into a number of equally-sized groups of values; values are sorted by default.
    """

    plan = get_partition_plan( partitions, len( values ), **kwargs )

    keyword_args = update_if_not_set( kwargs, ( "sort", True ), in_place = False )
    data_values = list( get_values( *values, **keyword_args ) )

    result = []
    for starting_index, partition_size in plan:
        ending_index = starting_index + partition_size
        result.append( data_values[ starting_index: ending_index ] )

    return tuple( result )
