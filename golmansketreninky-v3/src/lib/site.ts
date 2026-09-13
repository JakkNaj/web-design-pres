import { getCollection } from 'astro:content';
export const contact = { email: 'dotazy@golmansketreninky.cz', address: 'Škroupova 2625/4, Říčany', venue: 'COM-SYS Ice Arena', people: [{ name: 'Martin Altrichter', phone: '+420 737 268 000', tel: '+420737268000' }, { name: 'Marek Zapletal', phone: '+420 603 118 008', tel: '+420603118008' }] };
export const url = (path = '') => `${import.meta.env.BASE_URL.replace(/\/$/, '')}/${path.replace(/^\//, '')}`;
export const campUrl = (id: string) => url(`kempy/${id}/`);
export const articleUrl = (id: string) => url(`aktuality/${id}/`);
export const galleryUrl = (id: string) => url(`galerie/${id}/`);

export async function siteContent() {
  const [camps, sessions, galleries, articles, coaches, partners] = await Promise.all([
    getCollection('camps', x => !x.data.draft), getCollection('sessions', x => !x.data.draft),
    getCollection('galleries', x => !x.data.draft), getCollection('articles', x => !x.data.draft), getCollection('coaches'), getCollection('partners'),
  ]);
  const maps = { camps: new Map(camps.map(x => [x.id, x])), galleries: new Map(galleries.map(x => [x.id, x])), coaches: new Map(coaches.map(x => [x.id, x])) };
  for (const c of camps) {
    if (c.data.gallery && !maps.galleries.has(c.data.gallery.id)) throw new Error(`Kemp ${c.id}: chybí publikovaná galerie.`);
    if (c.data.gallery && maps.galleries.get(c.data.gallery.id)?.data.camp?.id !== c.id) throw new Error(`Kemp ${c.id}: galerie musí odkazovat zpět na tento ročník.`);
    for (const coach of c.data.coaches) if (!maps.coaches.has(coach.id)) throw new Error(`Kemp ${c.id}: neznámý trenér ${coach.id}.`);
  }
  for (const item of [...galleries, ...articles]) if (item.data.camp && !maps.camps.has(item.data.camp.id)) throw new Error(`${item.id}: chybí publikovaný kemp.`);
  for (const article of articles) if (article.data.gallery && !maps.galleries.has(article.data.gallery.id)) throw new Error(`${article.id}: chybí publikovaná galerie.`);
  return { camps: camps.sort((a,b) => (a.data.start ?? '9999').localeCompare(b.data.start ?? '9999')), sessions: sessions.sort((a,b) => a.data.start.localeCompare(b.data.start)), galleries, articles: articles.sort((a,b) => b.data.date.localeCompare(a.data.date)), coaches: coaches.sort((a,b) => a.data.order-b.data.order), partners: partners.sort((a,b) => a.data.order-b.data.order), galleryMap: maps.galleries };
}
