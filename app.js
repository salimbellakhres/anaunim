let NETWORKS = [
  {
    id: "instagram",
    name: "Instagram",
    shortName: "IG",
    accent: "#d9467a",
    status: "connected",
    handle: "@anaunim.studio",
    scopes: ["comments", "likes", "saves"],
    capability: "Official adapter needed",
  },
  {
    id: "facebook",
    name: "Facebook",
    shortName: "FB",
    accent: "#1877f2",
    status: "connected",
    handle: "Anaunim",
    scopes: ["comments", "reactions", "shares"],
    capability: "Page-scoped adapter",
  },
  {
    id: "tiktok",
    name: "TikTok",
    shortName: "TT",
    accent: "#00a7b5",
    status: "review",
    handle: "@anaunim",
    scopes: ["comments", "likes", "favorites", "reposts"],
    capability: "Requires app review",
  },
  {
    id: "linkedin",
    name: "LinkedIn",
    shortName: "IN",
    accent: "#0a66c2",
    status: "connected",
    handle: "Anaunim Labs",
    scopes: ["comments", "reactions", "reposts"],
    capability: "Organization/member adapter",
  },
  {
    id: "x",
    name: "X",
    shortName: "X",
    accent: "#111111",
    status: "disconnected",
    handle: "@anaunim",
    scopes: ["replies", "likes", "reposts", "bookmarks"],
    capability: "Elevated access likely",
  },
];

const TYPES = {
  comment: { label: "Comments", singular: "comment", icon: "message-square" },
  reply: { label: "Replies", singular: "reply", icon: "messages-square" },
  like: { label: "Likes", singular: "like", icon: "heart" },
  reaction: { label: "Reactions", singular: "reaction", icon: "thumbs-up" },
  repost: { label: "Reposts", singular: "repost", icon: "repeat-2" },
  share: { label: "Shares", singular: "share", icon: "send" },
  save: { label: "Saves", singular: "save", icon: "bookmark" },
  favorite: { label: "Favorites", singular: "favorite", icon: "star" },
  bookmark: { label: "Bookmarks", singular: "bookmark", icon: "book-marked" },
};

