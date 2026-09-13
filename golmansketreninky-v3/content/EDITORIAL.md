# Redakční obsah akademie

Web zůstává statický Astro mockup (`noindex`). Přihláška pouze předvede průchod; nic neodesílá, neukládá a nerezervuje. Kontakty: `src/lib/site.ts`.

## Co je publikované

- 15 doložených hlavních letních ročníků 2012–2026; 2012 označuje nejstarší doložený ročník, nikoli založení.
- Samostatný ukázkový zářijový kemp a dva ukázkové tréninky.
- 9 kempových a 3 tréninkové galerie, celkem 1 145 fotografií. Základní galerie nemá doložený rok, proto je bez letopočtu.
- 6 fotoreportáží s původními daty publikace, 4 medailonky + 7 doložených jmen, 5 partnerů.
- Jeden vybraný krátký záznam výuky z Říčan 2018. Optimalizovaný, bez zvuku, spouští se ručně.

`content/wordpress` je nedotčený zdrojový archiv, nikoli publikační složka. Staré nabídky výstroje a provozní oznámení zůstávají pouze tam. `sources` v redakčních datech a `source` u fotografií/video zachovávají dohledatelnost interně. Veřejné texty jsou redakčně upravené.

## Struktura

| Složka | Význam |
|---|---|
| `src/content/camps` | Jeden JSON na ročník; název souboru je stabilní ID a URL. |
| `src/content/sessions` | Jednotlivé tréninkové termíny. |
| `src/content/articles` | Články, datum, kategorie, volitelné vazby na kemp a galerii. |
| `src/content/galleries` | Seřazené snímky, titulní fotografie, výběr, vazba na kemp. |
| `src/content/coaches` | Medailonky a jména, portréty jen tam, kde existují. |
| `src/content/partners` | Názvy, odkazy a loga. |
| `src/assets/editorial` | Optimalizované obrazové podklady. |
| `public/media` | Pouze vybrané webové video, žádný úplný videoarchiv. |

Schémata a reference validuje `src/content.config.ts`; oboustrannou vazbu kemp–galerie a odkazy na publikované záznamy ověřuje `src/lib/site.ts`.

## Přidání dalšího ročníku

1. Založte např. `src/content/camps/letni-special-2027.json`. Ponechte `series: "letni-special"`. ID po publikaci neměňte: `/kempy/letni-special-2027/` zůstává po celý život ročníku.
2. Začněte `availability: "announced"`. Neznámé datum, cenu, kapacitu a věkové určení vynechte. Pro nepublikovaný rozpracovaný obsah lze použít `draft: true`.
3. Před vypsáním doplňte skutečné `start` a `end` v ISO formátu s časovým posunem, místo, cenu, věk, kapacitu, program, praktické pokyny a potvrzené trenéry. Změňte dostupnost na `open`. UI přihlášky je stále pouze demonstrace.
4. Při naplnění nastavte `full`; stránka zachová nabídku a nabídne kontakt místo přihlášky.
5. Po skončení nastavte `completed`, přepište `summary` a `body` na ohlédnutí, přidejte galerii. Původní `program`, `practical`, cenu a kapacitu ponechte: zobrazují se jako archivní údaje.
6. Přidejte související článek. Přehledy, historie, nejbližší nabídka a odkazy na další ročník se sestaví automaticky při buildu, bez úprav šablon.

Minimální připravovaný ročník:

```json
{
  "title": "Letní speciál 2027",
  "series": "letni-special",
  "year": 2027,
  "location": "Místo připravujeme",
  "venue": "Bude upřesněno",
  "availability": "announced",
  "summary": "Další společný čas na ledě. Podrobnosti připravujeme.",
  "body": ["Informace o novém ročníku zveřejníme po jejich potvrzení."],
  "program": [],
  "practical": [],
  "coaches": [],
  "sources": []
}
```

