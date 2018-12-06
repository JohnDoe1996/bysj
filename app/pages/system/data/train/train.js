// pages/system/data/train/train.js
var app = getApp();
var md5 = require("../../../../utils/md5.js");

Page({

  /**
   * 页面的初始数据
   */
  data: {
    ing: false,
    err: false,
    suc: false,
  },

  // 返回主页
  gotoTab(){
    wx.switchTab({
      url: '/pages/system/data/data',
    })
  },

  // 错误时弹出对话框
  errorMsgBox: function (title, content) {
    wx.showModal({
      title: title,
      content: content,
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this;
    var tm = Date.parse(new Date) / 1000;
    wx.getStorage({
      key: 'userData',
      success: function(res) {
        that.setData({
          ing: true,
          err: false,
          suc: false,
        });
        var _id = res.data._id;
        var tel = res.data.tel;
        var email = res.data.email;
        var secret = md5.md5(tm + _id + tel);
        wx.request({
          url: app.globalData.serverUrl + '/ai/train',
          method: "POST",
          dataType: "json",
          header: {
            "Content-Type": "application/x-www-form-urlencoded"
          },
          data: {
            'email': email,
            'secret': secret,
            'timestamp': tm,
          },
          success(res){
            if (res.statusCode == 200) {
              if (res.data.code == 0) {
                that.setData({
                  ing: false,
                  err: false,
                  suc: true,
                });
              } else {
                that.errorMsgBox("失败", res.data.msg);
                that.setData({
                  ing: false,
                  err: true,
                  suc: false,
                });
              }
            } else {
              console.log(res);
              that.setData({
                ing: false,
                err: true,
                suc: false,
              });
            }

          },
          fail(err){
            console.log(err);
            that.setData({
              ing: false,
              err: true,
              suc: false,
            });
          }
        })
      },
    })
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