let interactions = [
  {
    id: "ig-001",
    network: "instagram",
    type: "comment",
    status: "active",
    actor: "Mara V.",
    handle: "@maraviews",
    avatar: "assets/avatar-mara.png",
    media: "assets/post-city.png",
    target: "Launch reel",
    text: "Love how this lands visually. Can you share the preset?",
    date: "Today, 09:42",
  },
  {
    id: "ig-002",
    network: "instagram",
    type: "like",
    status: "active",
    actor: "Noam A.",
    handle: "@noamframes",
    avatar: "assets/avatar-noam.png",
    media: "assets/post-studio.png",
    target: "Behind the scenes carousel",
    text: "Liked a carousel from your saved creator list.",
    date: "Today, 08:05",
  },
  {
    id: "ig-003",
    network: "instagram",
    type: "save",
    status: "review",
    actor: "Olivia Chen",
    handle: "@oliviaworks",
    avatar: "assets/avatar-olivia.png",
    media: "assets/post-wire.png",
    target: "Research board",
    text: "Saved a visual benchmark post for campaign planning.",
    date: "Yesterday, 18:21",
  },
  {
    id: "fb-001",
    network: "facebook",
    type: "reaction",
    status: "active",
    actor: "The Atlas Room",
    handle: "facebook.com/atlasroom",
    avatar: "assets/avatar-atlas.png",
    media: "assets/post-city.png",
    target: "Community update",
    text: "Reacted with Like on a partner page post.",
    date: "Today, 11:12",
  },
  {
    id: "fb-002",
    network: "facebook",
    type: "comment",
    status: "active",
    actor: "Local Founders",
    handle: "facebook.com/groups/localfounders",
    avatar: "assets/avatar-founders.png",
    media: "assets/post-studio.png",
    target: "Group discussion",
    text: "We tried a similar workflow last quarter and it scaled well.",
    date: "Jun 18, 16:43",
  },
  {
    id: "fb-003",
    network: "facebook",
    type: "share",
    status: "review",
    actor: "Anaunim",
    handle: "facebook.com/anaunim",
    avatar: "assets/avatar-anaunim.png",
    media: "assets/post-wire.png",
    target: "Event announcement",
    text: "Shared a public event post to the page timeline.",
    date: "Jun 17, 12:10",
  },
  {
    id: "tt-001",
    network: "tiktok",
    type: "like",
    status: "active",
    actor: "Cam Studio",
    handle: "@camstudio",
    avatar: "assets/avatar-cam.png",
    media: "assets/post-motion.png",
    target: "Motion edit",
    text: "Liked a short edit saved for reference.",
    date: "Today, 10:02",
  },
  {
    id: "tt-002",
    network: "tiktok",
    type: "repost",
    status: "review",
    actor: "Pulse Daily",
    handle: "@pulsedaily",
    avatar: "assets/avatar-pulse.png",
    media: "assets/post-motion.png",
    target: "Trend recap",
    text: "Reposted to followers during campaign scouting.",
    date: "Yesterday, 21:54",
  },
  {
    id: "tt-003",
    network: "tiktok",
    type: "favorite",
    status: "active",
    actor: "Niko Builds",
    handle: "@nikobuilds",
    avatar: "assets/avatar-niko.png",
    media: "assets/post-wire.png",
    target: "Creator workflow",
    text: "Added to favorites for outreach research.",
    date: "Jun 17, 08:29",
  },
  {
    id: "li-001",
    network: "linkedin",
    type: "comment",
    status: "active",
    actor: "Sofia Martinez",
    handle: "linkedin.com/in/sofia-martinez",
    avatar: "assets/avatar-sofia.png",
    media: "assets/post-studio.png",
    target: "Founder essay",
    text: "The operational detail here is the interesting part.",
    date: "Today, 07:40",
  },
  {
    id: "li-002",
    network: "linkedin",
    type: "reaction",
    status: "active",
    actor: "Northstar AI",
    handle: "linkedin.com/company/northstar-ai",
    avatar: "assets/avatar-northstar.png",
    media: "assets/post-wire.png",
    target: "Hiring post",
    text: "Reacted with Celebrate on a company update.",
    date: "Jun 18, 14:18",
  },
  {
    id: "li-003",
    network: "linkedin",
    type: "repost",
    status: "review",
    actor: "Anaunim Labs",
    handle: "linkedin.com/company/anaunim",
    avatar: "assets/avatar-anaunim.png",
    media: "assets/post-city.png",
    target: "Partner launch",
    text: "Reposted a partner announcement with added context.",
    date: "Jun 16, 09:02",
  },
  {
    id: "x-001",
    network: "x",
    type: "reply",
    status: "active",
    actor: "Rae",
    handle: "@raewrites",
    avatar: "assets/avatar-rae.png",
    media: "assets/post-city.png",
    target: "Design thread",
    text: "That second example is the cleanest framing.",
    date: "Today, 12:22",
  },
  {
    id: "x-002",
    network: "x",
    type: "like",
    status: "active",
    actor: "Build Notes",
    handle: "@buildnotes",
    avatar: "assets/avatar-build.png",
    media: "assets/post-wire.png",
    target: "Product update",
    text: "Liked a release note thread.",
    date: "Yesterday, 15:36",
  },
  {
    id: "x-003",
    network: "x",
    type: "bookmark",
    status: "review",
    actor: "Alex Morgan",
    handle: "@alexmorgan",
    avatar: "assets/avatar-alex.png",
    media: "assets/post-motion.png",
    target: "API policy thread",
    text: "Bookmarked a policy update for later review.",
    date: "Jun 18, 20:05",
  },
];

const state = {
  activeNetworks: new Set(NETWORKS.map((network) => network.id)),
  activeType: "all",
  status: "all",
  query: "",
  selected: new Set(),
  lastRemoved: null,
  pendingRemoval: null,
  backendOnline: false,
  serverMode: "static-demo",
};

