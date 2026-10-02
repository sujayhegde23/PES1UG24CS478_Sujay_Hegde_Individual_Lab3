import test from 'node:test';
import assert from 'node:assert/strict';
import { MonitoringCore, expiryThreshold, boundedLookup } from './monitoring_core.mjs';
const NOW = new Date('2026-10-02T00:00:00Z');
const after = days => new Date(+NOW + days * 86_400_000).toISOString();
const admin = { id: 'sujay', role: 'SysAdmin' };
function fixture(overrides = {}) {
  const events = [];
  let clock = NOW;
  const core = new MonitoringCore({ tlsLookup: async () => after(15), whoisLookup: async () => after(45),
    notify: async event => events.push(event), now: () => clock, sleep: async () => {}, ...overrides });
  core.upsertAsset(admin, { id: 'a', domain: 'example.test', highPriority: true });
  return { core, events, setClock: value => { clock = new Date(value); } };
}
test('TC-001/003: exact expiry thresholds and invalid lookup data', () => {
  for (const days of [30, 15, 3]) assert.equal(expiryThreshold('tls', after(days), NOW), days);
  for (const days of [45, 30, 7]) assert.equal(expiryThreshold('whois', after(days), NOW), days);
  assert.equal(expiryThreshold('tls', after(31), NOW), null);
  assert.equal(expiryThreshold('whois', after(46), NOW), null);
  assert.equal(expiryThreshold('tls', after(0), NOW), 'expired');
  assert.equal(expiryThreshold('tls', after(-1), NOW), 'expired');
  assert.throws(() => expiryThreshold('tls', 'unknown', NOW), /Invalid timestamp/);
});
test('TC-001: repeat scans do not duplicate threshold notifications', async () => {
  const { core, events } = fixture();
  await core.scan(); await core.scan();
  assert.equal(core.alerts.length, 2); assert.equal(events.length, 2);
});
test('TC-004: transient failure recovers with increasing backoff', async () => {
  let calls = 0; const waits = [];
  const result = await boundedLookup(async () => { if (++calls < 3) throw new Error('rate limit'); return 'ok'; }, async n => waits.push(n));
  assert.equal(result, 'ok'); assert.deepEqual(waits, [1000, 2000]);
});
test('TC-004: persistent failure is bounded to initial attempt plus three retries', async () => {
  let calls = 0; const waits = [];
  await assert.rejects(boundedLookup(async () => { calls++; throw new Error('offline'); }, async n => waits.push(n)), /offline/);
  assert.equal(calls, 4); assert.deepEqual(waits, [1000, 2000, 4000]);
});
test('TC-005: acknowledgment suppresses pending escalation and records actor', async () => {
  const { core, events, setClock } = fixture(); await core.scan();
  for (const a of core.alerts) core.acknowledge(admin, a.id);
  setClock(+NOW + 49 * 3_600_000); await core.escalate();
  assert.equal(events.filter(e => e.type === 'escalation').length, 0);
  assert.equal(core.alerts[0].acknowledgedBy, 'sujay');
});
test('TC-006: high-priority escalation starts at 48h and is sent once', async () => {
  const { core, events, setClock } = fixture(); await core.scan();
  setClock(+NOW + 48 * 3_600_000 - 1); await core.escalate();
  assert.equal(events.length, 2);
  setClock(+NOW + 48 * 3_600_000); await core.escalate(); await core.escalate();
  assert.equal(events.filter(e => e.type === 'escalation').length, 2);
});
test('TC-006: low-priority assets do not escalate', async () => {
  const { core, events, setClock } = fixture(); core.upsertAsset(admin, { id: 'a', domain: 'example.test', highPriority: false });
  await core.scan(); setClock(+NOW + 48 * 3_600_000); await core.escalate();
  assert.equal(events.filter(e => e.type === 'escalation').length, 0);
});
test('TC-007: edits replace registry values and removed assets are not scanned', async () => {
  const visited = []; const { core } = fixture({ tlsLookup: async asset => { visited.push(asset.domain); return after(31); } });
  core.upsertAsset(admin, { id: 'a', domain: 'changed.test' }); await core.scan();
  assert.deepEqual(visited, ['changed.test']); core.removeAsset(admin, 'a'); await core.scan();
  assert.deepEqual(visited, ['changed.test']); assert.equal(core.monthlySummary().assets.length, 0);
});
test('TC-008: unauthorized registry mutations and acknowledgment are rejected', async () => {
  const { core } = fixture(); await core.scan();
  for (const role of ['Security Officer', 'unknown']) {
    assert.throws(() => core.upsertAsset({ role }, { id: 'b', domain: 'x.test' }), /Forbidden/);
    assert.throws(() => core.removeAsset({ role }, 'a'), /Forbidden/);
    assert.throws(() => core.acknowledge({ role }, core.alerts[0].id), /Forbidden/);
  }
});
test('TC-009/013: failed lookup does not block other assets; report includes errors and unknowns', async () => {
  const { core } = fixture({ whoisLookup: async asset => { if (asset.id === 'a') throw new Error('rate limit'); return after(46); } });
  core.upsertAsset(admin, { id: 'b', domain: 'second.test' });
  const result = await core.scan(); assert.equal(result.errors.length, 1);
  core.upsertAsset(admin, { id: 'c', domain: 'unscanned.test' });
  const report = core.monthlySummary(); assert.equal(report.assets.length, 3);
  assert.equal(report.assets[0].whois.status, 'error'); assert.equal(report.assets[1].whois.status, 'ok'); assert.equal(report.assets[2].tls.status, 'unknown');
});
test('expiry notification failures stay pending and retry on a repeated scan', async () => {
  let attempts = 0; const { core } = fixture({ notify: async () => { if (++attempts === 1) throw new Error('mail unavailable'); } });
  const first = await core.scan(); assert.equal(first.errors.length, 1); assert.equal(core.alerts[0].delivery, 'pending');
  assert.equal(core.monthlySummary().assets[0].tls.status, 'ok');
  await core.scan(); assert.equal(core.alerts[0].delivery, 'sent'); assert.equal(core.alerts.length, 2);
});
test('lookup failure after a successful scan records failure and preserves last success', async () => {
  let offline = false;
  const { core } = fixture({ tlsLookup: async () => { if (offline) throw new Error('offline'); return after(15); } });
  await core.scan(); offline = true; await core.scan();
  const tls = core.monthlySummary().assets[0].tls;
  assert.equal(tls.status, 'error'); assert.equal(tls.error, 'offline');
  assert.equal(tls.lastSuccess.expiresAt, after(15));
});
