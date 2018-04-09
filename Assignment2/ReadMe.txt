There are 4 major sub-folders in the Assignment. One for scraping the UFO stalker website to fetch the image URLs, ....


The main input file containing the ufo data is :- 
The intermediate files are as following:-

The main modified output file containing the ufo data is :- 

The libraries used/need to be installed are:-
pip install selenium

The important files present in the folders are :-

1) url_extract[1-4].py
-- The UFO Stalker website has urls ranging from the event id 1 to event id 91148. To scrape all these events from the UFO stalker website, we have written 5 programs - url_extract.py, url_extract1.py, .... ,url_extract4.py where each program is run parallely and executes ~20000 event ids to scapre the image urls.
-- These programs give us the scraped image urls and are stored in text files - urls_images2.txt, urls_images2.txt, ... , urls_images5.txt

2) combine_urls.py
-- This program is used to take all the scapred urls_images[1-5].txt files and combine them all and store just the unique ones in the file image_urls.txt. This new text file is inturn used by the OCR pipeline for captioning and defining the objects from the images.






The order in which the programs need to be executed:
1)  url_extract[1-4].py
2)  combine_urls.py