let removalJobs = [];
let auditLog = [];
let providerCapabilities = {};
let metaStatus = null;

const elements = {
  networkList: document.querySelector("#networkList"),
  connectionList: document.querySelector("#connectionList"),
  typeTabs: document.querySelector("#typeTabs"),
  statusFilter: document.querySelector("#statusFilter"),
  searchInput: document.querySelector("#searchInput"),
  interactionList: document.querySelector("#interactionList"),
  queueSummary: document.querySelector("#queueSummary"),
  selectAllVisible: document.querySelector("#selectAllVisible"),
  selectedCount: document.querySelector("#selectedCount"),
  removeSelectedButton: document.querySelector("#removeSelectedButton"),
  clearSelectionButton: document.querySelector("#clearSelectionButton"),
  typeBulkList: document.querySelector("#typeBulkList"),
  capabilityList: document.querySelector("#capabilityList"),
  confirmDialog: document.querySelector("#confirmDialog"),
  confirmTitle: document.querySelector("#confirmTitle"),
  confirmCopy: document.querySelector("#confirmCopy"),
  confirmBreakdown: document.querySelector("#confirmBreakdown"),
  confirmRemoveButton: document.querySelector("#confirmRemoveButton"),
  undoButton: document.querySelector("#undoButton"),
  syncButton: document.querySelector("#syncButton"),
  metaConnectButton: document.querySelector("#metaConnectButton"),
  toast: document.querySelector("#toast"),
  jobList: document.querySelector("#jobList"),
  auditList: document.querySelector("#auditList"),
  backendStatus: document.querySelector("#backendStatus"),
};

const api = {
  async request(path, options = {}) {
    const response = await fetch(path, {
      headers: { "Content-Type": "application/json", ...(options.headers || {}) },
      ...options,
    });

    if (!response.ok) {
      let message = `Request failed with ${response.status}`;
      try {
        const body = await response.json();
        message = body.error || message;
      } catch {
        // Keep the generic HTTP error message.
      }
      throw new Error(message);
    }

    return response.json();
  },

  bootstrap() {
    return this.request("/api/bootstrap");
  },

  sync() {
    return this.request("/api/sync", { method: "POST", body: JSON.stringify({}) });
  },

  remove(ids, mode = "manual") {
    return this.request("/api/removals", {
      method: "POST",
      body: JSON.stringify({ ids, mode, actor: "local-user" }),
    });
  },

  undo(jobId) {
    return this.request("/api/removals/undo", {
      method: "POST",
      body: JSON.stringify({ jobId, actor: "local-user" }),
    });
  },

  toggleAccount(networkId) {
    return this.request("/api/accounts/toggle", {
      method: "POST",
      body: JSON.stringify({ networkId, actor: "local-user" }),
    });
  },
};

function applyServerPayload(payload) {
  NETWORKS = payload.networks || NETWORKS;
  interactions = payload.interactions || interactions;
  removalJobs = payload.jobs || removalJobs;
  auditLog = payload.auditLog || auditLog;
  providerCapabilities = payload.capabilities || providerCapabilities;
  metaStatus = payload.meta || metaStatus;
  state.serverMode = payload.serverMode || state.serverMode;
  state.backendOnline = true;

  const validNetworkIds = new Set(NETWORKS.map((network) => network.id));
  state.activeNetworks = new Set([...state.activeNetworks].filter((id) => validNetworkIds.has(id)));
  if (state.activeNetworks.size === 0) {
    state.activeNetworks = new Set(NETWORKS.map((network) => network.id));
  }

  if (!availableTypes().includes(state.activeType) && state.activeType !== "all") {
    state.activeType = "all";
  }

  trimSelectionToVisible();
}

async function loadBackendState() {
  try {
    const payload = await api.bootstrap();
    applyServerPayload(payload);
  } catch {
    state.backendOnline = false;
    state.serverMode = "static-demo";
  }
  render();
}

function networkById(id) {
  return NETWORKS.find((network) => network.id === id);
}

