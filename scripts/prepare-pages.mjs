import { readFile, readdir, writeFile } from 'node:fs/promises';
import { extname, join } from 'node:path';

const [directory, basePath] = process.argv.slice(2);

if (!directory || !basePath) {
  throw new Error('Usage: node scripts/prepare-pages.mjs <dist-directory> <base-path>');
}

async function rewrite(directoryPath) {
  const escapedBasePath = basePath
    .replace(/^\/+/, '')
    .replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const rootRelativeHtmlAttribute = new RegExp(`\\b(href|src|poster|action|content)=(["'])/(?!/|${escapedBasePath}/)`, 'g');
  const rootRelativeCssUrl = new RegExp(`url\\(\\s*(["']?)/(?!/|${escapedBasePath}/)`, 'g');

  for (const entry of await readdir(directoryPath, { withFileTypes: true })) {
    const entryPath = join(directoryPath, entry.name);
    if (entry.isDirectory()) {
      await rewrite(entryPath);
      continue;
    }
    const extension = extname(entry.name);
    if (!['.html', '.css'].includes(extension)) continue;

    const source = await readFile(entryPath, 'utf8');
    const output = extension === '.html'
      ? source.replace(rootRelativeHtmlAttribute, `$1=$2${basePath}/`)
      : source.replace(rootRelativeCssUrl, `url($1${basePath}/`);

    if (output !== source) await writeFile(entryPath, output);
  }
}

await rewrite(directory);
