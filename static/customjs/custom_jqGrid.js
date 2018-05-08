/**
 * Created by xhl on 15-12-2.
 */

function ad_jqgrid(captionString, colNamesList, colModelListDict, queryurlString, editurlString, multiselectBool, navGridBool) {
    //数据填充地址
    var grid_selector = "#grid-table";
    var pager_selector = "#grid-pager";

    //网格选择器，［数据类型，高度，列标题头，列属性，常规属性］
    jQuery(grid_selector).jqGrid({
        rownumbers: true, /* 序号 */
        pager: pager_selector, /* 	定义分页浏览导航条，必须是一个有效的html元素，位置可以随意*/

        /* array[], 列名称数组。该名称将在Header中显示。名称以逗号分隔，数量应与colModel 数组数量相等*/
        colNames: colNamesList,

        /* 	array,常用到的属性：name 列显示的名称；index 传到服务器端用来排序用的列名称；width 列宽度；align 对齐方式['left', 'center', 'right']；sortable 是否可以排序*/
        colModel: colModelListDict,

        editurl: editurlString, /*string, 定义行内编辑地址URL*/
        url: queryurlString, /*string, 定义查询数据地址URL*/
        mtype: "post",
        caption: captionString, /* 	表格的标题。显示在Header上。若为空时将不会显示。*/
        rowNum: 10, /*integer, 表格中可见的记录数。此参数通过url传递给服务器供检索数据用。注意：若此参数设置为10，而服务器返回15条记录，将只有10条记录被装入。若此参数被设置为-1，则此检查失效*/

        rowList: [10, 20, 30], /*array[], 用于改变显示行数的下拉列表框的元素数组。，格式为[10,20,30]*/

        datatype: 'json', /* string, 从服务器端返回的数据类型，默认xml。可选类型：xml，local，json，jsonnp，script，xmlstring，jsonstring，clientside*/

        height: "auto", /* mixed, 表格高度。可为数值、百分比或auto*/

        /* 当设置为true时，表格宽度将自动匹配到父元素的宽度。这个匹配只在表格建立时进行，
         * 为了使表格在父元素宽度变化时也随之变化，可以使用setGridWidth方法 */
        autowidth: true,

        viewrecords: true, /*boolean, 是否在浏览导航栏显示记录总数*/

        altRows: true, /*boolean, 设置为交替行表格*/

        multiselect: multiselectBool, /* 	boolean, 此属性设为true时启用多行选择，出现复选框*/

        //multikey: "ctrlKey", /*string, 此属性只有当multiselect为true时有效，定义多选时的组合键，可选值有： shiftKey ，altKey，ctrlKey*/

        multiboxonly: true, /*此属性只有当multiselect为true时有效，. Multiboxonly设置为true时，只有点击checkbox时该行才被选中，点击其他列，将清除当前行的选中。*/

        /*当从服务器返回响应时执行，xhr：XMLHttpRequest 对象*/
        loadComplete: function () {
            var table = this;
            setTimeout(function () {
                //styleCheckbox(table);//勾选框样式
                //updateActionIcons(table);//左下角工具图标
                updatePagerIcons(table);//翻页图标
                enableTooltips(table);//鼠标悬停提示
            }, 0);
        }

        /** //是否设置子表
         //boolean, 设置为true，可使用子表格。启用子表格，将在基本表的左边将添加一列，并包含一个“+”图像，用户可以点击扩展行。
         subGrid: true,
         //array-[],该属性用于描述子表格的模式，只有subGrid 为true时有效。它是一个用于描述子表格列的数组。
         //subGridModel: [{ name : ['No','Item Name','Qty'], width : [55,200,80] }],
         //子表格参数
         subGridOptions: {
            plusicon: "ace-icon fa fa-plus center bigger-110 blue",
            minusicon: "ace-icon fa fa-minus center bigger-110 blue",
            openicon: "ace-icon fa fa-chevron-right center orange"
        },

         //for this example we are using local data
         subGridRowExpanded: function (subgridDivId, rowId) {
            var subgridTableId = subgridDivId + "_t";
            $("#" + subgridDivId).html("<table id='" + subgridTableId + "'></table>");
            $("#" + subgridTableId).jqGrid({
                datatype: 'local',
                data: subgrid_data,
                colNames: ['No', 'Item Name', 'Qty'],
                colModel: [
                    {name: 'id', width: 50},
                    {name: 'name', width: 150},
                    {name: 'qty', width: 50}
                ]
            });
        },
         */

        /**
         ,
         grouping:true,  //boolean, 是否设置表格组
         groupingView : {
             groupField : ['name'],
             groupDataSorted : true,
             plusicon : 'fa fa-chevron-down bigger-110',
             minusicon : 'fa fa-chevron-up bigger-110'
        },
         caption: "Grouping" //表格的标题。显示在Header上。若为空时将不会显示。
         */

    });

    var parent_column = $(grid_selector).closest('[class*="col-"]');//调整大小以适应页面大小
    $(window).on('resize.jqGrid', function () {
        $(grid_selector).jqGrid('setGridWidth', parent_column.width());
    });

    //调整在侧边栏 折叠/展开
    $(document).on('settings.ace.jqGrid', function (ev, event_name, collapsed) {
        if (event_name === 'sidebar_collapsed' || event_name === 'main_container_fixed') {
            //setTimeout is for webkit only to give time for DOM changes and then redraw!!!
            setTimeout(function () {
                $(grid_selector).jqGrid('setGridWidth', parent_column.width());
            }, 0);
        }
    });

    //如果你的网格是另一个元素，例如一个标签面板，你应该使用它的父的宽度：
    /**
     $(window).on('resize.jqGrid', function () {
        var parent_width = $(grid_selector).closest('.tab-pane').width();
        $(grid_selector).jqGrid( 'setGridWidth', parent_width );
    })
     //and also set width when tab pane becomes visible
     $('#myTab a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
      if($(e.target).attr('href') == '#mygrid') {
        var parent_width = $(grid_selector).closest('.tab-pane').width();
        $(grid_selector).jqGrid( 'setGridWidth', parent_width );
      }
    })
     */

        //触发窗口调整大小以使网格得到正确的大小
    $(window).triggerHandler('resize.jqGrid');
    //启用 search/filter 工具栏
    //jQuery(grid_selector).jqGrid('filterToolbar',{defaultSearch:true,stringResult:true})
    //jQuery(grid_selector).filterToolbar({});

    //导航按钮
    if (navGridBool == true) {
        jQuery(grid_selector).jqGrid('navGrid', pager_selector,
            {
                //导航栏选项
                edit: false,
                editicon: 'ace-icon fa fa-pencil blue',
                add: false,
                addicon: 'ace-icon fa fa-plus-circle purple',
                del: false,
                delicon: 'ace-icon fa fa-trash-o red',

                search: false,
                searchicon: 'ace-icon fa fa-search orange',
                refresh: true,
                refreshicon: 'ace-icon fa fa-refresh green',
                view: true,
                viewicon: 'ace-icon fa fa-search-plus grey'
            }

            //{
            //    //编辑记录表单设置
            //    //closeAfterEdit: true,
            //    recreateForm: true,
            //    beforeShowForm: function (e) {
            //        var form = $(e[0]);
            //        form.closest('.ui-jqdialog').find('.ui-jqdialog-titlebar').wrapInner('<div class="widget-header" />');
            //        style_edit_form(form);
            //    }
            //}
            //{
            //    //新增记录表单设置
            //    //width: 700,
            //    closeAfterAdd: true,
            //    recreateForm: true,
            //    viewPagerButtons: false,
            //    beforeShowForm: function (e) {
            //        var form = $(e[0]);
            //        form.closest('.ui-jqdialog').find('.ui-jqdialog-titlebar')
            //            .wrapInner('<div class="widget-header" />');
            //        style_edit_form(form);
            //    }
            //},
            //{
            //    //删除记录表单设置
            //    recreateForm: true,
            //    beforeShowForm: function (e) {
            //        var form = $(e[0]);
            //        if (form.data('styled')) return false;
            //
            //        form.closest('.ui-jqdialog').find('.ui-jqdialog-titlebar').wrapInner('<div class="widget-header" />');
            //        style_delete_form(form);
            //
            //        form.data('styled', true);
            //    },
            //    onClick: function (e) {
            //        //alert(1);
            //    }
            //},
            //{
            //    //查询表单设置
            //    recreateForm: true,
            //    afterShowSearch: function (e) {
            //        var form = $(e[0]);
            //        form.closest('.ui-jqdialog').find('.ui-jqdialog-title').wrap('<div class="widget-header" />');
            //        style_search_form(form);
            //    },
            //    afterRedraw: function () {
            //        style_search_filters($(this));
            //    }
            //    ,
            //    multipleSearch: true
            //    /**
            //     multipleGroup:true,
            //     showQuery: true
            //     */
            //},
            //{
            //    //查看记录详情表单设置
            //    recreateForm: true,
            //    beforeShowForm: function (e) {
            //        var form = $(e[0]);
            //        form.closest('.ui-jqdialog').find('.ui-jqdialog-title').wrap('<div class="widget-header" />')
            //    }
            //}
        );
        jQuery(grid_selector).jqGrid('inlineNav', pager_selector,
            {
                editParams: {
                    aftersavefunc: function (rowid, response) {
                        var jsonResponse = $.parseJSON(response.responseText);
                        if (jsonResponse.state != 1) {
                            alert(jsonResponse.message)
                        } else {
                            alert(jsonResponse.message)
                        }
                        return true
                    },
                    afterSubmit: function (rowid, response) {
                        var jsonResponse = $.parseJSON(response.responseText);
                        if (jsonResponse.state != 1) {
                            alert(jsonResponse.message)
                        } else {
                            alert(jsonResponse.message)
                        }
                        return true
                    }
                },
                //导航栏选项
                edit: true,
                editicon: 'ace-icon fa fa-pencil blue',
                add: true,
                addicon: 'ace-icon fa fa-plus-circle purple',
                del: true,
                delicon: 'ace-icon fa fa-trash-o red',
                search: true,
                searchicon: 'ace-icon fa fa-search orange',
                refresh: true,
                refreshicon: 'ace-icon fa fa-refresh green',
                view: true,
                viewicon: 'ace-icon fa fa-search-plus grey'
            },
            {
                jqModal: true,
                reloadAfterSubmit: true,
                afterSubmit: function (response, postdata) {
                    var json = response.responseText;
                    alert(json)
                }
            } // edit options
        );
    }


    //var selr = jQuery(grid_selector).jqGrid('getGridParam','selrow');
    $(document).one('ajaxloadstart.page', function (e) {
        $.jgrid.gridDestroy(grid_selector);
        $('.ui-jqdialog').remove();
    });
//});
}


