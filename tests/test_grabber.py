# -*- coding: utf-8 -*-

"""Run with py.test"""

from grabber import *


def test_fix_title():
    """Test that title is correctly fixed"""

    good = 'Roger Glover - Love is all'
    assert good == fix_title(good, None)

    assert 'Me here - Missing dash' == fix_title('Me here- Missing dash', None)

    assert 'Roger Glover - Love is all' == fix_title('Roger Glover - Love is all // Out now', None)

    assert 'DJ Crontab - Execute Every Minute' == fix_title('Execute Every Minute', 'DJ Crontab')