function typeById(id) {
  return TYPES[id] || { label: id, singular: id, icon: "circle" };
}

function icon(name, fallback) {
  return `<i data-lucide="${name}" data-fallback="${fallback}" aria-hidden="true"></i>`;
}

function activeInteractions() {
  return interactions.filter((item) => item.status !== "removed");
}

function filteredInteractions() {
  const query = state.query.trim().toLowerCase();

  return interactions.filter((item) => {
    const matchesNetwork = state.activeNetworks.has(item.network);
    const matchesType = state.activeType === "all" || item.type === state.activeType;
    const matchesStatus = state.status === "all" || item.status === state.status;
    const haystack = `${item.actor} ${item.handle} ${item.target} ${item.text}`.toLowerCase();
    const matchesQuery = !query || haystack.includes(query);

    return matchesNetwork && matchesType && matchesStatus && matchesQuery;
  });
}

function visibleActiveInteractions() {
  return filteredInteractions().filter((item) => item.status !== "removed");
}

function pluralize(count, singular, plural = `${singular}s`) {
  return `${count} ${count === 1 ? singular : plural}`;
}

function refreshIcons() {
  if (window.lucide) {
    window.lucide.createIcons();
  }
}

function showToast(message) {
  elements.toast.textContent = message;
  elements.toast.classList.add("is-visible");
  window.clearTimeout(showToast.timeoutId);
  showToast.timeoutId = window.setTimeout(() => {
    elements.toast.classList.remove("is-visible");
  }, 2600);
}

function renderNetworks() {
  elements.networkList.innerHTML = NETWORKS.map((network) => {
    const count = interactions.filter(
      (item) => item.network === network.id && item.status !== "removed",
    ).length;
    const active = state.activeNetworks.has(network.id);

    return `
      <button class="network-button ${active ? "is-active" : ""}" type="button" data-network="${network.id}" style="--accent: ${network.accent}">
        <span class="network-mark">${network.shortName}</span>
        <span class="network-name">${network.name}</span>
        <span class="network-count">${count}</span>
      </button>
    `;
  }).join("");
}

function renderConnections() {
  elements.connectionList.innerHTML = NETWORKS.map((network) => {
    const statusLabel = {
      connected: "Connected",
      disconnected: "Disconnected",
      review: "Review",
    }[network.status];

    return `
      <div class="connection-row">
        <span class="connection-dot ${network.status}" style="--accent: ${network.accent}"></span>
        <div>
          <strong>${network.name}</strong>
          <span>${network.handle}</span>
        </div>
        <button class="icon-button" type="button" data-connect="${network.id}" title="${statusLabel}">
          ${icon(network.status === "connected" ? "plug-zap" : "plug", "P")}
        </button>
      </div>
    `;
  }).join("");
}

function availableTypes() {
  const activeNetworkIds = state.activeNetworks.size
    ? [...state.activeNetworks]
    : NETWORKS.map((network) => network.id);
  const typeSet = new Set();

  activeNetworkIds.forEach((networkId) => {
    interactions
      .filter((item) => item.network === networkId && item.status !== "removed")
      .forEach((item) => typeSet.add(item.type));
  });

  return [...typeSet].sort((a, b) => TYPES[a].label.localeCompare(TYPES[b].label));
}

function renderTypeTabs() {
  const types = availableTypes();
  const allCount = visibleCountForType("all");
  const tabs = [
    `
      <button class="tab ${state.activeType === "all" ? "is-active" : ""}" type="button" role="tab" aria-selected="${state.activeType === "all"}" data-type="all">
        All
        <span>${allCount}</span>
      </button>
    `,
    ...types.map((type) => {
      const definition = typeById(type);
      const active = state.activeType === type;
      return `
        <button class="tab ${active ? "is-active" : ""}" type="button" role="tab" aria-selected="${active}" data-type="${type}">
          ${definition.label}
          <span>${visibleCountForType(type)}</span>
        </button>
      `;
    }),
  ];

  elements.typeTabs.innerHTML = tabs.join("");
}

