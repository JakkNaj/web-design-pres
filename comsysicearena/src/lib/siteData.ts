export type NavItem = {
  label: string;
  href: string;
  primary?: boolean;
};

export const formatDate = (date: Date | string) =>
  new Intl.DateTimeFormat('cs-CZ', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  }).format(new Date(date));

export type ServiceItem = {
  title: string;
  label: string;
  text: string;
  href: string;
};

export type PublicSkatingDate = {
  day: string;
  date: string;
  time: string;
  surface: string;
};

export type NewsTeaserItem = {
  title: string;
  slug: string;
  date: string;
  excerpt: string;
  category: string;
};

export type VirtualTourItem = {
  label: string;
  title: string;
  text: string;
  href: string;
  embedSrc: string;
};

export type ArenaFeatureItem = {
  label: string;
  title: string;
  text: string;
};

export type ArenaStatementItem = {
  name: string;
  role: string;
  text: string;
};

export type AdvertisingOffer = {
  title: string;
  text: string;
  email: string;
};

export const site = {
  name: 'COM-SYS ICE ARENA',
  subline: 'Zimní stadion Říčany',
  description: 'Moderní ledová aréna v Říčanech se dvěma ledovými plochami, veřejným bruslením, pronájmem ledu a zázemím pro sport i akce.',
  email: 'info@comsysicearena.cz',
  gatePhone: '+420 737 144 990',
  ccmPhone: '+420 321 022 380',
  ccmServicePhone: '+420 720 056 960',
  eventsPhone: '+420 737 268 000',
  address: 'Škroupova 2625, 251 01 Říčany',
  mapEmbedUrl: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3422.2473757939406!2d14.657971684892274!3d49.988216597019616!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x470b895ab9a1e993%3A0x145e52140db0c781!2sComSys%20Ice%20Arena!5e1!3m2!1scs!2scz!4v1783417188274!5m2!1scs!2scz',
  ccmShopUrl: 'https://www.stridasport.cz/cs/module/ups_storesgroups/store?id_store=9',
  restaurantMapsUrl: 'https://www.google.com/maps/place/%C5%98%C3%AD%C4%8Dansk%C3%BD+long%C3%A1l/@49.988565,14.655938,1213m/data=!3m1!1e3!4m15!1m8!3m7!1s0x470b895644d1fa21:0x1b9cf1cb889cc05e!2zxZjDrcSNYW5za8O9IGxvbmfDoWw!8m2!3d49.9885616!4d14.6585183!10e9!16s%2Fg%2F11l2ls61vn!3m5!1s0x470b895644d1fa21:0x1b9cf1cb889cc05e!8m2!3d49.9885616!4d14.6585183!16s%2Fg%2F11l2ls61vn?entry=ttu&g_ep=EgoyMDI2MDYyOS4wIKXMDSoASAFQAw%3D%3D',
  fitnessUrl: 'https://icearenafitness.eu/',
  reservationFormUrl: '/rozpis-a-rezervace/#rezervace',
  hcRicanyUrl: 'https://www.hcricany.cz/',
  hcRicanyRecruitmentUrl: 'https://www.hcricany.cz/nabor/',
  virtualTourUrl: 'https://www.google.com/maps/@49.9885131,14.6581759,3a,82.2y,106.27h,88.23t/data=!3m8!1e1!3m6!1sAF1QipOzfSp3pTTeNzhhN46gLd5Z0-DnwZVXOGKsihw!2e10!3e12!6shttps:%2F%2Flh3.googleusercontent.com%2Fp%2FAF1QipOzfSp3pTTeNzhhN46gLd5Z0-DnwZVXOGKsihw%3Dw900-h600-k-no-pi1.769999999999996-ya89.23193313598632-ro0-fo100!7i9424!8i4712?entry=ttu&g_ep=EgoyMDI2MDYyOS4wIKXMDSoASAFQAw%3D%3D',
};

export const advertisingOffer: AdvertisingOffer = {
  title: 'Reklamní plochy v aréně',
  text: 'Nabízíme reklamní plochy na mantinelech, ledové ploše a prostor pro bannery na vnitřních stěnách haly.',
  email: site.email,
};

