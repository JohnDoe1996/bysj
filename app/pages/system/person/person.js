// pages/control/person/person.js
var app = getApp();
var md5 = require("../../../utils/md5.js");

Page({

  /**
   * 页面的初始数据
   */
  data: {
    msgShow: false
  },

  // 展开数据
  open(){
    if (this.data.msgShow){
      this.setData({
        msgShow: false
      })
    } else {
      this.postRefresh()
    }
  },

  // 刷新秘钥
  refresh(){
    var that = this
    wx.showModal({
      title: '提示',
      content: '刷新后原秘钥会失效，确定要刷新吗？',
      success(res) {
        if (res.confirm) {
          that.postRefresh()
        }
      }
    })
  },

  // 提交刷新请求
  postRefresh(){
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
          url: app.globalData.serverUrl + '/ai/refresh',
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
                  download_code: res.data.data.download_code,
                  secret_code: res.data.data.secret_code,
                  msgShow: true
                });
              } else {
                that.errorMsgBox("失败", res.data.msg);
              }
            } else {
              console.log(res);
            }
          },
          fail(err){
            console.log(err);
          }
        })
      },
    })
  },

  // 删除数据
  deleteData(){
    var that = this
    wx.showModal({
      title: '提示',
      content: '此操作不可逆，继续？',
      success(res) {
        if (res.confirm) {
          that.postDelete()
        }
      }
    })
  },

  // 提交删除数据
  postDelete(){
    var that = this;
    var tm = Date.parse(new Date) / 1000;
    wx.getStorage({
      key: 'userData',
      success: function (res) {
        var _id = res.data._id;
        var tel = res.data.tel;
        var email = res.data.email;
        var secret = md5.md5(tm + _id + tel);
        wx.request({
          url: app.globalData.serverUrl + '/ai/delete',
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
          success(res) {
            if (res.statusCode == 200) {
              if (res.data.code == 0) {
                that.setData({
                  download_code: "",
                  secret_code: "",
                  msgShow: false
                });
                wx.showToast({
                  title: '数据删除成功',
                })
              } else {
                that.errorMsgBox("失败", res.data.msg);
              }
            } else {
              console.log(res);
            }
          },
          fail(err) {
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

  // 跳转到修改密码页面
  gotoChangePwd: function (){
    wx.navigateTo({
      url: '../../user/change/change',
    })
  },

  // 跳转到注销登录
  logout: function () {
    wx.showModal({
      title: '提示',
      content: '确定要注销账号登录吗？',
      success(res){
        if(res.confirm){
          wx.removeStorage({
            key: 'userData',
            success: function (res) {
              wx.redirectTo({
                url: '../../user/login/login',
              })
            },
          })
        }
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
      success: function(res) {
        // console.log(res);
        that.setData({
          user: res.data
        });
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