function visibleCountForType(type) {
  return interactions.filter((item) => {
    const matchesNetwork = state.activeNetworks.has(item.network);
    const matchesType = type === "all" || item.type === type;
    const matchesStatus = state.status === "all" || item.status === state.status;
    return matchesNetwork && matchesType && matchesStatus && item.status !== "removed";
  }).length;
}

function renderInteractions() {
  const visible = filteredInteractions();

  if (!visible.length) {
    elements.interactionList.innerHTML = `
      <div class="empty-state">
        ${icon("inbox", "0")}
        <h3>No interactions found</h3>
        <p>Try another network, status, or interaction type.</p>
      </div>
    `;
  } else {
    elements.interactionList.innerHTML = visible.map(renderInteraction).join("");
  }

  const activeVisible = visible.filter((item) => item.status !== "removed");
  const selectedVisible = activeVisible.filter((item) => state.selected.has(item.id));
  elements.selectAllVisible.checked = activeVisible.length > 0 && selectedVisible.length === activeVisible.length;
  elements.selectAllVisible.indeterminate = selectedVisible.length > 0 && selectedVisible.length < activeVisible.length;
  elements.queueSummary.textContent = `${pluralize(activeVisible.length, "visible item")} - ${state.selected.size} selected`;
}

function renderInteraction(item) {
  const network = networkById(item.network);
  const type = typeById(item.type);
  const selected = state.selected.has(item.id);
  const removed = item.status === "removed";

  return `
    <article class="interaction-row ${selected ? "is-selected" : ""} ${removed ? "is-removed" : ""}" style="--accent: ${network.accent}">
      <label class="row-check">
        <input type="checkbox" data-select="${item.id}" ${selected ? "checked" : ""} ${removed ? "disabled" : ""} />
      </label>
      <img class="avatar" src="${item.avatar}" alt="" />
      <div class="interaction-body">
        <div class="interaction-topline">
          <span class="network-pill">
            <span class="mini-mark">${network.shortName}</span>
            ${network.name}
          </span>
          <span class="type-pill">
            ${icon(type.icon, type.singular.slice(0, 1).toUpperCase())}
            ${type.singular}
          </span>
          <span class="status-pill ${item.status}">${item.status}</span>
        </div>
        <h3>${item.target}</h3>
        <p>${item.text}</p>
        <div class="interaction-meta">
          <span>${item.actor}</span>
          <span>${item.handle}</span>
          <span>${item.date}</span>
        </div>
      </div>
      <img class="media-thumb" src="${item.media}" alt="" />
      <div class="row-actions">
        <button class="icon-button" type="button" data-focus="${item.id}" title="Focus item">
          ${icon("scan-search", "F")}
        </button>
        <button class="icon-button danger-icon" type="button" data-remove-one="${item.id}" title="Remove" ${removed ? "disabled" : ""}>
          ${icon("trash-2", "X")}
        </button>
      </div>
    </article>
  `;
}

function renderBulkPanel() {
  const selectedCount = state.selected.size;
  elements.selectedCount.textContent = `${selectedCount} selected`;
  elements.removeSelectedButton.disabled = selectedCount === 0;
  elements.clearSelectionButton.disabled = selectedCount === 0;
  elements.undoButton.disabled = !state.lastRemoved;

  const activeVisible = visibleActiveInteractions();
  const countsByType = activeVisible.reduce((map, item) => {
    map[item.type] = (map[item.type] || 0) + 1;
    return map;
  }, {});

  const rows = Object.entries(countsByType)
    .sort(([a], [b]) => TYPES[a].label.localeCompare(TYPES[b].label))
    .map(([type, count]) => {
      const definition = typeById(type);
      return `
        <div class="type-bulk-row">
          <span class="type-bulk-name">
            ${icon(definition.icon, definition.singular.slice(0, 1).toUpperCase())}
            ${definition.label}
          </span>
          <span class="type-bulk-count">${count}</span>
          <button class="button mini danger" type="button" data-remove-type="${type}">
            Remove
          </button>
        </div>
      `;
    });

  elements.typeBulkList.innerHTML = rows.length
    ? rows.join("")
    : `<div class="subtle-empty">No active visible interactions</div>`;
}

