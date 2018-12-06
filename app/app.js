//app.js
var serverUrl = "http://127.0.0.1:5000";
var fileUrl = "http://127.0.0.1:8888";

App({
  globalData: {
    serverUrl: serverUrl,
    fileUrl: fileUrl,
    loginUrl: serverUrl + "/login",
    registerUrl: serverUrl + "/register",
    addUrl: serverUrl + "/data/create",
  }
})