export const virtualTours: VirtualTourItem[] = [
  {
    label: 'Velká ledová plocha',
    title: 'Hlavní ledová plocha',
    text: '360° Google Street View prohlídka hlavní plochy pro veřejné bruslení, zápasy, tréninky i pronájem ledu.',
    href: site.virtualTourUrl,
    embedSrc: 'https://www.google.com/maps/embed?pb=!4v0!6m8!1m7!1sAF1QipOzfSp3pTTeNzhhN46gLd5Z0-DnwZVXOGKsihw!2m2!1d49.9885131!2d14.6581759!3f89.23193313598632!4f1.769999999999996!5f0.7820865974627469',
  },
  {
    label: 'Malá ledová plocha',
    title: 'Malá říčanská nudle',
    text: '360° prohlídka menší tréninkové plochy vhodné pro individuální tréninky, gólmany a menší skupiny.',
    href: 'https://www.google.com/maps/@49.988422,14.6585366,3a,82.2y,247.24h,79.75t/data=!3m8!1e1!3m6!1sAF1QipMBbVFGzCNWegrGxRDPxXf8fYYWnoMxcoUTtIQ!2e10!3e12!6shttps:%2F%2Flh3.googleusercontent.com%2Fp%2FAF1QipMBbVFGzCNWegrGxRDPxXf8fYYWnoMxcoUTtIQ%3Dw900-h600-k-no-pi10.253700753088253-ya289.115341402481-ro0-fo100!7i9424!8i4712?entry=ttu&g_ep=EgoyMDI2MDYyOS4wIKXMDSoASAFQAw%3D%3D',
    embedSrc: 'https://www.google.com/maps/embed?pb=!4v0!6m8!1m7!1sAF1QipMBbVFGzCNWegrGxRDPxXf8fYYWnoMxcoUTtIQ!2m2!1d49.988422!2d14.6585366!3f289.115341402481!4f10.253700753088253!5f0.7820865974627469',
  },
  {
    label: 'Zázemí arény',
    title: 'Šatna',
    text: '360° prohlídka šatny a zázemí pro týmy, tréninky i pronájmy ledu.',
    href: 'https://www.google.com/maps/@49.9887076,14.6581878,0a,82.2y,106.27h,88.23t/data=!3m4!1e1!3m2!1sAF1QipN3NVcz4Yrf0BQDLTXkRBA2-nyEAFiobjIS97s!2e10?source=apiv3',
    embedSrc: 'https://www.google.com/maps/embed?pb=!4v0!6m8!1m7!1sAF1QipN3NVcz4Yrf0BQDLTXkRBA2-nyEAFiobjIS97s!2m2!1d49.9887076!2d14.6581878!3f106.27!4f0!5f0.7820865974627469',
  },
];

export const arenaFeatures: ArenaFeatureItem[] = [
  {
    label: 'Zázemí haly',
    title: '8 moderních šaten a suchá příprava',
    text: 'Prostorné šatny doplňuje malá tělocvična pro předzápasový strečink, kompenzační cvičení a posílení stabilizačního systému hokejistů každého věku.',
  },
  {
    label: 'Velká plocha',
    title: 'Kanadsko-americké NHL rozměry',
    text: 'Hlavní plocha odpovídá modernímu světovému trendu. Menší rozměr dělá hru rychlejší, kontaktnější a pro diváky atraktivnější.',
  },
  {
    label: 'Malá říčanská nudle',
    title: 'Kamera, LED obrazovka a trénink 3 na 3',
    text: 'Malá plocha má kamerový systém pro gólmany i okamžitý rozbor střelby. Obraz se přenáší na LED obrazovku u mantinelů a plocha je vhodná pro individuální tréninky i formát 3 na 3.',
  },
];