function renderCapabilityList() {
  elements.capabilityList.innerHTML = NETWORKS.map((network) => {
    const active = state.activeNetworks.has(network.id);
    const matrix = providerCapabilities[network.id];
    const sources = matrix?.sources || [];
    return `
      <div class="capability-row ${active ? "is-active" : ""}" style="--accent: ${network.accent}">
        <div class="capability-head">
          <span class="network-mark">${network.shortName}</span>
          <strong>${network.name}</strong>
        </div>
        <span>${network.capability}</span>
        <div class="scope-list">
          ${network.scopes.map((scope) => `<small>${scope}</small>`).join("")}
          ${matrix ? `<small>${matrix.production_status.replaceAll("_", " ")}</small>` : ""}
          ${sources.length ? `<small>${sources.length} docs</small>` : ""}
        </div>
      </div>
    `;
  }).join("");
}

function renderBackendStatus() {
  if (!elements.backendStatus) {
    return;
  }

  const metaText = metaStatus?.hasUserToken
    ? `Meta connected (${metaStatus.accounts?.length || 0} Page accounts)`
    : metaStatus?.configured && !metaStatus?.hasLoginConfigId
      ? "Meta login config ID needed"
    : metaStatus?.configured
      ? "Meta credentials configured"
      : "Meta not configured";

  elements.backendStatus.textContent = state.backendOnline
    ? `Backend online - ${metaText}`
    : "Static demo mode";
  elements.backendStatus.classList.toggle("is-online", state.backendOnline);

  if (elements.metaConnectButton) {
    elements.metaConnectButton.disabled =
      !state.backendOnline || !metaStatus?.configured || !metaStatus?.hasLoginConfigId;
    elements.metaConnectButton.innerHTML = `
      ${icon(metaStatus?.hasUserToken ? "badge-check" : "key-round", "M")}
      ${metaStatus?.hasUserToken ? "Refresh Meta" : "Connect Meta"}
    `;
  }
}

function renderJobs() {
  if (!elements.jobList) {
    return;
  }

  elements.jobList.innerHTML = removalJobs.length
    ? removalJobs.slice(0, 5).map((job) => `
      <div class="job-row">
        <strong>${job.id}</strong>
        <div class="job-meta">
          <small class="${job.status}">${job.status}</small>
          <small>${job.processedCount}/${job.requestedCount} removed</small>
        </div>
        <span>${new Date(job.createdAt).toLocaleString()}</span>
      </div>
    `).join("")
    : `<div class="subtle-empty">No removal jobs yet</div>`;
}

function renderAuditLog() {
  if (!elements.auditList) {
    return;
  }

  elements.auditList.innerHTML = auditLog.length
    ? auditLog.slice(0, 5).map((entry) => `
      <div class="audit-row">
        <strong>${entry.action.replaceAll("_", " ")}</strong>
        <span>${entry.network || "system"}${entry.interactionId ? ` - ${entry.interactionId}` : ""}</span>
        <span>${new Date(entry.createdAt).toLocaleString()}</span>
      </div>
    `).join("")
    : `<div class="subtle-empty">No audit entries yet</div>`;
}

function render() {
  renderBackendStatus();
  renderNetworks();
  renderConnections();
  renderTypeTabs();
  renderInteractions();
  renderBulkPanel();
  renderCapabilityList();
  renderJobs();
  renderAuditLog();
  refreshIcons();
}

function setNetworkFilter(networkId) {
  if (state.activeNetworks.has(networkId)) {
    state.activeNetworks.delete(networkId);
  } else {
    state.activeNetworks.add(networkId);
  }

  if (!availableTypes().includes(state.activeType) && state.activeType !== "all") {
    state.activeType = "all";
  }

  trimSelectionToVisible();
  render();
}

function trimSelectionToVisible() {
  const visibleIds = new Set(visibleActiveInteractions().map((item) => item.id));
  [...state.selected].forEach((id) => {
    if (!visibleIds.has(id)) {
      state.selected.delete(id);
    }
  });
}

