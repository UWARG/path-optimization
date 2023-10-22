"""
Test Process.
"""

from modules import waypoints_dict_to_list

def test_valid_waypoint_dict():
    """
    Test valid waypoints dictionary.
    """

    input =  {"Alpha": (43.4340501,-80.5789803), "Bravo": (43.4335758,-80.5775237), "Charlie": (43.4336672,-80.57839)}
    expected = [(43.4340501,-80.5789803), (43.4335758,-80.5775237), (43.4336672,-80.57839)]  #expected output

    # determine if action was successful
    result, output = waypoints_dict_to_list.waypoints_dict_to_list(input)

    assert result
    assert output == expected

def test_empty_waypoint_dict():
    """
    Test empty dictionary of waypoints.
    """

    input =  {}
    expected = None  # expected output 

    # determine if action was successful
    result, output = waypoints_dict_to_list.waypoints_dict_to_list(input)

    assert not result
    assert output == expected
