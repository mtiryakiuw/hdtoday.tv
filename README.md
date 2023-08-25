# hdtoday.tv
Web Scraping with BeautifulSoup (Soup)

    Obtain the "Soup" folder by downloading it.
    Launch the "soup.py" file in your Python environment.
    The script will commence the web scraping process, extracting data from web pages.
    The results will be compiled and saved in an Excel file produced within the same folder.

Web Scraping with Scrapy

    Open your preferred development environment and navigate to the Scrapy folder.
    Launch your terminal and navigate to the Scrapy folder location.
    Execute the command: scrapy crawl link_lists -O links.csv. This will trigger the first spider to collect movie links and save them in a "links.csv" file.
    Run the command: scrapy crawl movies -o movies.csv to activate the second spider. This spider scrapes movie details and stores them in a "movies.csv" file.

Web Scraping with Selenium

    Download the "Selenium" folder to your computer.
    Make sure you have both the "Chrome" web driver and the "uBlock Origin" browser extension installed.
    Open the "selenium.py" file in a text editor.
    Update the paths for the "Chrome" web driver and "uBlock Origin" extension to match your machine's locations.
    Run the "selenium.py" file to initiate the scraping process.
    The collected data will be saved in an Excel file generated in the current folder.


Feel free to reach out if you encounter any issues or have questions while following these instructions. Remember to ensure that you have the necessary drivers, extensions, and prerequisites installed before running the code.

If you get error about openpyxl, please use below command on terminal.

    pip install openpyxl
