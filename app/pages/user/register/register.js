// pages/user/register/register.js
var app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {

  },

  // 点击提交
  registerSubmit: function (e) {
    // console.log(e);
    var tel = e.detail.value.tel;
    var email = e.detail.value.email;
    var pwd1 = e.detail.value.pwd1;
    var pwd2 = e.detail.value.pwd2;
    if (
      this.checkTel(tel) &&
      this.checkEmail(email) &&
      this.checkPwd(pwd1,pwd2) 
    ){
      this.userRegister(tel,email,pwd1);
    }
  },

  // 注册
  userRegister: function (tel, email, pwd) {
    var that = this;
    wx.request({
      url: app.globalData.registerUrl,
      method: "POST",
      dataType: "json",
      header: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      data: {
        'email': email,
        'tel': tel,
        'pwd': pwd
      },
      success: function (res) {
        if (res.statusCode == 200) {
          if (res.data.code == 0) {
            that.successToast("注册成功",that.backtoLogin);
          } else {
            that.errorMsgBox("注册失败", res.data.msg);
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

  // 校验手机号
  checkTel: function (tel) {
    var result = false;
    var re = /^1[34578]\d{9}$/;
    if (tel == "") {
      this.errorMsgBox("错误", "手机号码不能为空");
    } else if (!re.test(tel)) {
      this.errorMsgBox("错误", "手机号码格式有误");
    } else {
      result = true;
    }
    return result;
  },

  // 校验邮箱
  checkEmail: function (email) {
    var result = false;
    var emailSplited = email.split("@");
    if (email == "") {
      this.errorMsgBox("错误", "邮箱不能为空");
    } else if (
        emailSplited.length != 2 ||
        emailSplited[0].length == 0 ||
        emailSplited[1].length == 0 
      ) {
      this.errorMsgBox("错误", "邮箱格式有误");
    } else {
      result = true;
    }
    return result;
  },

  // 校验密码
  checkPwd: function (pwd1,pwd2) {
    var result = false;
    if (pwd1 == "") {
      this.errorMsgBox("错误", "密码不能为空");
    } else if (pwd1.length < 6 || pwd1.length >13){
      this.errorMsgBox("错误", "密码必须6~13位字母或者数字组成");
    } else if (pwd2 == "") {
      this.errorMsgBox("错误", "确认密码不能为空");
    } else if (pwd1 != pwd2){
      this.errorMsgBox("错误", "确认密码与密码不一致");
    } else {
      result = true;
    }
    return result;
  },

  // 错误时弹出对话框
  errorMsgBox: function (title, content) {
    wx.showModal({
      title: title,
      content: content,
    })
  },

  // 注册成功时吐司
  successToast: function (title, recall){
    wx.showToast({
      title: title,
      icon: 'success',
      duration: 3000,
      mask: true,
      complete: function(res){
        setTimeout(function () { }, 3000);
        recall();
      }
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  backtoLogin: function(){
    wx.navigateBack({
      delta: 1
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