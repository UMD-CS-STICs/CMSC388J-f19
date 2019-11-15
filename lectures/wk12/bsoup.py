import requests
from bs4 import BeautifulSoup

response = requests.get('https://github.com/')

# print(response.text)

soup = BeautifulSoup(response.text)

lists = soup.find_all('li')

for i in lists:
    print(i)
    break



def table_processor(self, soup: BeautifulSoup):
    element = WebDriverWait(self.driver, 5).until(
        ec.presence_of_element_located((By.XPATH, "//table"))
    )

    table = soup.find("table")

    all_data = []

    body = table.find("tbody")
    for row in body.find_all("tr"):
        data = {}

        # Get rid of the cover column
        columns = row.find_all("td")[1:]

        # Sanity checks
        year_col = columns[0]
        assert year_col["class"][0] == "year"

        year = int(year_col.string)
        data["Year"] = year

        # Sanity checks
        artist_col = columns[1]
        assert artist_col["class"][0] == "artist"

        try:
            artist = artist_col.a.string
        except AttributeError:
            artist = artist_col.string

        data["Artist"] = artist

        # Sanity checks
        title_col = columns[2]
        assert title_col["class"][0] == "title"

        try:
            title = title_col.a.string
        except AttributeError:
            title = title_col.string

        data["Album"] = title

        # Sanity checks
        ratings_col = columns[3]
        assert ratings_col["class"][0] == "rating"

        match = re.match(r"rating-allmusic-(\d)", ratings_col.div["class"][1])

        if match:
            """ The '\d' captured from the class of our div, corresponds to some rating

            The lowest rating is 1 star, that corresponds to the class of 1. Each subsequent
            increment in class number increases the rating by 0.5 of a star
            """
            rating = (int(match.group(1)) + 1) * 0.5
            data["Rating"] = rating

            all_data.append(data)

    return all_data
