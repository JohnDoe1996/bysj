// pages/system/data/data.js
var app = getApp();
var md5 = require("../../../utils/md5.js");

Page({

  /**
   * 页面的初始数据
   */
  data: {
    data:{}
  },

  // 点击每一项 跳转
  onClickList: function(e){
    console.log(e);
    var nickname = e.currentTarget.id;
    wx.navigateTo({
      url: './face/face?nickname='+nickname,
    })
  },

  // 跳转到添加数据
  gotoAdd: function(){
    wx.navigateTo({
      url: './add/add',
    })
  },

  //获取所有数据
  getAllDate: function(_id,email,tel){
    var that = this;
    var tm = Date.parse(new Date) / 1000;
    var secret = md5.md5(tm + _id + tel);
    wx.request({
      url: app.globalData.serverUrl + "/data/show",
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
      success: function (res) {
        if (res.statusCode == 200) {
          if (res.data.code == 0) {
            that.setData({
              data:res.data.data,
            });
          } else {
            console.log(res);
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

  // 点击删除按钮
  delPeople: function(e){
    console.log(e);
    var nickname = e.currentTarget.id;
    var that = this;
    wx.showModal({
      title: '提示',
      content: '确定要删除此数据吗？',
      success(res){
        if(res.confirm){
          wx.getStorage({
            key: 'userData',
            success: function (res) {
              var _id = res.data._id;
              var tel = res.data.tel;
              var email = res.data.email;
              var tm = Date.parse(new Date) / 1000;
              var secret = md5.md5(tm + _id + tel);
              that.DataDel(email, secret, tm, nickname, that.onLoad);
            },
          })
        }
      }
    })
    
  },

  // 删除请求
  DataDel: function(email,secret,tm,nickname,callvack){
    var that = this;
    wx.request({
      url: app.globalData.serverUrl + '/data/delete',
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
      success: function(res){
        if(res.statusCode == 200){
          if (res.data.code == 0){
            that.successToast("删除成功",that.onLoad);
          } else {
            that.errorMsgBox("错误", res.data.msg, null);
          }
        }else{
          that.errorMsgBox("错误", "未知错误", null);
          console.log(res);
        }
      },
      fail: function(err){
        that.errorMsgBox("错误","未知错误",function(){});
        console.log(err);
      }
    })
  },

  gotoTrian(){
    wx.showModal({
      title: '提示',
      content: '确定要训练数据吗？\n原数据会被覆盖！',
      success(res){
        if (res.confirm) {
          wx.redirectTo({
            url: './train/train',
          })
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
    var that = this;
    wx.getStorage({
      key: 'userData',
      success: function (res) {
        var _id = res.data._id;
        var tel = res.data.tel;
        var email = res.data.email;
        that.getAllDate(_id, email, tel);
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
    this.onLoad();
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
    this.onLoad();
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