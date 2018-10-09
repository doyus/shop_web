window.onload=function(){
    var fl=document.getElementsByClassName('fl');
var ul=document.getElementById("ul");
var li=ul.getElementsByTagName('li');
var span=ul.getElementsByTagName("span");
window.addEventListener("scroll",function(){
    var scrollTop=document.documentElement.scrollTop||window.pageYOffset||document.body.scrollTop;
    console.log(scrollTop)
    if(scrollTop>=1250){
        ul.parentNode.style.display="block";
    }
    if(scrollTop<650){
        ul.parentNode.style.display="none";
    }
    for(i in fl){
        if(fl[i].offsetTop-scrollTop>-760){
            that=span[i];
            for(var j=0;j<span.length;j++){
                if (span[j]!=that) {
                    span[j].style.display="none"
                }
            }
            span[i].style.display="block";
            return false
        }
    }
},0)


for(var i=0;i<li.length;i++){
    (function(index){
        li[index].addEventListener("mouseover",function(){
            span[index].style.display="block";
        },false)
    })(i)
}
for(var i=0;i<li.length;i++){
    (function(index){
        li[index].addEventListener("click",function(){
            span[index].style.display="block";
            document.documentElement.scrollTop=index*760+1300;
        },false)
    })(i)
}
for(var i=0;i<li.length;i++){
    (function(index){
        li[index].addEventListener("mouseout",function(){
            span[index].style.display="none";
        },false)
    })(i)
}

// var con1 = document.getElementById('con1');
// var con2 = document.getElementById('con2');
// var con3 = document.getElementById('con3');
// var con4 = document.getElementById('con4');
var con = document.getElementsByClassName('slider-item ');
for(var i=0;i<con.length;i++){
    (function(index){
        li[index].addEventListener("click",function(){
            console.log('aaaaaaaaaaaaaaaa');
            // con[index].style.backgroundImage = a[index]
        },false)
    })(i)
}

}