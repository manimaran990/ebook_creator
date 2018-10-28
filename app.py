#!/usr/bin/python3
import os, json, bson
import collections
from flask import Flask, render_template, request, redirect, url_for,send_from_directory
from werkzeug.utils import secure_filename
from flask_pymongo import PyMongo
import convert_utils

UPLOAD_FOLDER = 'files/'
#allowed extension to upload
ALLOWED_EXTENSIONS = set(['odt', 'jpg','jpeg','png'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MONGO_URI'] = "mongodb://m4n1g:DragonBall9@ds249092.mlab.com:49092/blog_db"
mongo = PyMongo(app)


@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")
    
@app.route("/new", methods=['GET'])
def newbook():
    return render_template("home.html")
    

@app.route("/new", methods=['POST','GET'])
def getdetails():
    
    #to updload cover and content files to server
    cover = request.files['cover_image']
    content = request.files['content']
    cover.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(cover.filename)))
    content.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(content.filename)))
    
    #get form data and convert to dictionary
    d = request.form.to_dict()
    d['cover_image'] = secure_filename(cover.filename)
    d['content'] = secure_filename(content.filename)
    record = mongo.db.books.insert(d)
    
    #create ordered dictionary
    od = collections.OrderedDict(sorted(d.items()))
        
    return render_template("create.html", datadict=od)
    
    
@app.route("/create/<format>/<id>", methods=['POST'])
def command(format=None,id=None):
    data = mongo.db.books.find_one({"_id":bson.ObjectId(oid=str(id))})
    
    cover = data['cover_image']
    cover_file = os.path.join(app.config['UPLOAD_FOLDER'],cover)
    
    content = data['content']
    content_file = os.path.join(app.config['UPLOAD_FOLDER'], content)
    
    print("app.rootpath :" +app.root_path)
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    print(uploads)
    
    epubconv = convert_utils.converter(data['eng_title'],data['book_title'], data['author'],content_file,cover_file)
    
    if format == 'epub':
        print("came to epub post")
        
        epubconv.convert_to_epub()
        
        print(data['eng_title']+".epub")
        return send_from_directory(directory=uploads, filename=data['eng_title']+".epub", as_attachment=True)
        
    elif format == 'mobi':
        epubconv.convert_to_mobi()
        print(data['eng_title']+".mobi")
        return send_from_directory(directory=uploads, filename=data['eng_title']+".mobi", as_attachment=True)


if __name__ == '__main__':
    app.run(port='5002')
    
    
