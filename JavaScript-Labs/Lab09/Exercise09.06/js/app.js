window.addEventListener('load',function(){
 const divs=document.querySelectorAll('.movingDiv');
 for(let i=0;i<divs.length;i++){
  divs[i].addEventListener('mouseover',function(e){
   // BREAKPOINT: đặt điểm dừng ở dòng dưới để kiểm tra e và e.target trong DevTools.
   const triggeredBy=e.target.id;
   console.log('triggered by '+triggeredBy,e,e.target);
   document.getElementById('eventOutput').textContent='Sự kiện mouseover được kích hoạt bởi '+triggeredBy;
  });
 }
});
