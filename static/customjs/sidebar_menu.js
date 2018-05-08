/**
 * Created by admin on 2016/1/28.
 * http://www.jb51.net/article/77263.htm
 */
(function ($) {
    $.fn.sidebarMenu = function (options) {
        options = $.extend({}, $.fn.sidebarMenu.defaults, options || {});
        var target = $(this);
        target.addClass('nav');
        target.addClass('nav-list');
        if (options.data) {
            var TARGET = init(target, options.data);
            add_class(TARGET)
        } else {
            if (!options.url) return;
            $.getJSON(options.url, null, function (data) {
                var TARGET = init(target, data.data);
                add_class(TARGET)
            });
        }

        function add_class(TARGET){
                var url = window.location.pathname;
                var host = window.location.host;
                var referrer = document.referrer;
                var referrer_url = referrer.split(host);
                var menu = TARGET.find("[href='" + url + "']");
                if (menu.length == 0 && referrer){
                    menu = TARGET.find("[href='" + referrer_url[1] + "']");
                }
                menu.parent().addClass('active');
                menu.parent().parentsUntil('.nav-list', 'li').addClass('active').addClass('open');
        }

        function init(target, data) {
            $.each(data, function (i, item) {
                var li = $('<li></li>');
                var a = $('<a></a>');
                var icon = $('<i></i>');
                //icon.addClass('glyphicon');
                icon.addClass(item.icon);
                var text = $('<span></span>');
                text.addClass('menu-text').text(item.text);
                a.append(icon);
                a.append(text);
                if (item.menus && item.menus.length > 0 && item.show) {
                    a.attr('href', '#');
                    a.addClass('dropdown-toggle');
                    var arrow = $('<b></b>');
                    arrow.addClass('arrow').addClass('fa').addClass('fa-angle-down');
                    a.append(arrow);
                    li.append(a);
                    var menus = $('<ul></ul>');
                    menus.addClass('submenu');
                    init(menus, item.menus);
                    li.append(menus);
                } else {
                    //var href = 'javascript:addTabs({id:\'' + item.id + '\',title: \'' + item.text + '\',close: true,url: \'' + item.url + '\'});';
                    //a.attr('href', href);
                    if (item.istab) {
                        a.attr('href', href);
                    } else {
                        a.attr('href', item.url);
                        a.attr('title', item.text);
                        //a.attr('target', '_blank')
                    }
                    li.append(a);
                }
                if (item.show) {
                    target.append(li);
                }
            });
            return target
        }
    };

    $.fn.sidebarMenu.defaults = {
        url: null,
        param: null,
        data: null
    };
})(jQuery);

