#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from typing import List

from cdp_backend.pipeline.ingestion_models import EventIngestionModel
from cdp_scrapers.legistar_utils import LegistarScraper

###############################################################################


def get_events(
    from_dt: datetime,
    to_dt: datetime,
    **kwargs,
) -> List[EventIngestionModel]:
    scraper = LegistarScraper(
        client="sanjose",
        timezone="America/Los_Angeles",
        ignore_minutes_item_patterns=[
            "* COVID-19 NOTICE *",
            (
                "this meeting will not be physically open to the public "
                "and the Committee Members will be teleconferencing from "
                "remote locations"
            ),
            "How to observe the Meeting",
            (
                "1) Cable Channel 26, "
                "2) https://www.sanjoseca.gov/news-stories/watch-a-meeting, "
                "or 3) https://www.youtube.com/CityofSanJoseCalifornia"
            ),
            "How to submit written Public Comment:",
            (
                "1) By email to city.clerk@sanjoseca.gov by "
                "9:00 a.m. the day of the meeting."
            ),
            "How to provide spoken Public Comment during the Committee Meeting:",
            (
                "Certain functionality may be disabled in older "
                "browsers including Internet Explorer",
            ),
            "City Council (City Clerk)",
            "Notice to the public",
            "Members of the Public are invited to speak on any item",
            "The Code of Conduct",
            "The City of San José is committed to open and honest government",
            "All public records relating to an open session item on this agenda",
            "To request an accommodation or alternative format",
            "Access the video, the agenda and related reports",
        ],
    )

    return scraper.get_events(begin=from_dt, end=to_dt)
