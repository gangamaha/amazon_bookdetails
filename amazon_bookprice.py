import urllib2
from __builtin__ import any


def download_link(url):
    try:
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        req = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(req)
        page = response.read()
        return page
    except:
        print "Cannot reach amazon.com, check your internet connection and try again later!!"
        exit(0)


def get_next_link(raw_html):
        start_line = raw_html.find("a class=\"a-link-normal a-text-normal\"")
        if start_line == -1:
            end_content = 0
            next_link = "no_more_link"
            return next_link, end_content
        else:
            start_line = raw_html.find("a class=\"a-link-normal a-text-normal\"")
            start_content = raw_html.find("href=", start_line+1)
            end_content = raw_html.find("\">", start_content+1)
            next_link = str(raw_html[start_content+6:end_content])
            return next_link, end_content


def get_url_details(raw_html):
    url_list = []
    while True:
        link, end_content = get_next_link(raw_html)
        if link == "no_more_link":
            break
        else:
            url_list.append(link)
            raw_html = raw_html[end_content:]
    return url_list


def extract_product_details(product_page):
    start_line = product_page.find("<span class=\"sims-fbt-this-item a-text-bold\">")
    with open(books_file, 'a') as output:  # output is redirected to this file.
        # if file output.txt exist in same directory the contents will be appended
        if start_line != -1:
            start_product_name = product_page.find("This item:</span><span>",start_line+1)
            end_product_name = product_page.find("</span><span class=\"a-size-small\">", start_product_name+1)
            product_title = str(product_page[start_product_name+23:end_product_name])  # Holds the title
            start_price_line = product_page.find("</span><span class=\"a-size-small a-color-secondary\">")
            # if start_price_line != -1:
            start_product_price = product_page.find("</span> <span class=\"a-color-price\">", start_price_line+1)
            end_product_price = product_page.find("</span> <div class=\"a-row a-spacing", start_product_price+1)
            product_price = str(product_page[start_product_price+36:end_product_price])  # holds the price
            output.write("Name: "+product_title+"\n")
            output.write("Price: "+product_price+"\n")
    output.close()


def get_product_details(product):
    try:
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        req = urllib2.Request(product, headers=headers)
        resp = urllib2.urlopen(req)
        product_page = resp.read()  # raw html content for every book link
        extract_product_details(product_page)  # get name and price of book, pass the html content as parameter
    except:
        return False

"""
Main program logic.
The keyword is a string and search is carried in amazon.com website
The product details and the prices from the web search is written in file output.txt
Please change the keyword string if you want to search for another product
"""
keyword = raw_input("Enter the book name you want to purchase:").strip()
if keyword is '':
    print "Looks like you have not entered any book name to be searched. Exiting!!"
    exit(0)

print "Processing your request for "+keyword+". This may take some time!!"
if ' ' in keyword:  # if space is present, replace with + for proper search
    keyword = keyword.replace(' ', '+')


# url = "https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords="+keyword
url = "https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords="+keyword+"&rh=i%3Aaps%2Ck%3A"+keyword
# print url
raw_html = download_link(url)  # gets the raw content of the url search page
# print raw_html
overall_search_results = []
overall_search_results = get_url_details(raw_html)  # gets the url of each search result from the entire page
remove_dummy_links = []
for links in overall_search_results:
    book_name = links.split("/")[3]
    if 'https://www.amazon.com' in links and links not in remove_dummy_links:
        if not any(book_name in check for check in remove_dummy_links):
            # removes any unwanted links or duplicate results
            remove_dummy_links.append(links)


links_file = (keyword+"_links.txt").replace("+", "_")
print "Writing the search result links in "+links_file
with open(links_file, "w") as out:
    out.write("\n".join(remove_dummy_links))
out.close()

print links_file+" created successfully. Please wait when we get the specific product details"
books_file = (keyword + "_details.txt").replace("+", "_")

print "Retrieving the price details for popular "+keyword.replace("+", " ")+" in "+books_file
limit_search = 20
for link in remove_dummy_links:
    if limit_search >= 0:
        # print link
        get_product_details(link)  # main logic to get book name and price.
        limit_search -= 1

print "Product details are stored in "+books_file

"""
End of program
"""