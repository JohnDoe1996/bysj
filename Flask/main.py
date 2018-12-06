from flask import Flask, request
from id import Id
from ready import Ready
import json

app = Flask(__name__)

app.config['DEBUG'] = True


id = Id()
ready = Ready()


@app.route("/register", methods=['POST'])
def register():
    if request.method == "POST":
        email = request.form['email']
        tel = request.form['tel']
        pwd = request.form['pwd']
        res = id.register(email=email, tel=tel, pwd=pwd)
        print(json.dumps(res, ensure_ascii=False))
        return json.dumps(res, ensure_ascii=False)


@app.route("/password", methods=['POST'])
def password():
    if request.method == "POST":
        tel = request.form['tel']
        email = request.form['email']
        timestamp = request.form['timestamp']
        secret = request.form['secret']
        new_pwd = request.form['new_pwd']
        res = id.changePassword(tel=tel, email=email, timestamp=timestamp, secret=secret, new_pwd=new_pwd)
        return json.dumps(res, ensure_ascii=False)


@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        info = request.form['info']
        timestamp = request.form['timestamp']
        secret = request.form['secret']
        res = id.login(info=info, timestamp=timestamp, secret=secret)
        return json.dumps(res, ensure_ascii=False)


@app.route("/data/create", methods=["POST"])
def create():
    if request.method == "POST":
        secret = request.form['secret']
        timestamp = request.form['timestamp']
        email = request.form['email']
        nickname = request.form['nickname']
        res = ready.createPeople(secret=secret, timestamp=timestamp, email=email, nickname=nickname)
        return json.dumps(res, ensure_ascii=False)


@app.route("/data/delete", methods=["POST"])
def delete():
    if request.method == "POST":
        secret = request.form['secret']
        timestamp = request.form['timestamp']
        email = request.form['email']
        nickname = request.form['nickname']
        res = ready.deletePeople(secret=secret, timestamp=timestamp, email=email, nickname=nickname)
        return json.dumps(res, ensure_ascii=False)


@app.route("/data/upload_img/<img_id>", methods=['POST'])
def upload(img_id):
    if request.method == "POST":
        secret = request.form['secret']
        timestamp = request.form['timestamp']
        email = request.form['email']
        nickname = request.form['nickname']
        img_data = request.files.get("img_data")
        res = ready.makeImage(secret=secret, timestamp=timestamp,email=email,
                              img_data=img_data,nickname=nickname, img_id=img_id)
        return json.dumps(res, ensure_ascii=False)


@app.route("/data/delete_img/<img_id>", methods=["POST"])
def deleteImg(img_id):
    if request.method == "POST":
        secret = request.form['secret']
        timestamp = request.form['timestamp']
        email = request.form['email']
        nickname = request.form['nickname']
        res = ready.deleteImage(secret=secret, timestamp=timestamp, email=email,
                                nickname=nickname, img_id=img_id)
        return json.dumps(res, ensure_ascii=False)


@app.route("/data/show",methods=["POST"])
def show():
    if request.method == "POST":
        secret = request.form['secret']
        timestamp = request.form['timestamp']
        email = request.form['email']
        res = ready.showAllData(secret=secret, timestamp=timestamp, email=email)
        return json.dumps(res,ensure_ascii=False)


@app.route("/data/get_one",methods=["POST"])
def getOne():
    if request.method == "POST":
        secret = request.form['secret']
        timestamp = request.form['timestamp']
        email = request.form['email']
        nickname = request.form['nickname']
        res = ready.getOneData(secret=secret, timestamp=timestamp, email=email, nickname=nickname)
        return json.dumps(res,ensure_ascii=False)


@app.route("/ai/train",methods=["POST"])
def train():
    if request.method == "POST":
        secret = request.form['secret']
        timestamp = request.form['timestamp']
        email = request.form['email']
        res = ready.trainData(secret=secret, timestamp=timestamp, email=email)
        return json.dumps(res,ensure_ascii=False)

@app.route("/ai/refresh",methods=["POST"])
def aiRefresh():
    if request.method == "POST":
        secret = request.form['secret']
        timestamp = request.form['timestamp']
        email = request.form['email']
        res = ready.refreshDownloadCode(secret=secret, timestamp=timestamp, email=email)
        return json.dumps(res,ensure_ascii=False)


@app.route("/ai/delete",methods=["POST"])
def aiDelete():
    if request.method == "POST":
        secret = request.form['secret']
        timestamp = request.form['timestamp']
        email = request.form['email']
        res = ready.deleteModel(secret=secret, timestamp=timestamp, email=email)
        return json.dumps(res,ensure_ascii=False)


@app.route("/ai/download",methods=["GET","POST"])
def aiDownload():
    if request.method == "GET":
        tel = request.args['tel']
        secret = request.args['secret']
    elif request.method == "POST":
        tel = request.form['tel']
        secret = request.form['secret']
    res = ready.download(tel=tel, secret=secret)
    return json.dumps(res,ensure_ascii=False)






if __name__ == '__main__':
    app.run()
