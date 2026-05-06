/* World Monitor — frontend logic */

const state = {
  region: "all",
  category: "all",
  q: "",
  minImportance: 0,
  meta: { regions: {}, categories: {}, refresh_interval_seconds: 600 },
};

const $ = (id) => document.getElementById(id);

// ─── helpers ───────────────────────────────
function fmtTime(iso) {
  if (!iso) return "—";
  try {
    const d = new Date(iso);
    const now = new Date();
    const diff = (now - d) / 1000;
    if (diff < 60) return `${Math.floor(diff)}s ago`;
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
    return d.toISOString().slice(0, 16).replace("T", " ");
  } catch {
    return iso;
  }
}

function importanceClass(score) {
  if (score >= 6) return "crit";
  if (score >= 3) return "warn";
  if (score >= 1) return "norm";
  return "";
}

function escapeHtml(s) {
  return (s || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// ─── filter chips ───────────────────────────────
function buildChips(containerId, key, options, includeAll = true) {
  const c = $(containerId);
  // ラベル(span.label) 以外を除去
  Array.from(c.querySelectorAll(".chip")).forEach((el) => el.remove());

  const opts = includeAll ? { all: "All", ...options } : options;
  Object.entries(opts).forEach(([k, label]) => {
    const b = document.createElement("button");
    b.className = "chip";
    b.dataset.value = k;
    b.textContent = label;
    if (state[key] === k) b.classList.add("active");
    b.addEventListener("click", () => {
      state[key] = k;
      Array.from(c.querySelectorAll(".chip")).forEach((el) =>
        el.classList.toggle("active", el.dataset.value === k)
      );
      loadEvents();
    });
    c.appendChild(b);
  });
}

// ─── data loading ───────────────────────────────
async function fetchJSON(url, opts) {
  const res = await fetch(url, opts);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

async function loadMeta() {
  const meta = await fetchJSON("/api/meta");
  state.meta = meta;
  buildChips("region-filters", "region", meta.regions);
  buildChips("category-filters", "category", meta.categories);
}

async function loadStats() {
  try {
    const s = await fetchJSON("/api/stats");
    $("stat-total").textContent = s.total ?? 0;
    $("stat-mil").textContent = s.by_category?.military ?? 0;
    $("stat-pol").textContent = s.by_category?.politics ?? 0;
    $("stat-cyb").textContent = s.by_category?.cyber ?? 0;

    const bars = $("region-bars");
    bars.innerHTML = "";
    const rmap = state.meta.regions || {};
    const items = Object.entries(rmap)
      .map(([k, name]) => [k, name, s.by_region?.[k] ?? 0])
      .sort((a, b) => b[2] - a[2]);
    const maxv = Math.max(1, ...items.map((x) => x[2]));
    items.forEach(([_, name, n]) => {
      const row = document.createElement("div");
      row.className = "bar-row";
      row.innerHTML = `
        <span class="name">${name}</span>
        <span class="bar"><span style="width:${(n / maxv) * 100}%"></span></span>
        <span class="val">${n}</span>
      `;
      bars.appendChild(row);
    });
  } catch (e) {
    console.warn("stats failed", e);
  }
}

async function loadSources() {
  try {
    const { sources } = await fetchJSON("/api/sources");
    const ul = $("sources");
    ul.innerHTML = "";
    if (!sources?.length) {
      ul.innerHTML = `<li><span class="s-name" style="color:var(--muted)">(まだフェッチされていません)</span></li>`;
      return;
    }
    sources
      .sort((a, b) => (b.last_fetched_at || "").localeCompare(a.last_fetched_at || ""))
      .forEach((s) => {
        const li = document.createElement("li");
        const cls = s.last_status === "ok" ? "ok" : "error";
        li.innerHTML = `
          <span class="s-status ${cls}" title="${s.last_status}"></span>
          <span class="s-name">${escapeHtml(s.name)}</span>
          <span class="s-count">${s.item_count ?? 0}</span>
        `;
        if (s.last_error) li.title = s.last_error;
        ul.appendChild(li);
      });
  } catch (e) {
    console.warn("sources failed", e);
  }
}

async function loadEvents() {
  const params = new URLSearchParams();
  if (state.region !== "all") params.set("region", state.region);
  if (state.category !== "all") params.set("category", state.category);
  if (state.q) params.set("q", state.q);
  if (state.minImportance > 0) params.set("min_importance", state.minImportance);
  params.set("limit", "300");

  try {
    const { events } = await fetchJSON("/api/events?" + params.toString());
    renderEvents(events || []);
    $("feed-meta").textContent = `${events.length} events`;
  } catch (e) {
    console.warn("events failed", e);
    $("feed-meta").textContent = "error";
  }
}

function renderEvents(events) {
  const ul = $("events");
  ul.innerHTML = "";
  $("empty-state").hidden = events.length > 0;

  for (const ev of events) {
    const li = document.createElement("li");
    li.className = `event ${importanceClass(ev.importance)}`;
    const tags = (ev.categories || [])
      .map((c) => `<span class="tag">${escapeHtml(c)}</span>`)
      .join("");
    const region = ev.region && ev.region !== "global"
      ? `<span class="tag region">${escapeHtml(state.meta.regions[ev.region] || ev.region)}</span>`
      : "";
    li.innerHTML = `
      <div class="top">
        <span class="src">${escapeHtml(ev.source)}</span>
        <span>${fmtTime(ev.published_at || ev.fetched_at)}<span class="imp">${ev.importance?.toFixed(1) ?? "0.0"}</span></span>
      </div>
      <div class="title-line">
        <a href="${escapeHtml(ev.url)}" target="_blank" rel="noopener">${escapeHtml(ev.title)}</a>
      </div>
      ${ev.summary ? `<div class="summary">${escapeHtml(ev.summary)}</div>` : ""}
      <div class="tags">${region}${tags}</div>
    `;
    ul.appendChild(li);
  }
}

// ─── interactions ───────────────────────────────
let searchTimer = null;
$("search").addEventListener("input", (e) => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => {
    state.q = e.target.value.trim();
    loadEvents();
  }, 250);
});

$("importance").addEventListener("input", (e) => {
  const v = parseFloat(e.target.value);
  state.minImportance = v;
  $("importance-val").textContent = v.toFixed(1) + "+";
});
$("importance").addEventListener("change", () => loadEvents());

$("refresh").addEventListener("click", async () => {
  const btn = $("refresh");
  btn.disabled = true;
  btn.textContent = "… refreshing";
  try {
    await fetch("/api/refresh", { method: "POST" });
    await Promise.all([loadEvents(), loadStats(), loadSources()]);
    $("last-update").textContent = "Updated " + new Date().toISOString().slice(11, 19) + " UTC";
  } catch (e) {
    console.warn(e);
  } finally {
    btn.disabled = false;
    btn.textContent = "⟳ Refresh";
  }
});

// ─── boot ───────────────────────────────
async function boot() {
  await loadMeta();
  await Promise.all([loadEvents(), loadStats(), loadSources()]);
  $("last-update").textContent = "Updated " + new Date().toISOString().slice(11, 19) + " UTC";

  // 1 分ごとにポーリング (バックエンドは別途 10 分ごとに自動更新)
  setInterval(async () => {
    await Promise.all([loadEvents(), loadStats(), loadSources()]);
    $("last-update").textContent = "Updated " + new Date().toISOString().slice(11, 19) + " UTC";
  }, 60_000);
}

boot();
