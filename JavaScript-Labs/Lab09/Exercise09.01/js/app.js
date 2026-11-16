const msg=document.getElementById('msgArea');
document.querySelectorAll('[data-action]').forEach(button=>button.addEventListener('click',()=>{
 const action=button.dataset.action;
 if(action==='id') msg.value='Đã chọn textarea theo ID: '+msg.id;
 if(action==='inner'){document.getElementById('pageTitle').innerHTML='Tiêu đề mới';msg.value='pageTitle.innerHTML đã được cập nhật';}
 if(action==='html') msg.value=document.getElementById('first').innerHTML;
 if(action==='text') msg.value=document.getElementById('first').innerText;
 if(action==='attr') msg.value='Class của textarea là '+msg.getAttribute('class');
 if(action==='tag') document.getElementsByTagName('textarea')[0].value='Đã chọn bằng tag name';
 if(action==='spans') msg.value=[...document.getElementsByTagName('span')].map(x=>x.innerText).join('\n');
 if(action==='class') msg.value=[...document.getElementsByClassName('count-number')].map(x=>x.innerText).join('\n');
 if(action==='query') msg.value=document.querySelector('#first p').innerHTML;
 if(action==='all') msg.value=[...document.querySelectorAll('#first p')].map(x=>x.innerHTML).join('\n');
 if(action==='hidden') msg.classList.toggle('hidden');
 if(action==='style') document.getElementById('features').style.backgroundColor='#b7efc5';
 if(action==='reset'){location.reload();}
}));
