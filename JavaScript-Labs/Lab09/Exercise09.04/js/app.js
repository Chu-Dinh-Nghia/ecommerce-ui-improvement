const btn=document.getElementById('testButton');
const content=document.getElementById('content');
function simpleHandler(){
 if(btn.textContent==='Hide'){
  btn.textContent='Show';content.className='makeItDisappear';
  window.setTimeout(()=>{content.style.display='none';},1000);
 }else{
  btn.textContent='Hide';content.style.display='block';content.className='makeItDisappear';
  window.setTimeout(()=>{content.className='makeItNormal';},20);
 }
}
btn.addEventListener('click',simpleHandler);
const img=document.getElementById('mainImage');
img.addEventListener('mouseover',()=>{img.className='makeItGray';});
img.addEventListener('mouseout',()=>{img.className='makeItNormal';});
