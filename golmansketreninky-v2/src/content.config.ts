import { defineCollection, reference } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const sources = z.array(z.string().url()).default([]);
const availability = z.enum(['announced', 'open', 'full', 'completed']);
const timed = {
  start: z.string().datetime({ offset: true }).optional(),
  end: z.string().datetime({ offset: true }).optional(),
  availability, demo: z.boolean().default(false), draft: z.boolean().default(false),
};
const loader = (name: string) => glob({ base: `./src/content/${name}`, pattern: '**/*.json' });
const camps = defineCollection({ loader: loader('camps'), schema: z.object({
  title: z.string(), series: z.string(), year: z.number().int(), location: z.string(), venue: z.string(),
  ...timed, summary: z.string(), body: z.array(z.string()), program: z.array(z.string()).default([]),
  practical: z.array(z.string()).default([]), age: z.string().optional(), capacity: z.string().optional(), price: z.string().optional(),
  coaches: z.array(reference('coaches')).default([]), gallery: reference('galleries').optional(), sources,
}).superRefine((data, ctx) => {
  if (data.availability !== 'announced' && (!data.start || !data.end)) ctx.addIssue({ code: 'custom', message: 'Vypsaný kemp musí mít začátek a konec.' });
  if (data.start && data.end && Date.parse(data.end) < Date.parse(data.start)) ctx.addIssue({ code: 'custom', message: 'Konec kempu předchází začátku.' });
}) });
const sessions = defineCollection({ loader: loader('sessions'), schema: z.object({
  title: z.string(), kind: z.enum(['individual', 'group']), ...timed, start: z.string().datetime({ offset: true }), end: z.string().datetime({ offset: true }),
  summary: z.string(), location: z.string(), capacity: z.string(), sources,
}).refine(d => Date.parse(d.end) >= Date.parse(d.start), 'Konec tréninku předchází začátku.') });
const galleries = defineCollection({ loader: loader('galleries'), schema: ({ image }) => z.object({
  title: z.string(), year: z.number().int().optional(), kind: z.enum(['camp', 'training']), camp: reference('camps').optional(),
  coverIndex: z.number().int().nonnegative().default(0), sources, draft: z.boolean().default(false),
  video: z.object({ title: z.string(), file: z.string().regex(/^media\/[a-z0-9-]+\.mp4$/), poster: image(), description: z.string(), source: z.string().url() }).optional(),
  photos: z.array(z.object({ image: image(), alt: z.string().min(1), caption: z.string(), featured: z.boolean().default(false), source: z.string().url() })).min(1),
}).refine(d => d.coverIndex < d.photos.length, 'Titulní fotografie musí být součástí galerie.') });
const articles = defineCollection({ loader: loader('articles'), schema: ({ image }) => z.object({
  title: z.string(), date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/), category: z.enum(['Z kempů', 'Z tréninku', 'Informace']),
  summary: z.string(), body: z.array(z.string()), camp: reference('camps').optional(), gallery: reference('galleries').optional(), cover: image().optional(), coverAlt: z.string().optional(), sources, draft: z.boolean().default(false),
}) });
const coaches = defineCollection({ loader: loader('coaches'), schema: ({ image }) => z.object({
  name: z.string(), order: z.number(), summary: z.string(), intro: z.string(), body: z.array(z.string()),
  credentials: z.array(z.string()), portrait: image().optional(), sources,
}) });
const partners = defineCollection({ loader: loader('partners'), schema: ({ image }) => z.object({
  name: z.string(), order: z.number(), url: z.string().url(), logo: image(), sources,
}) });
export const collections = { camps, sessions, galleries, articles, coaches, partners };
