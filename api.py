__author__ = 'arian'
from flask import Flask,request
app = Flask(__name__,static_url_path='')
@app.route("/download_index")
def index():
    return app.send_static_file("index.html")



if __name__ == "__main__":
    app.run()