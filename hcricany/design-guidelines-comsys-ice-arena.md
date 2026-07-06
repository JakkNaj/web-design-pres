# Design Guidelines pro COM-SYS ICE ARENA

Navazujici designovy manual vychazi z redesignu webu `web-design-pres/hcricany/`. Cilem je, aby web COM-SYS ICE ARENY pusobil jako prirozena soucast stejneho sportovniho ekosystemu jako HC Ricany, ale nebyl jen prebarvenou klubovou strankou.

Hlavni vec k preneseni neni konkretni hokejovy obsah, ale system rozlozeni: tmavy sportovni zacatek, jasne akcni rozcestniky, stridani bilych/ledovych/tmavych sekci, karty pro rychlou orientaci a prakticky kontakt na konci kazde klicove cesty.

## Vychodiska z HC Ricany

Referencni prvky jsou uvedene relativne ke koreni workspace `/Users/jakubnajman/web-projects`:

- Astro projekt: `web-design-pres/hcricany/`
- Design tokeny: `web-design-pres/hcricany/src/styles/tokens.css`
- Globalni layout a responzivita: `web-design-pres/hcricany/src/styles/global.css`
- Homepage blueprint: `web-design-pres/hcricany/src/pages/index.astro`
- Podstrankove vzory: `web-design-pres/hcricany/src/pages/klub.astro`, `web-design-pres/hcricany/src/pages/nabor.astro`, `web-design-pres/hcricany/src/pages/mladez.astro`, `web-design-pres/hcricany/src/pages/kontakt.astro`
- Zakladni data a navigace: `web-design-pres/hcricany/src/lib/siteData.ts`

Zachovat:

- sportovne-technicky ton,
- tmavy header a footer,
- vyraznou kondenzovanou typografii,
- cervenou jako primarni akcni barvu,
- ledove svetle pozadi pro informacni sekce,
- male polomery rohu,
- pevny rytmus sekci a content-first rozlozeni.

Upravit pro arenu:

- COM-SYS ICE ARENA ma byt hlavni znacka v prvnim viewportu, ne jen partner klubu.
- Obsah ma byt servisni: provoz, verejne brusleni, pronajem ledu, restaurace/sluzby, akce, kontakt.
- Fotky maji ukazovat prostor arenu, led, satny, zazemi, verejnost a akce. Klubove fotky pouzivat jen v kontextu partneru nebo aktivit v arene.
- Ton ma byt mene klubovy a vice provozni: jasne terminy, ceny, kontakt, dostupnost, rezervace.

## Vizuální Směr

### Charakter

Web ma pusobit jako moderni lokalni sportovni areal: energicky, prakticky, duveryhodny, cisty. Ne jako marketingova landing page s dekoracemi. Uzivatel ma rychle najit, kdy muze prijit, co si muze objednat, kde zaparkuje a komu napsat.

### Paleta

Pouzij stejny zaklad jako HC Ricany, ale arene dej o neco vice "ice/tech" charakteru.

| Role | Token | Barva | Pouziti |
| --- | --- | --- | --- |
| Zakladni tmava | `--black` | `#0f1114` | header, footer, hero, tmave CTA sekce |
| Mekkci tmava | `--black-soft` | `#14171b` | tmave karty, tlacitka, text na svetlem pozadi |
| Uhlova seda | `--charcoal` | `#1b2026` | alternativni tmave plochy |
| Text sekundarni | `--steel` | `#5a6470` | popisy a pomocne informace |
| Muted text | `--muted` | `#8a939c` | text na tmavem pozadi, meta informace |
| Ledove pozadi | `--ice` | `#f0f3f5` | informacni sekce |
| Svetle ledove pozadi | `--ice-2` | `#f6f8f9` | boxy, placeholdery, formularove plochy |
| Linky | `--line` | `#e3e8eb` | okraje karet a oddeleni |
| Primarni akce | `--red` | `#c8102e` | hlavni CTA, aktivni navigace, kratke akcenty |
| Hover akce | `--red-dark` | `#a50d26` | hover hlavniho CTA |
| Sekundarni akcent | `--teal` | `#2f8f88` | rozpis, dostupnost, provozni informace |
| Jasny akcent | `--teal-bright` | `#52b3ac` | focus, drobne highlighty |

