/**
 * Created by sunying
 */
function gx(){
		var x = parseInt(priceTotal.innerHTML);
        var value = new Array();
        var nameid = document.getElementById('nameid');
        console.log('aaaaaaaaaaaaaa');
        console.log(nameid.value);
        nameid = nameid.value;
        var zong = document.getElementsByClassName('check1');
        console.log(x);

            for(var i = 0; i < zong.length; i++){
            // console.log(zong[i])
             if(zong[i].checked)
             value.push(zong[i].value);
            }
            value.push(x);
            value.push(nameid);
        	// console.log(value);
        	b = value.join("-");
        	console.log(b);
			//创建异步对象
			var xhr = new XMLHttpRequest();
			//设置请求的类型及url
			//post请求一定要添加请求头才行不然会报错

			xhr.open('post', 'jiesuan');
			xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");
			xhr.onreadystatechange = function () {
			    // 这步为判断服务器是否正确响应
			  if (xhr.readyState == 4 && xhr.status == 200) {
			    alert(xhr.responseText);
			    location.reload();
			    // alert(responseText);
			  }
			};

			//发送请求
			xhr.send("dxt="+b);
			// xhr.send("dxt=xxxx");
// ppppppppppppppppppppppppppppppppppppppppppppppppp

	}
window.onload = function () {

	var table = document.getElementById("cartTable");//购物车表格
	var selectInputs = document.getElementsByClassName("check");//所有勾选框
	var checkAllInputs = document.getElementsByClassName("check-all");//全选框
	var selectedTotal = document.getElementById("selectedTotal");//已选商品数目
	var tr = table.children[1].rows;//每一行的属性
	var priceTotal = document.getElementById("priceTotal");//商品总价
	var deleteAll = document.getElementById("deleteAll");//删除所有商品
	var selectedViewList = document.getElementById("selectedViewList");//浮动层已选商品的列表
	var selected = document.getElementById("selected");//已选商品


	var foot = document.getElementById("foot");

	//更新总数和总价
	// console.log('xxxxxxxxxxxxxxxxxxx');

	function getTotal(){
		var selected = 0; //总数
		var price = 0;  //总价
		var HTMLStr = "";
		for(var i=0;i<tr.length;i++){
			if(tr[i].getElementsByTagName('input')[0].checked){
				selected += parseInt(tr[i].getElementsByTagName('input')[1].value);
				price+= parseFloat(tr[i].cells[4].innerHTML);

				// <div><img src="images/1.jpg"><span>取消选择</span></div>
				HTMLStr+='<div><img src="'+tr[i].getElementsByTagName('img')[0].src+'"><span class="del" index="'+i+'">取消选择</span></div>'
			}

		}
		selectedTotal.innerHTML = selected;
		priceTotal.innerHTML =price.toFixed(2);
		selectedViewList.innerHTML =HTMLStr;

		//当没有商品的时候 我们不需要浮动层
		if(selected==0){
			foot.className="foot";
		}
		// console.log(price);

	}

	//计算单行价格
	function getSubtotal(tr){
		var cells = tr.cells;
		var price = cells[2];//单价
		var subTotal =cells[4]//单行小计
		var countInput = tr.getElementsByTagName('input')[1];//数目的input
		var span = tr.getElementsByTagName('span')[1]//-号
		//写入结果
		subTotal.innerHTML = (parseInt(countInput.value)*parseFloat(price.innerHTML)).toFixed(2);
		//每次用户操作一次 我们都要判断一下 减号是否可用
		if(countInput.value==1){
			span.innerHTML ="";
		}else{
			span.innerHTML ="-";
		}
	}
	//点击选择框
	for(var i=0;i<selectInputs.length;i++){
		selectInputs[i].onclick=function(){
			if(this.className.indexOf("check-all")>=0){//全选状态
				//把所有的选择框全勾选中
				for(var j=0;j<selectInputs.length;j++){
					selectInputs[j].checked = this.checked;
				}
			}
			//只要有一个未勾选,取消全选框
			if(!this.checked){
				for(var i=0;i<checkAllInputs.length;i++){
					checkAllInputs[i].checked = false;
				}
			}
			getTotal();//选完更新总计
		}
	}
	//显示已选商品的弹出层
	selected.onclick=function(){
		if(selectedTotal.innerHTML!=0){
			foot.className = (foot.className=='foot'?'foot show':'foot');
		}

	}

	//取消选择的按钮
	selectedViewList.onclick=function(e){
		//以后点击span或者其他无点击事件的标签 就这么写
		var e = e||window.event;//让e变成一个可以操作的window.event独享
		var el = e.target||e.srcElement;//通过实践对象的target属性获取触发元素
		if(el.className=='del'){
			var input = tr[el.getAttribute('index')].getElementsByTagName('input')[0];
			input.checked = false;
			input.onclick();
		}
	}
	//常见的切换两种状态的方式


		for(var i= 0;i<tr.length;i++){
			tr[i].onclick = function(e){//e就是我们要操作的对象
				var e = e||window.event;//让e变成一个可以操作的window.event独享
				var el = e.target||e.srcElement;//通过实践对象的target属性获取触发元素
				var cls = el.className;//给span去赋予 点击事件
				var countInput = this.getElementsByTagName('input')[1];
				var value = parseInt(countInput.value);//数目
				switch(cls){
					case 'add'://点击了加好
					countInput.value = value+1;
					getSubtotal(this);
					break;
					case 'reduce'://点击了减号
						if(value>1){
							countInput.value = value-1;
							getSubtotal(this);
						}
					break;
					case 'delete'://点击删除按钮
					var conf = confirm("确定删除此商品么?");
					if(conf){
						//咱们要通过父控件删除该内容 但是怎么找父控件呢?
						this.parentNode.removeChild(this);
					}
					break;

				}
				getTotal();
			}

			//给数目输入框这里加一个keyup事件
			tr[i].getElementsByTagName('input')[1].onkeyup=function(){
				var val =parseInt(this.value);
				if(isNaN(val)||val<=0){
					val = 1;
				}
				if(this.value!=val){
					this.value=val;
				}

				getTotal();//更新总数
			}
		}
		//点击删除指定对象
		deleteAll.onclick=function(){
				if(selectedTotal.innerHTML!=0){
					var conf = confirm("确定删除指定商品吗?");
					if(conf){
						for(var i=0;i<tr.length;i++){
							if(tr[i].getElementsByTagName("input")[0].checked){
								//删除了第一个条目的是时候 我们下一个要删除的条目变成了tr[1]
								tr[i].parentNode.removeChild(tr[i]);
								i--;//把新的i坐标给新的对象
							}
						}
					}
				}else{
					alert("请选择要删除的商品");

				}
				getTotal();//更新总数
		}
		checkAllInputs[0].checked=true;
		checkAllInputs[0].onclick();

}









