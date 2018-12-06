// pages/system/data/add/add.js
var app = getApp();
var md5 = require("../../../../utils/md5.js");

Page({

  /**
   * 页面的初始数据
   */
  data: {

  },

  addSubmit: function(e){
    var nickname = e.detail.value.nickname;
    if(nickname == ""){
      this.errorMsgBox("错误","昵称不能为空");
    }else{
      this.dataAdd(nickname);
    }
  },

  dataAdd: function(nickname){
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
          url: app.globalData.addUrl,
          method: "POST",
          dataType: "json",
          header: {
            "Content-Type": "application/x-www-form-urlencoded"
          },
          data: {
            'email': email,
            'secret': secret,
            'timestamp': tm,
            'nickname':nickname
          },
          success: function (res) {
            if (res.statusCode == 200) {
              if (res.data.code == 0) {
                that.backPage();
              } else {
                that.errorMsgBox("失败", res.data.msg);
              }
            } else {
              console.log(res);
            }

          },
          fail: function (err) {
            console.log(err);
          }
        })
      },
    })
  },

  // 错误时弹出对话框
  errorMsgBox: function (title, content) {
    wx.showModal({
      title: title,
      content: content,
    })
  },

  // 注册成功时吐司
  successToast: function (title, recall) {
    wx.showToast({
      title: title,
      icon: 'success',
      duration: 30000,
      mask: true,
      complete: function (res) {
        recall();
      }
    })
  },

  backPage: function () {
    wx.navigateBack({
      delta: 1
    })
  },


  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

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