Pro COM-SYS ICE ARENU pouzivej cervenou mene casto nez u klubu: primarne pro "Rezervovat", "Kontakt", "Koupit vstup". Tyrkys pouzivej pro provozni a casove informace: rozpis, otevreno, verejne brusleni, dostupnost.

### Typografie

Zaklad:

- Display: `Barlow Condensed`, fallback `Barlow`, system sans.
- Body: `Barlow`, fallback system sans.

Pouziti:

- H1: velke, kondenzovane, sportovni, uppercase muze byt u znacky nebo kratkych titulku.
- H2: `clamp(2.35rem, 5vw, 2.8rem)`, vzdy s jasnym obsahem sekce.
- H3 v kartach: kondenzovane, kratke, informacni.
- Body text: vecny, kratke odstavce, max. 2-3 vety.
- Eyebrow: uppercase, letter spacing okolo `0.16em-0.2em`, kratka cervena nebo tyrkysova linka pred textem.

Nezvetsovat bezduvodne text uvnitr karet. Hero typografie patri jen na hero a page hero.

### Tvary a hrany

- Globalni radius: `6px`.
- Tlacitka: `4px`.
- Karty: `6px`.
- Fotky: `6px`.
- Nepouzivat velke zaobleni, pilulky jen vyjimecne u malych tagu.
- Karty maji byt utilitarni, ne dekorativni.

### Pohyb

Pouzij jemny reveal z HC Ricany:

- `opacity: 0 -> 1`
- `translateY(22px) -> 0`
- trvani cca `560ms`
- hover karet `translateY(-3px)`
- hover tlacitek `translateY(-1px)`
- respektovat `prefers-reduced-motion: reduce`

Pohyb nesmi schovavat dulezity obsah, rozpis, cenu ani kontakt.

## Layout System

### Shell

Zakladni sirka obsahu:

- desktop max: `1304px`,
- desktop padding: `32px`,
- tablet padding: `20px`,
- mobile padding: `14px`.

Sekce:

- `.section`: `clamp(3.75rem, 7vw, 4.5rem) 0`
- typy sekci:
  - bila sekce pro primarni obsah,
  - ledova sekce pro prehledy, listy a provozni boxy,
  - tmava sekce pro silne CTA nebo dulezity servisni blok,
  - border top pri prechodu mezi podobnymi svetlymi sekcemi.

### Grid vzory

Opakovatelne gridy:

- Hero: `1.04fr / 0.96fr`, vlevo obsah, vpravo velka media plocha.
- Dvousloupec: `1.5fr / minmax(280px, 1fr)` pro hlavni text + postranni panel.
- Karty: 3 sloupce na desktopu, 2 na tabletu, 1 na mobilu.
- Partneri/loga: 4 sloupce desktop, 1-2 podle sirky.
- Informacni band: 2 stejne sloupce desktop, 1 sloupec tablet/mobile.
- Detailni seznam: radky s vice sloupci na desktopu, prechod na 2 a potom 1 sloupec.

### Responzivni pravidla

- Pod `1080px`: hlavni navigace schovat, ukazat mobilni menu, vsechny hlavni dvousloupce prevest na 1 sloupec.
- Pod `720px`: zkratit texty v hustych prehledech, gridy karet prevest na 1 sloupec, u stat/fact bloku pouzit kompaktni rozlozeni.
- Nikdy nenechat hero, karty nebo tlacitka pretekat kvuli dlouhym ceskym slovum. Pouzit `overflow-wrap: anywhere` u nadpisu v uzkych kontejnerech.

## Komponenty K Přepoužití

### Header

Vzor z HC Ricany:

- sticky,
- tmavy background,
- logo v bilem ramecku,
- znacka vlevo,
- navigace uprostred/vpravo,
- primarni CTA vpravo,
- aktivni polozka podtrzena cervenym borderem.

COM-SYS varianta:

- Brand: `COM-SYS ICE ARENA`
- Subline: `ZIMNI STADION RICANY` nebo podobne.
- CTA: `Rezervovat led`, `Verejne brusleni`, pripadne podle obchodni priority.
- Navigace: `Uvod`, `Verejne brusleni`, `Pronajem ledu`, `Akce`, `Sluzby`, `Aktuality`, `Kontakt`.

