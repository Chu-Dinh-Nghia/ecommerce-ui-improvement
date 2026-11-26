const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const {randomUUID} = require('node:crypto');
const {DatabaseSync} = require('node:sqlite');

const db = new DatabaseSync(process.env.TODO_DB_PATH || path.join(__dirname, 'todo.sqlite'));
db.exec('CREATE TABLE IF NOT EXISTS tasks (id TEXT PRIMARY KEY, title TEXT NOT NULL, done INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL)');
const port = Number(process.env.PORT || 8080);
function json(res, status, value) {
  res.writeHead(status, {'Content-Type': 'application/json; charset=utf-8'});
  res.end(JSON.stringify(value));
}
async function readBody(req) {
  let raw = '';
  for await (const chunk of req) {
    raw += chunk;
    if (raw.length > 10000) throw new Error('Dữ liệu quá lớn');
  }
  try { return JSON.parse(raw || '{}'); }
  catch { throw new Error('JSON không hợp lệ'); }
}
const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://localhost');
  if (req.method === 'GET' && (url.pathname === '/' || url.pathname === '/app.js')) {
    const file = url.pathname === '/' ? 'index.html' : 'app.js';
    res.writeHead(200, {'Content-Type': file.endsWith('.js') ? 'text/javascript; charset=utf-8' : 'text/html; charset=utf-8'});
    fs.createReadStream(path.join(__dirname, file)).pipe(res);
    return;
  }
  try {
    if (url.pathname === '/api/tasks' && req.method === 'GET') {
      const rows = db.prepare('SELECT id, title, done FROM tasks ORDER BY created_at DESC').all();
      return json(res, 200, rows.map(row => ({...row, done: Boolean(row.done)})));
    }
    if (url.pathname === '/api/tasks' && req.method === 'POST') {
      const data = await readBody(req);
      const title = typeof data.title === 'string' ? data.title.trim() : '';
      if (!title || title.length > 120) return json(res, 400, {error: 'Tên công việc phải có từ 1 đến 120 ký tự.'});
      const task = {id: randomUUID(), title, done: false};
      db.prepare('INSERT INTO tasks VALUES (?, ?, 0, ?)').run(task.id, title, new Date().toISOString());
      return json(res, 201, task);
    }
    const match = url.pathname.match(/^\/api\/tasks\/([0-9a-f-]{36})$/);
    if (match && (req.method === 'PATCH' || req.method === 'DELETE')) {
      const id = match[1];
      const old = db.prepare('SELECT id, title, done FROM tasks WHERE id = ?').get(id);
      if (!old) return json(res, 404, {error: 'Không tìm thấy công việc.'});
      if (req.method === 'DELETE') {
        db.prepare('DELETE FROM tasks WHERE id = ?').run(id);
        return json(res, 200, {deleted: true});
      }
      const data = await readBody(req);
      if (data.title === undefined && data.done === undefined) return json(res, 400, {error: 'Thiếu dữ liệu cập nhật.'});
      const title = data.title === undefined ? old.title : typeof data.title === 'string' ? data.title.trim() : '';
      if (!title || title.length > 120 || (data.done !== undefined && typeof data.done !== 'boolean')) return json(res, 400, {error: 'Dữ liệu cập nhật không hợp lệ.'});
      const done = data.done === undefined ? Boolean(old.done) : data.done;
      db.prepare('UPDATE tasks SET title = ?, done = ? WHERE id = ?').run(title, Number(done), id);
      return json(res, 200, {id, title, done});
    }
    json(res, 404, {error: 'Không tìm thấy đường dẫn.'});
  } catch (error) {
    const bad = error.message === 'JSON không hợp lệ' || error.message === 'Dữ liệu quá lớn';
    json(res, bad ? 400 : 500, {error: error.message});
  }
});
server.listen(port, () => console.log(`TODO server running at http://localhost:${port}`));
