function ajaxfetchimg9(C,B,Z,T){C="#"+C;var A=B;jq.ajax({url:A,async:false,dataType:"html",success:function(G){var E;if(window.ActiveXObject){E=new ActiveXObject("Microsoft.XMLDOM");E.async=false;E.loadXML(G)}else{var H=new DOMParser();E=H.parseFromString(G,"text/xml")}if(E.childNodes.length==0){return}jq(E).find("banner ad").each(function(){var I,H,T,S,F;H=jq(this).find("a").attr("href");T=jq(this).find("img").attr("alt");S=jq(this).find("img").attr("src");if(T){F="<div class=\"imgtitle\">"+T+"</div>"}else{f=""}I="<li><a href='"+H+"' title='"+T+"' target='_blank'><img src='"+S+"' /></a>"+F+"</li>";jq(C+" .img").append(I)});jq(Z).each(function(){jq(this).marquee()})}})}
function rolltext(Z) {
jq(Z).each(function() {
        			jq(this).marquee();
     								}
     								);
}
function ajaxfetchimg(C,B,Z,T){
	C="#"+C;
	var A=B;
	jq.ajax({
			url:A,async:false,dataType:"html",success:function(G){
				var E;
				if(window.ActiveXObject){
				E=new ActiveXObject("Microsoft.XMLDOM");
				E.async=false;
				E.loadXML(G);}
				else{
				var H=new DOMParser();
				E=H.parseFromString(G,"text/xml");}
				if(E.childNodes.length==0){return;}				
				jq(E).find(".banner").each(function(){
				var I,H,T,S,F;
				H=jq(this).find("a").attr("href");
				T=jq(this).find("img").attr("alt");
				S=jq(this).find("img").attr("src");
				if (T) {				
				F="<div class=\"imgtitle\">" +T+ "</div>";
				      }
				      else {f="";}
				I="<li><a href='"+H+"' title='"+T+"' target='_blank'><img src='"+S+"' /></a>" +F+ "</li>";				
				jq(C+" .img").append(I);				
				});
				jq(Z).each(function() {
        			jq(this).marquee();
     								});
				}});}
var $ = jQuery.noConflict();
(function($) {
	$.fn.marquee = function(o) {
		//获取滚动内容内各元素相关信息
		o = $.extend({
			speed:		parseInt($(this).attr('speed')), // 滚动速度
			step:		parseInt($(this).attr('step')), // 滚动步长
			direction:	$(this).attr('direction'), // 滚动方向
			pause:		parseInt($(this).attr('pause')) // 停顿时长
		}, o || {});
		var dIndex = jQuery.inArray(o.direction, ['right', 'down']);
		if (dIndex > -1) {
			o.direction = ['left', 'up'][dIndex];
			o.step = -o.step;
		}
		var mid;
		var div 		= $(this); // 容器对象
		var divWidth 	= div.innerWidth(); // 容器宽
		var divHeight 	= div.innerHeight(); // 容器高
		var ul 			= $("ul", div);
		var li 			= $("li", ul);
		var liSize 		= li.size(); // 初始元素个数
		var liWidth 	= li.width(); // 元素宽
		var liHeight 	= li.height(); // 元素高
		var width 		= liWidth * liSize;
		var height 		= liHeight * liSize;
		if ((o.direction == 'left' && width > divWidth) || 
			(o.direction == 'up' && height > divHeight)) {
			// 元素超出可显示范围才滚动
			if (o.direction == 'left') {
				ul.width(2 * liSize * liWidth);
				if (o.step < 0) {div.scrollLeft(width);}
			} else {
				ul.height(2 * liSize * liHeight);
				if (o.step < 0) {div.scrollTop(height);}
			}
			ul.append(li.clone()); // 复制元素
			mid = setInterval(_marquee, o.speed);
			div.hover(
				function(){clearInterval(mid);},
				function(){mid = setInterval(_marquee, o.speed);}
			);
		}
		function _marquee() {
			// 滚动
			if (o.direction == 'left') {
				var l = div.scrollLeft();
				if (o.step < 0) {
					div.scrollLeft((l <= 0 ? width : l) + o.step);
				} else {
					div.scrollLeft((l >= width ? 0 : l) + o.step);
				}
				if (l % liWidth == 0) {_pause();}
			} else {
				var t = div.scrollTop();
				if (o.step < 0) {
					div.scrollTop((t <= 0 ? height : t) + o.step);
				} else {
					div.scrollTop((t >= height ? 0 : t) + o.step);
				}
				if (t % liHeight == 0) {_pause();}
			}
		}
		function _pause() {
			if (o.pause > 0) {
				var tempStep = o.step;
				o.step = 0;
				setTimeout(function() {
					o.step = tempStep;
				}, o.pause);
			}
		}
	};
})(jQuery);



	
	