### Hero

Hero musi byt prakticky rozcestnik, ne cisty image banner.

Struktura:

1. Eyebrow: lokalita / typ provozu.
2. H1: `COM-SYS ICE ARENA`.
3. Lead: jedna veta, co arena nabizi.
4. Kratky text: komu slouzi a co lze udelat na webu.
5. Primarni a sekundarni CTA.
6. Stat/fact row: napr. `2 ledove plochy`, `celorocni provoz`, `Ricany`.
7. Vpravo realna fotka arény s tmavym overlayem a malym popiskem.
8. Pod hero trojice rychlych odkazu.

### Quick Links

Nejdulezitejsi komponent pro orientaci. Pouzivat hned pod hero.

Pro COM-SYS:

- `Dnes na lede` / `Verejne brusleni`
- `Pronajem ledu` / rezervace terminu
- `Akce a kurzy` / narozeniny, skoly, kempy, klubove akce

Kazdy quick link:

- levy datovy blok nebo ikona ve ctverci,
- kategorie uppercase,
- kratky titulek,
- pomocny text,
- sipka v kruhu.

### Section Heading

Vzdy:

- eyebrow,
- H2,
- volitelny textovy odkaz vpravo.

Pouziti:

- Homepage sekce.
- Dlouhe podstranky.
- Prehledy novinek, akci, partneru, sluzeb.

### Karty

Pouzivat pro opakovatelne nebo skenovatelne informace:

- sluzby,
- typy pronajmu,
- aktuality,
- akce,
- kontakty,
- provozni pravidla,
- partneri.

Karta:

- `border: 1px solid var(--line)`,
- `background: white`,
- `border-radius: 6px`,
- padding `1.35rem-1.8rem`,
- hover pouze jemne,
- nadpis kondenzovany,
- popis kratky.

Nedavat karty do dalsich karet.

### Arena Panel

Vzor z `arena-panel` je pro COM-SYS obzvlast dulezity. Pouzit pro velke informacni bloky:

- oteviraci doba,
- pronajem ledu,
- technicke parametry,
- gastro/sluzby,
- kontakt a adresa.

Panel ma mit:

- tag,
- velky H2,
- kratky popis,
- 2-4 facts v malych boxech,
- jasne CTA.

### Formular

Formular je prakticky servisni blok, ne hlavni vizualni atrakce.

Pouziti:

- dotaz na pronajem ledu,
- skupinova rezervace,
- dotaz k akci,
- obecny kontakt.

Pole:

- jmeno,
- e-mail,
- telefon,
- typ poptavky,
- preferovany termin,
- zprava.

Tlacitko vzdy cervene, text konkretni: `Odeslat poptavku`, ne obecne `Odeslat`.

## Doporučená Homepage Struktura Pro COM-SYS

Toto je nejdulezitejsi prepis vzoru z HC Ricany. Strukturu drzet co nejverneji, obsah zmenit na provoz areny.

### 1. Hero: Znacka + rychle rozhodnuti

Ucel: uzivatel behem prvnich sekund pochopi, ze je na webu arény a najde hlavni akce.

Obsah:

- `COM-SYS ICE ARENA`
- lead o zimnim stadionu v Ricanech,
- CTA `Rezervovat led` a `Verejne brusleni`,
- facts: ledove plochy, provoz, adresa/lokalita,
- velka realna fotka ledu nebo exterieru/interieru,
- kratky overlay popisek.

### 2. Quick Links: tři nejrychlejší cesty

Ucel: nahradit slozite menu pro nejcastejsi potreby.

Navrh:

- `Verejne brusleni` - nejblizsi termin, ceny, pravidla.
- `Pronajem ledu` - dostupnost, kontakt, rezervace.
- `Akce v arene` - skoly, kempy, turnaje, narozeniny.

### 3. Aktuální Provoz / Rozpis

Ucel: servisni jadro webu.

Rozlozeni:

- vlevo velky box s embedem kalendare nebo rozpisu,
- vpravo seznam nejblizsich udalosti/provoznich oznameni.

