const STORAGE_KEY = "printoptimizer-pro-settings-v1";

const defaultState = {
  settings: {
    theme: "dark",
    autosave: true,
    defaultPrinter: "Bambu X1C",
    defaultFilament: "PLA Basic",
    units: "mm"
  },
  profiles: [
    {
      id: "profile-1",
      name: "Beginner PLA Quality",
      printer: "Bambu X1C",
      filament: "PLA Basic",
      printType: "Miniature",
      goal: "Best Quality",
      settings: {
        layerHeight: 0.12,
        nozzleTemp: 215,
        bedTemp: 60,
        wallCount: 3,
        infill: 15,
        printSpeed: 180,
        cooling: 100
      }
    }
  ],
  queue: [
    {
      id: "queue-1",
      name: "Desk organizer",
      material: "PLA Basic",
      printTime: 6.5,
      weight: 210,
      priority: "Normal",
      status: "Queued"
    }
  ],
  filamentLibrary: [
    {
      name: "PLA Basic",
      type: "PLA",
      color: "Natural",
      nozzle: 205,
      bed: 60,
      notes: "Balanced quality and ease of use for everyday prints."
    },
    {
      name: "PETG Pro",
      type: "PETG",
      color: "Black",
      nozzle: 240,
      bed: 80,
      notes: "Durable and impact-resistant for functional parts."
    },
    {
      name: "ABS Plus",
      type: "ABS",
      color: "Gray",
      nozzle: 245,
      bed: 95,
      notes: "Heat resistant and strong for enclosure-like assemblies."
    },
    {
      name: "TPU Flex",
      type: "TPU",
      color: "Blue",
      nozzle: 220,
      bed: 55,
      notes: "Flexible and forgiving for vibration-damping parts."
    },
    {
      name: "PLA-CF",
      type: "Composite",
      color: "Carbon",
      nozzle: 230,
      bed: 60,
      notes: "Great stiffness and crisp edges for light structural use."
    }
  ]
};

const state = loadState();

const tabButtons = document.querySelectorAll(".tab-button");
const tabPanels = document.querySelectorAll(".tab-panel");
const saveButton = document.getElementById("saveButton");
const profileForm = document.getElementById("profileForm");
const queueForm = document.getElementById("queueForm");
const settingsForm = document.getElementById("settingsForm");
const profileList = document.getElementById("profileList");
const queueList = document.getElementById("queueList");
const filamentList = document.getElementById("filamentList");
const overviewCards = document.getElementById("overviewCards");
const recommendationPanel = document.getElementById("recommendationPanel");
const filamentSearch = document.getElementById("filamentSearch");
const resetProfileFormButton = document.getElementById("resetProfileForm");
const resetDataButton = document.getElementById("resetDataButton");

init();

function init() {
  bindTabs();
  bindForms();
  fillSettingsForm();
  renderAll();
  applyTheme();
}

function loadState() {
  const stored = localStorage.getItem(STORAGE_KEY);
  if (!stored) {
    return structuredClone(defaultState);
  }

  try {
    const parsed = JSON.parse(stored);
    return {
      ...structuredClone(defaultState),
      ...parsed,
      settings: {
        ...defaultState.settings,
        ...(parsed.settings || {})
      },
      profiles: Array.isArray(parsed.profiles) ? parsed.profiles : defaultState.profiles,
      queue: Array.isArray(parsed.queue) ? parsed.queue : defaultState.queue,
      filamentLibrary: Array.isArray(parsed.filamentLibrary)
        ? parsed.filamentLibrary
        : defaultState.filamentLibrary
    };
  } catch (error) {
    return structuredClone(defaultState);
  }
}

function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function bindTabs() {
  tabButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const { tab } = button.dataset;
      tabButtons.forEach((item) => item.classList.toggle("active", item === button));
      tabPanels.forEach((panel) => panel.classList.toggle("active", panel.id === tab));
    });
  });
}

