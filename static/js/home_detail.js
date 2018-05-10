//获取当前浏览路径
//alert(window.location.pathname);
//获取浏览器访问地址参数(?后面的带的东西)
let DETAIL_URL = 'http://127.0.0.1:8000/home/detail'
    + window.location.search; //?pid=89
let pid;
$(function () {
    $.get(DETAIL_URL, function (result) {
        if (result != null && result.data != null) {
            pid = result.data.id;
            show_shop_info(result.data);
            show_shop_img(result.data.imgs);
        }
    })


});

//显示产品信息
function show_shop_info(product) {

    let $name = $('#shop_detail').find('h3');
    $name.text(product.name);
    let $orignal_price = $('#orignal_price');
    $orignal_price.text(product.orignal_price);
    let $promote_price = $('#promote_price');
    $promote_price.text(product.promote_price);
    let $stock = $('#stock');
    $stock.text(product.stock);
}

let SINGLE_IMG_URL = 'http://127.0.0.1:8000/static/img/productSingle_middle/';

function show_shop_img(img_list) {
    let $small_img = $('#shop_small_img');
    for (let img of img_list) {
        $('<img>')
            .attr('src', SINGLE_IMG_URL + img.id + '.jpg')
            .mousemove(function () {
                $('#shop_big_img').attr('src', $(this).attr('src'))
            })
            .appendTo($small_img)
    }
    $('#shop_big_img').attr('src', SINGLE_IMG_URL + img_list[0].id + '.jpg');
}