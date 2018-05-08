/**
 * Created by Administrator on 2016/12/14 0014.
 */

    //load data input
$('#load_info').ace_file_input('update_settings', {
    style: 'well',
    btn_choose: '点击选择Excel',
    btn_change: null,
    no_icon: 'ace-icon fa fa-cloud-upload',
    allowExt: ["xls", "xlsx", "xlsm"],
    allowMime: [],
    droppable: false,
    thumbnail: 'small'
}).on('file.error.ace', function (event, info) {
    layer.open({icon: 7, title: '提示', content: "请上传excel格式文件"});
});