function bindForms() {
  saveButton.addEventListener("click", () => {
    saveState();
    buttonPulse(saveButton, "Saved");
  });

  profileForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const profile = getProfileFromForm();
    const existingId = document.getElementById("profileId").value;

    if (existingId) {
      const index = state.profiles.findIndex((item) => item.id === existingId);
      if (index >= 0) {
        state.profiles[index] = { ...state.profiles[index], ...profile };
      }
    } else {
      state.profiles.unshift({
        id: `profile-${Date.now()}`,
        ...profile
      });
    }

    if (state.settings.autosave) {
      saveState();
    }
    profileForm.reset();
    resetProfileForm();
    renderAll();
  });

  queueForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const job = {
      id: `queue-${Date.now()}`,
      name: document.getElementById("queueName").value.trim(),
      material: document.getElementById("queueMaterial").value.trim(),
      printTime: Number(document.getElementById("queueTime").value),
      weight: Number(document.getElementById("queueWeight").value),
      priority: document.getElementById("queuePriority").value,
      status: "Queued"
    };

    state.queue.unshift(job);
    if (state.settings.autosave) {
      saveState();
    }
    queueForm.reset();
    renderAll();
  });

  settingsForm.addEventListener("submit", (event) => {
    event.preventDefault();
    state.settings.defaultPrinter = document.getElementById("settingPrinter").value.trim() || "Bambu X1C";
    state.settings.defaultFilament = document.getElementById("settingFilament").value.trim() || "PLA Basic";
    state.settings.units = document.getElementById("settingUnits").value;
    state.settings.autosave = document.getElementById("settingAutosave").checked;

    saveState();
    applyTheme();
    renderAll();
  });

  filamentSearch.addEventListener("input", () => renderFilaments());

  resetProfileFormButton.addEventListener("click", () => {
    resetProfileForm();
  });

  resetDataButton.addEventListener("click", () => {
    localStorage.removeItem(STORAGE_KEY);
    Object.keys(state).forEach((key) => delete state[key]);
    Object.assign(state, structuredClone(defaultState));
    fillSettingsForm();
    renderAll();
    saveState();
    buttonPulse(resetDataButton, "Reset");
  });
}

function getProfileFromForm() {
  return {
    name: document.getElementById("profileName").value.trim(),
    printer: document.getElementById("profilePrinter").value.trim(),
    filament: document.getElementById("profileFilament").value.trim(),
    printType: document.getElementById("profileType").value.trim(),
    goal: document.getElementById("profileGoal").value.trim(),
    settings: {
      layerHeight: Number(document.getElementById("profileLayerHeight").value),
      nozzleTemp: Number(document.getElementById("profileNozzleTemp").value),
      bedTemp: Number(document.getElementById("profileBedTemp").value),
      wallCount: Number(document.getElementById("profileWallCount").value),
      infill: Number(document.getElementById("profileInfill").value),
      printSpeed: Number(document.getElementById("profilePrintSpeed").value),
      cooling: Number(document.getElementById("profileCooling").value)
    }
  };
}

function fillSettingsForm() {
  document.getElementById("settingPrinter").value = state.settings.defaultPrinter;
  document.getElementById("settingFilament").value = state.settings.defaultFilament;
  document.getElementById("settingUnits").value = state.settings.units;
  document.getElementById("settingAutosave").checked = state.settings.autosave;
}

function renderAll() {
  renderOverview();
  renderProfiles();
  renderFilaments();
  renderQueue();
  fillSettingsForm();
}

