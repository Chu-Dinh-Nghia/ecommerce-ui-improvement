const first=document.getElementById('first');
for(let i=0;i<first.childNodes.length;i++){
 const node=first.childNodes[i];
 console.log('child '+i+' =',node,'nodeType='+node.nodeType);
 if(node.nodeType!==Node.TEXT_NODE && node.nodeType!==Node.COMMENT_NODE) node.classList.add('child-highlight');
}
console.log('firstChild:',first.firstChild,'nextSibling:',first.firstChild.nextSibling,'parentNode:',first.parentNode);
document.getElementById('inspect').addEventListener('click',()=>{
 const nodes=[...first.childNodes];
 document.getElementById('output').textContent=nodes.map((node,i)=>'child '+i+' | nodeType='+node.nodeType+' | '+(node.textContent||'').trim().slice(0,70)).join('\n');
 console.log('parentNode:',first.parentNode);
});
