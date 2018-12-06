// pages/login/login.js
var app = getApp();
var md5 = require("../../../utils/md5.js");

Page({

  /**
   * 页面的初始数据
   */
  data: {

  },

  // 提交登录
  loginSubmit: function(e){
    // console.log(e);
    var id = e.detail.value.id;
    var pwd = e.detail.value.pwd;
    if (id == ""){
      this.errorMsgBox("错误","账号不能为空");
    } else if (pwd == ""){
      this.errorMsgBox("错误", "密码不能为空");
    }else{
      this.userLogin(id,pwd);
    }
  },

  // 账号登录
  userLogin: function(id,pwd){
    var that = this;
    var tm = Date.parse(new Date) / 1000;
    var secret = md5.md5(tm+pwd);
    wx.request({
      url: app.globalData.loginUrl,
      method: "POST",
      dataType: "json",
      header: {
        "Content-Type": "application/x-www-form-urlencoded" 
      },
      data: {
        'info': id,
        'secret': secret,
        'timestamp': tm
      },
      success: function(res){
        if (res.statusCode == 200){
          if (res.data.code == 0){
            wx.setStorage({
              key: 'userData',
              data: res.data.data,
            })
            wx.switchTab({
              url: '../../system/data/data',
            })
          }else{
            that.errorMsgBox("登录失败",res.data.msg);
          }
        }else{
          console.log(res);
        }
        
      },
      fail: function(err){
        console.log(err);
      }
    })
  },

  // 错误时弹出对话框
  errorMsgBox: function(title,content){
    wx.showModal({
      title: title,
      content: content,
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  // 跳转到注册页面
  gotoRegister: function () {
    wx.navigateTo({
      url: '../register/register',
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