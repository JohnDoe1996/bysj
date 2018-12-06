//index.js
//获取应用实例
const app = getApp()
var timeout;
Page({
  data: {
    timer: 3
  },
  onLoad: function () {
    timeout = setInterval(this.timerSubtract, 1000);
  },

  // 倒计时器-1
  timerSubtract: function(){
    this.data.timer -= 1;
    var that = this;
    this.setData({
      timer: that.data.timer
    });
    if (this.data.timer <= 0){
      this.passAd();
    }
 
  },
	
	// 跳过广告
  passAd: function(){
    clearInterval(timeout);
    var that = this;
    // wx.getStorage({
    //   key: 'userData',
    //   success: function(res) {
    //     that.gotoSystem();
    //   },
    //   fail: function(err) {
    //     that.gotoLogin();
    //   }
    // })

    if (false){
      this.gotoLogin();
    }else{
      this.gotoSystem();
    }
  },

  // 跳转到系统页面
  gotoSystem: function(){
    wx.switchTab({
      url: '../system/data/data',
    });
  },
	
	// 跳转到登录页面
	gotoLogin: function() {
		wx.reLaunch({
      url: '../user/login/login',
    });
	}
})