function openRemovalDialog(ids, title) {
  const candidates = interactions.filter((item) => ids.includes(item.id) && item.status !== "removed");

  if (!candidates.length) {
    showToast("Nothing active to remove.");
    return;
  }

  const byNetwork = candidates.reduce((map, item) => {
    const network = networkById(item.network).name;
    map[network] = (map[network] || 0) + 1;
    return map;
  }, {});

  const byType = candidates.reduce((map, item) => {
    const type = typeById(item.type).label;
    map[type] = (map[type] || 0) + 1;
    return map;
  }, {});

  state.pendingRemoval = candidates.map((item) => item.id);
  elements.confirmTitle.textContent = title;
  elements.confirmCopy.textContent = state.backendOnline
    ? `This will create a removal job for ${pluralize(candidates.length, "interaction")}. The mock adapter will mark them removed and write audit entries.`
    : `This will mark ${pluralize(candidates.length, "interaction")} as removed in the local queue. Real connectors would call the provider-specific delete or unlike endpoint here.`;
  elements.confirmBreakdown.innerHTML = `
    <div>
      <strong>Networks</strong>
      ${Object.entries(byNetwork).map(([label, count]) => `<span>${label}: ${count}</span>`).join("")}
    </div>
    <div>
      <strong>Types</strong>
      ${Object.entries(byType).map(([label, count]) => `<span>${label}: ${count}</span>`).join("")}
    </div>
  `;

  elements.confirmDialog.showModal();
  refreshIcons();
}

async function removeInteractions(ids) {
  if (state.backendOnline) {
    try {
      const payload = await api.remove(ids, state.activeType === "all" ? "selection" : state.activeType);
      applyServerPayload(payload);
      state.lastRemoved = payload.job || null;
      state.pendingRemoval = null;
      state.selected.clear();
      showToast(`${pluralize(payload.job?.processedCount || 0, "interaction")} queued and removed.`);
      render();
      return;
    } catch (error) {
      showToast(error.message);
      state.pendingRemoval = null;
      render();
      return;
    }
  }

  const removed = [];

  interactions.forEach((item) => {
    if (ids.includes(item.id) && item.status !== "removed") {
      removed.push({ id: item.id, status: item.status });
      item.status = "removed";
      state.selected.delete(item.id);
    }
  });

  if (removed.length) {
    state.lastRemoved = { source: "local", items: removed };
    showToast(`${pluralize(removed.length, "interaction")} removed.`);
  }

  state.pendingRemoval = null;
  render();
}

async function undoLastRemoval() {
  if (!state.lastRemoved) {
    return;
  }

  if (state.backendOnline && state.lastRemoved.id) {
    try {
      const payload = await api.undo(state.lastRemoved.id);
      applyServerPayload(payload);
      state.lastRemoved = null;
      showToast("Last removal job restored.");
      render();
      return;
    } catch (error) {
      showToast(error.message);
      return;
    }
  }

  state.lastRemoved.items.forEach((entry) => {
    const item = interactions.find((candidate) => candidate.id === entry.id);
    if (item) {
      item.status = entry.status;
    }
  });

  const count = state.lastRemoved.items.length;
  state.lastRemoved = null;
  showToast(`${pluralize(count, "interaction")} restored.`);
  render();
}

async function syncMockData() {
  elements.syncButton.classList.add("is-loading");
  elements.syncButton.disabled = true;

  if (state.backendOnline) {
    try {
      const payload = await api.sync();
      applyServerPayload(payload);
      showToast(`${pluralize(payload.syncResults?.length || 0, "provider")} synced.`);
    } catch (error) {
      showToast(error.message);
    } finally {
      elements.syncButton.classList.remove("is-loading");
      elements.syncButton.disabled = false;
      render();
    }
    return;
  }

  window.setTimeout(() => {
    elements.syncButton.classList.remove("is-loading");
    elements.syncButton.disabled = false;
    showToast("Mock providers synced.");
    refreshIcons();
  }, 700);
}

