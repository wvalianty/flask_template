//依赖于jquery
layui.use(['form','layer','jquery'], function () {
    // 操作对象
});

$(function () {
    //校验密码合规性
    $('#pwd').blur(function() {
            var reg = /^[\w]{6,12}$/;
            if(!($('#pwd').val().match(reg))){
                //layer.msg('请输入合法密码');
                $('#pwr').removeAttr('hidden');
                $('#pri').attr('hidden','hidden');
                layer.msg('请输入合法密码');
            }else {
                $('#pri').removeAttr('hidden');
                $('#pwr').attr('hidden','hidden');
            }
    });

    // 验证两次密码是否一致
    $('#rpwd').blur(function() {
            if($('#pwd').val() != $('#rpwd').val()){
                $('#rpwr').removeAttr('hidden');
                $('#rpri').attr('hidden','hidden');
                layer.msg('两次输入密码不一致!');
            }else {
                $('#rpri').removeAttr('hidden');
                $('#rpwr').attr('hidden','hidden');
            };
    });

});