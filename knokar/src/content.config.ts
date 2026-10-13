import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';
const vehicles = defineCollection({
  loader: glob({ pattern: '*.json', base: './src/content/vehicles' }),
  schema: ({ image }) => z.object({
    order: z.number(), name: z.string(), photo: image(), alt: z.string(),
    position: z.string(), specs: z.array(z.string()),
  }),
});
export const collections = { vehicles };
