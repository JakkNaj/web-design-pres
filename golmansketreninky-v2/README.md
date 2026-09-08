# Gólmanské tréninky — koncept 02

Samostatný statický Astro návrh vedle původního `golmansketreninky`: úvod, kempy a jejich ročníky, historie, aktuality, trenéři a galerie.

Pravidla obsahu a postup přidání dalšího ročníku: [content/EDITORIAL.md](content/EDITORIAL.md).

Podklady původního WordPressu jsou v [content/wordpress](content/wordpress/README.md). Pro výběr fotografií a obsahu otevřete [lokální katalog](content/wordpress/index.html); rozdíly před použitím shrnuje [K_REVIZI.md](content/wordpress/K_REVIZI.md).

## Spuštění

```sh
npm ci
npm run dev -- --port 4323
```

`npm run build` spouští Astro kontrolu typů a statický build do `dist/`. `npm run preview` otevře produkční build. Node 22.18+.

## Návrh

Výchozí inspirace: uživatelem dodaný Nike `DESIGN.md`. Na přání uživatele návrh rozvíjí hravější hokejovou identitu: tyrkysovou a červenou z loga akademie, doplňkovou fialovou, natočené štítky a taktické značky. Zachovává velké nadpisy Inter 400/500, černé bloky, ostré hrany fotografií a oválná tlačítka. Úvodní sekce zůstává na desktopu přes celou šířku. Původní černobílá fotografie zachovává celou helmu a skloněnou hlavu brankáře; plynule přechází do černého pozadí pod textem vpravo. Další fotografie zůstávají barevné. Hokejové prvky zahrnují návrh emblému masky, siluetu brankáře, barevné brankoviště, puk a ilustraci masky u FAQ.

Vanilla JavaScript: filtry termínů, předvýběr typu z karet, mobilní menu, lokální demo přihlášky v nativním dialogu. FAQ používá nativní `details`. Komponenta `GoalieSave.astro` animuje vektorového brankáře před brankou s červenými tyčemi a sítí v perspektivě. Střídá záklek do motýlka podle uživatelem dodaného videa, chycení vysoké střely do lapačky včetně zavření rukavice a odražení puku vyrážečkou do strany. Při zákroku vyrážečkou se s rukou pohybuje i hůl. Každý zákrok přes Web Animations API trvá 1,6 sekundy, mezi nimi je 0,9 sekundy klid. Sekvence se automaticky střídají ve viditelné sekci; tlačítko umožňuje pohyb pozastavit a plynule obnovit. Mimo viditelnou sekci nebo při skrytí stránky se animace pozastaví. Při `prefers-reduced-motion` se zobrazí statický záklek. Kliknutí nebo klepnutí na led vypustí vlastní puk; lze použít také Enter nebo mezerník. Čtyři samostatné střely do 900 ms s rozestupy nejvýše 320 ms znamenají gól. Gól doprovází velký nápis a konfety v barvách akademie. Brankář důrazně zavrtí hlavou, rozhodí ruce a bouchne holí; nad hlavou se objeví blesk a vykřičník. Po 2,2 s lze hrát znovu. Pomalé střely chytá střídavě betonem, lapačkou a vyrážečkou. Pozastavení ovládá automatické ukázky, ruční střelba funguje dál. Omezený pohyb zachovává hru se statickou zpětnou vazbou. Fotografie a šipky mají jemné přechody. Prvky pod úvodním viewportem se při scrollování jednou jemně odhalí (600 ms, posun 16 px). Bez JavaScriptu a při omezení pohybu zůstává obsah viditelný. Přichycená navigace při scrollování získá lehce průsvitný, rozostřený povrch.

Přihláška údaje neodesílá ani neukládá a nerezervuje místo. Termíny a část textů jsou ukázkové; před publikací je nutné schválit skutečný obsah. Kontakty, trenéři, partneři a 12 galerií vycházejí ze zdrojového WordPress archivu. Návrh má `noindex, nofollow`.

## Zdroje fotografií

- `src/assets/mask.jpg`: Andy Hall / Unsplash, `andy-hall-M4gkgNQ_T3k-unsplash.jpg`, dodal uživatel.
- `src/assets/young-goalie.jpg`: Nikolay Loubet / Unsplash, `nikolay-loubet-YdO6o1S9z6A-unsplash.jpg`, dodal uživatel.
- `src/assets/goalie-ready.jpg`: uživatelem dodaný `olegng-sports-5500917_1920.jpg`.
- `src/assets/junior-on-ice.jpg`: uživatelem dodaný `11040735-hockey-4119968_1920.jpg`.
- `src/assets/mask-illustration.png`: uživatelem dodaný `pixsila-hockey-2996682_1920.png`.
- `team.jpg`, `camp.jpg`, `goalie-silhouette.png`: existující podklady původního návrhu.
- Lokální Inter Variable: převzatý z existujícího projektu ve workspace; licence v `public/fonts/OFL.txt`.

Fotografie zpracovává Astro Image do responzivních WebP. [Dokumentace Astro Images](https://docs.astro.build/en/guides/images/).

## GitHub Pages

Návrh je zapojený do rozcestníku a stávajícího workflow. Push na `main` spustí kontrolu, build a nasazení na https://jakknaj.github.io/web-design-pres/golmansketreninky-v2/.

Zdrojový archiv `content/wordpress/` zůstává lokální a je ignorovaný Gitem. Repozitář obsahuje redakční kolekce a optimalizované fotografie potřebné pro samostatný build; archiv není k nasazení potřeba.

Pro ověření cest v podadresáři:

```sh
ASTRO_BASE=/web-design-pres/golmansketreninky-v2 npm run build
```

Editace: `src/pages/index.astro` (sekce), `src/styles/global.css` (vzhled), `src/content/` (redakční kolekce), `src/content.config.ts` (schémata), `src/styles/editorial.css` (obsahové stránky), `src/data/training.ts` (FAQ), `src/components/Registration.astro` (demo formulář).
