import type { ImageMetadata } from 'astro';
import amg from '../assets/fleet-amg-gt63s.jpg';
import amgSide from '../assets/amg-side.jpg';
import amgRear from '../assets/amg-rear.jpg';
import amgInterior from '../assets/amg-interior.jpg';
import amgSeats from '../assets/amg-seats.jpg';
import amgDetail from '../assets/amg-detail.jpg';
import s400d from '../assets/fleet-s400d.jpg';
import autobiography from '../assets/fleet-rr-autobiography.jpg';
import sport from '../assets/news-rrsport.jpg';
import g500 from '../assets/fleet-g500.jpg';
import gle from '../assets/fleet-gle580.jpg';
import brabus from '../assets/fleet-v250-brabus.jpg';

export interface FleetPhoto {
  img: ImageMetadata;
  alt: string;
}

export interface FleetVehicle {
  id: string;
  name: string;
  brand: string;
  img: ImageMetadata;
  pos: string;
  alt: string;
  kw: string;
  fuel: string;
  seats: string;
  specs: [string, string][];
  gallery: FleetPhoto[];
}

// Model selection and card photography follow VozovyPark.dc.html. Specifications
// are supplied in legacy-site/pages.json, in each model's Czech portfolio entry.
const specifications = (engine: string, power: string, fuel: string, seats: string, limit = '200 km'): [string, string][] => [
  ['Obsah motoru', engine], ['Výkon', power], ['Palivo', fuel],
  ['Převodovka', 'automatická'], ['Pohon', '4×4'], ['Počet míst', seats],
  ['Denní kilometrový limit', limit],
];

const singlePhoto = (img: ImageMetadata, alt: string): FleetPhoto[] => [{ img, alt }];

export const fleet: FleetVehicle[] = [
  {
    id: 'amg', name: 'Mercedes-Benz AMG GT 63 S+ 4MATIC', brand: 'Mercedes-Benz',
    img: amg, pos: '50% 86%',
    alt: 'Mercedes-Benz AMG GT 63 S+ 4MATIC v matně šedém laku, pohled zepředu ze strany.',
    kw: '470 kW', fuel: 'benzín', seats: '4 místa',
    specs: specifications('3982 ccm', '470 kW', 'benzín', '4'),
    gallery: [
      { img: amg, alt: 'Mercedes-Benz AMG GT 63 S+ 4MATIC, pohled zepředu ze strany' },
      { img: amgSide, alt: 'Mercedes-Benz AMG GT 63 S+ 4MATIC, pohled z boku' },
      { img: amgRear, alt: 'Mercedes-Benz AMG GT 63 S+ 4MATIC, pohled zezadu ze strany' },
      { img: amgInterior, alt: 'Mercedes-Benz AMG GT 63 S+ 4MATIC, interiér s palubní deskou' },
      { img: amgSeats, alt: 'Mercedes-Benz AMG GT 63 S+ 4MATIC, přední sedadla' },
      { img: amgDetail, alt: 'Mercedes-Benz AMG GT 63 S+ 4MATIC, detail zádi s označením GT 63 S' },
    ],
  },
  {
    id: 's', name: 'Mercedes-Benz S 400d 4MATIC', brand: 'Mercedes-Benz',
    img: s400d, pos: '50% 58%', alt: 'Mercedes-Benz S 400d 4MATIC v matném laku v showroomu.',
    kw: '243 kW', fuel: 'nafta', seats: '5 míst',
    specs: specifications('2925 ccm', '243 kW', 'nafta', '5'),
    gallery: singlePhoto(s400d, 'Mercedes-Benz S 400d 4MATIC v matném laku v showroomu.'),
  },
  {
    id: 'rra', name: 'Range Rover Autobiography', brand: 'Land Rover',
    img: autobiography, pos: '60% 65%', alt: 'Černý Range Rover Autobiography před prodejnou, pohled zepředu ze strany.',
    kw: '250 kW', fuel: 'nafta', seats: '5 míst',
    specs: specifications('4367 ccm', '250 kW', 'nafta', '5'),
    gallery: singlePhoto(autobiography, 'Černý Range Rover Autobiography před prodejnou, pohled zepředu ze strany.'),
  },
  {
    id: 'rrs', name: 'Range Rover Sport', brand: 'Land Rover',
    img: sport, pos: '50% 62%', alt: 'Černý Range Rover Sport na trávníku před prodejnou.',
    kw: '221 kW', fuel: 'nafta', seats: '5 míst',
    specs: specifications('2997 ccm', '221 kW', 'nafta', '5'),
    gallery: singlePhoto(sport, 'Černý Range Rover Sport na trávníku před prodejnou.'),
  },
  {
    id: 'g500', name: 'Mercedes-Benz G 500', brand: 'Mercedes-Benz',
    img: g500, pos: '50% 60%', alt: 'Matně černý Mercedes-Benz G 500 z boku v hale.',
    kw: '310 kW', fuel: 'benzín', seats: '5 míst',
    specs: specifications('3982 ccm', '310 kW', 'benzín', '5'),
    gallery: singlePhoto(g500, 'Matně černý Mercedes-Benz G 500 z boku v hale.'),
  },
  {
    id: 'gle', name: 'Mercedes-Benz GLE 580 4MATIC', brand: 'Mercedes-Benz',
    img: gle, pos: '50% 62%', alt: 'Bílý Mercedes-Benz GLE 580 4MATIC před showroomem.',
    kw: '360 kW', fuel: 'benzín', seats: '5 míst',
    specs: specifications('3982 ccm', '360 kW', 'benzín', '5'),
    gallery: singlePhoto(gle, 'Bílý Mercedes-Benz GLE 580 4MATIC před showroomem.'),
  },
  {
    id: 'v', name: 'Mercedes V 250 Brabus', brand: 'Mercedes-Benz',
    img: brabus, pos: '45% 62%', alt: 'Stříbrný Mercedes V250 Brabus s logem KNOKAR na polní cestě.',
    kw: '140 kW', fuel: 'nafta', seats: '4–7 míst',
    specs: specifications('2143 ccm', '140 kW', 'nafta', '4–7', '300 km'),
    gallery: singlePhoto(brabus, 'Stříbrný Mercedes V250 Brabus s logem KNOKAR na polní cestě.'),
  },
];
