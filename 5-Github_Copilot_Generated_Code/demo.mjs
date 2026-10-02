import { MonitoringCore } from './monitoring_core.mjs';
const now = new Date('2026-10-02T00:00:00Z');
const events = [];
const core = new MonitoringCore({
  tlsLookup: async () => '2026-10-17T00:00:00Z',
  whoisLookup: async () => '2026-11-16T00:00:00Z',
  notify: async event => events.push(event), now: () => now
});
core.upsertAsset({ id: 'sujay', role: 'SysAdmin' }, { id: 'demo', domain: 'example.test', highPriority: true });
await core.scan();
console.log(JSON.stringify({ mode: 'injected fixture demo; no real network scans or email', events, report: core.monthlySummary() }, null, 2));
