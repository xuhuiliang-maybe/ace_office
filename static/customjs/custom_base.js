/**
 * Created by Administrator on 2016/3/20 0020.
 */

datepickerOptions = {
    language: 'zh-CN',
    format: "yyyy/mm/dd",
    autoclose: true,
    todayHighlight: true
};

datepickerOptionsMonth = {
    language: 'zh-CN',
    format: "yyyy/mm/dd",
    startView: 2,
    maxViewMode: 1,
    minViewMode: 1,
    changeMonth: true,
    changeYear: true,
    showButtonPanel: true,
    showMonthAfterYear: true,
    todayHighlight: true,
    autoclose: true
};

function select_dept(bindId, modelId) {
    get_all_dept(bindId, false);
    $(modelId).modal({backdrop: 'static', keyboard: false})
}


function address_modal(id_string, disable_area) {
    $("#myAddressModal").modal({backdrop: 'static', keyboard: false});
    $("#city_1").citySelect({prov: "北京", nodata: "none"});
    var target = document.getElementById('change_address');
    target.onclick = function () {
        var dist = "";
        var province = $('.prov option:selected').text();
        var city = $('.city option:selected').text();
        if (disable_area) {
            dist = $('.dist option:selected').text();
        }
        var address_str = province + city + dist;
        $('#' + id_string).val(address_str);
    };
}

function custom_ajax_post_new(url, param) {
    $.ajax({
               async: false,
               url: url,
               type: 'POST',
               dataType: 'JSON',
               data: param,

               success: function (data, textStatus) {
                   code = data.code;
                   var msg = data.msg;
                   layer.open({title: '提示', content: msg});
               },
               error: function (XMLHttpRequest, textStatus, errorThrown) {
                   console.log(XMLHttpRequest);
                   console.log(textStatus);
                   console.log(errorThrown);
                   layer.open({icon: 7, title: '提示', content: "异常"});
                   code = 0
               }
           });
    return code
}

function custom_ajax_post(url, param) {
    var load_index = layer.load(0, {shade: [0.1, '#fff']});
    var result = 0;
    $.ajax({
               async: false,
               url: url,
               type: 'POST',
               dataType: 'JSON',
               data: param,

               success: function (data, textStatus) {
                   var code = data.code;
                   var msg = data.msg;
                   layer.close(load_index);
                   layer.open({title: '提示', content: msg});
                   result = 1
               },
               error: function (XMLHttpRequest, textStatus, errorThrown) {
                   console.log(XMLHttpRequest);
                   console.log(textStatus);
                   console.log(errorThrown);
                   layer.close(load_index);
                   layer.open({icon: 7, title: '提示', content: "异常"});
                   result = 0
               }
           });
    return result
}

function batch_delete(url) {
    var ids = "";
    $("input[name='db_id']").each(function () {
        if ($(this).is(":checked")) {
            ids += $(this).val() + ",";
        }
    });
    if (!ids) {

        layer.confirm("确认删除全部数据?", {btn: ['确定', '取消']}, function (index) {
            var load_index = layer.load(0, {shade: [0.1, '#fff']});
            var result = custom_ajax_post(url, {"ids": "all"});
            if (result == 1) {
                window.location.reload();
            } else {
                layer.open({icon: 3, title: '提示', content: "异常"});
            }
        })
    } else {
        ids = ids.substring(0, ids.length - 1);
        var load_index = layer.load(0, {shade: [0.1, '#fff']});
        var result = custom_ajax_post(url, {"ids": ids});
        if (result == 1) {
            window.location.reload();
        } else {
            layer.open({icon: 3, title: '提示', content: "异常"});
        }
    }
}

function delHtmlTag(str) {
    return str.replace(/<[^>]+>/g, "");//去掉所有的html标记
}

function batch_oper(url, oper_type) {
    var ids = "";
    $("input[name='db_id']").each(function () {
        if ($(this).is(":checked")) {
            ids += $(this).val() + ",";
        }
    });
    if (!ids) {
        layer.open({icon: 3, title: '提示', content: "至少选择一条数据"});
    } else {
        var data = {};
        ids = ids.substring(0,ids.length-1);
        data["pk"] = ids;
        data["oper_type"] = "batch_oper";
        data["filed"] = oper_type;
        data["verify_value"] = '2';
        var result = custom_ajax_post(url, data);
        if (result == 1) {
            window.location.reload();
        }
    }
}

function window_href(url) {
    window.location.href = url
}

function submit_after(id_str) {
    $(id_str).modal('hide');
    var load_index = layer.load(0, {shade: [0.1, '#fff']});
}

