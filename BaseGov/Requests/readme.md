# Usign Requests for Web Scraping


## Challenge 

Scrapy is a powerful tool for web scraping, but it has limitations when it comes to scraping dynamic websites. Dynamic websites use JavaScript to load data and update content on the page without having to reload the entire page. This makes the website more interactive and user-friendly, but it also makes it more difficult to scrape the data.

When you use Scrapy to scrape a website, it makes an HTTP request to the website's server and retrieves the HTML content of the page. However, if the website is dynamic and uses JavaScript to load content, the HTML content that Scrapy retrieves may not include all of the data that you need. This is because the data may be loaded after the initial HTML content is retrieved, and may only be accessible through JavaScript code.

In the case of [base.gov](https://www.base.gov.pt/base4), the data was indeed being loaded dynamically through JavaScript. This means that even if I was able to retrieve the HTML content using Scrapy, I would not be able to access the data I needed without executing the JavaScript code that loads the data.

## Solution

To retrieve the necessary information, I decided to create a script that goes directly to the database and makes a request based on the network data, specifically the JavaScript request. With the help of a great AI tool you might have heard of, I created a function that would take the header for the request (from Inspect -> Network -> Resultados -> Copy Request Headers)

To work around this limitation, we can also use a headless browser like Selenium to automate the web scraping process. You can find this script on Web-Scraping-Projects /BaseGov/Requests [Selenium](Selenium/)





