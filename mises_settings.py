#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Mises scraper settings """

class Settings():
    """A class to store all settings for Mises scraper"""

    def __init__(self):
        """Initialize the app's settings."""
        # Basic settings

        self.download_folder = "G:\docs\mises_books" # default download folder
        self.reporting_folder = "G:\docs\mises_reporting" # default reporting/logging folder
        self.verbose = False

        # Settings for features yet to be added


        self.sleep_duration = 3 # default period to wait between processing up to 10 files in the dictionary for download to save the server's bandwidth.
        self.time_from = "" # default time period from current date to check for new content
        self.target_url = "" # base url for the mises ebooks & articles

# TODO: change default directories to user desktop folder