export const arenaStatements: ArenaStatementItem[] = [
  {
    name: 'Martin Altrichter',
    role: 'majitel COM-SYS Ice Areny',
    text: 'Postavil jsem pro Vás v Říčanech nejmodernější tréninkovou halu v ČR, která bude otevřena 365 dnů v roce. Výstavbě zimního stadionu jsem věnoval několik let svého života a věřím, že se mi podařilo vybudovat to nejlepší, co si takové město, jako Říčany, zaslouží. Ti z Vás, kteří náš říčanský zimní stadion už navštívili, mě tu mohou vidět od rána do večera. Dávám maximum tomu, abyste byli se všemi službami stadionu maximálně spokojeni.',
  },
  {
    name: 'Tomáš Kucharčík',
    role: 'hokejový útočník, mistr světa 1999',
    text: 'S Martinem jsme dlouholetí kamarádi a jako trenér mládežnických ročníků HC Slavic Praha jsem uvítal možnost využívat služeb zimního stadionu v Říčanech k individuálním tréninkům svých svěřenců. Myslím, že se Martinovi podařilo vybudovat ledové plochy opravdu světové úrovně, a to včetně často opomíjené kvality šaten, míst pro veškerou suchou přípravu a veškerého zázemí.',
  },
];

export const navItems: NavItem[] = [
  { label: 'Úvod', href: '/' },
  { label: 'Veřejné bruslení', href: '/verejne-brusleni/' },
  { label: 'Rozpis a rezervace', href: '/rozpis-a-rezervace/' },
  { label: 'Služby', href: '/sluzby/' },
  { label: 'Ceník', href: '/cenik/' },
  { label: 'Virtuální prohlídka', href: '/virtualni-prohlidka/' },
  { label: 'Akce a pronájem', href: '/akce-a-pronajem/' },
  { label: 'Kontakt', href: '/kontakt/' },
];

export const quickLinks = [
  {
    marker: 'DNES',
    label: 'Veřejné bruslení',
    title: 'Nejbližší termíny',
    text: 'vstupné, půjčovna a pravidla',
    href: '/verejne-brusleni/',
    tone: 'teal',
  },
  {
    marker: 'LED',
    label: 'Rozpis a rezervace',
    title: 'Pronájem ledu',
    text: 'velká i malá plocha',
    href: '/rozpis-a-rezervace/',
    tone: 'blue',
  },
  {
    marker: "15'",
    label: 'Kontakt a parkování',
    title: 'Jak se k nám dostanete',
    text: 'adresa, mapa a telefon',
    href: '/kontakt/',
    tone: 'dark',
  },
];

export const publicSkatingDates: PublicSkatingDate[] = [
  { day: 'Sobota', date: '11. 7. 2026', time: '09:00-10:30', surface: 'Velká ledová plocha' },
  { day: 'Sobota', date: '18. 7. 2026', time: '09:00-10:30', surface: 'Velká ledová plocha' },
  { day: 'Sobota', date: '25. 7. 2026', time: '09:00-10:30', surface: 'Velká ledová plocha' },
];

export const prices = {
  publicSkating: [
    { label: 'Dospělí', value: '120 Kč' },
    { label: 'Děti a mládež do 15 let', value: '60 Kč' },
    { label: 'Doprovod dětí', value: '20 Kč' },
  ],
  rental: [
    { label: 'Velká ledová plocha Po-Pá 6:00-15:00', value: '3 100 Kč / hod.' },
    { label: 'Velká ledová plocha Po-Pá 15:00-24:00', value: '4 500 Kč / hod.' },
    { label: 'Malá ledová plocha Po-Pá 6:00-15:00', value: '1 800 Kč / hod.' },
    { label: 'Malá ledová plocha Po-Pá 15:00-24:00', value: '2 600 Kč / hod.' },
    { label: 'Velká plocha víkend, svátek, červenec/srpen 6:00-8:00', value: '3 100 Kč / hod.' },
    { label: 'Velká plocha víkend, svátek, červenec/srpen 8:00-24:00', value: '4 500 Kč / hod.' },
    { label: 'Malá plocha víkend, svátek, červenec/srpen 6:00-8:00', value: '1 800 Kč / hod.' },
    { label: 'Malá plocha víkend, svátek, červenec/srpen 8:00-24:00', value: '2 600 Kč / hod.' },
  ],
  services: [
    { label: 'Půjčení bruslí', value: '100 Kč' },
    { label: 'Vratná záloha za brusle', value: '500 Kč' },
    { label: 'Školička bruslení', value: '350 Kč / lekce' },
  ],
  parking: [
    { label: 'Do 15 minut', value: 'zdarma' },
    { label: 'První 3 hodiny', value: '20 Kč' },
    { label: 'Každá další započatá hodina', value: '10 Kč' },
    { label: 'Ztráta parkovacího lístku', value: '500 Kč' },
  ],
};

