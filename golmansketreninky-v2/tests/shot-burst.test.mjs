import test from 'node:test';
import assert from 'node:assert/strict';
import { createShotBurst } from '../src/lib/shot-burst.ts';

test('První tři střely jsou zákroky, čtvrtá rychlá střela je gól', () => {
  const burst = createShotBurst();
  [0, 200, 400].forEach(t => assert.equal(burst.shoot(t).goal, false));
  assert.deepEqual(burst.shoot(600), { accepted: true, goal: true, count: 4 });
});
test('Pomalejší klikání ani natažená série nedají gól', () => {
  const slow = createShotBurst();
  [0, 400, 800, 1200].forEach(t => assert.equal(slow.shoot(t).count, 1));
  const stretched = createShotBurst();
  [0, 310, 620, 930].forEach(t => assert.equal(stretched.shoot(t).goal, false));
});
test('Během reakce po gólu nepřibývají střely; potom lze hrát znovu', () => {
  const burst = createShotBurst();
  [0, 100, 200, 300].forEach(t => burst.shoot(t));
  assert.equal(burst.shoot(2499).accepted, false);
  assert.deepEqual(burst.shoot(2500), { accepted: true, goal: false, count: 1 });
  [2600, 2700].forEach(t => burst.shoot(t));
  assert.equal(burst.shoot(2800).goal, true);
  burst.reset();
  assert.equal(burst.shoot(2801).count, 1);
});