function renderOverview() {
  const totalProfiles = state.profiles.length;
  const activeQueue = state.queue.filter((job) => job.status !== "Completed").length;
  const avgInfill = totalProfiles
    ? Math.round(state.profiles.reduce((sum, item) => sum + (item.settings.infill || 0), 0) / totalProfiles)
    : 0;
  const totalHours = state.queue.reduce((sum, job) => sum + Number(job.printTime || 0), 0);

  const cards = [
    { label: "Profiles", value: totalProfiles },
    { label: "Queue jobs", value: activeQueue },
    { label: "Avg infill", value: `${avgInfill}%` },
    { label: "Total time", value: `${totalHours.toFixed(1)}h` }
  ];

  overviewCards.innerHTML = cards
    .map(
      (card) => `
        <article class="stat-card">
          <div class="stat-label">${card.label}</div>
          <div class="stat-value">${card.value}</div>
        </article>
      `
    )
    .join("");

  const primaryProfile = state.profiles[0] || null;
  const recommendation = primaryProfile
    ? {
        score: 92,
        name: primaryProfile.name,
        printer: primaryProfile.printer,
        filament: primaryProfile.filament,
        settings: primaryProfile.settings,
        type: primaryProfile.printType
      }
    : {
        score: 0,
        name: "No profile yet",
        printer: "—",
        filament: "—",
        settings: {},
        type: "—"
      };

  recommendationPanel.innerHTML = `
    <div class="recommendation-head">
      <div>
        <h3>${recommendation.name}</h3>
        <div class="meta-row">
          <span class="meta-pill">${recommendation.printer}</span>
          <span class="meta-pill">${recommendation.filament}</span>
          <span class="meta-pill">${recommendation.type}</span>
        </div>
      </div>
      <div class="big-score">${recommendation.score}</div>
    </div>
    <div class="meta-line">
      <span>Layer: ${recommendation.settings.layerHeight ?? "—"} mm</span>
      <span>Infill: ${recommendation.settings.infill ?? "—"}%</span>
      <span>Cooling: ${recommendation.settings.cooling ?? "—"}%</span>
    </div>
    <div class="meta-line">
      <span>Nozzle: ${recommendation.settings.nozzleTemp ?? "—"}°C</span>
      <span>Bed: ${recommendation.settings.bedTemp ?? "—"}°C</span>
      <span>Speed: ${recommendation.settings.printSpeed ?? "—"} mm/s</span>
    </div>
  `;
}

function renderProfiles() {
  if (!state.profiles.length) {
    profileList.innerHTML = '<div class="empty-state">No profiles yet. Add one to start optimizing your workflow.</div>';
    return;
  }

  profileList.innerHTML = state.profiles
    .map(
      (profile) => `
        <article class="profile-item">
          <div class="profile-item-header">
            <h4>${profile.name}</h4>
            <span class="chip">${profile.goal}</span>
          </div>
          <div class="meta-line">
            <span>${profile.printer}</span>
            <span>•</span>
            <span>${profile.filament}</span>
            <span>•</span>
            <span>${profile.printType}</span>
          </div>
          <div class="meta-line">
            <span>Layer ${profile.settings.layerHeight} mm</span>
            <span>•</span>
            <span>${profile.settings.nozzleTemp}°C nozzle</span>
            <span>•</span>
            <span>${profile.settings.infill}% infill</span>
          </div>
          <div class="item-actions">
            <button class="action-button" type="button" data-action="edit-profile" data-id="${profile.id}">Edit</button>
            <button class="action-button delete" type="button" data-action="delete-profile" data-id="${profile.id}">Delete</button>
          </div>
        </article>
      `
    )
    .join("");

  profileList.querySelectorAll("[data-action='edit-profile']").forEach((button) => {
    button.addEventListener("click", () => fillProfileForm(button.dataset.id));
  });

  profileList.querySelectorAll("[data-action='delete-profile']").forEach((button) => {
    button.addEventListener("click", () => {
      state.profiles = state.profiles.filter((profile) => profile.id !== button.dataset.id);
      if (state.settings.autosave) {
        saveState();
      }
      renderAll();
    });
  });
}

function fillProfileForm(profileId) {
  const profile = state.profiles.find((item) => item.id === profileId);
  if (!profile) {
    return;
  }

  document.getElementById("profileId").value = profile.id;
  document.getElementById("profileName").value = profile.name;
  document.getElementById("profilePrinter").value = profile.printer;
  document.getElementById("profileFilament").value = profile.filament;
  document.getElementById("profileType").value = profile.printType;
  document.getElementById("profileGoal").value = profile.goal;
  document.getElementById("profileLayerHeight").value = profile.settings.layerHeight;
  document.getElementById("profileNozzleTemp").value = profile.settings.nozzleTemp;
  document.getElementById("profileBedTemp").value = profile.settings.bedTemp;
  document.getElementById("profileWallCount").value = profile.settings.wallCount;
  document.getElementById("profileInfill").value = profile.settings.infill;
  document.getElementById("profilePrintSpeed").value = profile.settings.printSpeed;
  document.getElementById("profileCooling").value = profile.settings.cooling;

  const formButton = profileForm.querySelector("button[type='submit']");
  formButton.textContent = "Update profile";
}

