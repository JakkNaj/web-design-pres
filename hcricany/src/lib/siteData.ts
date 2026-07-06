export const navItems = [
  { label: 'Úvod', href: '/' },
  { label: 'Klub', href: '/klub/' },
  { label: 'Nábor', href: '/nabor/' },
  { label: 'Mládež', href: '/mladez/' },
  { label: 'Aktuality', href: '/aktuality/' },
  { label: 'Fotogalerie', href: '/fotogalerie/' },
  { label: 'Kontakt', href: '/kontakt/' },
];

export const clubStats = [
  { value: '120+', label: 'dětí v klubu' },
  { value: '4', label: 'kategorie mládeže' },
  { value: '12', label: 'trenérů a vedoucích' },
];

export const recruitmentFacts = ['Od 4 let', 'Výbavu půjčíme', 'První měsíc na zkoušku'];

export const recruitmentSteps = [
  {
    title: 'Napište nám nebo přijďte na stadion',
    text: 'Domluvíme první trénink podle věku dítěte a aktuální skupiny.',
  },
  {
    title: 'Výstroj na první vyzkoušení půjčíme',
    text: 'Stačí teplé oblečení, rukavice a chuť zkusit led.',
  },
  {
    title: 'Rodičům vše vysvětlíme na místě',
    text: 'Probereme tréninky, příspěvky, vybavení i další postup.',
  },
];

export const coaches = [
  { initials: 'MF', name: 'Martin Frolík', role: 'trenér HC Říčany 2009' },
  { initials: 'OL', name: 'Ondřej Lechner', role: 'trenér HC Říčany 2010' },
  { initials: 'JJ', name: 'Jan Jakubec', role: 'trenér HC Říčany 2011/2012' },
];

export const galleryAlbums = [
  {
    title: 'Týden hokeje v COM-SYS ICE ARENĚ',
    meta: '25. 9. 2025 · 34 fotek',
    image: '/images/navrh01/ricany_kids.jpg',
  },
  {
    title: 'První tréninky nejmenších',
    meta: '12. 4. 2026 · 18 fotek',
    image: '/images/navrh01/ricany_girl.jpg',
  },
  {
    title: 'Turnaj mladších žáků',
    meta: '8. 3. 2026 · 22 fotek',
    image: '/images/navrh01/ricany_boy.jpg',
  },
  {
    title: 'Zázemí klubu a kabiny',
    meta: '12. 5. 2026 · 26 fotek',
    image: '/images/navrh01/ricany_room.jpg',
  },
  {
    title: 'Náborové odpoledne',
    meta: 'únor 2026 · 12 fotek',
    image: '/images/navrh01/ricany_kids.jpg',
  },
  {
    title: 'Vánoční bruslení',
    meta: '21. 12. 2025 · 40 fotek',
    image: '/images/navrh01/ricany_girl.jpg',
  },
];

export const contactPeople = [
  { label: 'Nábor a školička', name: 'Martin Frolík', email: 'nabor@hcricany.cz', phone: '+420 604 123 456' },
  { label: 'Mládežnické kategorie', name: 'Ondřej Lechner', email: 'mladez@hcricany.cz', phone: '+420 604 234 567' },
  { label: 'Vedení klubu', name: 'HC Říčany', email: 'info@hcricany.cz', phone: '+420 604 345 678' },
];

export const legalInfo = [
  'HC Říčany, z.s.',
  'IČO 044 12 358',
  'spolek vedený u Městského soudu v Praze',
  'sídlo: Černokostelecká 2050, 251 01 Říčany',
];

export function formatDate(date: Date) {
  return new Intl.DateTimeFormat('cs-CZ', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  }).format(date);
}

export function formatShortDate(date: Date) {
  return new Intl.DateTimeFormat('cs-CZ', {
    day: 'numeric',
    month: 'short',
  }).format(date).replace('.', '').toUpperCase();
}
