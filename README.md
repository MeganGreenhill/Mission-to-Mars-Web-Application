# Mission to Mars Web Application

For this assignment, a web application was built that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page.

Firstly, Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter were used to perform a scrape of the following:
* The Mars News Site (https://redplanetscience.com/) - to collect the latest News Title and Paragraph Text.
* The Featured Space Image site (https://spaceimages-mars.com) - to find the image url for the current Featured Mars Image and assign the url string to a variable.
* The Mars Facts webpage (https://galaxyfacts-mars.com) - to scrape the table containing facts about the planet including Diameter, Mass, etc.
* The astrogeology site (https://marshemispheres.com/) - to obtain high resolution images for each of Mar's hemispheres.

After this, MongoDB was used with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.
