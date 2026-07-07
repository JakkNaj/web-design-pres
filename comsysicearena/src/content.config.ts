import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const news = defineCollection({
  loader: glob({ base: './src/content/news', pattern: '**/*.md' }),
  schema: z.object({
    title: z.string(),
    slug: z.string().regex(/^[a-z0-9-]+$/),
    date: z.coerce.date(),
    excerpt: z.string(),
    image: z.string().default('/images/news/arena-ledova-plocha.jpg'),
    imageStyle: z.enum(['photo', 'logo']).default('photo'),
    gallery: z.array(z.string()).default([]),
    category: z.string(),
    published: z.boolean().default(false),
  }),
});

export const collections = { news };
