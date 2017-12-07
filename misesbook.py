#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Mises Institute ebook scraper"""

import requests, os, bs4, urllib.request, json, csv, time

from mises_settings import Settings

settings = Settings() # create object with default settings from class in  mises_settings.py


# TODO: Move other settings below to settings file
base_url = 'https://mises.org/library/institute-publications' # library list


base_file_url = 'https://mises.org' # files downloaded from different directory - 'files' which is appended to the file URL download link.

page_url = '?page=' # page number

full_ebook_dict_list = [] # complete list of all ebooks found

no_doc_dict = {} # dictionary to inform user of any entries without corresponding PDFs

non_pdf_dict = {} # temporary dict to help identify other formats  # TODO; delete this!

# TODO: add a check for the last page to dynamically calculate len

def main():

    for i in range(0,1,1): # TODO: Restore to 251
        url = base_url + page_url + str(i)

        print(f'Downloading page {url}...')

        res = requests.get(url)
        res.raise_for_status() # check request was successful

        ebook_dict_list = [] # reset list of dictionaries for file downloads for *this* page. Used to manage downloads and to push ebook details to the full dictionary in chunks

        # Main div for each entry is class 'group-right  col-xs-9'

        # Title is <a> within <h2> class 'teaser-title'
        # teaser_headline = soup.select('.teaser-title')


        soup = bs4.BeautifulSoup(res.text,"html.parser")

        book_sections = soup.select("div[class^=group-right]")

        book_sections_found = len(book_sections)

        for i in range(book_sections_found):

            title = book_sections[i].select('h2[class^=teaser-title] a')[0].getText()
            article_url = base_file_url + (book_sections[i].select('h2[class^=teaser-title] a')[0].get('href')) # used for entries with no doc. Effectively duplicated by content_url in loop below but makes code clearer
            description = book_sections[i].select('div[class^=body-content]')[0].getText()
            date = book_sections[i].select('span[class^=date]')[0].getText()
            source = book_sections[i].select('span[class^=search-label]')[0].getText()

            # returns entire block of document formats available

            format_block = book_sections[i].select('div[class^=book-formats]')

            if not len(format_block) == 0:


                content_blocks = format_block[0].select('div[class^=content] a')

                file_name_url = format_block[0].select('h2[class^=element-invisible] a')
                file_name = file_name_url[0].getText()

                content_type = content_blocks[0].getText()

                content_url = content_blocks[0]['href']

                full_file_url = base_file_url + content_url

                # TODO: Need a loop to identify tags (if any)

                if content_type == "PDF":


                    ebook_dict = {
                            'title': title,
                            'description': description,
                            'date': date,
                            'source': source,
                            'complete_url': full_file_url,
                            'download_filename':file_name,
                    }

                    ebook_dict_list.append(ebook_dict.copy())
                    full_ebook_dict_list.append(ebook_dict.copy())


                else:
                    print("\nNon PDF entry found")
                    # Add to dictionary
                    non_pdf_dict[content_url] = content_type


            else:
                print(f"\n NO DOCUMENT ENTRIES FOR {title}\n") # entries that just provide links to an article rather than an ebook/document format.
                no_doc_dict[title] = article_url
                continue


            # TODO: select only for PDF types. Add in loops/logic for others later


            if settings.verbose == True:

                print(f"\nTitle: {title}")
                print(f"\nDescription: \n {description}")
                print(f"\nSource: {source} \n Date: {date} \n")
                print(f"\nContent type: {content_type} \n")

                #full_file_url = base_file_url + content_url

                print(f"Content URL: {full_file_url}\n")
                print(f"Content file download name: {file_name}")

        download_ebook_dict(ebook_dict_list,settings.download_folder)

        print("\n Waiting for 3 seconds.... \n")
        time.sleep(3) # TODO: Add in sleep setting from mises_settings

    # Create report files from dictionaries
    my_folder = settings.reporting_folder

    report(my_folder)

# Functions. To be refactored

def download_ebook_dict(books,my_path):
    """Manages download of dictionary for page of ebooks found"""

    books_number = len(books)

    # TODO: Account for files that are in same publication & avoid multiple unnecessary downloads.

    for book in range(books_number):
        current_book = books[book]
        fullfilename = os.path.join(my_path, current_book['download_filename'])
        urllib.request.urlretrieve(current_book['complete_url'],fullfilename)
        print(f"\nDOWNLOADED: {current_book['title']}")
        print(f"\nLOCATION: {fullfilename}")

    # TODO add verbose functionality

def report(my_folder):
    """
    Creates and saves reporting files based on stored dictionaries.
    Two JSON files are created (viewable in Firefox or similarly modern browser) and one CSV. mises_ebooks.json and mises_ebooks.csv contain identical information in different formats - showing the full details for each ebook downloaded and its source article.
    mises_articles_no_ebook.json saves a json file with titles and URL links for articles found with no PDF attachment.
    """

    # Save reporting files
    # JSON files

    # Ebook list
    with open((os.path.join(settings.reporting_folder, 'mises_ebooks.json')), 'w') as ebook_file:
        json.dump(full_ebook_dict_list, ebook_file)

    # Articles without PDFs
    with open((os.path.join(settings.reporting_folder, 'mises_articles_no_ebook.json')), 'w') as no_ebook_file:
        json.dump(no_doc_dict, no_ebook_file)

    # CSV files

    # Ebook list
    ebook_csv_keys = full_ebook_dict_list[0].keys()
    with open((os.path.join(settings.reporting_folder,'mises_ebooks.csv')), 'w', newline="\n", encoding="utf-8") as ebook_csv:
        dict_writer = csv.DictWriter(ebook_csv, ebook_csv_keys)
        dict_writer.writeheader()
        dict_writer.writerows(full_ebook_dict_list)
    # Articles without PDFs

    # TODO: csv output of dictionary for no ebook articles (just a simple dict in this case, not a list of dicts as above)


main()


if __name__ == "__main__":
    main()
