function batchExecution() {
    var checkout = table.checkStatus('demo')
    var caseId = []
    if (checkout.data.length == 0) {
        layer.msg('请选择用例')
        return false
    }
    for (var i = 0; i < checkout.data.length; i++) {
        if (checkout.data[i].status == 0) {
            layer.msg('包含已禁用的用例')
            return false
        }
        caseId.push(checkout.data[i].case_id)
    }
    console.log(caseId)
    $.post(hostUrl + '/batchExecution', {caseId: JSON.stringify(caseId)}, function (data) {
        var json_msg = JSON.parse(data).msg
        layer.msg(json_msg)

    })
}

function openAdd(i) {
    parent.layer.open({
        type: 2
        , title: '添加商品'
        , content: './static/caseupdate.html'
        , skin: 'layui-layer-lan'
        , area: ['1000px', '600px']
        , btnAlign: 'c'
        , maxmin: true
        , shadeClose: true
        , success: function (layero, index) {
            var body = parent.layer.getChildFrame('body', index);
            body.find('#casename').val(CaseName);
            body.find('#caseurl').val(url);
            postdata == '' ? body.find('#bodyText').val(request_body) : body.find('#bodyText').val(JSON.stringify(postdata));
            postheader == '' ? body.find('#headerText').val(request_header) : body.find('#headerText').val(JSON.stringify(postheader))
            $.post(hostUrl + '/queryForProduct', {}, function (data) {
                var _html, json_data;
                json_data = JSON.parse(data).data
                for (var i = 0; i < json_data.length; i++) {
                    _html += "<option value='" + json_data[i].id + "'>" + json_data[i].name + "</option>"
                }
                body.find('#pid-cp').append(_html);
            })
        }
        , end: function (data) {
            // window.location.reload()
        }
    })

}

