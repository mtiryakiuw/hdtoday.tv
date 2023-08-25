# hdtoday.tv
Web Scraping with BeautifulSoup (Soup)

    Obtain the "Soup" folder by downloading it.
    Launch the "main.py" file in your Python environment.
    The script will commence the web scraping process, extracting data from web pages.
    The results will be compiled and shows results on console
    
Web Scraping with Scrapy

    Open a terminal or command prompt.
    Make sure you have Scrapy installed. If not, install it using the command: pip install scrapy
    Create a new Scrapy project using the command: scrapy startproject myproject
    Place the spiders provided in the appropriate "spiders" folder within your Scrapy project directory.
    Navigate to your Scrapy project directory.
    Execute the command: scrapy crawl LinkListsSpider -o links.csv to run the "link_lists" spider and save the extracted links to a CSV file named "links.csv".
    After the above step, execute the command: scrapy crawl MoviesSpider -o films.csv to run the "films" spider and save the scraped movie data to a CSV file named "films.csv".
    Verify the generated CSV files ("link_list.csv" and "films.csv") to check if the data has been successfully scraped.


Web Scraping with Selenium

    Download the "Selenium" folder to your computer.
    Run the "main.py" file to initiate the scraping process.
    The script will commence the web scraping process, extracting data from web pages.
    The results will be compiled and shows results on console


Feel free to reach out if you encounter any issues or have questions while following these instructions. Remember to ensure that you have the necessary drivers, extensions, and prerequisites installed before running the code.

If you get error about openpyxl, please use below command on terminal.

    pip install openpyxl
