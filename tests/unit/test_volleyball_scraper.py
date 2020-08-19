# Standard library imports...
from unittest.mock import Mock, patch
from pathlib import Path

import pytest
from volleyball_scraper import VolleyballLadder, VolleyballRoster

roster_content = Path('tests/data/monday.html').read_text()


@patch('volleyball_scraper.requests.get')
def test_Volleyball_ladder(mock_get):

    ladder_content = Path('tests/data/monday_ladder.html').read_text()

    mock_get.text = ladder_content
    # mock_get.return = 200

    ladder = VolleyballLadder("http://ossieindoorbeachvolleyball.com.au/monday-mens")

    assert ladder.competition_name == "Monday Mens"
