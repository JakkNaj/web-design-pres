export const pages = [
  { id: 'about', slug: 'o-nas', title: 'O nás', description: 'Privátní mobilita. Osobní servis. Poznejte KNOKAR, naši filozofii a hodnoty.' },
  { id: 'short', slug: 'kratkodoby-pronajem', title: 'Krátkodobý pronájem', description: 'Vůz luxusní značky pro dobu, kdy ho potřebujete.' },
  { id: 'long', slug: 'dlouhodoby-pronajem', title: 'Dlouhodobý pronájem', description: 'Full service plus spojuje dlouhodobý pronájem vozidla s komplexním servisem.' },
  { id: 'finance', slug: 'financni-servis', title: 'Finanční servis', description: 'Potřebujete poradit s individuálním nastavením financování? Ozvěte se našemu obchodnímu týmu.' },
  { id: 'fleet', slug: 'vozovy-park', title: 'Vozový park', description: 'Prohlédněte si vybrané vozy z naší nabídky. Dostupnost a podmínky konkrétního vozu s vámi rádi projdeme osobně.' },
  { id: 'news', slug: 'aktuality', title: 'Aktuality', description: 'Ze světa KNOKAR' },
  { id: 'contact', slug: 'kontakt', title: 'Kontakt', description: 'Napište nám. Ozveme se vám a osobně s vámi projdeme dostupné možnosti.' },
] as const;

export type PageId = typeof pages[number]['id'] | 'vehicle';