//删除表单风格
function style_delete_form(form) {
    var buttons = form.next().find('.EditButton .fm-button');
    buttons.addClass('btn btn-sm btn-white btn-round').find('[class*="-icon"]').hide();//ui-icon, s-icon
    buttons.eq(0).addClass('btn-danger').prepend('<i class="ace-icon fa fa-trash-o"></i>');
    buttons.eq(1).addClass('btn-default').prepend('<i class="ace-icon fa fa-times"></i>')
}

//编辑表单风格
function style_edit_form(form) {
    //enable datepicker on "sdate" field and switches for "stock" field
    form.find('input[name=sdate]').datepicker({format: 'yyyy-mm-dd', autoclose: true});
    form.find('input[name=date_joined]').datepicker({format: 'yyyy-mm-dd', autoclose: true});

    form.find('input[name=is_superuser]').addClass('ace ace-switch ace-switch-5').after('<span class="lbl"></span>');
    //don't wrap inside a label element, the checkbox value won't be submitted (POST'ed)
    //.addClass('ace ace-switch ace-switch-5').wrap('<label class="inline" />').after('<span class="lbl"></span>');


    //update buttons classes
    var buttons = form.next().find('.EditButton .fm-button');
    buttons.addClass('btn btn-sm').find('[class*="-icon"]').hide();//ui-icon, s-icon
    buttons.eq(0).addClass('btn-primary').prepend('<i class="ace-icon fa fa-check"></i>');
    buttons.eq(1).prepend('<i class="ace-icon fa fa-times"></i>');

    buttons = form.next().find('.navButton a');
    buttons.find('.ui-icon').hide();
    buttons.eq(0).append('<i class="ace-icon fa fa-chevron-left"></i>');
    buttons.eq(1).append('<i class="ace-icon fa fa-chevron-right"></i>');
}