export const cancellationTerms = [
  'Zrušení rezervace v den rezervace až 3 dny před rezervací: 100 % z ceny ledu včetně DPH.',
  'Zrušení rezervace 4 až 10 dní před rezervací: 50 % z ceny ledu včetně DPH.',
  'Zrušení rezervace více než 10 dní před rezervací: 1 000 Kč za velkou plochu a 500 Kč za malou plochu.',
];

export const services: ServiceItem[] = [
  {
    label: 'Led',
    title: 'Dvě ledové plochy',
    text: 'Velká ledová plocha a malá říčanská nudle pro tréninky, zápasy, školy i skupinové bruslení.',
    href: '/rozpis-a-rezervace/',
  },
  {
    label: 'Veřejnost',
    title: 'Veřejné bruslení',
    text: 'Pravidelné termíny pro rodiny i jednotlivce, včetně půjčovny bruslí přímo v aréně.',
    href: '/verejne-brusleni/',
  },
  {
    label: 'Servis',
    title: 'CCM obchod a broušení',
    text: 'Hokejové vybavení, doplňky a broušení bruslí. Otevírací doba Po-Pá 13:00-19:00, So-Ne 10:00-16:00.',
    href: site.ccmShopUrl,
  },
  {
    label: 'Suchá příprava',
    title: 'Tělocvična a fitness',
    text: 'Tělocvična, boxerna a Ice Arena Fitness pro kompenzační cvičení, stabilitu a kondici.',
    href: '/sluzby/',
  },
  {
    label: 'Akce',
    title: 'Turnaje, kempy a firemní akce',
    text: 'Prostor pro sportovní soustředění, rekreační hokej, narozeniny i firemní program na ledě.',
    href: '/akce-a-pronajem/',
  },
  {
    label: 'Děti',
    title: 'Školička bruslení',
    text: 'Školička pro děti od 3 let slouží jako nábor do hokejového a krasobruslařského klubu.',
    href: '/sluzby/',
  },
];

export const audience = [
  { title: 'Veřejnost', text: 'Rodiny a bruslaři, kteří hledají veřejné bruslení, půjčovnu a pohodlné zázemí.', href: '/verejne-brusleni/', cta: 'Veřejné bruslení' },
  { title: 'Hokejisté a trenéři', text: 'Obě ledové plochy dávají prostor pro osobní tréninky hráčů, gólmanů i menších skupin.', href: '/rozpis-a-rezervace/', cta: 'Osobní tréninky a led' },
  { title: 'Firmy a akce', text: 'Organizátoři turnajů, firemních akcí, dětských oslav a kempů.', href: '/akce-a-pronajem/', cta: 'Akce a pronájem' },
  { title: 'Děti a kurzy', text: 'Rodiče dětí, kteří řeší školičku bruslení, nábor nebo individuální tréninky.', href: '/sluzby/', cta: 'Služby a kurzy' },
];

export const eventsAndRentals = [
  'Turnaje mládežnických týmů',
  'Hokejové kempy',
  'Firemní akce na ledě',
  'Dětské oslavy',
  'Rekreační hokej a skupinové bruslení',
];

