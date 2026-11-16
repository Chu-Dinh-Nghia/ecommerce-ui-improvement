let divToGet=null;
window.addEventListener('load',function(){
 divToGet=document.getElementById('div1');
 console.log('DOM đã tải; div1.innerHTML =',divToGet.innerHTML);
 document.getElementById('show').addEventListener('click',function(){
  document.getElementById('result').textContent='Đọc sau load: '+divToGet.innerHTML;
 });
});