//搜索表单的风格
function style_search_filters(form) {
    form.find('.delete-rule').val('X');
    form.find('.add-rule').addClass('btn btn-xs btn-primary');
    form.find('.add-group').addClass('btn btn-xs btn-success');
    form.find('.delete-group').addClass('btn btn-xs btn-danger');
}

//查询表单风格
function style_search_form(form) {
    var dialog = form.closest('.ui-jqdialog');
    var buttons = dialog.find('.EditTable');
    buttons.find('.EditButton a[id*="_reset"]').addClass('btn btn-sm btn-info').find('.ui-icon').attr('class', 'ace-icon fa fa-retweet');
    buttons.find('.EditButton a[id*="_query"]').addClass('btn btn-sm btn-inverse').find('.ui-icon').attr('class', 'ace-icon fa fa-comment-o');
    buttons.find('.EditButton a[id*="_search"]').addClass('btn btn-sm btn-purple').find('.ui-icon').attr('class', 'ace-icon fa fa-search');
}

//点击删除按钮前回调函数
function beforeDeleteCallback(e) {
    alert("11")
    var form = $(e[0]);
    if (form.data('styled')) return false;
    form.closest('.ui-jqdialog').find('.ui-jqdialog-titlebar').wrapInner('<div class="widget-header" />');
    style_delete_form(form);
    form.data('styled', true);
}


