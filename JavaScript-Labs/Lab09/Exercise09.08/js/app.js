function init(){
 document.getElementById('sampleForm').addEventListener('submit',checkForEmptyFields);
}
window.addEventListener('load',init);
function checkForEmptyFields(e){
 const errorArea=document.getElementById('errors');
 const success=document.getElementById('success');
 errorArea.className='hidden';errorArea.innerHTML='';success.className='result hidden';
 const fields=document.querySelectorAll('input[type=text],input[type=password]');
 const fieldList=[];
 for(let i=0;i<fields.length;i++){
  if(fields[i].value.trim()===''){e.preventDefault();fieldList.push(fields[i]);}
 }
 if(fieldList.length>0){
  e.preventDefault();
  const msg="Các trường sau không được để trống: "+fieldList.map(field=>field.id).join(', ');
  const paragraph=document.createElement('p');paragraph.textContent=msg;
  errorArea.appendChild(paragraph);errorArea.className='visible';
 }else{
  e.preventDefault();success.textContent='Biểu mẫu hợp lệ: tất cả trường đã có dữ liệu.';success.className='result visible';
 }
}
