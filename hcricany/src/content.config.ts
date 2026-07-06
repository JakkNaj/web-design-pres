import { defineCollection } from 'astro:content';
import { file, glob } from 'astro/loaders';
import { z } from 'astro/zod';

const news = defineCollection({
  loader: glob({ base: './src/content/news', pattern: '**/*.md' }),
  schema: z.object({
    title: z.string(),
    slug: z.string().regex(/^[a-z0-9-]+$/),
    date: z.coerce.date(),
    excerpt: z.string(),
    image: z.string().default('/images/navrh01/ricany_kids.jpg'),
    category: z.string(),
    published: z.boolean().default(false),
  }),
});

const teams = defineCollection({
  loader: glob({ base: './src/content/teams', pattern: '**/*.md' }),
  schema: z.object({
    name: z.string(),
    ageGroup: z.string(),
    description: z.string(),
    image: z.string().default('/images/navrh01/ricany_kids.jpg'),
    contactPerson: z.string(),
    order: z.number().optional(),
    birthYears: z.string().optional(),
    coach: z.string().optional(),
    training: z.string().optional(),
    level: z.string().optional(),
    resultsLink: z.string().optional(),
    rosterLink: z.string().optional(),
  }),
});

const partners = defineCollection({
  loader: file('src/content/data/partners.yaml'),
  schema: z.array(z.object({
    name: z.string(), logo: z.string(), image: z.string().optional(), website: z.string().url(), tier: z.enum(['generalni', 'hlavni', 'partner']),
  })),
});

const events = defineCollection({
  loader: file('src/content/data/events.yaml'),
  schema: z.array(z.object({
    title: z.string(), date: z.coerce.date(), location: z.string(), type: z.string(), link: z.string(),
  })),
});

const settings = defineCollection({
  loader: glob({ base: './src/content/data', pattern: 'settings.yaml' }),
  schema: z.object({
    clubName: z.string(), contactEmail: z.string().email(), address: z.string(),
    socialLinks: z.object({ facebook: z.string().url(), instagram: z.string().url() }),
  }),
});

export const collections = { news, teams, partners, events, settings };
