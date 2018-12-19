var cur_page = 1;
var next_page = 1;
var total_page = 1;
var house_data_querying = true;
var pre_point=(116.331398,39.897445);
var opts = {
				width : 300,     // 信息窗口宽度
				height: 320,     // 信息窗口高度
				title : "" , // 信息窗口标题
				enableMessage:true//设置允许信息窗发送短息
			   };
//地图放大比例
var mapzoom=13;
//地图覆盖物，{"地址":"marker"}
var map_marker={};
//地图覆盖物地址，["地址1","地址2","地址3"]
var marker_list=[];
//上一次鼠标点击的地址
var pre_address='';
var num=1;

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function updateFilterDateDisplay() {
    var startDate = $("#start-date").val();
    var endDate = $("#end-date").val();
    var $filterDateTitle = $(".filter-title-bar>.filter-title").eq(0).children("span").eq(0);
    if (startDate) {
        var text = startDate.substr(5) + "/" + endDate.substr(5);
        $filterDateTitle.html(text);
    } else {
        $filterDateTitle.html("入住日期");
    }
}




$(document).ready(function(){
//    创建地图，指定放大比例
    var map = new BMap.Map("allmap",{minZoom:1,maxZoom:18},{enableMapClick:false});
    var myGeo = new BMap.Geocoder();
    var top_left_control = new BMap.ScaleControl({anchor: BMAP_ANCHOR_TOP_LEFT});// 左上角，添加比例尺
	var top_left_navigation = new BMap.NavigationControl();  //左上角，添加默认缩放平移控件
	var top_right_navigation = new BMap.NavigationControl({anchor: BMAP_ANCHOR_TOP_RIGHT, type: BMAP_NAVIGATION_CONTROL_SMALL}); //右上角，仅包含平移和缩放按钮
//	添加放大缩小组件
	map.addControl(top_left_control);
	map.addControl(top_left_navigation);
	map.addControl(top_right_navigation);

    var queryData = decodeQuery();
    var startDate = queryData["sd"];
    var endDate = queryData["ed"];
    $("#start-date").val(startDate);
    $("#end-date").val(endDate);
    updateFilterDateDisplay();
    var areaName = queryData["aname"];
    if (!areaName){
        areaName = "位置区域";
        mapname="北京";
    }
    else{
        mapname=areaName;
    }
    demap(mapname)
    $(".filter-title-bar>.filter-title").eq(1).children("span").eq(0).html(areaName);

    $.get("/api/house/area", function(data){
        console.log(data)
        if ("0" == data.errcode) {
            var areaId = queryData["aid"];
            if (areaId) {
                for (var i=0; i<data.data.length; i++) {
                    areaId = parseInt(areaId);
                    if (data.data[i].area_id == areaId) {
                        $(".filter-area").append('<li area-id="'+ data.data[i].area_id+'" class="active">'+ data.data[i].name+'</li>');
                    } else {
                        $(".filter-area").append('<li area-id="'+ data.data[i].area_id+'">'+ data.data[i].name+'</li>');
                    }
                }
            } else {
                for (var i=0; i<data.data.length; i++) {
                    $(".filter-area").append('<li area-id="'+ data.data[i].area_id+'">'+ data.data[i].name+'</li>');
                }
            }
            updateHouseData("renew");
            var windowHeight = $(window).height()
            window.onscroll=function(){
                // var a = document.documentElement.scrollTop==0? document.body.clientHeight : document.documentElement.clientHeight;
                var b = document.documentElement.scrollTop==0? document.body.scrollTop : document.documentElement.scrollTop;
                var c = document.documentElement.scrollTop==0? document.body.scrollHeight : document.documentElement.scrollHeight;
                if(c-b<windowHeight+50){
                    if (!house_data_querying) {
                        house_data_querying = true;
                        if(cur_page < total_page) {
                            next_page = cur_page + 1;
                            updateHouseData();
                        }
                    }
                }
            }
        }
    });


    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    var $filterItem = $(".filter-item-bar>.filter-item");
    $(".filter-title-bar").on("click", ".filter-title", function(e){
        var index = $(this).index();
        if (!$filterItem.eq(index).hasClass("active")) {
            $(this).children("span").children("i").removeClass("fa-angle-down").addClass("fa-angle-up");
            $(this).siblings(".filter-title").children("span").children("i").removeClass("fa-angle-up").addClass("fa-angle-down");
            $filterItem.eq(index).addClass("active").siblings(".filter-item").removeClass("active");
            $(".display-mask").show();
        } else {
            $(this).children("span").children("i").removeClass("fa-angle-up").addClass("fa-angle-down");
            $filterItem.eq(index).removeClass('active');
            $(".display-mask").hide();
            updateFilterDateDisplay();
            cur_page = 1;
            next_page = 1;
            total_page = 1;
            updateHouseData("renew");
        }
    });
    $(".display-mask").on("click", function(e) {
        $(this).hide();
        $filterItem.removeClass('active');
        updateFilterDateDisplay();
        cur_page = 1;
        next_page = 1;
        total_page = 1;
        updateHouseData("renew");
    });
    $(".filter-item-bar>.filter-area").on("click", "li", function(e) {
        if (!$(this).hasClass("active")) {
            $(this).addClass("active");
            $(this).siblings("li").removeClass("active");
            $(".filter-title-bar>.filter-title").eq(1).children("span").eq(0).html($(this).html());
        } else {
            $(this).removeClass("active");
            $(".filter-title-bar>.filter-title").eq(1).children("span").eq(0).html("位置区域");
        }
    });
    $(".filter-item-bar>.filter-sort").on("click", "li", function(e) {
        if (!$(this).hasClass("active")) {
            $(this).addClass("active");
            $(this).siblings("li").removeClass("active");
            $(".filter-title-bar>.filter-title").eq(2).children("span").eq(0).html($(this).html());
        }
    })

//    demap(mapname)

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function updateFilterDateDisplay() {
    var startDate = $("#start-date").val();
    var endDate = $("#end-date").val();
    var $filterDateTitle = $(".filter-title-bar>.filter-title").eq(0).children("span").eq(0);
    if (startDate) {
        var text = startDate.substr(5) + "/" + endDate.substr(5);
        $filterDateTitle.html(text);
    } else {
        $filterDateTitle.html("入住日期");
    }
}





function updateHouseData(action="append") {
    var areaId = $(".filter-area>li.active").attr("area-id");
    if (undefined == areaId) areaId = "";
    var startDate = $("#start-date").val();
    var endDate = $("#end-date").val();
    var sortKey = $(".filter-sort>li.active").attr("sort-key");
    var params = {
        aid:areaId,
        sd:startDate,
        ed:endDate,
        sk:sortKey,
        p:next_page
    };
    $.get("/api/house/list2", params, function(data){
        house_data_querying = false;
        if ("0" == data.errcode) {
            if (0 == data.total_page) {
                $(".house-list").html("暂时没有符合您查询的房屋信息。");
            } else {
                total_page = data.total_page;
                if ("append" == action) {
                    cur_page = next_page;
                    $(".house-list").append(template("house-list-tmpl", {houses:data.data}));

                    showmap(data.data)
                    $(".house-item").mouseover(function(){
                        address=$(this).children().eq(0).text()
//		                showmap(data.data)
		                addAnimation(address)
	                });
	                $(".house-item").mouseout(function(){
                        address=$(this).children().eq(0).text()
		                console.log("mouse leave")
		                deleteAnimation(address)
	                });

                } else if ("renew" == action) {
                    cur_page = 1;
                    $(".house-list").html(template("house-list-tmpl", {houses:data.data}));
                    showmap(data.data)
                    $(".house-item").mouseover(function(){
		                address=$(this).children().eq(0).text()
//		                showmap(data.data)
		                addAnimation(address)
	                });
	                $(".house-item").mouseout(function(){
		                address=$(this).children().eq(0).text()
		                deleteAnimation(address)
	                });
                }
//                默认把第一个房屋地址设置为地图中心点
                demap(data.data[0].address)

            }
        }
    })
}




function addClickHandler(content,marker){
		marker.addEventListener("click",function(e){
			openInfo(content,e)}
		);
	}
function openInfo(content,e){
    var p = e.target;
    var point = new BMap.Point(p.getPosition().lng, p.getPosition().lat);
    var infoWindow = new BMap.InfoWindow(content,opts);  // 创建信息窗口对象
    map.openInfoWindow(infoWindow,point); //开启信息窗口
}






//
//
//    // 编写自定义函数,创建标注
//function addMarker(point,label){
////    var map = new BMap.Map("allmap");
//    var marker = new BMap.Marker(point);
//    map.addOverlay(marker);
//    marker.setLabel(label);
//    }
//function geocodeSearch(add){
//
//    var myGeo = new BMap.Geocoder();
//    myGeo.getPoint(add, function(point){
//        if (point) {
//
//            var address = new BMap.Point(point.lng, point.lat);
//            console.log('haaha',address)
//            addMarker(address,new BMap.Label(":"+add,{offset:new BMap.Size(20,-10)}));
//        }
//        else{
//            console.log('error')
//        }
//    }, "合肥市");
//}
function showmap(data){
    var data_info=[]
    var address_info=[]
    for(var i=0;i<data.length;i++){


//        data_info.push("<h2><b>"+data[i].title+"</b> <a href='http://192.168.0.120:9000/detail.html?id="+data[i].house_id+"'> 详情...</a></h2> <p> 地址："+data[i].address+" <br> 咨询热线："+data[i].telephone+"<br> 客服QQ："+data[i].qqnum+"</p> <br> <img src='"+data[i].image_url+"' width='95%'/>")

//        data_info.push("<div class='house-item'> <a href='http://192.168.0.120:9000/detail.html?id="+data[i].house_id+"'> <img src='"+data[i].image_url+"'> </a> <div class='house-desc'> <div class='landlord-pic'> <img src='"+data[i].avatar+"'> </div> <div class='house-price'>￥<span>"+data[i].price/100.0.toFixed(0)+"</span> /晚 </div> <div class='house-intro'> <span class='house-title'> "+data[i].title+" </span>  地址："+data[i].address+" 咨询热线："+data[i].telephone+"  客服QQ："+data[i].qqnum+"  </div> </div> </div>")
             data_info.push("<div class='house2-item'> <a href='http://192.168.0.120:9000/detail.html?id="+data[i].house_id+"'> <img src='"+data[i].image_url+"'> </a> <div class='house2-desc'> <div class='landlord2-pic'> <img src='"+data[i].avatar+"'> </div> <div class='house2-price'>￥<span>"+data[i].price/100.0.toFixed(0)+"</span> /晚 </div> <div class='house2-intro'> <span class='house2-title'> "+data[i].title+" </span>  地址："+data[i].address+"<br> 咨询热线："+data[i].telephone+" <br> 客服QQ："+data[i].qqnum+"  </div> </div> </div>");
             address_info.push(data[i].address)




    }
//    console.log(data_info[0])

    for (var i = 0; i < data.length; i++){
        var myGeo = new BMap.Geocoder();
        myGeo.getPoint(data[i].address, function(point){
            if (point) {
//                console.log('point address',address)
                console.log('=============',data[i].address)
                var address=address_info[0];
                if (marker_list.indexOf(address) == -1){
                    var marker = new BMap.Marker(point);  // 创建标注
                    var content = data_info.shift();
                    var address =address_info.shift();

                    map.addOverlay(marker);               // 将标注添加到地图中
                    addClickHandler(content,marker);
                    map_marker[address]=marker
                    marker_list.push(address)
                    console.log('add map_marker')
                }
            }

        }, "合肥市")
    }
    console.log(map_marker)
}
//初始地图中心位置，房屋列表中第一个地址
function demap(site){
    // 创建地址解析器实例
    var myGeo = new BMap.Geocoder();
	// 将地址解析结果显示在地图上,并调整地图视野
	myGeo.getPoint(site, function(point){
		if (point) {
//		    pre_point=point
		    console.log("demap")
			map.centerAndZoom(point, mapzoom);


		}
	}, "北京市");
}

//鼠标移动到房屋列表，地图覆盖物跳动
function addAnimation(site){
    // 百度地图API功能
//    var map = new BMap.Map("allmap");
//	放大，移动，拖拽
//	map.enableScrollWheelZoom(true);
//	map.enableContinuousZoom();
//    map.enableDragging();
    mapzoom=map.getZoom()
//	var point = new BMap.Point(pre_point);
//	map.centerAndZoom(point,mapzoom);

// 创建地址解析器实例
    var myGeo = new BMap.Geocoder();
	// 将地址解析结果显示在地图上,并调整地图视野
	myGeo.getPoint(site, function(point){
		if (point) {
//		    pre_point=point
//		    console.log(point)

			map.centerAndZoom(point, mapzoom);
//			marker=new BMap.Marker(point);
//
//			map.addOverlay(marker);
            if (pre_address !=''){
                    pre_address.setAnimation(null)
                    console.log("stop add")

            }
			map_marker[site].setAnimation(BMAP_ANIMATION_BOUNCE); //跳动的动画
			pre_address=map_marker[site]
			console.log('start  ',site)
//			console.log('haha',map_marker[point])
//			console.log(point)

		}else{
			alert("您选择地址没有解析到结果!");
		}
	}, "北京市");
}
//鼠标移开房屋列表，地图覆盖物停止跳动
function deleteAnimation(site){
    pre_address.setAnimation(null)


// 创建地址解析器实例
//    var myGeo = new BMap.Geocoder();
//	// 将地址解析结果显示在地图上,并调整地图视野
//	myGeo.getPoint(site, function(point){
//		if (point) {
////		    pre_point=point
////		    console.log(point)
////		    mapzoom=map.getZoom()
////			map.centerAndZoom(point, mapzoom);
//			pre_address.setAnimation(null)
//			map_marker[site].setAnimation(null); //跳动的动画
//            console.log('stop  delete')
//		}else{
//			alert("您选择地址没有解析到结果!");
//		}
//	}, "北京市");
}

})