export const newsTeasers: NewsTeaserItem[] = [
  {
    title: 'Letní termíny veřejného bruslení',
    slug: 'letni-terminy-verejneho-brusleni',
    date: '2026-07-06',
    excerpt: 'Aktuální červencové termíny veřejného bruslení najdete v přehledu a rozpisu ledu.',
    category: 'Veřejné bruslení',
  },
  {
    title: 'Rezervace ledu zůstává jako poptávka',
    slug: 'rezervace-ledu-poptavka',
    date: '2026-07-06',
    excerpt: 'Vybraný termín vždy potvrzuje aréna. Formulář slouží k odeslání poptávky.',
    category: 'Provoz',
  },
  {
    title: 'COM-SYS Ice Arena je domovem HC Říčany',
    slug: 'domov-hc-ricany',
    date: '2026-07-06',
    excerpt: 'Aréna poskytuje zázemí pro klubové tréninky, zápasy i náborové akce.',
    category: 'Aréna',
  },
];

export const partners = [
  { name: 'COM-SYS', url: 'https://www.comsys.cz/' },
  { name: 'HC Říčany', url: site.hcRicanyUrl },
  { name: 'Město Říčany', url: 'https://www.ricany.cz/' },
  { name: 'Gólmanské tréninky', url: 'https://www.golmansketreninky.cz/' },
];

export const documents = [
  { label: 'Zpracování osobních údajů', href: '/dokumenty/zpracovani-osobnich-udaju/' },
  { label: 'Provozní řád COM-SYS ICE ARENA', href: '/dokumenty/provozni-rad/' },
];

export const legacyRedirects = [
  { from: 'hokejova-hala/hokejova-hala', to: '/' },
  { from: 'hokejova-hala/cenik', to: '/cenik/' },
  { from: 'hokejova-hala/virtualni-prohlidka', to: '/virtualni-prohlidka/' },
  { from: 'hokejova-hala/aktuality', to: '/aktuality/' },
  { from: 'hokejova-hala/golmanske-treninky', to: '/sluzby/' },
  { from: 'hokejova-hala/individualni-treninky-hraci', to: '/akce-a-pronajem/' },
  { from: 'hokejova-hala/pro-partnery', to: '/akce-a-pronajem/' },
  { from: 'hokejova-hala/firemni-akce-na-ledu-detske-oslavy', to: '/akce-a-pronajem/' },
  { from: 'verejne-brusleni', to: '/verejne-brusleni/' },
  { from: 'rozpis-ledovych-ploch/rezervace-ledu', to: '/rozpis-a-rezervace/' },
  { from: 'rozpis-ledovych-ploch/velka-ledova-plocha', to: '/rozpis-a-rezervace/' },
  { from: 'rozpis-ledovych-ploch/mala-ledova-plocha-ricanska-nudle', to: '/rozpis-a-rezervace/' },
  { from: 'sluzby/ccm-obchod', to: site.ccmShopUrl },
  { from: 'sluzby/telocvicna-boxerna', to: '/sluzby/' },
  { from: 'kontakty', to: '/kontakt/' },
  { from: 'informace-o-zpracovani-osobnich-udaju-v-com-sys-ice-arena', to: '/dokumenty/zpracovani-osobnich-udaju/' },
  { from: 'provozni-rad-com-sys-ice-arena', to: '/dokumenty/provozni-rad/' },
  { from: 'rekreacni-hrac', to: '/aktuality/rekreacni-hraci-hledaji-tym/' },
  { from: 'nabor-mladych-hokejistu', to: '/sluzby/' },
  { from: 'com-sys-ice-liga-3-na-3', to: '/aktuality/com-sys-ice-liga-3-na-3/' },
  { from: 'olympijsti-vitezove-a-mistri-sveta-v-ricanech', to: '/aktuality/olympijsti-vitezove-a-mistri-sveta-v-ricanech/' },
  { from: 'cs/hokejova-hala/aktuality/256-olympijsti-vitezove-a-mistri-sveta-u-nas-v-ricanech-na-zimnim-stadionu', to: '/aktuality/olympijsti-vitezove-a-mistri-sveta-v-ricanech/' },
  { from: 'hokejova-hala/aktuality/434-com-sys-ice-arenu-navstivili-fotbaliste-sk-slavia', to: '/aktuality/com-sys-ice-arenu-navstivili-fotbaliste-sk-slavia/' },
];

export const futureNewsFields = ['title', 'slug', 'date', 'excerpt', 'image', 'imageStyle', 'gallery', 'category', 'published', 'body'];
