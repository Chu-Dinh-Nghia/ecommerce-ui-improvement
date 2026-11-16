function setBackground(e){
 if(e.type==='focus') e.target.style.backgroundColor='#FFE393';
 else if(e.type==='blur') e.target.style.backgroundColor='white';
}
window.addEventListener('load',function(){
 const fields=document.querySelectorAll('input[type=text],input[type=password]');
 for(let i=0;i<fields.length;i++){
  fields[i].addEventListener('focus',setBackground);
  fields[i].addEventListener('blur',setBackground);
 }
});
