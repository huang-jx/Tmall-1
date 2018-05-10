$(function () {
    init();
});

function init() {
    /*加载数据*/
    load_data();
}

//初始化数据
function load_data() {

    let cate_url = 'http://127.0.0.1:8000/home/cates/';
    let setting = {
        type: 'GET',
        success: function (result) {
            if (result.state === 200) {
                init_cate(result.data);
                init_banner(result.banners);
            }
        },
    };
    $.ajax(cate_url, setting)
}

//创建分类菜单
function init_cate(data) {
    //给外层div设置移除事件
    let $cate_ul = $('.category').mouseout(function () {
        $('.sub').toggle()
    });
    //动态创建li
    for (let cate of data) {
        //创建li
        $('<li>')
            .mouseover(function () {
                //当鼠标移动到一级菜单的li上面的时候 显示二级菜单
                let $ul = $('.sub').empty().toggle();
                //动态的创建二级菜单
                for (let sub of cate.subs) {
                    $('<li>').append($('<a>').text(sub.name)).appendTo($ul)
                }
            })
            // 在li中添加a标签
            .append($('<a>').text(cate.name))
            .appendTo($cate_ul)
    }
}

function init_banner(banners) {

    if (banners.length > 0) {
        let $banner = $('#banner>ul');
        for (let banner of banners) {
            $('<li>')
                .append($('<a>')
                    .append($('<img>')
                        .attr('src', 'http://127.0.0.1:8000/static/' + banner.path)))
                .appendTo($banner);
        }
        //  开始自动轮播
        lunbo()
    }
}

function lunbo() {
    $('#banner').unslider({
        dots: true
    })
}