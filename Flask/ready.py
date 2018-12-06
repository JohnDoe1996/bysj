from mongo import Mongo
import time
import os
import shutil
import hashlib
import random
from face import Face
from ai import Ai


class Ready(Mongo):
    face = Face()
    ai = Ai()

    def checkUser(self, secret, email, timestamp):
        user = self.findUserByEmail(email)
        _id = str(user['_id'])
        tel = str(user['tel'])
        tm = int(time.time())
        # tm = 900
        if not 0 <= tm - int(timestamp) <= 300:  # 请求发起时间必须 在响应之前5分钟内
            result = {
                'code': 1,
                'msg': "超时",
                'data': {}
            }
            return False, result
        md5 = hashlib.md5()
        md5.update((str(timestamp) + _id + user['tel']).encode('utf-8'))
        if secret != md5.hexdigest():
            result = {
                'code': 1,
                'msg': "用户信息错误",
                'data': {}
            }
            return False, result
        return True, {
            'code': 0,
            'msg': "用户信息正确",
            'data': {'tel': tel}
        }

    def makeImage(self, secret, email, timestamp, img_id, nickname, img_data):
        if not 0 <= int(img_id) <= 3:
            result = {
                'code': 1,
                'msg': "参数错误",
                'data': {'img_id': img_id}
            }
            return result
        success, ret = self.checkUser(secret, email, timestamp)
        if not success:
            result = ret
            return result
        else:
            tel = ret['data']['tel']
        img_dir = "./data/" + tel + "/" + nickname
        suc, img = self.face.cutFace(Face.byte2Img(img_data))
        if suc < 0:
            result = {
                'code': 1,
                'msg': "图片不包含人脸数据",
                'data': {}
            }
            return result
        elif suc > 0:
            result = {
                'code': 1,
                'msg': "图片包含多个人脸数据",
                'data': {}
            }
            return result
        else:
            Face.saveImg(img, img_dir + "/" + img_id + ".jpg")
        self.updatePeopleState(tel, nickname, img_id, "已通过")
        result = {
            'code': 0,
            'msg': "图片保存成功",
            'data': {'img_dir': img_dir + "/" + img_id + ".jpg"}
        }
        return result

    def deleteImage(self, secret, email, timestamp, nickname, img_id):
        if not 0 <= int(img_id) <= 3:
            result = {
                'code': 1,
                'msg': "参数错误",
                'data': {'img_id': img_id}
            }
            return result
        success, ret = self.checkUser(secret, email, timestamp)
        if not success:
            result = ret
            return result
        else:
            tel = ret['data']['tel']
        img_file = "./data/" + tel + "/" + nickname + "/" + img_id + ".jpg"
        if not os.path.exists(img_file):
            result = {
                'code': 1,
                'msg': "文件不存在",
                'data': {'img_id': img_id}
            }
            return result
        else:
            os.remove(img_file)
            self.updatePeopleState(tel, nickname, img_id, "没数据")
            result = {
                'code': 0,
                'msg': "删除成功",
                'data': {'img_id': img_id}
            }
            return result

    def createPeople(self, secret, timestamp, email, nickname):
        success, ret = self.checkUser(secret, email, timestamp)
        if not success:
            result = ret
            return result
        else:
            tel = ret['data']['tel']
        people = self.findPeople(tel, nickname)
        if people is not None:
            result = {
                'code': 1,
                'msg': "数据已存在",
                'data': {}
            }
            return result
        user_dir = "./data/" + tel
        people_dir = user_dir + "/" + nickname
        if not os.path.exists(user_dir):
            os.mkdir(user_dir)
        if not os.path.exists(people_dir):
            os.mkdir(people_dir)
        ret = self.addPeopleByTel(tel, nickname)
        result = {
            'code': 0,
            'msg': "数据创建成功",
            'data': {"people_id": str(ret)}
        }
        return result

    def deletePeople(self, secret, timestamp, email, nickname):
        success, ret = self.checkUser(secret, email, timestamp)
        if not success:
            result = ret
            return result
        else:
            tel = ret['data']['tel']
        people = self.findPeople(tel, nickname)
        if people is None:
            result = {
                'code': 1,
                'msg': "数据不存在",
                'data': {}
            }
            return result
        user_dir = "./data/" + tel
        people_dir = user_dir + "/" + nickname
        if os.path.exists(people_dir):
            shutil.rmtree(people_dir)
        ret = self.deletePeopleByTel(tel, nickname)
        if ret == 0:
            result = {
                'code': 1,
                'msg': "数据删除失败",
                'data': {}
            }
            return result
        else:
            result = {
                'code': 0,
                'msg': "数据删除成功",
                'data': {}
            }
            return result

    def showAllData(self, secret, timestamp, email):
        success, ret = self.checkUser(secret, email, timestamp)
        if not success:
            result = ret
            return result
        else:
            tel = ret['data']['tel']
        peoples = self.findAllPeople(tel)
        data = []
        if peoples is None:
            result = {
                'code': 1,
                'msg': "数据不存在",
                'data': {}
            }
            return result
        count = 0
        for people in peoples:
            data.append({
                'nickname': people['nickname'],
                'state': people['state']
            })
            count += 1
        result = {
            'code': 0,
            'msg': "获取数据成功",
            'data': {
                'count': count,
                'dataList': data
            }
        }
        return result

    def getOneData(self, secret, timestamp, email, nickname):
        success, ret = self.checkUser(secret, email, timestamp)
        if not success:
            result = ret
            return result
        else:
            tel = ret['data']['tel']
        people = self.findPeople(tel, nickname)
        if people is None:
            result = {
                'code': 1,
                'msg': "数据不存在",
                'data': {}
            }
            return result
        else:
            img_data = []
            for i in range(len(people['state'])):
                if people['state'][i] == "已通过":
                    img_data.append({
                        'uri': "/data/" + tel + "/" + nickname + "/" + str(i) + ".jpg",
                        'state': people['state'][i]
                    })
                else:
                    img_data.append({
                        'uri': "/data/void.jpg",
                        'state': people['state'][i]
                    })
            result = {
                'code': 0,
                'msg': "获取数据成功",
                'data': {
                    'nickname': people['nickname'],
                    'img': img_data
                }
            }
            return result

    def trainData(self, secret, timestamp, email):
        success, ret = self.checkUser(secret, email, timestamp)
        if not success:
            result = ret
            return result
        else:
            tel = ret['data']['tel']
        peoples = self.findAllPeople(tel)
        nickNameList = []
        failList = []
        for people in peoples:
            nickNameList.append(people['nickname'])
            if people['state'][0] != "已通过" or \
                    people['state'][1] != "已通过" or \
                    people['state'][2] != "已通过" or \
                    people['state'][3] != "已通过":
                failList.append(people['nickname'])
        if len(failList) != 0:
            result = {
                'code': 1,
                'msg': "数据不是全部已通过不能训练",
                'data': {
                    'nickname': failList,
                }
            }
            return result
        dataPath = self.ai.train(tel, nickNameList)
        if dataPath == "":
            result = {
                'code': 1,
                'msg': "数据训练出错",
                'data': {}
            }
            return result
        else:
            secretCode = str(random.randint(0, 9)) \
                         + str(random.randint(0, 9)) \
                         + str(random.randint(0, 9)) \
                         + str(random.randint(0, 9)) \
                         + str(random.randint(0, 9)) \
                         + str(random.randint(0, 9))
            if self.updateDownloadCode(tel,secretCode) == 0:
                result = {
                    'code': 1,
                    'msg': "数据存储出错",
                    'data': {}
                }
                return result
            else:
                result = {
                    'code': 0,
                    'msg': "成功",
                    'data':{
                        "download_code": tel,
                        "secret_code": secretCode
                    }
                }
                return result

    def refreshDownloadCode(self, secret, timestamp, email):
        success, ret = self.checkUser(secret, email, timestamp)
        if not success:
            result = ret
            return result
        else:
            tel = ret['data']['tel']
        user = self.findUserByTel(tel)
        if user is None:
            result = {
                'code': 1,
                'msg': "用户不存在",
                'data': {}
            }
            return result
        if 'download_code' not in user or user['download_code'] == "":
            result = {
                'code': 1,
                'msg': "数据不存在",
                'data': {}
            }
            return result
        secretCode = str(random.randint(0, 9)) \
                     + str(random.randint(0, 9)) \
                     + str(random.randint(0, 9)) \
                     + str(random.randint(0, 9)) \
                     + str(random.randint(0, 9)) \
                     + str(random.randint(0, 9))
        if self.updateDownloadCode(tel, secretCode) == 0:
            result = {
                'code': 1,
                'msg': "数据更新时出错",
                'data': {}
            }
            return result
        else:
            result = {
                'code': 0,
                'msg': "成功",
                'data': {
                    "download_code": tel,
                    "secret_code": secretCode
                }
            }
            return result

    def deleteModel(self, secret, timestamp, email):
        success, ret = self.checkUser(secret, email, timestamp)
        if not success:
            result = ret
            return result
        else:
            tel = ret['data']['tel']
        ret = self.ai.deleteData(tel)
        if ret < 0 :
            result = {
                'code': 1,
                'msg': "数据库位置错误",
                'data': {}
            }
            return result
        elif ret > 0:
            result = {
                'code': 1,
                'msg': "模型数据不存在",
                'data': {}
            }
            return result
        else:
            if self.deleteDownloadCode(tel) == 0:
                result = {
                    'code': 1,
                    'msg': "数据删除时出错",
                    'data': {}
                }
                return result
            else:
                result = {
                    'code': 0,
                    'msg': "数据删除成功 ",
                    'data': {}
                }
                return result

    def download(self, tel, secret):
        user = self.findUserByTel(tel)
        if user is None:
            result = {
                'code': 1,
                'msg': "用户不存在",
                'data': {}
            }
            return result
        if 'download_code' not in user or user['download_code'] == "":
            result = {
                'code': 1,
                'msg': "数据不存在",
                'data': {}
            }
            return result
        if user['download_code']['secret'] != secret:
            result = {
                'code': 1,
                'msg': "秘钥不正确",
                'data': {}
            }
            return result
        now =  int(time.time())
        if 0 > now - user['download_code']['update_time'] > 15000:
            result = {
                'code': 1,
                'msg': "秘钥已超时失效",
                'data': {}
            }
            return result
        suc, data = self.ai.getModelData(tel)
        if suc > 0:
            result = {
                'code': 1,
                'msg': "文件不存在",
                'data': data
            }
        elif suc <0:
            result = {
                'code': -1,
                'msg': "未知错误",
                'data': data
            }
        else:
            result = {
                'code': 0,
                'msg': "成功",
                'data': data
            }
        return result




