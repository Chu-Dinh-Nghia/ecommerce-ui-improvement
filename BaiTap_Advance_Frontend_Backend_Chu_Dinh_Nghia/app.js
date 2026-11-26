let tasks = [];
const form = document.querySelector('#task-form');
const input = document.querySelector('#task-input');
const list = document.querySelector('#task-list');
const filter = document.querySelector('#filter');

async function api(path, options = {}) {
  const response = await fetch(path, {headers: {'Content-Type': 'application/json'}, ...options});
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || 'Yêu cầu thất bại');
  return data;
}
async function refresh() { tasks = await api('/api/tasks'); render(); }
async function change(path, options) {
  try { await api(path, options); await refresh(); }
  catch (error) { alert(error.message); }
}
function render() {
  document.querySelector('#total').textContent = tasks.length;
  document.querySelector('#pending').textContent = tasks.filter(x => !x.done).length;
  document.querySelector('#completed').textContent = tasks.filter(x => x.done).length;
  list.replaceChildren();
  const shown = tasks.filter(x => filter.value === 'all' || (filter.value === 'completed') === x.done);
  const empty = document.querySelector('#empty');
  empty.hidden = shown.length > 0;
  empty.textContent = tasks.length ? 'Không có công việc ở trạng thái này.' : 'Chưa có công việc nào.';
  for (const task of shown) {
    const row = document.createElement('li');
    const check = document.createElement('input');
    check.type = 'checkbox'; check.checked = task.done; check.setAttribute('aria-label', `Hoàn thành: ${task.title}`);
    check.addEventListener('change', () => change(`/api/tasks/${task.id}`, {method: 'PATCH', body: JSON.stringify({done: check.checked})}));
    const title = document.createElement('span');
    title.className = `task-title${task.done ? ' done' : ''}`; title.textContent = task.title;
    const edit = document.createElement('button');
    edit.className = 'secondary'; edit.textContent = 'Sửa'; edit.setAttribute('aria-label', `Sửa: ${task.title}`);
    edit.addEventListener('click', () => {
      const value = prompt('Sửa tên công việc:', task.title);
      if (value === null) return;
      const next = value.trim();
      if (!next || next.length > 120) return alert('Tên công việc phải có từ 1 đến 120 ký tự.');
      change(`/api/tasks/${task.id}`, {method: 'PATCH', body: JSON.stringify({title: next})});
    });
    const remove = document.createElement('button');
    remove.className = 'danger'; remove.textContent = 'Xóa'; remove.setAttribute('aria-label', `Xóa: ${task.title}`);
    remove.addEventListener('click', () => {
      if (confirm(`Xóa công việc "${task.title}"?`)) change(`/api/tasks/${task.id}`, {method: 'DELETE'});
    });
    row.append(check, title, edit, remove); list.append(row);
  }
}
form.addEventListener('submit', async event => {
  event.preventDefault();
  const title = input.value.trim();
  if (!title) return;
  try { await api('/api/tasks', {method: 'POST', body: JSON.stringify({title})}); input.value = ''; await refresh(); input.focus(); }
  catch (error) { alert(error.message); }
});
filter.addEventListener('change', render);
refresh().catch(error => {
  document.querySelector('#empty').textContent = 'Không kết nối được server. Chạy node server.js rồi mở http://localhost:8080.';
  console.error(error);
});
