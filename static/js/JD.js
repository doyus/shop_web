
function LunBo(){

	var win=document.getElementById('img-window');
	var ul=win.getElementsByTagName("ul")[0];
	var ol=win.getElementsByTagName("ol")[0];
	var ulLi=ul.getElementsByTagName("li");
	var olLi=ol.getElementsByTagName("li");
	var liW=-ulLi[0].offsetWidth;
	var i=1;
	var cur=0;
	function moveLB(){
		if(i==(ulLi.length-1)){
			startMove(ul,{"left":liW*i},function(){
				ul.style.left=0;
				i=1;
			});
		}else{
			startMove(ul,{"left":liW*i});
		}
		for(var m=0;m<olLi.length;m++){
			olLi[m].className="";
		}
		if(i==(ulLi.length-1)){
			olLi[0].className="active";
		}else{
			olLi[i].className="active";
		}
		i++;
		cur=i-1;
		if(i>ulLi.length-1){
			i=0;
			cur=0;
		}
	}
	var lunbo=setInterval(moveLB,2000);
	for(var n=0;n<olLi.length;n++){
		olLi[n].index=n;
		olLi[n].onouseover=function(){clearInterval(lunbo);};
		olLi[n].onclick=function(){
			i=this.index;
			cur=this.index;
			for(var m=0;m<olLi.length;m++){
				olLi[m].className="";
			}
			this.className="active";
			if(i==(ulLi.length-1)){
				startMove(ul,{"left":liW*i},function(){
					ul.style.left=0;
					i=1;
				});
			}else{
				startMove(ul,{"left":liW*i});
			}
		}
	}
	var ToLeft=document.getElementById("ToLeft");
	var ToRight=document.getElementById("ToRight");

	ToLeft.onmouseover=ToRight.onmouseover=function(){clearInterval(lunbo)};
	ToLeft.onmouseout=ToRight.onmouseout=function(){lunbo=setInterval(moveLB,2000);};
	ToLeft.onclick=function(){
		if(Math.abs(ul.offsetLeft)<=Math.abs(liW)){
			ul.style.left=liW*(ulLi.length-1)+"px";
			cur=ulLi.length-1;
		}
		cur--;
		if(cur<0){cur=ulLi.length-2;}
		startMove(ul,{"left":liW*cur});
		for(var m=0;m<olLi.length;m++){
			olLi[m].className="";
		}
		olLi[cur].className="active";
		i=cur+1;

	};
	ToRight.onclick=function(){
		cur++;
		if(Math.abs(ul.offsetLeft)>Math.abs(liW*(ulLi.length-2))){
			startMove(ul,{"left":liW*cur});
			ul.style.left=0;
			cur=1;
		}else{
			startMove(ul,{"left":liW*cur});
		}
		if(cur>ulLi.length-2){
			cur=0;
		}
		i=cur+1;
		if(i==1){
			i=ulLi.length-1;
		}
		for(var m=0;m<olLi.length;m++){
			olLi[m].className="";
		}
		olLi[cur].className="active";
	};

}
LunBo();









function startMove(obj,json,fn){
	clearInterval(obj.t);
	obj.t=setInterval(function(){
		var bstop=true;//检测是否所有的属性值都到达目标值
		for(var attr in json){
			var curstyle=0;
			if(attr=='opacity'){
				curstyle=parseInt(parseFloat(getStyle(obj,attr))*100);
			}else{
				curstyle=parseInt(getStyle(obj,attr));
			}
			var speed=(json[attr]-curstyle)/8;
			speed=speed>0?Math.ceil(speed):Math.floor(speed);
			if(curstyle!=json[attr]){
				bstop=false;//如果有一个当前值与目标值不相等，那就不停止
			}
			if(attr=='opacity'){
				obj.style.filter='alpha(opacity:'+(curstyle+speed)+')';
				obj.style.opacity=(curstyle+speed)/100;
			}else{
				obj.style[attr]=curstyle+speed+'px';
			}
		}
		if(bstop){
			if(fn){fn();}
			clearInterval(obj.t);
		}
	},10)
}
//获取css样式
function getStyle(obj,attr){
	if(obj.currentStyle){
		return obj.currentStyle[attr];
	}else{
		return getComputedStyle(obj,false)[attr];
	}
}



