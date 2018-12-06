// pages/system/data/face/camera/camera.js
var app = getApp();
var md5 = require("../../../../../utils/md5.js");

Page({

  /**
   * 页面的初始数据
   */
  data: {
    showCamera: true,
  },

  // 拍照
  takePhoto: function (){
    var that = this;
    const ctx = wx.createCameraContext();
    ctx.takePhoto({
      quality: 'high',
      success: function(res){
        console.log(res);
        that.data.frame = res.tempImagePath;
        that.setData({
          frame: that.data.frame,
          showCamera: false
        })
      }
    });
  },

  // 重拍
  retakePhoto: function (){
    this.data.frame = "";
    this.setData({
      frame: "",
      showCamera: true
    });
  },

  // 点击上传
  upload: function(){
    var that = this;
    var tm = Date.parse(new Date) / 1000;
    wx.getStorage({
      key: 'userData',
      success: function(res) {
        var _id = res.data._id;
        var tel = res.data.tel;
        var email = res.data.email;
        var secret = md5.md5(tm + _id + tel);
        that.dataUpload(email,secret,tm);
      },
    })
  },

  // 上传照片到服务器
  dataUpload: function(email,secret,tm){
    var that = this;
    var nickname = this.data.nickname;
    wx.uploadFile({
      url: app.globalData.serverUrl + '/data/upload_img/' + that.data.img_id,
      dataType: "json",
      filePath: that.data.frame,
      name: 'img_data',
      formData:{
        'email': email,
        'secret': secret,
        'timestamp': tm,
        'nickname': nickname
      },
      success: function(res){
        var _res = JSON.parse(res.data);
        console.log(_res)
        if (res.statusCode == 200) {
          if (_res.code == 0) {
            that.backPage();
          } else {
            that.errorMsgBox("失败", _res.msg,that.retakePhoto);
          }
        } else {
          console.log(res);
        }
      },
      fail: function(err){
        console.log(err);
      }
    })
  },

  // 错误时弹出对话框
  errorMsgBox: function (title, content,callback) {
    var that = this;
    wx.showModal({
      title: title,
      content: content,
      success: function(){
        callback();
      }
    })
  },

  // 注册成功时吐司
  successToast: function (title, recall) {
    wx.showToast({
      title: title,
      icon: 'success',
      duration: 3000,
      mask: true,
      complete: function (res) {
        setTimeout(function () { }, 3000);
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
    var nickname = options.nickname;
    var imgId = parseInt(options.img_id);
    this.data.img_id = options.img_id;
    var tip = "";
    switch(imgId){
      case 0:
        tip = "张眼闭嘴图";
        break;
      case 1:
        tip = "闭眼闭嘴图";
        break;
      case 2:
        tip = "张眼张嘴图";
        break;
      case 3:
        tip = "闭眼张嘴图";
        break;
    }
    this.setData({
      nickname: nickname,
      tip: tip
    });
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