# Gólmanské tréninky · v3

Samostatná tmavá verze Altrichter Goalie Academy. Vychází z obsahu, fotografií a funkcí v2; rozhraní je nově sestavené z Lumos for Astro. V2 zůstává samostatným projektem.

## Spuštění

Node.js 22.12+.

```sh
npm ci
npm run dev -- --background --host 127.0.0.1 --port 4324
```

Náhled: http://127.0.0.1:4324. Správa serveru: `npm run astro -- dev status`, `npm run astro -- dev stop`.

```sh
npm run build
npm test
npm run check:links
```

Pro sestavení pod jinou cestou:

```sh
ASTRO_BASE=/web-design-pres/golmansketreninky-v3 npm run build
python3 scripts/check-built-site.py dist /web-design-pres/golmansketreninky-v3
```

Publikování ani změna nasazovacího workflow není součástí této verze.

## Lumos a vzhled

Výchozí zdroj: [Lumos for Astro](https://github.com/lumosframework/lumos-for-astro), verze a přesný commit v `LUMOS_VERSION.json`. Původní MIT licence je v `LICENSE`; pravidla tvorby komponent v `LUMOS.md`.

- Plná knihovna komponent a tokenů v `src/components` a `src/styles`. Společné importy přes `src/ui.ts`.
- Stránky používají Lumos `Section`, `Grid`, `ContentWrapper`, typografii, `Card`, `Button`, `Accordion`, `Slider`, `Input` a `Select`.
- Úpravy pro akademii v `src/components/academy`. Galerie a ukázková přihláška mají vlastní stavovou logiku a nativní dialogy s Lumos tlačítky.
- Značkové tokeny v `src/styles/academy.css`: tmavý základ `#0a1118`, vyvýšené plochy `#101e29`, ledová modrá `#77cce3`, grepová `#e87780`.
- Globální tmavé téma, lokální variabilní Inter, responzivní typografie a rozestupy z Lumos. Galerie podporuje tlačítka, klávesnici a tažení; ovládací ikony jsou centrované v pevných čtvercových tlačítkách.
- Zachovaná brankářská hra z v2, přebarvená pro tmavé pozadí; její SVG používá vlastní souřadnicový systém.

## Obsah

40 sestavených stránek včetně 404: úvod, kempy a jejich detaily, trenéři, historie, aktuality a galerie. Obsahové kolekce a média pocházejí z v2; nejsou závislé na sourozeneckém adresáři. Redakční pravidla a původ obsahu: `content/EDITORIAL.md`.

Stejně jako v2 jde o ukázkovou prezentaci s `noindex`. Příznaky ukázkových termínů zůstávají v datech; redakční poznámky a označení ukázek se ve veřejném rozhraní na přání nezobrazují. Přihláška se nikam neodesílá, neukládá údaje ani nerezervuje místo. Reálné termíny a nabídku potvrzuje akademie.

## Ověření

- Produkční build a Astro kontrola; kontrola všech místních odkazů, médií, kotev, alt textů a noindex pro kořenovou i vnořenou cestu.
- 9 převzatých testů pravidel termínů a brankářské hry.
- Vizuální kontrola desktopu a mobilů 390 a 320 px; menu, filtr termínů, formulář, accordion, slider a lightbox.

### Vizuální návaznost na v2

Úvod přebírá kompozici v2 s textem vlevo, fotografií vpravo, štítkem a čtyřmi claims. Velikosti nadpisů, FAQ, karet i patičky vycházejí z v2. Programy mají odkazy na fotografiích, trenéři jsou ve dvou sloupcích, historie ukazuje pět milníků a stránka příběhu používá řádky ročníků. Zachované uspořádání brankářské sekce; tmavý dres s dvojitým A, černé betony a barevné odznaky principů.

Vše zůstává složené z Lumos komponent. `Card` přijímá sloty `visual` a `meta` pro fotografii s označením kategorie a datumový řádek. Samostatná galerie na homepage ustoupila sekci článků podle v2; Lumos slider a lightbox zůstávají v detailech kempů a galerií. CTA kempu nahoře má světlý podklad, závěrečná výzva je vystředěná a patička používá 14px kontakty / 12px popisky bez nechtěného podtržení.

### Logo akademie

Ručně překreslená vektorová verze dodané předlohy: `public/brand/aga-emblem.svg`, úplné logo `aga-logo-dark.svg` a `aga-logo-light.svg`. Nápisy úplného loga jsou převedené na křivky. Sdílený `Brand` používá znak se dvěma A a brankářem v hlavičce i patičce; `public/favicon.svg` vychází ze stejné kresby. Kompaktní webová podoba používá vedle znaku čitelný název akademie.
