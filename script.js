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
      notes: "Impact resistant and durable for functional parts."
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
      notes: "Flexible and forgiving for vibration-damping applications."
    },
    {
      name: "PLA-CF",
      type: "Composite",
      color: "Carbon",
      nozzle: 230,
      bed: 60,
      notes: "Stiff, lightweight, and ideal for crisp engineering details."
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
const filamentSearch = document.getElementById("filamentSearch");
const overviewCards = document.getElementById("overviewCards");
const recommendationPanel = document.getElementById("recommendationPanel");
const resetProfileFormButton = document.getElementById("resetProfileForm");
const resetDataButton = document.getElementById("resetDataButton");
const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const browseFilesButton = document.getElementById("browseFilesButton");

init();

function init() {
  bindTabs();
  bindForms();
  bindFileDrop();
  fillSettingsForm();
  renderAll();
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
      const target = button.dataset.tab;
      tabButtons.forEach((item) => {
        item.classList.toggle("active", item === button);
      });
      tabPanels.forEach((panel) => {
        panel.classList.toggle("active", panel.id === target);
      });
    });
  });
}

function bindForms() {
  saveButton.addEventListener("click", () => {
    saveState();
    flashButton(saveButton, "Saved");
  });

  profileForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const formData = readProfileForm();
    const existingId = document.getElementById("profileId").value;

    if (existingId) {
      const index = state.profiles.findIndex((profile) => profile.id === existingId);
      if (index >= 0) {
        state.profiles[index] = {
          ...state.profiles[index],
          ...formData
        };
      }
    } else {
      state.profiles.unshift({
        id: `profile-${Date.now()}`,
        ...formData
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

    if (!job.name || !job.material) {
      return;
    }

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
    renderAll();
  });

  filamentSearch.addEventListener("input", () => {
    renderFilaments();
  });

  resetProfileFormButton.addEventListener("click", () => {
    resetProfileForm();
  });

  resetDataButton.addEventListener("click", () => {
    if (!confirm("Reset all saved browser data?")) {
      return;
    }

    Object.keys(state).forEach((key) => delete state[key]);
    Object.assign(state, structuredClone(defaultState));
    fillSettingsForm();
    renderAll();
    saveState();
    flashButton(resetDataButton, "Reset");
  });

  browseFilesButton.addEventListener("click", () => fileInput.click());
  fileInput.addEventListener("change", (event) => {
    const files = Array.from(event.target.files || []);
    if (files.length) {
      addDroppedFiles(files);
    }
    fileInput.value = "";
  });
}

function bindFileDrop() {
  ["dragenter", "dragover"].forEach((eventName) => {
    dropZone.addEventListener(eventName, (event) => {
      event.preventDefault();
      event.stopPropagation();
      dropZone.classList.add("dragover");
    });
  });

  ["dragleave", "drop"].forEach((eventName) => {
    dropZone.addEventListener(eventName, (event) => {
      event.preventDefault();
      event.stopPropagation();
      dropZone.classList.remove("dragover");
    });
  });

  dropZone.addEventListener("drop", (event) => {
    const files = Array.from(event.dataTransfer?.files || []);
    if (files.length) {
      addDroppedFiles(files);
    }
  });

  dropZone.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      fileInput.click();
    }
  });
}

function addDroppedFiles(files) {
  const supported = files.filter((file) => isSupportedPrintFile(file.name));

  if (!supported.length) {
    alert("Please drop a supported printable file: STL, OBJ, 3MF, G-code, AMF, or STEP.");
    return;
  }

  const chosen = supported[0];
  const name = stripExtension(chosen.name);
  const estimatedHours = estimatePrintTime(chosen.size);
  const material = detectMaterial(chosen.name);

  document.getElementById("queueName").value = name;
  document.getElementById("queueMaterial").value = material;
  document.getElementById("queueTime").value = estimatedHours;
  document.getElementById("queueWeight").value = Math.max(80, Math.round(chosen.size / 120));
  document.getElementById("queuePriority").value = "Normal";

  flashButton(dropZone.querySelector("h4"), "File ready");
}

function isSupportedPrintFile(name) {
  const allowed = [
    ".stl",
    ".3mf",
    ".obj",
    ".gcode",
    ".gcodes",
    ".amf",
    ".step",
    ".stp"
  ];

  const lower = name.toLowerCase();
  return allowed.some((ext) => lower.endsWith(ext));
}

function stripExtension(name) {
  return name.replace(/\.[^/.]+$/, "") || name;
}