//勾选框样式，重新加载表格会有闪烁
function styleCheckbox(table) {
    $(table).find('input:checkbox').addClass('ace')
        .wrap('<label />')
        .after('<span class="lbl align-center" />');


    $('.ui-jqgrid-labels th[id*="_cb"]:first-child')
        .find('input.cbox[type=checkbox]').addClass('ace')
        .wrap('<label />').after('<span class="lbl align-center" />');
}

//置换左下角工具图标，可置换图标，新增，编辑，查看，删除图标
function updateActionIcons(table) {
    var replacement =
    {
        'ui-ace-icon fa fa-pencil': 'ace-icon fa fa-pencil blue',
        'ui-ace-icon fa fa-trash-o': 'ace-icon fa fa-trash-o red',
        'ui-icon-disk': 'ace-icon fa fa-check green',
        'ui-icon-cancel': 'ace-icon fa fa-times red'
    };
    $(table).find('.ui-pg-div span.ui-icon').each(function () {
        var icon = $(this);
        var $class = $.trim(icon.attr('class').replace('ui-icon', ''));
        if ($class in replacement) icon.attr('class', 'ui-icon ' + replacement[$class]);
    })
}

//用FontAwesome置换翻页图标
function updatePagerIcons(table) {
    var replacement =
    {
        'ui-icon-seek-first': 'ace-icon fa fa-angle-double-left bigger-140',
        'ui-icon-seek-prev': 'ace-icon fa fa-angle-left bigger-140',
        'ui-icon-seek-next': 'ace-icon fa fa-angle-right bigger-140',
        'ui-icon-seek-end': 'ace-icon fa fa-angle-double-right bigger-140'
    };
    $('.ui-pg-table:not(.navtable) > tbody > tr > .ui-pg-button > .ui-icon').each(function () {
        var icon = $(this);
        var $class = $.trim(icon.attr('class').replace('ui-icon', ''));

        if ($class in replacement) icon.attr('class', 'ui-icon ' + replacement[$class]);
    })
}

//开启工具提示，鼠标悬停按钮提示帮助信息
function enableTooltips(table) {
    $('.navtable .ui-pg-button').tooltip({container: 'body'});
    $(table).find('.ui-pg-div').tooltip({container: 'body'});
}