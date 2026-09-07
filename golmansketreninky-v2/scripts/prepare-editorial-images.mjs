import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';
const root = fileURLToPath(new URL('../', import.meta.url));
const assets = JSON.parse(await fs.readFile(path.join(root,'content/editorial-assets.json'),'utf8'));
let cursor=0, created=0;
await Promise.all(Array.from({length:4},async()=>{
  while(cursor<assets.length){
    const item=assets[cursor++],target=path.resolve(root,item.target);
    try{await fs.access(target);continue;}catch{}
    await fs.mkdir(path.dirname(target),{recursive:true});
    await sharp(path.resolve(root,item.source)).rotate().resize({width:1600,withoutEnlargement:true}).webp({quality:80}).toFile(target);created++;
  }
}));
console.log(`Připraveno ${created} nových obrázků; ${assets.length} položek v manifestu.`);
