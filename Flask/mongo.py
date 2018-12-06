import pymongo
import datetime
import time


class Mongo:

    URL = "127.0.0.1"
    PORT = 27017

    def __init__(self):
        self.mongo = pymongo.MongoClient(self.URL, self.PORT)
        self.db = self.mongo.tired

    def addUser(self,**user):
        user['create_datetime'] = datetime.datetime.now()
        res = self.db.user.insert_one(user)
        return res

    def findUserByTel(self, tel_str):
        user = self.db.user.find_one({"tel": tel_str})
        return user

    def findUserByEmail(self, email_str):
        user = self.db.user.find_one({"email": email_str})
        return user

    def updateUserPwd(self, new_pwd, **kwargs):
        email = kwargs['email']
        tel = kwargs['tel']
        res = self.db.user.update_one(
            {"email": email, "tel": tel},
            {
                "$set": {"pwd": new_pwd}
            }
        )
        return res.matched_count

    def addPeopleByTel(self, tel, nickname):
        res = self.db.people.insert_one({
            "tel": tel,
            "nickname": nickname,
            "state": ["没数据", "没数据", "没数据", "没数据"]
        })
        return res.inserted_id

    def deletePeopleByTel(self, tel, nickname):
        res = self.db.people.delete_many({
            'tel': tel,
            'nickname': nickname
        })
        return res.deleted_count

    def findPeople(self, tel, nickname):
        people = self.db.people.find_one({
            'tel': tel,
            'nickname': nickname
        })
        return people

    def findAllPeople(self, tel):
        peoples = self.db.people.find({'tel': tel})
        return peoples

    def updatePeopleState(self, tel, nickname, state_number, state):
        res = self.db.people.update_many(
            {
                'tel': tel,
                'nickname': nickname
            },
            {
                '$set':{
                    "state." + str(state_number): state
                }
            }
        )
        return res.modified_count

    def updateDownloadCode(self, tel, download_secret):
        update_time = int(time.time())
        res = self.db.user.update_one(
            {'tel': tel},
            {'$set': {
                'download_code': {
                    'secret': download_secret,
                    'update_time': update_time
                }
            }}
        )
        return res.matched_count

    def deleteDownloadCode(self, tel):
        res = self.db.user.update_one(
            {'tel': tel},
            {'$unset': {
                'download_code': ""
            }}
        )
        return res.matched_count