/** Four deliberate shots in a short burst beat the goalie. No persistent score. */
export function createShotBurst() {
  let shots: number[] = [];
  let blockedUntil = -Infinity;
  return {
    shoot(now: number) {
      if (now < blockedUntil) return { accepted: false, goal: false, count: 0 };
      if (shots.length && now - shots[shots.length - 1] > 320) shots = [];
      shots = shots.filter(time => now - time <= 900);
      shots.push(now);
      const count = shots.length;
      const goal = count === 4;
      if (goal) { shots = []; blockedUntil = now + 2200; }
      return { accepted: true, goal, count };
    },
    reset() { shots = []; blockedUntil = -Infinity; },
  };
}
