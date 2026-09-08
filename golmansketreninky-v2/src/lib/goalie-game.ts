import { createShotBurst } from './shot-burst';

export function setupGoalieGame(scene: HTMLElement, callbacks: { onStart(): void; onFinish(): void }) {
  const trigger = scene.querySelector<HTMLButtonElement>('.shot-trigger')!;
  const feedback = scene.querySelector<HTMLElement>('.shot-feedback')!;
  const result = scene.querySelector<HTMLElement>('.shot-result')!;
  const stamp = scene.querySelector<HTMLElement>('.save-stamp')!;
  const svg = scene.querySelector<SVGSVGElement>('.save-scene')!;
  const puckTemplate = scene.querySelector<SVGGElement>('.shot-puck')!;
  const rig = [...scene.querySelectorAll<SVGElement>('[data-rig]')];
  const head = scene.querySelector<SVGElement>('.goalie-head')!;
  const preference = matchMedia('(prefers-reduced-motion: reduce)');
  const ease = getComputedStyle(scene).getPropertyValue('--ease-out').trim();
  const burst = createShotBurst();
  const motions = new Set<Animation>();
  const rigMotions = new Map<Element, Animation>();
  const pucks = new Set<SVGElement>();
  const timers = new Set<number>();
  let playing = false;
  let finishTimer: number | undefined;
  let meterTimer: number | undefined;
  let shotNumber = 0;
  let latestShot = 0;

  function later(callback: () => void, delay: number) {
    const timer = window.setTimeout(() => { timers.delete(timer); callback(); }, delay);
    timers.add(timer);
    return timer;
  }

  function cancelTimer(timer?: number) {
    window.clearTimeout(timer);
    if (timer !== undefined) timers.delete(timer);
  }

  function animate(element: Element, frames: Keyframe[], duration: number, delay = 0) {
    const motion = element.animate(frames, { duration, delay, fill: 'both' });
    motions.add(motion);
    // Finished fill effects are cancelled by stop(), not left attached forever.
    motion.finished.catch(() => motions.delete(motion));
    return motion;
  }

  function move(part: SVGElement, frames: Keyframe[], duration: number) {
    // Retarget from the visible pose, even if the preceding shot is mid-save.
    const current = getComputedStyle(part).transform;
    const old = rigMotions.get(part);
    old?.cancel();
    if (old) motions.delete(old);
    const motion = animate(part, [{ transform: current, offset: 0, easing: ease }, ...frames], duration);
    rigMotions.set(part, motion);
  }

  function meter(count: number) {
    scene.querySelectorAll('.shot-meter i').forEach((dot, i) => dot.toggleAttribute('data-lit', i < count));
  }

  function stop() {
    if (!playing) return;
    playing = false;
    latestShot++;
    timers.forEach(timer => window.clearTimeout(timer));
    timers.clear();
    motions.forEach(motion => motion.cancel());
    motions.clear();
    rigMotions.forEach(motion => motion.cancel());
    rigMotions.clear();
    pucks.forEach(puck => puck.remove());
    pucks.clear();
    rig.forEach(part => { part.style.transform = part.dataset.ready!; });
    head.style.removeProperty('transform');
    scene.querySelectorAll<SVGElement>('.anger-mark,.goal-light,.goal-ripple,.goal-celebration,.goal-confetti').forEach(part => part.style.removeProperty('opacity'));
    delete scene.dataset.interactive;
    delete scene.dataset.gameResult;
    trigger.removeAttribute('aria-disabled');
    burst.reset();
    meter(0);
    result.textContent = 'Ještě jednu? Klikni na led.';
    callbacks.onFinish();
  }

  function launch(goal: boolean, mode: 'save' | 'catch' | 'block') {
    const puck = puckTemplate.cloneNode(true) as SVGGElement;
    puck.removeAttribute('class');
    puck.dataset.gamePuck = '';
    puck.setAttribute('aria-hidden', 'true');
    svg.append(puck);
    pucks.add(puck);
    const start = mode === 'catch' || goal ? 'translate(505px, 447px) scale(1.15)' : 'translate(94px, 447px) scale(1.15)';
    const contact = goal ? 'translate(405px, 192px) scale(.65)' : mode === 'catch' ? 'translate(420px, 174px) scale(.78)' : mode === 'block' ? 'translate(166px, 232px) scale(.78)' : 'translate(275px, 382px) scale(.78)';
    if (preference.matches) {
      puck.style.transform = contact;
      puck.style.opacity = '1';
      later(() => { puck.remove(); pucks.delete(puck); }, goal ? 2000 : 500);
      return;
    }
    const end = goal ? 'translate(411px, 219px) scale(.65)' : mode === 'block' ? 'translate(-35px, 320px) scale(1.1)' : mode === 'catch' ? contact : 'translate(200px, 436px) scale(.9)';
    const flight = animate(puck, [
      { transform: start, opacity: 1, offset: 0, easing: 'linear' },
      { transform: contact, opacity: 1, offset: .45, easing: ease },
      { transform: end, opacity: mode === 'catch' && !goal ? 0 : 1, offset: .75 },
      { transform: end, opacity: goal ? 1 : 0, offset: 1 },
    ], 500);
    // Once it crosses the goal line, the scored puck belongs behind the goalie.
    if (goal) later(() => svg.insertBefore(puck, scene.querySelector('.goal-ripple')), 225);
    flight.finished.then(() => {
      const remove = () => { flight.cancel(); motions.delete(flight); puck.remove(); pucks.delete(puck); };
      if (goal) later(remove, 1500);
      else remove();
    }).catch(() => {});
  }

  function save(mode: 'save' | 'catch' | 'block') {
    if (preference.matches) return;
    for (const part of rig) {
      move(part, [
        { transform: part.dataset[mode]!, offset: .34 },
        { transform: part.dataset[mode]!, offset: .6, easing: ease },
        { transform: part.dataset.ready!, offset: 1 },
      ], 600);
    }
  }

  function celebrate() {
    const banner = scene.querySelector('.goal-celebration')!;
    const sparks = scene.querySelector('.goal-confetti')!;
    const particles = [...scene.querySelectorAll<SVGElement>('[data-goal-confetti]')];
    if (preference.matches) {
      particles.forEach(part => { part.style.transform = `translate(${part.dataset.x}px, ${part.dataset.y}px) rotate(${part.dataset.turn}deg)`; });
      return;
    }
    animate(banner, [
      { opacity: 0, transform: 'translateY(8px) scale(.92) rotate(-5deg)', offset: 0 },
      { opacity: 0, transform: 'translateY(8px) scale(.92) rotate(-5deg)', offset: .1, easing: ease },
      { opacity: 1, transform: 'translateY(0px) scale(1.04) rotate(-3deg)', offset: .22, easing: ease },
      { opacity: 1, transform: 'translateY(0px) scale(1) rotate(-3deg)', offset: .33 },
      { opacity: 1, transform: 'translateY(0px) scale(1) rotate(-3deg)', offset: .85, easing: ease },
      { opacity: 0, transform: 'translateY(-6px) scale(.98) rotate(-3deg)', offset: 1 },
    ], 2100);
    animate(sparks, [{ opacity: 0, offset: 0 }, { opacity: 1, offset: .1 }, { opacity: 1, offset: 1 }], 2100);
    particles.forEach((part, i) => {
      const x = Number(part.dataset.x), y = Number(part.dataset.y), turn = Number(part.dataset.turn);
      part.style.removeProperty('transform');
      animate(part, [
        { transform: `translate(300px, 245px) rotate(0deg)`, opacity: 0, offset: 0 },
        { transform: `translate(300px, 245px) rotate(0deg)`, opacity: 0, offset: .1 + i % 3 * .015, easing: ease },
        { transform: `translate(${x}px, ${y}px) rotate(${turn}deg)`, opacity: 1, offset: .42, easing: 'linear' },
        { transform: `translate(${x}px, ${y + 30}px) rotate(${turn + 70}deg)`, opacity: 1, offset: .7, easing: 'linear' },
        { transform: `translate(${x}px, ${y + 50}px) rotate(${turn + 110}deg)`, opacity: 0, offset: 1 },
      ], 2100);
    });
    animate(scene.querySelector('.anger-mark')!, [
      { opacity: 0, transform: 'scale(.95) rotate(0deg)', offset: 0 },
      { opacity: 0, transform: 'scale(.95) rotate(0deg)', offset: .32, easing: ease },
      { opacity: 1, transform: 'scale(1.12) rotate(-6deg)', offset: .43, easing: ease },
      { opacity: 1, transform: 'scale(1) rotate(5deg)', offset: .57, easing: ease },
      { opacity: 1, transform: 'scale(1.08) rotate(-4deg)', offset: .7, easing: ease },
      { opacity: 1, transform: 'scale(1) rotate(0deg)', offset: .85 },
      { opacity: 0, transform: 'scale(1) rotate(0deg)', offset: 1 },
    ], 2100);
  }

  function concede() {
    celebrate();
    if (preference.matches) {
      scene.querySelectorAll<SVGElement>('.anger-mark,.goal-light,.goal-ripple,.goal-celebration,.goal-confetti').forEach(part => { part.style.opacity = '1'; });
      return;
    }
    for (const part of rig) {
      const ready = part.dataset.ready!;
      const isBody = part.classList.contains('goalie-body');
      const isStick = part.classList.contains('goalie-stick');
      const angry = isBody ? 'translate(0px, -12px)' : isStick ? 'rotate(23deg)' : part.classList.contains('catching-arm') ? 'rotate(-52deg)' : part.classList.contains('blocker-arm') ? 'rotate(39deg)' : ready;
      const missed = isBody ? 'translate(-28px, 40px)' : part.dataset.save!;
      move(part, [
        { transform: missed, offset: .12 },
        { transform: missed, offset: .25, easing: ease },
        { transform: ready, offset: .39, easing: ease },
        { transform: angry, offset: .49 },
        { transform: isStick ? 'rotate(-12deg)' : isBody ? 'translate(0px, 5px)' : angry, offset: .56, easing: ease },
        { transform: angry, offset: .65 },
        { transform: isStick ? 'rotate(-12deg)' : isBody ? 'translate(0px, 5px)' : angry, offset: .72 },
        { transform: angry, offset: .8, easing: ease },
        { transform: ready, offset: 1 },
      ], 2100);
    }
    move(head, [
      { transform: 'rotate(0deg)', offset: .4, easing: ease },
      { transform: 'rotate(-20deg)', offset: .49, easing: ease },
      { transform: 'rotate(19deg)', offset: .59, easing: ease },
      { transform: 'rotate(-16deg)', offset: .69, easing: ease },
      { transform: 'rotate(12deg)', offset: .79, easing: ease },
      { transform: 'rotate(0deg)', offset: 1 },
    ], 2100);
    for (const selector of ['.goal-light', '.goal-ripple']) {
      animate(scene.querySelector(selector)!, [
        { opacity: 0, offset: 0 }, { opacity: 0, offset: .1 },
        { opacity: 1, offset: .48 }, { opacity: 1, offset: .8 }, { opacity: 0, offset: 1 },
      ], 2100);
    }
  }

  function shoot() {
    const shot = burst.shoot(performance.now());
    if (!shot.accepted) return;
    if (!playing) {
      const current = rig.map(part => getComputedStyle(part).transform);
      callbacks.onStart();
      rig.forEach((part, i) => { part.style.transform = current[i]; });
      playing = true;
      scene.dataset.interactive = '';
    }
    cancelTimer(finishTimer);
    cancelTimer(meterTimer);
    const id = ++latestShot;
    const mode = (['save', 'catch', 'block'] as const)[shotNumber++ % 3];
    meter(shot.count);
    scene.dataset.gameResult = shot.goal ? 'goal' : 'save';
    result.textContent = shot.goal ? 'Čtvrtá střela…' : `Střela ${shot.count} ze 4 — ještě rychleji!`;
    stamp.textContent = 'STŘELA!';
    launch(shot.goal, mode);
    if (shot.goal) { trigger.setAttribute('aria-disabled', 'true'); concede(); }
    else save(mode);
    later(() => {
      if (id !== latestShot) return;
      stamp.textContent = shot.goal ? 'TO SNAD NE!' : mode === 'catch' ? 'V LAPAČCE.' : mode === 'block' ? 'VYRÁŽEČKA!' : 'PUK? MÁM.';
      result.textContent = shot.goal ? 'Gól! Teď jsi ho naštval.' : mode === 'catch' ? 'Lapačka. Zkus ho zaskočit rychlou sérií.' : mode === 'block' ? 'Vyrážečka. Zkus to rychleji!' : 'Chyceno! Zkus čtyři rychlé střely.';
    }, preference.matches ? 0 : 225);
    if (!shot.goal) meterTimer = later(() => meter(0), 900);
    finishTimer = later(stop, shot.goal ? 2200 : 2400);
  }

  trigger.addEventListener('click', shoot);
  // Native Enter / Space work, but holding a key is not four separate shots.
  trigger.addEventListener('keydown', event => {
    if (event.repeat && (event.key === 'Enter' || event.key === ' ')) event.preventDefault();
  });
  scene.dataset.gameReady = '';
  trigger.hidden = false;
  feedback.hidden = false;
  return { stop };
}
