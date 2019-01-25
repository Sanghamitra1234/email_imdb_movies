import requests
import urllib.request
from bs4 import BeautifulSoup
import csv
import smtplib
from flask import Flask, request, render_template

app = Flask(__name__)

# calling the html page


@app.route('/hello')
def index():
    return render_template('hello.html')

# defining a function to call python function and return success


@app.route('/upload')
def upload():
    main()
    return '<h>Hi, this is Sanghamitra and the task is complete</h>'


def read_m_by_rating(first_year, last_year, num_of_m=50):
    # Below is the code for reading html and create a beautifulsoup object
    url = "http://www.imdb.com/search/title?at=0&sort=user_rating&start=1&title_type=feature&year=" + first_year + "," + last_year + "&view=simple"
    test_url = requests.get(url)
    readHtml = test_url.text
    soup = BeautifulSoup(readHtml, "html.parser")

    # contained in a table. They are actually enclosed in a <div class="lister-list"> tag. Then within this div tag, you can find a number of
    # <div class="lister-item mode-simple">, each of which represents a movie
    movies_div = soup.find('div', attrs={'class': 'lister-list'})
    movies = movies_div.find_all('div', attrs={'class': 'lister-item mode-simple'})
    list_movies = []  # initialize the return value, a list of movies

    # Using count track the number of movies processed. now it's 0 - No movie has been processed yet.
    count = 0

# for m in movies: # each row represents information of a movie
    for movie in movies:
        dict_each_movie = {}

        # code to fetch year movie title.
        title_dictionary = movie.find('span', attrs={'class': 'lister-item-header'})
        title = title_dictionary.find('a').get_text().encode("ascii", "ignore")
        dict_each_movie["title"] = title

        list_movies.append(dict_each_movie)
        count = count + 1
        if count == num_of_m:
            break
    return list_movies


def write_movies_csv(list_movies, filename, s):
    lis = []  # to write the file, we create a list of strings
    header = "TITLE"
    lis.append(header)  # add the header to the list
    for movie in list_movies:
        string = str.encode(str(len(lis))) + str.encode(" ") + movie["title"]
        lis.append(string)  # add the string to the list

    thelist = lis
    f = open(filename, "w")

    for item in thelist:

        # print(item)
        s = s + str(item) + "\n"
        f.write("%s \n" % item)  # trying to send the csv but couldnt understand the process.
    f.close()
    return s


def main():
    li = read_m_by_rating("2005", "2016", 50)
    s = ""
    content = (write_movies_csv(li, "movies.csv", s))
    send_movies(content)


def send_movies(content):
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login('sender_email_id', '********')
    mail.sendmail('sender_email_id', 'reciever_email.id', content)
    mail.close()


if __name__ == '__main__':
    app.run(debug=True)