function estimatePrintTime(sizeBytes) {
  const mb = sizeBytes / (1024 * 1024);
  return Math.min(48, Math.max(1.5, Number((mb * 1.7 + 2).toFixed(1))));
}

function detectMaterial(fileName) {
  const lower = fileName.toLowerCase();
  if (lower.includes("petg")) return "PETG Pro";
  if (lower.includes("abs")) return "ABS Plus";
  if (lower.includes("tpu") || lower.includes("flex")) return "TPU Flex";
  if (lower.includes("cf") || lower.includes("carbon")) return "PLA-CF";
  return "PLA Basic";
}

function readProfileForm() {
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
  const activeQueue = state.queue.filter((item) => item.status !== "Completed").length;
  const avgInfill = totalProfiles
    ? Math.round(
        state.profiles.reduce((sum, item) => sum + Number(item.settings.infill || 0), 0) / totalProfiles
      )
    : 0;
  const totalHours = state.queue.reduce((sum, item) => sum + Number(item.printTime || 0), 0);

  const cards = [
    { label: "Profiles", value: totalProfiles },
    { label: "Queue jobs", value: activeQueue },
    { label: "Avg infill", value: `${avgInfill}%` },
    { label: "Print hours", value: `${totalHours.toFixed(1)}h` }
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

  const profile = state.profiles[0];
  const recommendation = profile
    ? {
        score: 92,
        name: profile.name,
        printer: profile.printer,
        filament: profile.filament,
        settings: profile.settings,
        printType: profile.printType
      }
    : {
        score: 0,
        name: "No profile yet",
        printer: "—",
        filament: "—",
        settings: {},
        printType: "—"
      };

  recommendationPanel.innerHTML = `
    <div class="recommendation-head">
      <div>
        <h3>${recommendation.name}</h3>
        <div class="meta-row">
          <span class="meta-pill">${recommendation.printer}</span>
          <span class="meta-pill">${recommendation.filament}</span>
          <span class="meta-pill">${recommendation.printType}</span>
        </div>
      </div>
      <div class="big-score">${recommendation.score}</div>
    </div>

    <div class="meta-line">
      <span>Layer: ${recommendation.settings.layerHeight ?? "—"} mm</span>
      <span>•</span>
      <span>Infill: ${recommendation.settings.infill ?? "—"}%</span>
      <span>•</span>
      <span>Cooling: ${recommendation.settings.cooling ?? "—"}%</span>
    </div>

    <div class="meta-line">
      <span>Nozzle: ${recommendation.settings.nozzleTemp ?? "—"}°C</span>
      <span>•</span>
      <span>Bed: ${recommendation.settings.bedTemp ?? "—"}°C</span>
      <span>•</span>
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
    button.addEventListener("click", () => {
      fillProfileForm(button.dataset.id);
    });
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
  if (!profile) return;

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

  const submitButton = profileForm.querySelector("button[type='submit']");
  submitButton.textContent = "Update profile";
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
  const filtered = state.filamentLibrary.filter((material) => {
    const haystack = `${material.name} ${material.type} ${material.color} ${material.notes}`.toLowerCase();
    return haystack.includes(query);
  });

  if (!filtered.length) {
    filamentList.innerHTML = '<div class="empty-state">No materials match your search.</div>';
    return;
  }

  filamentList.innerHTML = filtered
    .map(
      (material) => `
        <article class="filament-card">
          <span class="badge">${material.type}</span>
          <h4>${material.name}</h4>
          <div class="meta-line">
            <span>${material.color}</span>
            <span>•</span>
            <span>${material.nozzle}°C nozzle</span>
            <span>•</span>
            <span>${material.bed}°C bed</span>
          </div>
          <p class="meta-line">${material.notes}</p>
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
            <button class="action-button" type="button" data-action="toggle-status" data-id="${job.id}">
              ${job.status === "Completed" ? "Reopen" : "Complete"}
            </button>
            <button class="action-button delete" type="button" data-action="delete-job" data-id="${job.id}">Delete</button>
          </div>
        </article>
      `
    )
    .join("");

  queueList.querySelectorAll("[data-action='toggle-status']").forEach((button) => {
    button.addEventListener("click", () => {
      const job = state.queue.find((item) => item.id === button.dataset.id);
      if (!job) return;

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

function flashButton(buttonOrElement, label) {
  const element = buttonOrElement instanceof HTMLElement ? buttonOrElement : null;
  if (!element) return;

  const previous = element.textContent;
  element.textContent = label;

  setTimeout(() => {
    element.textContent = previous;
  }, 800);
}
