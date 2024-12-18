"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.openDb = openDb;
exports.initDb = initDb;
exports.getPodcasts = getPodcasts;
exports.getPodcast = getPodcast;
exports.createPodcast = createPodcast;
const sqlite3 = __importStar(require("sqlite3"));
const sqlite_1 = require("sqlite");
const fs = __importStar(require("fs/promises"));
const path = __importStar(require("path"));
// 创建数据库连接
async function openDb() {
    return (0, sqlite_1.open)({
        filename: path.resolve(process.cwd(), 'podcast.db'),
        driver: sqlite3.Database
    });
}
// 初始化数据库
async function initDb() {
    const db = await openDb();
    // 读取并执行 SQL 文件
    const createTables = await fs.readFile(path.resolve(process.cwd(), 'sqls/sqlite/01_create_tables.sql'), 'utf-8');
    const createTriggers = await fs.readFile(path.resolve(process.cwd(), 'sqls/sqlite/02_create_triggers.sql'), 'utf-8');
    await db.exec(createTables);
    await db.exec(createTriggers);
    return db;
}
// 数据库操作函数
async function getPodcasts() {
    const db = await openDb();
    try {
        return await db.all('SELECT * FROM podcasts ORDER BY latest_episode_at DESC');
    }
    finally {
        await db.close();
    }
}
async function getPodcast(id) {
    const db = await openDb();
    try {
        return await db.get('SELECT * FROM podcasts WHERE id = ?', id);
    }
    finally {
        await db.close();
    }
}
async function createPodcast(podcast) {
    const db = await openDb();
    try {
        const result = await db.run(`
      INSERT INTO podcasts (
        title, description, cover_url, level, category,
        language, author, rss_url, website_url, status
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `, [
            podcast.title,
            podcast.description,
            podcast.cover_url,
            podcast.level,
            podcast.category,
            podcast.language,
            podcast.author,
            podcast.rss_url,
            podcast.website_url,
            podcast.status || 'active'
        ]);
        return result.lastID;
    }
    finally {
        await db.close();
    }
}
