# amazon_bookdetails
This is a ready-to-run project to can fetch the book details from amazon website. It stores the books link, book name and price in output files. NO ADDITIONAL LIBRARIES OR API ARE NEEDED!!!!!

Platform: Python 2.7
This program can take a book search string (e.g C books, python programming, cracking coding interviews) and it searches for them in amazon.com. User will be prompted to enter for his search criteria.

The output of program is split into 2 output files
1) keyword_links.txt --> Saves the URL of the search results from amazon.com. Technically it will be the direct URL of the available books in Amazon based on your search

2) keyword_details.txt --> Stores the book name and paperback price of the top books

PS: This is an ongoing project. Future work will mainly focus on below action items
1) Will be incorporated to run on Python 3 platform. Minor changes required
2) The prices of only paperback type is stored in keyword_detials.txt file. Future worl will focus on getting other prices of the same book, like Kindle, Hardcover, Other sellers
3) Currently can search for books. Will be made generic to see if it can retrieve any product detail from Amazon.com

