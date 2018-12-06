from mongo import Mongo
import time
import hashlib


class Id(Mongo):
    def register(self, tel, email, pwd):
        cursor = self.findUserByTel(tel)
        if cursor is not None:
            result = {
                'code': 1,
                'msg': "手机号码已存在",
                'data': {}
            }
            return result
        cursor = self.findUserByEmail(email)
        if cursor is not None:
            result = {
                'code': 1,
                'msg': "邮箱已存在",
                'data': {}
            }
            return result
        res = self.addUser(tel=tel, email=email, pwd=pwd)
        print(res)
        result = {
            'code': 0,
            'msg': "注册成功",
            'data': {'_id': str(res.inserted_id)}
        }
        return result

    def changePassword(self,  tel, email, timestamp, secret, new_pwd):
        tm = int(time.time())
        if not 0 <= tm - int(timestamp) <= 300:  # 请求发起时间必须 在响应之前5分钟内
            result = {
                'code': 1,
                'msg': "超时",
                'data': {}
            }
            return result
        user = self.findUserByTel(tel)
        if user is None:
            result = {
                'code': 1,
                'msg': "手机号码不正确",
                'data': {}
            }
            return result
        if user['email'] != email:
            result = {
                'code': 1,
                'msg': "邮箱不正确",
                'data': {}
            }
            return result
        _md5 = hashlib.md5()
        _md5.update((str(timestamp)+str(user['pwd'])).encode("utf8"))
        if _md5.hexdigest() != secret:
            result = {
                'code': 1,
                'msg': "原始密码不正确",
                'data': {}
            }
            return result
        if user['pwd'] == new_pwd:
            result = {
                'code': 1,
                'msg': "新密码不能和原始密码一致",
                'data': {}
            }
            return result
        matched_count = self.updateUserPwd(new_pwd, tel=tel, email=email)
        if matched_count == 0:
            result = {
                'code': 1,
                'msg': "未知错误",
                'data': {}
            }
            return result
        result = {
            'code': 0,
            'msg': "密码修改成功",
            'data': {}
        }
        return result

    def login(self, info, timestamp, secret):
        index = info.find("@")
        if index == -1:
            user = self.findUserByTel(info)
        else:
            user = self.findUserByEmail(info)
        if user is None:
            result = {
                'code': 1,
                'msg': "账号不存在",
                'data': {}
            }
            return result
        tm = int(time.time())
        # tm=900
        if not 0 <= tm - int(timestamp) <= 300:  # 请求发起时间必须 在响应之前5分钟内
            result = {
                'code': 1,
                'msg': "超时",
                'data': {}
            }
            return result
        _md5 = hashlib.md5()
        _md5.update((str(timestamp)+str(user['pwd'])).encode("utf8"))
        if _md5.hexdigest() != secret:
            result = {
                'code': 1,
                'msg': "密码不正确",
                'data': {}
            }
            return result
        result = {
            'code': 0,
            'msg': "登录成功",
            'data': {
                '_id': str(user['_id']),
                'email': user['email'],
                'tel': user['tel']
            }
        }
        return result








