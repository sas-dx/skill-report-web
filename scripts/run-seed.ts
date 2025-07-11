import { fileURLToPath, pathToFileURL } from 'url'
import { dirname, resolve } from 'path'

const __dirname = dirname(fileURLToPath(import.meta.url))
const seedPath = resolve(__dirname, '../src/database/prisma/seed.ts')

async function run() {
  const seedModule = await import(pathToFileURL(seedPath).href)
  if (seedModule.runSampleSeed) {
    await seedModule.runSampleSeed()
  }
}

run()