function resetProfileForm() {
  profileForm.reset();
  document.getElementById("profileId").value = "";
  document.getElementById("profilePrinter").value = state.settings.defaultPrinter;
  document.getElementById("profileFilament").value = state.settings.defaultFilament;
  document.getElementById("profileType").value = "Miniature";
  document.getElementById("profileGoal").value = "Best Quality";
  document.getElementById("profileLayerHeight").value = 0.12;
  document.getElementById("profileNozzleTemp").value = 215;
  document.getElementById("profileBedTemp").value = 60;
  document.getElementById("profileWallCount").value = 3;
  document.getElementById("profileInfill").value = 15;
  document.getElementById("profilePrintSpeed").value = 180;
  document.getElementById("profileCooling").value = 100;

  const submitButton = profileForm.querySelector("button[type='submit']");
  submitButton.textContent = "Save profile";
}

function renderFilaments() {
  const query = filamentSearch.value.trim().toLowerCase();
  const filtered = state.filamentLibrary.filter((item) => {
    const haystack = `${item.name} ${item.type} ${item.color} ${item.notes}`.toLowerCase();
    return haystack.includes(query);
  });

  if (!filtered.length) {
    filamentList.innerHTML = '<div class="empty-state">No material matches your search.</div>';
    return;
  }

  filamentList.innerHTML = filtered
    .map(
      (item) => `
        <article class="filament-card">
          <span class="badge">${item.type}</span>
          <h4>${item.name}</h4>
          <div class="meta-line">
            <span>${item.color}</span>
            <span>•</span>
            <span>${item.nozzle}°C nozzle</span>
            <span>•</span>
            <span>${item.bed}°C bed</span>
          </div>
          <p class="meta-line">${item.notes}</p>
        </article>
      `
    )
    .join("");
}

function renderQueue() {
  if (!state.queue.length) {
    queueList.innerHTML = '<div class="empty-state">No jobs in the queue yet.</div>';
    return;
  }

  queueList.innerHTML = state.queue
    .map(
      (job) => `
        <article class="queue-item">
          <div class="queue-item-header">
            <h4>${job.name}</h4>
            <span class="priority-tag ${job.priority.toLowerCase()}">${job.priority}</span>
          </div>
          <div class="meta-line">
            <span>${job.material}</span>
            <span>•</span>
            <span>${job.printTime}h</span>
            <span>•</span>
            <span>${job.weight}g</span>
          </div>
          <div class="item-actions">
            <button class="action-button" type="button" data-action="toggle-status" data-id="${job.id}">${job.status === "Completed" ? "Reopen" : "Complete"}</button>
            <button class="action-button delete" type="button" data-action="delete-job" data-id="${job.id}">Delete</button>
          </div>
        </article>
      `
    )
    .join("");

  queueList.querySelectorAll("[data-action='toggle-status']").forEach((button) => {
    button.addEventListener("click", () => {
      const job = state.queue.find((item) => item.id === button.dataset.id);
      if (!job) {
        return;
      }
      job.status = job.status === "Completed" ? "Queued" : "Completed";
      if (state.settings.autosave) {
        saveState();
      }
      renderAll();
    });
  });

  queueList.querySelectorAll("[data-action='delete-job']").forEach((button) => {
    button.addEventListener("click", () => {
      state.queue = state.queue.filter((job) => job.id !== button.dataset.id);
      if (state.settings.autosave) {
        saveState();
      }
      renderAll();
    });
  });
}

function applyTheme() {
  const root = document.documentElement;
  if (state.settings.theme === "dark") {
    root.style.setProperty("--bg", "#0b1120");
    root.style.setProperty("--bg-soft", "#111827");
    root.style.setProperty("--panel", "rgba(17, 24, 39, 0.9)");
    root.style.setProperty("--card", "#0f172a");
    root.style.setProperty("--card-alt", "#172033");
    root.style.setProperty("--line", "rgba(148, 163, 184, 0.2)");
    root.style.setProperty("--text", "#e2e8f0");
    root.style.setProperty("--text-muted", "#94a3b8");
  }
}

function buttonPulse(button, label) {
  const previous = button.textContent;
  button.textContent = label;
  setTimeout(() => {
    button.textContent = previous;
  }, 800);
}
