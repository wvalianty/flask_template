// 提交表单
//依赖layui
//处理表单函数，可以单独放到一个js文件中，然后引用。
//针对password字段做了特殊处理，使用sha1加密
//删除了repassword字段
function ajax_form_submit(url, method, send_data, data){
    var index = layer.load(1, {
      shade: [0.1,'green'],
      time: 2000
    });

    if (method == "get"){
         $.get(url).success(function(data){
             if (send_data){
                 send_data(data);
             }
        }).error(function(data) {
            layer.msg("表单提交失败！");
        });
    }

    if (method == "post"){
        if ("password" in data){
            data.password = CryptoJS.SHA1(data.password.toString()).toString(); //使用sha1加密
        }
        if ("repassword" in data) {
            delete data.repassword;
        }
        $.post(url, data).success(function(data){
            if (send_data){
                send_data(data);
            }
        }).error(function(data) {
            layer.msg("表单提交失败！");
        });
    }
}