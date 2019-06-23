//依赖layui js
//依赖表单处理模块
function ask_layer(btn, content, request_url) {
    layui.use('layer', function(){ //独立版的layer无需执行这一句
        var $ = layui.jquery, layer = layui.layer; //独立版的layer无需执行这一句
        layer.open({
            type: 1,
            title: false,
            closeBtn: false,
            area: '700px;',
            shade: 0.8,
            id: 'LAY_layuipro', //设定一个id，防止重复弹出
            btn: btn,
            btnAlign: 'c',
            moveType: 1, //拖拽模式，0或者1
            content: content,
            success: function(layero){
                var btn = layero.find('.layui-layer-btn');
                btn.find('.layui-layer-btn0').off().click(function () {
                    ajax_form_submit(request_url, 'get', send_data);
                })
            }
        })
    });
}


function send_data(data) {
    if (data.saved == 1){
        setTimeout("layer.msg(\"成功！\");",1000);
        location.reload();
    }
}