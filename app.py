from flask import Flask,jsonify,send_file,request
import requests
import re
from wordcloud import WordCloud,STOPWORDS
from tempfile import NamedTemporaryFile
from shutil import copyfileobj
from os import remove,getcwd,environ
import base64
import cStringIO
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)
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
    cloud = WordCloud(width=800,height=400,stopwords=STOPWORDS).generate(text).to_image()
    #tempFile = NamedTemporaryFile(mode='w+b',suffix='jpg')
    #copyfileobj(cloud,tempFileObj)
    buffer = cStringIO.StringIO()
    cloud.save(buffer,format = "PNG")
    #cloud.close()
    #tempFile.seek(0,0)
    return base64.b64encode(buffer.getvalue())

if __name__ == '__main__':
  port = int(environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port, debug=True)