`coaches` obsahuje ID profilů, např. `"martin-altrichter"`. Nenaplňujte seznam automaticky celým týmem; účast v konkrétním ročníku musí být doložená. U demo termínů vždy `demo: true`.

Prošlé ročníky se při buildu automaticky vyhodnotí jako proběhlé i při zapomenutém stavu `open`. Přihlašování končí nejpozději začátkem akce. Prohlížeč znovu kontroluje datum při otevření, návratu na stránku i dokončení formuláře. Statický web je nutné po redakční změně a po skončení akce znovu sestavit, aby se změnilo i pořadí v historii; zastaralý build mezitím nedovolí přihlášku.

## Galerie a fotografie

Založte JSON do `src/content/galleries`. Pro kemp nastavte `camp` na jeho ID a v kempu `gallery` na ID galerie; vazba musí být oboustranná. `coverIndex` je index titulního snímku od nuly. U zhruba 12 nejlepších fotografií nastavte `featured: true`. Pole `photos` určuje pořadí. Stránka galerie zpřístupní všechny fotografie.

```json
{
  "title": "Letní speciál 2027 v obrazech",
  "year": 2027,
  "kind": "camp",
  "camp": "letni-special-2027",
  "coverIndex": 0,
  "sources": [],
  "photos": [{
    "image": "../../assets/editorial/ricany-2027-01.webp",
    "alt": "Trenér vysvětluje brankářům pohyb u tyče",
    "caption": "Práce na pohybu u tyče, Říčany 2027",
    "featured": true,
    "source": "https://www.golmansketreninky.cz/zdrojovy-odkaz/"
  }]
}
```

Příklad obsahuje zástupnou fotografii a odkaz: nahraďte skutečnými. Bez galerie se detail kempu normálně zobrazí. Nepoužívejte cizí ročník jako údajnou fotografii akce. U slabších starých snímků upřednostněte malé náhledy. Pište konkrétní, pravdivé popisky; neznámá jména ani rok nedoplňujte odhadem.

Připravujte WebP maximálně 1 600 px na šířku bez zvětšování originálu. Astro generuje menší náhledy, mřížky načítají snímky líně a plné webové rozlišení se načte až při otevření fotografie. Originály a jejich metadata zůstávají v archivu. Lightbox: šipky, Escape, návrat fokusu, ovládací tlačítka a vodorovný tah na telefonu.

Pro převod dalších archivních podkladů přidejte relativní cesty `source` a `target` do `content/editorial-assets.json` a spusťte `npm run prepare:media`. Existující výstupy se nepřepisují. `scripts/seed-editorial.py` je jednorázový počáteční import, nikoli redakční synchronizace; nespouští se při buildu.

Volitelné `video` galerie obsahuje `title`, `description`, relativní `file` v `public/media`, obrazový `poster` a `source`. Před přidáním vyberte konkrétní záznam, optimalizujte jej a zajistěte náhled; nepublikujte celý videoarchiv. Současný záznam je beze zvuku, jeho obsah popisuje doprovodný text. Budoucí mluvená videa doplňte titulky před publikací.

## Články

`date` je skutečné datum publikace ve formátu `YYYY-MM-DD`, nikoli datum migrace. Kategorie: `Z kempů`, `Z tréninku`, `Informace`. `camp` a `gallery` jsou volitelné reference. Více článků může mít tentýž `camp`. Titulní fotografii převezme článek z galerie, nebo určete vlastní `cover` a `coverAlt`. Bez fotografie vznikne čistá typografická karta.

## Ověření

```sh
npm test
npm run build
npm run check:links
ASTRO_BASE=/test-site/ npm run build
python3 scripts/check-built-site.py dist /test-site/
```

Testy používají Node 22.18+ (spouštění TypeScriptu bez dalšího runneru). Po testu vlastní cesty vytvořte normální build pro požadovanou cílovou URL. V prohlížeči zkontrolujte mobil, tablet a desktop, galerie i demo formulář. CMS, e-maily, platby a skutečné rezervace nejsou zapojené.
