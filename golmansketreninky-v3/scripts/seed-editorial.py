"""Initial editorial selection. Existing editorial entries are never overwritten."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / 'content/wordpress'
load = lambda path: json.loads((ARCHIVE / path).read_text())
records = {r.get('id'): r for r in load('data/records.json')}
galleries = {g['id']: g for g in load('data/galleries.json')}
assets = {}

def picture(source, name):
    assets[name] = {'source': str((ARCHIVE / source).relative_to(ROOT)), 'target': str(Path('src/assets/editorial') / (name + '.webp'))}
    return '../../assets/editorial/' + name + '.webp'

def save(collection, id, data):
    path = ROOT / 'src/content' / collection / (id + '.json')
    if not path.exists():
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

years = {2012:('Beroun',15,20,394,'3'),2013:('Jihlava',14,19,1448,'5'),2014:('Havlíčkův Brod',13,18,2765,'6'),2015:('Jihlava',12,17,4370,None),2016:('Jihlava',10,15,5497,None),2017:('Říčany',9,14,6982,'20'),2018:('Říčany',8,13,7782,'21'),2019:('Říčany',14,19,8362,None),2020:('Říčany',12,17,8653,'22'),2021:('Říčany',11,16,9126,'23'),2022:('Říčany',10,15,9698,None),2023:('Říčany',9,14,9871,'24'),2024:('Říčany',14,19,10078,None),2025:('Říčany',13,18,10198,None),2026:('Říčany',12,17,10296,'25')}
camp_ids = {y:f'letni-special-{y}' for y in years}
gallery_year = {v[4]:y for y,v in years.items() if v[4]}
selection = {'25':[0,3,4,7,10,13,17,20,22,24,29,36],'24':[0,1,5,6,7,9,11,15,16,18,19,21], '7':[3,5,6,7,10,12,18,21,38,60,80,110]}
selection.update({'3': [7, 15, 22, 29, 44, 58, 66, 73, 95, 124, 146, 153], '5': [0, 1, 2, 4, 8, 9, 10, 11, 12, 14, 16, 17], '6': [1, 2, 7, 8, 9, 11, 13, 16, 18, 20, 22, 26], '20': [0, 9, 19, 23, 37, 60, 70, 79, 88, 98, 102, 107], '21': [5, 10, 21, 26, 36, 56, 62, 67, 72, 82, 108, 113], '22': [3, 9, 20, 26, 29, 32, 37, 43, 52, 55, 60, 63], '23': [16, 32, 64, 95, 111, 127, 143, 191, 207, 271, 318, 350]})
covers = {'25': 20, '24': 0, '7': 6, '3': 153, '5': 9, '6': 7, '20': 98, '21': 113, '22': 60, '23': 32}

for gid,g in galleries.items():
    year = gallery_year.get(gid)
    picked = selection.get(gid, [round(i*(len(g['images'])-1)/max(1,min(12,len(g['images']))-1)) for i in range(min(12,len(g['images'])))])
    photos=[]
    for i,im in enumerate(g['images']):
        caption = f'{g["title"].replace(" – foto", "")} · fotografie {i+1}'
        if gid=='25':
            caption = ('Trénink brankářů na ledě v Říčanech, 2026' if i<13 or i in [19,38,41] else 'Brankáři a trenéři na ledě, kemp 2026' if i<22 else 'Společný program mimo led, kemp v Říčanech 2026')
        photos.append({'image':picture(im['local_path'],f'g{gid}-{i:04d}'),'alt':caption,'caption':caption,'featured':i in picked,'source':im['source_url']})
    data={'title':g['title'].replace(' – foto',''),'year':year or (2015 if gid=='7' else 2012),'kind':'camp' if year else 'training','coverIndex':covers.get(gid,0),'photos':photos,'sources':g['content_source_pages'][:1]}
    if gid=='1':data.pop('year',None)
    if year:data['camp']=camp_ids[year]
    save('galleries','gallery-'+gid,data)

for year,(city,start,end,source_id,gid) in years.items():
    source=records[source_id]
    program=['Technika bruslení a brankářských zákroků','Hra holí a organizace hry','Koordinace, postřeh a stabilita mimo led','Teorie a mentální příprava'] if year not in [2012,2025] else []
    summary=f'Letní gólmanský speciál {year}. {city}, šest dní věnovaných brankářskému řemeslu.'
    body=[f'Ročník {year} spojil gólmany a trenéry v lokalitě {city}. Původní nabídka uváděla termín {start}.–{end}. července {year}.']
    if gid:body.append('Fotografie zachycují konkrétní ročník: lidi, prostředí a práci, ke které se v akademii vracíme sezonu za sezonou.')
    else:body=[f'Ročník {year} je v historii akademie doložen původními propozicemi pro termín {start}.–{end}. července v lokalitě {city}. Samostatnou fotogalerii tohoto ročníku nemáme v publikovaném výběru.']
    if year==2026:
        summary='Šest dní na ledě i mimo něj. Ohlédnutí za letním speciálem v Říčanech.'
        body=['Od práce v brankovišti po společný program mimo led. Letní speciál 2026 v COM-SYS Ice Areně propojil gólmanskou techniku, pohyb a soustředění.', 'Program počítal s jedenácti tréninkovými jednotkami na ledě a jedenácti na suchu. Vedle bruslení a zákroků zahrnoval práci s videem, mentální přípravu i virtuální realitu.', 'Nahlédněte do ročníku, který se odehrál od 12. do 17. července. V galerii jsou skutečné fotografie z tréninků i společného zakončení.']
        program=['11 tréninkových jednotek na ledě','11 jednotek suché přípravy','Bruslení, zákroky, zakrytý výhled, hra holí','Video, mentální příprava a virtuální realita']
    data={'title':f'Letní speciál {year}','series':'letni-special','year':year,'location':city,'venue':'COM-SYS Ice Arena' if year>=2022 else 'MERKUR Ice Aréna' if year>=2017 else 'Zimní stadion '+city,'start':f'{year}-07-{start:02d}T13:30:00+02:00','end':f'{year}-07-{end:02d}T23:59:59+02:00','availability':'completed','summary':summary,'body':body,'program':program,'practical':[],'coaches':[],'sources':[source['source_url']]}
    if gid:data['gallery']='gallery-'+gid
    if year==2026:
        data.update(age='Od ročníku narození 2018 po dospělé',capacity='42 gólmanů · 2 skupiny po 21',price='14 990 Kč s ubytováním / 11 990 Kč bez ubytování',practical=['Na stanovišti maximálně tři brankáři.','Ubytování v hotelu Oáza v Říčanech.','S sebou výstroj, tři tenisáky, sportovní boty a oblečení na suchou přípravu.'])
    save('camps',camp_ids[year],data)

save('camps','vikend-v-brankovisti-2026',{'title':'Víkend v brankovišti.','series':'vikendovy-kemp','year':2026,'location':'Říčany','venue':'COM-SYS Ice Arena','start':'2026-09-26T09:00:00+02:00','end':'2026-09-27T18:00:00+02:00','availability':'open','demo':True,'summary':'Dva dny, které patří tvé hře. Led, suchá příprava a společný rozbor.','body':['Víkend zaměřený na techniku, pohyb v brankovišti a čtení hry. Prostor pro otázky i konkrétní zpětnou vazbu.','Tento termín je ukázkou nové nabídky. Skutečný program, cenu a účast trenérů potvrdí akademie před vypsáním.'],'program':['Technika a pohyb na ledě','Herní situace a práce s pukem','Suchá příprava a zpětná vazba'],'practical':['Kompletní brankářská výstroj a nabroušené brusle.','Sportovní oblečení, boty a láhev s pitím.'],'age':'Věkové skupiny upřesníme','capacity':'Malé skupiny · kapacitu upřesníme','coaches':[],'sources':[]})

coach_copy=[
('Martin Altrichter','Zkušenost z velkých zápasů. Pozornost k malým detailům.','Mistr extraligy 2004 s HC Zlín.','Během hráčské kariéry prošel řadou extraligových klubů a reprezentoval také v inline hokeji. Brankářům předává zkušenost s pohybem, rozhodováním a zvládáním zápasových situací.',['Mistrovský titul s HC Zlín v roce 2004','Mládežnický trenér gólmanů od roku 2007 podle medailonku akademie']),
('Mgr. Marek Zapletal','Gólmanské řemeslo v souvislostech.','Zkušenosti s rozvojem brankářů napříč kategoriemi.','Vyrostl v HK Kroměříž. Jeho trenérská cesta zahrnuje mládežnické i klubové brankáře; působil například ve Vsetíně, Havlíčkově Brodě, Šumperku a Karlových Varech.',['Hráčská zkušenost z Kroměříže a Kobry Praha','Trenérská práce s mládeží i celými kluby']),
('Daniel Zelenka','Od vlastního brankoviště k práci s další generací.','Hráčské zkušenosti z juniorských i mužských soutěží.','S hokejem začínal v Kroměříži. Dorosteneckou a juniorskou zkušenost získal v Šumperku, Havířově a Kometě Brno. V mužském hokeji prošel Břeclaví, Třebíčí a Šumperkem.',['Zkušenosti z první a druhé ligy','Trenérská práce s mládeží HC Kralupy podle zdrojového medailonku']),
('Luboš Horčička','Roky v bráně. Zkušenost pro další zákrok.','Dlouhá hráčská cesta extraligou a první ligou.','Začínal v Děčíně a prošel řadou českých i slovenských klubů. Akademie v jeho medailonku uvádí také trenérskou práci u A týmu, U20 a U17 ve Zlíně.',['Hráčské zkušenosti z české i slovenské extraligy','Práce s dospělými i mládežnickými brankáři'])]
profiles=load('data/coaches.json')
for i,p in enumerate(profiles):
    data={'name':p['name'],'order':i,'sources':[p['source_url']],'summary':'','intro':'','body':[],'credentials':[]}
    if i<4:
        _,intro,summary,body,credentials=coach_copy[i]
        data.update(intro=intro,summary=summary,body=[body],credentials=credentials,portrait=picture(p['portrait_local_path'],'coach-'+p['slug']))
    save('coaches',p['slug'],data)

for i,p in enumerate(load('data/partners.json')):
    save('partners',f'partner-{i}',{'name':p['name'],'order':i,'url':p['website'],'logo':picture(p['logo_local_path'],f'partner-{i}'),'sources':[p['source_page']]})

for id,kind,start,end,title,summary in [('individual-1','individual','2026-09-16T16:00:00+02:00','2026-09-16T17:00:00+02:00','Tvůj prostor. Tvůj posun.','Technika a pohyb v brankovišti'),('group-1','group','2026-09-20T09:00:00+02:00','2026-09-20T10:30:00+02:00','Společně o krok dál.','Herní situace a čtení hry')]:
    save('sessions',id,{'title':title,'kind':kind,'start':start,'end':end,'availability':'open','demo':True,'summary':summary,'location':'Říčany · COM-SYS Ice Arena','capacity':'1 gólman' if kind=='individual' else 'Max. 6 gólmanů','sources':[]})

article_seeds=[('z-kempu-2026','25',10368,'Šest dní. Spousta dalších kroků.',2026),('z-kempu-2023','24',9965,'Na ledě jako jeden tým.',2023),('z-kempu-2021','23',9612,'Zpátky mezi mantinely.',2021),('z-kempu-2020','22',8813,'Další léto v brankovišti.',2020),('z-kempu-2018','21',8096,'Led, pohyb a společná práce.',2018),('trenink-unor-2015','7',3798,'Základ vzniká opakováním.',None)]
for id,gid,sourceid,title,year in article_seeds:
    source=records[sourceid]
    data={'title':title,'date':source['date'][:10],'category':'Z kempů' if year else 'Z tréninku','summary':f'Fotografické ohlédnutí za '+(f'letním speciálem v Říčanech {year}.' if year else 'tréninkem z 8. února 2015.'),'body':[(f'Ročník {year} patří do příběhu letních gólmanských speciálů. Zachované fotografie ukazují jeho prostředí a lidi, kteří jej tvořili.' if year else 'Trénink z 8. února 2015 zachycuje práci s mladými brankáři: vysvětlování, opakování pohybu a soustředění na další zákrok.'),'Prohlédněte si výběr fotografií. Celá galerie zůstává dostupná pro další vzpomínky i pohled na práci akademie v daném období.'],'gallery':'gallery-'+gid,'sources':[source['source_url']]}
    if gid=='1':data.pop('year',None)
    if year:data['camp']=camp_ids[year]
    if year==2026:data['body']=['Letní speciál v Říčanech proběhl od 12. do 17. července 2026. Trénink na ledě doplnila suchá příprava a společný program.','V programu bylo jedenáct jednotek na ledě a jedenáct mimo něj, práce s videem, mentální příprava a virtuální realita. Fotografie přibližují brankoviště i chvíle, kdy se celý tým potkal mimo led.'];data['sources'].append(records[10296]['source_url'])
    save('articles',id,data)

(ROOT/'content/editorial-assets.json').write_text(json.dumps(list(assets.values()),ensure_ascii=False,indent=2)+'\n')
print(f'Editorial selection ready: {len(assets)} image sources')
