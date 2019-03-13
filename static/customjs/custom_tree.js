/**
 * Created by xhl on 2015/12/8.
 */

function self_init_tree(IdNameString, MultiSelectBool, TreeDataDict) {
    var ShowData = initiateData(TreeDataDict);//初始化树状数据
    $(IdNameString).ace_tree({
        dataSource: ShowData['dataSource'],
        cacheItems: false,
        loadingHTML: '<div class="tree-loading"><i class="ace-icon fa fa-refresh fa-spin blue"></i></div>',
        discloseVisible: true,

        'open-icon': 'ace-icon fa fa-folder-open',
        'close-icon': 'ace-icon fa fa-folder',
        'itemSelect': true,
        'folderSelect': true,//根节点能否选中
        'multiSelect': MultiSelectBool,//单,多选开关，true/false
        'selected-icon': 'ace-icon fa fa-check',
        'unselected-icon': 'ace-icon fa fa-times',
        'folder-open-icon': 'ace-icon tree-plus',
        'folder-close-icon': 'ace-icon tree-minus'
    });
    $(IdNameString).tree('discloseAll');

    /**
     //Use something like this to reload data
     $('#tree1').find("li:not([data-template])").remove();
     $('#tree1').tree('render');
     */

    /**
     //please refer to docs for more info
     $('#tree1')
     .on('loaded.fu.tree', function(e) {
	})
     .on('updated.fu.tree', function(e, result) {
	})
     .on('selected.fu.tree', function(e) {
	})
     .on('deselected.fu.tree', function(e) {
	})
     .on('opened.fu.tree', function(e) {
	})
     .on('closed.fu.tree', function(e) {
	});
     */

    //初始化显示数据,可用python初始化
    function initiateData(tree_data) {

        var dataSource = function (options, callback) {
            var $data = null;
            if (!("text" in options) && !("type" in options)) {
                $data = tree_data;//the root tree
                callback({data: $data});
                return;
            } else if ("type" in options && options.type == "folder") {
                if ("additionalParameters" in options && "children" in options.additionalParameters)
                    $data = options.additionalParameters.children || {};
                else $data = {};//no data
            }

            if ($data != null)//this setTimeout is only for mimicking some random delay
                setTimeout(function () {
                    callback({data: $data});
                }, parseInt(Math.random() * 500) + 200);

            //we have used static data here
            //but you can retrieve your data dynamically from a server using ajax call
            //checkout examples/treeview.html and examples/treeview.js for more info
        };

        return {'dataSource': dataSource}
    }
}

//获取部门信息并初始化树
function get_all_dept(idStr, isMany, edit_user_id) {
    $.ajax({
        url: "/organizational/departments/list",
        type: 'POST',
        dataType: 'JSON',
        data: {"edit_user_id": edit_user_id},
        success: function (result) {
            $(idStr).removeData("fu.tree");
            $(idStr).unbind('click.fu.tree');
            self_init_tree(idStr, isMany, result);
        }
    });
}

function reload_dept_tree(bindId, isMany) {
    $(bindId).removeData("fu.tree");
    $(bindId).unbind('click.fu.tree');
    get_all_dept(bindId, isMany);
}


function remove_dept_tree(bindId) {
    $(bindId).removeData("fu.tree");
    $(bindId).unbind('click.fu.tree');
}