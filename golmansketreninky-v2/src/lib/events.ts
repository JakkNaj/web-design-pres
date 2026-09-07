export interface EventTiming { start?: string; end?: string; availability: 'announced' | 'open' | 'full' | 'completed' }
export function eventState(event: EventTiming, now = Date.now()) {
  if (event.availability === 'completed' || (event.end && Date.parse(event.end) < now)) return 'completed';
  return event.availability;
}
export function canRegister(event: EventTiming, now = Date.now()) {
  return eventState(event, now) === 'open' && !!event.start && !!event.end && Date.parse(event.start) > now;
}
export const stateLabels = { announced: 'Připravujeme', open: 'Přihlašování', full: 'Obsazeno', completed: 'Proběhlo' };
export function dateLabel(value?: string) {
  return value ? new Intl.DateTimeFormat('cs-CZ', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'Europe/Prague' }).format(new Date(value)) : 'Termín připravujeme';
}
export function dateRange(start?: string, end?: string) {
  if (!start) return 'Termín připravujeme';
  const f = new Intl.DateTimeFormat('cs-CZ', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'Europe/Prague' });
  return end ? f.formatRange(new Date(start), new Date(end)) : f.format(new Date(start));
}
export function timeLabel(value: string) {
  return new Intl.DateTimeFormat('cs-CZ', { hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Prague' }).format(new Date(value));
}
