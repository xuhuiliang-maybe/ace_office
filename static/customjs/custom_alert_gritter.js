/**
 * Created by xhl on 15-12-2.
 */
function self_gritter_alert(titleString, textString, imageString, stickyBool, class_nameString, maxInt) {
    $.gritter.add({
                      title: titleString,//弹出框标题
                      text: textString,//弹出框内容
                      image: imageString,//图片url
                      sticky: stickyBool,//是否手动关闭
                      time: '',//显示时间
                      class_name: class_nameString + (!$('#gritter-light').get(0).checked ? ' gritter-light' : ''),
                      before_open: function () {
                          if (maxInt > 0) {
                              if ($('.gritter-item-wrapper').length >= maxInt) {
                                  return false;
                              }
                          }
                      }
                  });
}

function self_gritter_remove() {
    $.gritter.removeAll();
    return false;
}