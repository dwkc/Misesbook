# Mises Ebook Scraper

## Introduction

This code downloads all of the PDFs currently publicly available on the Von Mises Institute website in the library / publications section.

It also provides some documentation once the scrape and download is complete, listing all of the files downloaded with the following fields in both JSON and CSV formats:

- title
- description
- date (as given by the tag on the site)
- source (e.g. the specific journal it is published in)
- tags [To be added]
- complete_url
- download_filename (Filename as saved to disk)

A third JSON file is also provided listing the titles and URLs to articles that did not have PDFs and so were not downloaded.

## How to use

The misesbook.py is the main script to execute. Before doing this be sure to adjust the settings in mises_settings.py. The most important ones are:

- self.download_folder
Where to save downloaded PDFs
- self.reporting_folder
Where to save the reporting docs (two JSON files and one CSV detailing what has and has not been saved)
- self.verbose
Defaults to 'False' if set to True the script will print out detailed information to standard out for every file it finds (and for every article it does not find a downloadable file for). Be warned this prints out a LOT of information and will slow the script down significantly.

Be warned that the library is quite substantial and the script already waits between pages in order to avoid battering the server, so even without verbose set to True allow up to 45 minutes for it to complete the scrape and download. 

## Files included and their function

misesbook.py
Main script

mises_settings.py
Settings file - imports a settings class as an object in misesbook.py so default settings can be conveniently passed around.

mises_helper_funcs.py
When the code is refactored at least two of the functions in misesbook.py will be moved here for import.

## Further background:

The Mises Institute being the ruthless capitalists they are, freely give away many of their journals and books in PDF format. There are a lot of files - 250 pages at the time of writing. Their library may be of significant interest to anyone who has an interest in libertarian or anarcho-capitalist leaning politics and economics.

## Planned features

More settings including a verbose function, wait time between batches of file downloads.

Concurrent downloads

Scrape and download from x time ago to update the library

Scrape other formats provided on the site (including 'HTML book')

Error checking to ensure files have actually been downloaded before being added to the reporting dictionaries.
