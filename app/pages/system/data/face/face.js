// pages/system/data/face/face.js
var app = getApp();
var md5 = require("../../../../utils/md5.js");

Page({

  /**
   * 页面的初始数据
   */
  data: {
    img:[],
    state:[],
    uri: app.globalData.fileUrl
  },

  // 加载数据
  loadFaceData: function(){
    this.setData({
      random: Math.random()/9999
    });
    var nickname = this.data.nickname;
    var that = this;
    var tm = Date.parse(new Date) / 1000;
    wx.getStorage({
      key: 'userData',
      success: function(res) {
        var _id = res.data._id;
        var tel = res.data.tel;
        var email = res.data.email;
        var secret = md5.md5(tm + _id + tel);
        wx.request({
          url: app.globalData.serverUrl + '/data/get_one',
          method: "POST",
          dataType: "json",
          header: {
            "Content-Type": "application/x-www-form-urlencoded"
          },
          data: {
            'email': email,
            'secret': secret,
            'timestamp': tm,
            'nickname': nickname
          },
          success:function(res){
            console.log(res)
            if (res.statusCode == 200) {
              if (res.statusCode == 200) {
                if (res.data.code == 0) {
                  that.setData({
                    img: res.data.data.img,
                  });
                } else {
                  console.log(res.data.msg);
                }
              } else {
                console.log(res);
              }
            }
          },
          fail:function(err){
            console.log(err);
          }
        })
      },
    })
  },

  //跳转到相机页面
  gotoCamera: function(e){
    var nickname = this.data.nickname;
    var imgId = e.currentTarget.id;
    wx.navigateTo({
      url: './camera/camera?nickname=' + nickname + "&img_id=" + imgId,
    })
  },

  // 点击删除按钮
  delFace: function(e){
    var nickname = this.data.nickname;
    var imgId = e.currentTarget.id;
    var that = this;
    var tm = Date.parse(new Date) / 1000;
    wx.showModal({
      title: '提示',
      content: '确定要删除此人脸数据？',
      success(res){
        if(res.confirm){
          wx.getStorage({
            key: 'userData',
            success: function (res) {
              var _id = res.data._id;
              var tel = res.data.tel;
              var email = res.data.email;
              var secret = md5.md5(tm + _id + tel);
              wx.request({
                url: app.globalData.serverUrl + '/data/delete_img/' + imgId,
                method: "POST",
                dataType: "json",
                header: {
                  "Content-Type": "application/x-www-form-urlencoded"
                },
                data: {
                  'email': email,
                  'secret': secret,
                  'timestamp': tm,
                  'nickname': nickname
                },
                success(res){
                  console.log(res)
                  if (res.statusCode == 200) {
                    if (res.statusCode == 200) {
                      if (res.data.code == 0) {
                        that.setData({
                          img:[]
                        });
                        that.successToast("删除成功", that.loadFaceData);
                      } else {
                        that.errorMsgBox("错误",res.data.msg,function(){});
                        console.log(res.data.msg);
                      }
                    } else {
                      that.errorMsgBox("错误", "未知错误", function () { });
                      console.log(res);
                    }
                  }
                },
                fail(err){
                  that.errorMsgBox("错误", "未知错误", function () { });
                  console.log(err);
                }
              })
            }
          });
        }
      }
    })
  },

  // 错误时弹出对话框
  errorMsgBox: function (title, content, callback) {
    var that = this;
    wx.showModal({
      title: title,
      content: content,
      success: function () {
        callback();
      }
    })
  },

  // 注册成功时吐司
  successToast: function (title, callback) {
    wx.showToast({
      title: title,
      icon: 'success',
      duration: 3000,
      mask: true,
      complete: function (res) {
        setTimeout(function () { }, 3000);
        callback();
      }
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // console.log(options);
    var nickname = options.nickname;
    // this.data.nickname = nickname;
    this.setData({
      nickname:nickname
    });
    this.loadFaceData();
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    this.loadFaceData();
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

    this.loadFaceData();
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})