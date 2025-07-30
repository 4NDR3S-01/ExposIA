import sqlite3 from 'sqlite3';
import { open } from 'sqlite';

// Inicializa la base de datos y tabla si no existe
async function getDb() {
  const db = await open({
    filename: './agent_results.db',
    driver: sqlite3.Database
  });
  await db.exec(`CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )`);
  return db;
}

// Guarda el resultado en la base de datos
export async function saveResult(content: string) {
  const db = await getDb();
  const res = await db.run('INSERT INTO results (content) VALUES (?)', content);
  return { id: res.lastID, content };
}
