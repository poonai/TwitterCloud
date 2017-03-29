from flask import Flask,jsonify,send_file,request
import requests
import re
from wordcloud import WordCloud
from tempfile import NamedTemporaryFile
from shutil import copyfileobj
from os import remove,getcwd
app = Flask(__name__)
print getcwd()
@app.route('/')
def index():
    r = requests.get("http://loklak.org/api/search.json?q={0}&count=100".format(request.args.get('q')))
    data = r.json()
    text = " "
    for value in data["statuses"]:
        value = re.sub(r"@"," ",value["text"])
        value = re.sub(r"\#"," ",value)
        value = re.sub(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"," ",value)
        text+=value
    cloud = WordCloud(width=800,height=400).generate(text).to_image()
    #tempFile = NamedTemporaryFile(mode='w+b',suffix='jpg')
    #copyfileobj(cloud,tempFileObj)
    cloud.save(getcwd()+'/demo.png')
    #cloud.close()
    #tempFile.seek(0,0)
    return send_file(getcwd()+'/demo.png',mimetype='image/png')

app.run()