Obsah:

- verejne brusleni,
- treninky a zapasy,
- pronajmy,
- omezeni provozu,
- specialni akce.

Vizuálně navazat na `calendar-grid` z HC Ricany.

### 4. Služby Arény

Ucel: rychle ukazat, co arena nabizi ruznym skupinam.

Karty:

- verejne brusleni,
- pronajem ledu,
- skoly a skupiny,
- hokejove kluby a turnaje,
- broušení bruslí / půjčovna,
- občerstvení / zázemí.

Kazda karta:

- tag nebo mini label,
- kratky nadpis,
- 1-2 vety,
- odkaz na detail.

### 5. Rezervační / Poptávkový CTA Blok

Ucel: prevod zajmu na kontakt.

Tmava sekce podle `section--dark`.

Obsah:

- H2: konkretni nabidka, napr. `Chcete si pronajmout led?`
- kratke vysvetleni procesu,
- fact list: `rychla odpoved`, `skupiny i firmy`, `celorocni provoz`,
- CTA `Poslat poptavku`,
- doplnkovy odkaz `Zobrazit ceny`.

### 6. O Aréně / Zázemí

Ucel: duvera a kontext.

Rozlozeni:

- vlevo fotka arény nebo zázemí,
- vpravo text + facts + odkaz.

Obsah:

- lokalita,
- ledove plochy,
- satny,
- divaci/zazemi,
- dostupnost autem/MHD,
- spoluprace s HC Ricany.

Pouzit podobny vzor jako `club-grid`.

### 7. Akce a Aktuality

Ucel: ukazat zivy provoz.

Rozlozeni:

- jedna velka featured aktualita,
- 2-3 mensi polozky vpravo,
- CTA `Vsechny aktuality`.

Obsah:

- zmeny rozpisu,
- nove kurzy,
- verejne brusleni,
- turnaje,
- provozni informace.

### 8. Galerie / Prostory

Ucel: nechat uzivatele videt realny prostor.

Obsah:

- ledova plocha,
- satny,
- zázemí,
- exterier,
- restaurace/sluzby,
- akce.

Rozlozeni: 4 obrazkove karty jako `gallery-grid`.

### 9. Partneři / Kluby V Aréně

Ucel: propojit ekosystem.

Obsah:

- HC Ricany,
- COM-SYS,
- mesto Ricany,
- dalsi partneri/sluzby.

Vizuálně pouzit partner strip, ale nechat COM-SYS jako vlastnika/brand, ne jako jednu z mnoha partner karet.

### 10. Kontakt a Footer

Ucel: uzavrit vsechny cesty kontaktem.

Obsah:

- adresa,
- mapa,
- telefon/e-mail,
- rychle odkazy,
- socialni site,
- provozni dokumenty.

Footer zachovat tmavy, s gridem 4 sloupcu.

## Doporučené Podstránky

### Verejne brusleni

Sekce:

1. Page hero: co, kdy, pro koho.
2. Rozpis/casy: tabulka nebo embed.
3. Ceny a vstupenky: karty nebo jednoduchy cenik.
4. Pravidla navstevy: 4-6 feature cards.
5. Pujcovna/brouseni: doplnkova servisni sekce.
6. Kontakt/CTA: `Mam dotaz k verejnemu brusleni`.

### Pronajem ledu

Sekce:

1. Page hero: pronajem pro kluby, firmy, skupiny.
2. Proces poptavky: 3 step cards.
3. Typy pronajmu: sport, firemni akce, skoly, soustredeni.
4. Dostupnost/rozpis: calendar panel.
5. Poptavkovy formular.
6. FAQ nebo pravidla.

### Akce

Sekce:

1. Page hero.
2. Featured akce.
3. Seznam akci v kartach.
4. Moznosti usporadani vlastni akce.
5. Kontaktni CTA.

### Sluzby / Zazemi

Sekce:

1. Page hero.
2. Dvousloupec fotka + popis arény.
3. Arena facts: ledove plochy, satny, kapacita, provoz.
4. Karty sluzeb.
5. Galerie prostoru.
6. Kontakt nebo mapa.

