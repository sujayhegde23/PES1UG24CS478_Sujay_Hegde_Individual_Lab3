// Codex-authored local prototype. This is not GitHub Copilot output.
// Lookup, notification, and clock adapters are injected; state is in memory.
import { setTimeout as delay } from 'node:timers/promises';
const DAY = 86_400_000;
const HOUR = 3_600_000;
const THRESHOLDS = { tls: [30, 15, 3], whois: [45, 30, 7] };
function utc(value) {
  const date = new Date(value);
  if (!Number.isFinite(date.getTime())) throw new TypeError('Invalid timestamp');
  return date;
}
function requireAdmin(actor) {
  if (actor?.role !== 'SysAdmin') throw new Error('Forbidden: SysAdmin required');
}
export function expiryThreshold(kind, expiresAt, now) {
  if (!THRESHOLDS[kind]) throw new TypeError('Unsupported lookup kind');
  const days = Math.ceil((utc(expiresAt) - utc(now)) / DAY);
  return days <= 0 ? 'expired' : THRESHOLDS[kind].includes(days) ? days : null;
}
export async function boundedLookup(operation, sleep = delay) {
  // Initial attempt plus at most three retries, at 1s / 2s / 4s.
  for (let attempt = 0; attempt < 4; attempt++) {
    try { return await operation(); }
    catch (error) {
      if (attempt === 3) throw error;
      await sleep(1000 * 2 ** attempt);
    }
  }
}
export class MonitoringCore {
  #assets = new Map();
  #alerts = new Map();
  #results = new Map();
  constructor({ tlsLookup, whoisLookup, notify, now = () => new Date(), sleep = delay }) {
    for (const adapter of [tlsLookup, whoisLookup, notify]) {
      if (typeof adapter !== 'function') throw new TypeError('Lookup and notification adapters required');
    }
    Object.assign(this, { tlsLookup, whoisLookup, notify, now, sleep });
  }
  upsertAsset(actor, asset) {
    requireAdmin(actor);
    if (!asset?.id || !asset.domain || typeof asset.domain !== 'string') throw new TypeError('Asset ID and domain required');
    this.#assets.set(asset.id, { ...asset, highPriority: Boolean(asset.highPriority) });
  }
  removeAsset(actor, id) { requireAdmin(actor); this.#assets.delete(id); }
  get alerts() { return [...this.#alerts.values()].map(a => structuredClone(a)); }
  async scan() {
    const errors = [];
    for (const asset of [...this.#assets.values()]) {
      for (const kind of ['tls', 'whois']) {
        const key = `${asset.id}/${kind}`;
        let expiresAt;
        const checkedAt = utc(this.now()).toISOString();
        try {
          const raw = await boundedLookup(() => this[`${kind}Lookup`]({ ...asset }), this.sleep);
          expiresAt = utc(raw).toISOString();
        } catch (error) {
          const previous = this.#results.get(key);
          const lastSuccess = previous?.status === 'ok' ? previous : previous?.lastSuccess;
          this.#results.set(key, { status: 'error', error: error.message, checkedAt, ...(lastSuccess ? { lastSuccess } : {}) });
          errors.push({ assetId: asset.id, kind, error: error.message });
          continue;
        }
        this.#results.set(key, { status: 'ok', expiresAt, checkedAt });
        try {
          const threshold = expiryThreshold(kind, expiresAt, checkedAt);
          if (threshold === null) continue;
          const id = `${key}/${expiresAt}/${threshold}`;
          if (!this.#alerts.has(id)) {
            this.#alerts.set(id, { id, assetId: asset.id, kind, expiresAt, threshold,
              createdAt: checkedAt, state: 'open', delivery: 'pending' });
          }
          const alert = this.#alerts.get(id);
          if (alert.delivery === 'pending') {
            await this.notify({ type: 'expiry', alert: structuredClone(alert) });
            alert.delivery = 'sent';
          }
        } catch (error) {
          errors.push({ assetId: asset.id, kind, stage: 'notification', error: error.message });
        }
      }
    }
    return { errors };
  }
  acknowledge(actor, id) {
    requireAdmin(actor);
    const alert = this.#alerts.get(id);
    if (!alert) throw new Error('Unknown alert');
    if (!this.#assets.has(alert.assetId)) throw new Error('Asset no longer monitored');
    if (alert.state === 'open') {
      alert.state = 'acknowledged';
      alert.acknowledgedBy = actor.id;
      alert.acknowledgedAt = utc(this.now()).toISOString();
    }
  }
  async escalate() {
    for (const alert of this.#alerts.values()) {
      const asset = this.#assets.get(alert.assetId);
      if (!asset?.highPriority || alert.state !== 'open') continue;
      if (utc(this.now()) - utc(alert.createdAt) < 48 * HOUR) continue;
      await this.notify({ type: 'escalation', recipientRole: 'Security Officer', alert: structuredClone(alert) });
      alert.state = 'escalated';
      alert.escalatedAt = utc(this.now()).toISOString();
    }
  }
  monthlySummary() {
    return {
      generatedAt: utc(this.now()).toISOString(),
      assets: [...this.#assets.values()].map(asset => ({ ...asset,
        tls: structuredClone(this.#results.get(`${asset.id}/tls`) || { status: 'unknown' }),
        whois: structuredClone(this.#results.get(`${asset.id}/whois`) || { status: 'unknown' }) }))
    };
  }
}
