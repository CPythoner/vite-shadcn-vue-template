"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const db_1 = require("../src/lib/db");
async function main() {
    try {
        const db = await (0, db_1.initDb)();
        console.log('Database initialized successfully');
        await db.close();
    }
    catch (error) {
        console.error('Failed to initialize database:', error);
        process.exit(1);
    }
}
main();