### Kontakt

Sekce:

1. Page hero: jeden rozcestnik pro verejnost, pronajem a partnery.
2. Kontaktni karty podle typu dotazu.
3. Formular.
4. Arena panel: adresa, mapa, parkovani, dopravni instrukce.
5. Provozni/fakturacni udaje.

## Content Patterny

### Texty

Kazda sekce ma mit:

- eyebrow: orientacni stitek,
- H2: vecny titulek,
- uvodni odstavec max. 2-3 vety,
- skenovatelny obsah: karty, facts, seznam, tabulka,
- jasnou dalsi akci.

Dobry styl:

- `Verejne brusleni probiha podle aktualniho rozpisu. Podivejte se na nejblizsi terminy a pravidla vstupu.`
- `Led si muzete pronajmout pro trenink, firemni akci nebo skupinove brusleni. Poslete nam preferovany termin a ozveme se zpet.`

Vyhnout se:

- dlouhym marketingovym odstavcum,
- obecnym sloganum bez informace,
- prilis mnoha CTA v jedne sekci,
- opakovani stejneho textu na vice mistech.

### CTA Hierarchie

Primarni CTA:

- `Rezervovat led`
- `Poslat poptavku`
- `Zobrazit rozpis`
- `Verejne brusleni`

Sekundarni CTA:

- `Kontakt`
- `Ceny a pravidla`
- `O arene`
- `Zobrazit mapu`

Textove odkazy:

- `Vsechny aktuality ->`
- `Detail sluzby ->`
- `Jak to funguje ->`

### Obrazky

Preferovat realne fotky:

- cela ledova plocha,
- bruslici verejnost,
- trenink/akce,
- satny,
- vstup a recepce,
- exterier kvuli orientaci,
- restaurace/obcerstveni, pokud existuje.

Nepouzivat:

- tmave rozmazane stock fotky,
- fotky, kde neni poznat prostor,
- klubove detailni fotky jako hlavni vizual arény,
- genericke hokejove siluety jako hlavni obsah.

## AI Implementační Brief

Pri tvorbe webu COM-SYS ICE ARENY postupuj podle techto pravidel:

1. Zachovej vizualni system HC Ricany: Barlow/Barlow Condensed, tmavy header/footer, cervena CTA, tyrkys provozni akcent, bile a ledove sekce.
2. Nekopiruj klubovy obsah. Preved layout na provoz arény: rozpis, pronajem, verejne brusleni, sluzby, kontakt.
3. Homepage postav jako prakticky rozcestnik: hero, quick links, rozpis, sluzby, rezervacni CTA, o arene, aktuality, galerie, partneri, kontakt.
4. Kazdou podstranku zacni `PageHero`, potom dej 2-4 obsahove sekce a konci kontaktnim CTA.
5. Pouzivej karty jen pro opakovatelne polozky. Nedavej kartu do karty.
6. U kazde sekce nastav jednu hlavni informacni ulohu a jednu dalsi akci.
7. Na mobilu prevadej vsechny dvousloupce na jeden sloupec a zkracuj prehledove texty.
8. Animace maji byt jemne a respektovat reduced motion.
9. Fotky maji ukazovat realny prostor arény a realne pouziti sluzeb.
10. Pokud chybi presna data, pouzij neutralni placeholder, ktery je jasne oznaceny jako doplnitelny. Nevymyslej provozni casy, ceny ani pravni udaje.

## Kontrolní Checklist

Pred dokoncenim navrhu zkontrolovat:

- Je COM-SYS ICE ARENA hlavni signal v prvnim viewportu?
- Jsou videt nejdulezitejsi akce bez scrollovani nebo tesne pod hero?
- Je rozpis/provoz snadno dohledatelny?
- Ma kazda hlavni sekce jasny ucel?
- Stridaji se bile, ledove a tmave sekce v citelnem rytmu?
- Neni cervena pouzita na vsechno najednou?
- Jsou karty skenovatelne a kratke?
- Je kontakt dostupny z hlavni navigace, CTA bloku i footeru?
- Funguje layout na mobile bez pretekani dlouhych ceskych textu?
- Jsou fotky konkretni a relevantni pro arenu?
