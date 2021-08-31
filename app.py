from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from bingscraper.bingscraper import BingScraper

app = Flask(__name__)

# bs = BingScraper("driver//chromedriver.exe", 'cat', 4)


# search_query = request.form["content"]
# time_stamp = request.form["Sheduletime"]
# print(time_stamp)

# bs.store_links()
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_email', methods=['POST', 'GET'])
def send_email():
    search_query = request.form["content"]
    num_img = request.form["numImg"]
    time_stamp = request.form["Sheduletime"] # 2021-08-26T22:02 # <class 'str'>
    bs = BingScraper("chromedriver\chromedriver.exe", str(search_query), int(num_img))
    bs.check_links()
    # print(time_stamp) 
    # print(type(time_stamp))  
    return "downloading"

@app.route('/download_now', methods=['GET', 'POST'])
def download_now():
    if request.method == 'GET':
        search_query = request.args["content"] # getting the data from the form url
        num_img = request.args["numImg"]
        bs = BingScraper("chromedriver\chromedriver.exe", str(search_query), int(num_img))
        bs.check_links()
        return "Images are download successfully, Please check your Download Folder."
    elif request.method == 'POST':
        search_query = request.form["content"]
        num_img = request.form["numImg"]
        bs = BingScraper("chromedriver\chromedriver.exe", str(search_query), int(num_img))
        bs.check_links()
        return "Images are download successfully, Please check your Download Folder."

# http://127.0.0.1:5000/download_now?content=cat&numImg=5


if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True)

