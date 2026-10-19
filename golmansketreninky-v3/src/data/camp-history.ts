export const historyMilestones = [
 {years:'2012',city:'Beroun',venue:'Zimní stadion Beroun',campId:'letni-special-2012',events:1,camps:1,detail:'1 letní kemp'},
 {years:'2013–2016',city:'Jihlava',venue:'Zimní stadion Jihlava',campId:'letni-special-2013',events:3,camps:3,detail:'3 letní kempy'},
 {years:'2014',city:'Havlíčkův Brod',venue:'Zimní stadion Havlíčkův Brod',campId:'letni-special-2014',events:1,camps:1,detail:'1 letní kemp'},
 {years:'2016',city:'Praha a Vyškov',venue:'HC Kobra / ZS Vyškov',campId:null,events:13,camps:0,detail:'7 tréninků na Kobře, 6 ve Vyškově'},
 {years:'2017–2026',city:'Říčany',venue:'COM-SYS Ice Arena, dříve MERKUR',venueUrl:'https://comsysicearena.cz/',campId:'letni-special-2026',events:166,camps:19,detail:'147 tréninků a 19 kempů či speciálů'},
];
export const historyTotals = {
 events:historyMilestones.reduce((sum,item)=>sum+item.events,0),
 camps:historyMilestones.reduce((sum,item)=>sum+item.camps,0),
 trainings:historyMilestones.reduce((sum,item)=>sum+item.events-item.camps,0),
 venues:6,
};
