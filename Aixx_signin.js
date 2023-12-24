var request = require('request');
var options = {
   'method': 'POST',
   'url': 'https://www.aixx.ai/ajax/signin',
   'headers': {
      'Host': 'www.aixx.ai',
      'Connection': 'keep-alive',
      'sec-ch-ua': '"Brave";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
      'DNT': '1',
      'X-CSRF-Token': 'A8ZkgUDpm91uXyHLu2lku7iF3Mp2tf_abRij4_3z8EJtgyDSBr_WrDYtUa3yPjD33c6oojfC0p5eR5q2pYOHAQ==',
      'sec-ch-ua-mobile': '?0',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
      'Accept': '*/*',
      'X-Requested-With': 'XMLHttpRequest',
      'sec-ch-ua-platform': '"Windows"',
      'Sec-GPC': '1',
      'Origin': 'https://www.aixx.ai',
      'Sec-Fetch-Site': 'same-origin',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Dest': 'empty',
      'Referer': 'https://www.aixx.ai/site/invite',
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
      'Cookie': '__user_identity=013c9b66a804729f82ff94dc0e559c10ad08026bdedabbfafebb42b5b43d0640a%3A2%3A%7Bi%3A0%3Bs%3A15%3A%22__user_identity%22%3Bi%3A1%3Bs%3A50%3A%22%5B19273%2C%226QRm3JAl8Fo8oUDywzmVJ7W88YpgkUDT%22%2C7776000%5D%22%3B%7D; PHPSESSID=st24e02onp4ded0ordqoj02981; _csrf=6b682acc07cf1ab146764eea7e66f3bc02d0a968d2344b9069287889a0a74da7a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22nEDSFVMqXrpfIWTLeKthAw-D3_9UXpwC%22%3B%7D',
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
   },
   form: {

   }
};
request(options, function (error, response) {
   if (error) throw new Error(error);
   console.log(response.body);
});