elements.networkList.addEventListener("click", (event) => {
  const button = event.target.closest("[data-network]");
  if (!button) {
    return;
  }
  setNetworkFilter(button.dataset.network);
});

elements.connectionList.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-connect]");
  if (!button) {
    return;
  }

  if (state.backendOnline) {
    try {
      const payload = await api.toggleAccount(button.dataset.connect);
      applyServerPayload(payload);
      const network = networkById(button.dataset.connect);
      showToast(`${network.name} ${network.status}.`);
      render();
    } catch (error) {
      showToast(error.message);
    }
    return;
  }

  const network = networkById(button.dataset.connect);
  network.status = network.status === "connected" ? "disconnected" : "connected";
  showToast(`${network.name} ${network.status === "connected" ? "connected" : "disconnected"}.`);
  render();
});

elements.typeTabs.addEventListener("click", (event) => {
  const tab = event.target.closest("[data-type]");
  if (!tab) {
    return;
  }
  state.activeType = tab.dataset.type;
  trimSelectionToVisible();
  render();
});

elements.statusFilter.addEventListener("change", (event) => {
  state.status = event.target.value;
  trimSelectionToVisible();
  render();
});

elements.searchInput.addEventListener("input", (event) => {
  state.query = event.target.value;
  trimSelectionToVisible();
  render();
});

elements.selectAllVisible.addEventListener("change", (event) => {
  const activeVisible = visibleActiveInteractions();
  if (event.target.checked) {
    activeVisible.forEach((item) => state.selected.add(item.id));
  } else {
    activeVisible.forEach((item) => state.selected.delete(item.id));
  }
  render();
});

elements.interactionList.addEventListener("change", (event) => {
  const checkbox = event.target.closest("[data-select]");
  if (!checkbox) {
    return;
  }

  if (checkbox.checked) {
    state.selected.add(checkbox.dataset.select);
  } else {
    state.selected.delete(checkbox.dataset.select);
  }
  render();
});

elements.interactionList.addEventListener("click", (event) => {
  const removeButton = event.target.closest("[data-remove-one]");
  const focusButton = event.target.closest("[data-focus]");

  if (removeButton) {
    const item = interactions.find((candidate) => candidate.id === removeButton.dataset.removeOne);
    openRemovalDialog([item.id], `Remove this ${typeById(item.type).singular}?`);
    return;
  }

  if (focusButton) {
    const row = focusButton.closest(".interaction-row");
    row.classList.add("is-flashing");
    window.setTimeout(() => row.classList.remove("is-flashing"), 700);
  }
});

elements.removeSelectedButton.addEventListener("click", () => {
  openRemovalDialog([...state.selected], "Remove selected interactions?");
});

elements.clearSelectionButton.addEventListener("click", () => {
  state.selected.clear();
  render();
});

elements.typeBulkList.addEventListener("click", (event) => {
  const button = event.target.closest("[data-remove-type]");
  if (!button) {
    return;
  }

  const ids = visibleActiveInteractions()
    .filter((item) => item.type === button.dataset.removeType)
    .map((item) => item.id);
  openRemovalDialog(ids, `Remove visible ${typeById(button.dataset.removeType).label.toLowerCase()}?`);
});

elements.confirmRemoveButton.addEventListener("click", async () => {
  if (state.pendingRemoval) {
    elements.confirmRemoveButton.disabled = true;
    await removeInteractions(state.pendingRemoval);
    elements.confirmRemoveButton.disabled = false;
  }
  elements.confirmDialog.close();
});

elements.confirmDialog.addEventListener("close", () => {
  state.pendingRemoval = null;
});

elements.undoButton.addEventListener("click", undoLastRemoval);
elements.syncButton.addEventListener("click", syncMockData);
elements.metaConnectButton?.addEventListener("click", () => {
  if (!state.backendOnline || !metaStatus?.configured) {
    showToast("Meta credentials are not configured yet.");
    return;
  }
  window.location.href = "/api/oauth/start?provider=instagram";
});

loadBackendState();
