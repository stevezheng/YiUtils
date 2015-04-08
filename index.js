module.exports = {
  is: {
    QQ: function (qq) {
      var qqReg = /^[1-9]{1}[0-9]{4,10}$/;
      if (RegExp(qqReg).test(qq)) {
        return true;
      } else {
        return false;
      }
    },

    email: function (email) {
      var emailReg = /^([a-zA-Z0-9]+[_|\-|\.]?)*[a-zA-Z0-9]+@(vip.qq|qq|163|126)\.com/;
      if (RegExp(emailReg).test(email)) {
        return true;
      } else {
        return false;
      }
    },

    phone: function (phone) {
      var phoneReg = /^0{0,1}(13[0-9]|14[6|7]|15[0-3]|15[5-9]|18[0-9]|17[0-9])[0-9]{8}$/;
      if (RegExp(phoneReg).test(phone)) {
        return true;
      } else {
        return false;
      }
    }
  }
};
