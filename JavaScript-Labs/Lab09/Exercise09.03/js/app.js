document.getElementById('add').addEventListener('click',()=>{
 const p=document.createElement('p');
 p.appendChild(document.createTextNode('Nội dung này được tạo bằng document.createTextNode()'));
 document.getElementById('first').appendChild(p);
 document.getElementById('status').textContent='Đã thêm p node. Mở Inspect → Elements để xem cấu trúc DOM.';
});
document.getElementById('remove').addEventListener('click',()=>{
 const item=document.getElementById('deleteThisOne');
 if(item){document.getElementById('iconList').removeChild(item);document.getElementById('status').textContent='Đã xóa li#deleteThisOne.';}
 else document.getElementById('status').textContent='Mục này đã được xóa.';
});
