import { initDb } from '../src/lib/db'

async function main() {
  try {
    const db = await initDb()
    console.log('Database initialized successfully')
    await db.close()
  } catch (error) {
    console.error('Failed to initialize database:', error)
    process.exit(1)
  }
}

main()
