// ═══════════════════════════════════════════════════════════════
//  APP.JS — Main Application Logic
//  Interactive Data Analysis Web Sandbox
// ═══════════════════════════════════════════════════════════════

(function () {
  "use strict";

  // ── State ──────────────────────────────────────────────────
  const state = {
    pyodide: null,
    editor: null,
    activeProject: null,     // 'ecommerce' | 'health' | 'stock'
    activeChallenge: null,   // index within project
    pyodideReady: false,
    running: false,
    completedChallenges: new Set(),
    lastOutput: "",
    lastHasChart: false,
  };

  // ── DOM References ─────────────────────────────────────────
  const dom = {
    loadingScreen: document.getElementById("loading-screen"),
    loadingProgressBar: document.getElementById("loading-progress-bar"),
    loadingSteps: document.querySelectorAll(".loading-status .step"),
    appContainer: document.getElementById("app-container"),
    projectTabs: document.querySelectorAll(".project-tab"),
    sidebarProjectName: document.getElementById("sidebar-project-name"),
    challengesList: document.getElementById("challenges-list"),
    challengeInfoBar: document.getElementById("challenge-info-bar"),
    challengeTitle: document.getElementById("challenge-title"),
    challengeDesc: document.getElementById("challenge-desc"),
    hintBtn: document.getElementById("hint-btn"),
    hintPopup: document.getElementById("hint-popup"),
    editorWrapper: document.getElementById("editor-wrapper"),
    outputContent: document.getElementById("output-content"),
    btnRun: document.getElementById("btn-run"),
    btnCheck: document.getElementById("btn-check"),
    btnClear: document.getElementById("btn-clear"),
    statusDot: document.getElementById("status-dot"),
    statusText: document.getElementById("status-text"),
    toastContainer: document.getElementById("toast-container"),
    welcomeState: document.getElementById("welcome-state"),
    editorPanel: document.getElementById("editor-panel"),
  };

  // ── Initialize CodeMirror ──────────────────────────────────
  function initEditor() {
    state.editor = CodeMirror(dom.editorWrapper, {
      value: "# Select a challenge from the sidebar to begin\n",
      mode: "python",
      lineNumbers: true,
      indentUnit: 4,
      tabSize: 4,
      indentWithTabs: false,
      matchBrackets: true,
      autoCloseBrackets: true,
      styleActiveLine: true,
      lineWrapping: true,
      extraKeys: {
        "Ctrl-Enter": () => runCode(),
        "Shift-Enter": () => runCode(),
        Tab: (cm) => {
          if (cm.somethingSelected()) {
            cm.indentSelection("add");
          } else {
            cm.replaceSelection("    ", "end");
          }
        },
      },
    });
  }

  // ── Pyodide Initialization ─────────────────────────────────
  async function initPyodide() {
    try {
      updateLoadingStep(0, "active");
      updateProgress(10);

      state.pyodide = await loadPyodide({
        indexURL: "https://cdn.jsdelivr.net/pyodide/v0.24.1/full/",
      });

      updateLoadingStep(0, "done");
      updateLoadingStep(1, "active");
      updateProgress(30);

      // Install packages
      await state.pyodide.loadPackage(["micropip"]);
      updateProgress(40);
      await state.pyodide.loadPackage(["numpy"]);
      updateProgress(50);
      await state.pyodide.loadPackage(["pandas"]);
      updateProgress(65);
      await state.pyodide.loadPackage(["matplotlib"]);
      updateProgress(75);
      await state.pyodide.loadPackage(["scikit-learn"]);
      updateProgress(85);

      updateLoadingStep(1, "done");
      updateLoadingStep(2, "active");
      updateProgress(88);

      // Set up the virtual filesystem
      state.pyodide.FS.mkdir("/data");
      state.pyodide.FS.mkdir("/output");

      // Load datasets from ../datasets/
      const datasets = [
        { name: "ecommerce_transactions.csv", path: "../datasets/ecommerce_transactions.csv" },
        { name: "health_risk_data.csv", path: "../datasets/health_risk_data.csv" },
        { name: "stock_market_data.csv", path: "../datasets/stock_market_data.csv" },
        { name: "customer_segmentation_data.csv", path: "../datasets/customer_segmentation_data.csv" },
        { name: "house_prices_data.csv", path: "../datasets/house_prices_data.csv" },
        { name: "product_reviews_data.csv", path: "../datasets/product_reviews_data.csv" },
        { name: "energy_consumption_data.csv", path: "../datasets/energy_consumption_data.csv" },
        { name: "company_database.db", path: "../datasets/company_database.db" },
      ];

      for (const ds of datasets) {
        try {
          const response = await fetch(ds.path);
          if (response.ok) {
            if (ds.name.endsWith(".db")) {
              const buffer = await response.arrayBuffer();
              state.pyodide.FS.writeFile(`/data/${ds.name}`, new Uint8Array(buffer));
            } else {
              const text = await response.text();
              state.pyodide.FS.writeFile(`/data/${ds.name}`, text);
            }
          } else {
            console.warn(`Dataset ${ds.name} not found at ${ds.path}, creating placeholder.`);
            createPlaceholderDataset(ds.name);
          }
        } catch (e) {
          console.warn(`Failed to load ${ds.name}:`, e);
          createPlaceholderDataset(ds.name);
        }
      }

      updateLoadingStep(2, "done");
      updateLoadingStep(3, "active");
      updateProgress(92);

      // Configure matplotlib backend
      await state.pyodide.runPythonAsync(`
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
print("Python environment ready!")
      `);

      updateLoadingStep(3, "done");
      updateProgress(100);

      state.pyodideReady = true;
      dom.statusDot.classList.remove("loading");
      dom.statusDot.classList.add("ready");
      dom.statusText.textContent = "Python Ready";
      dom.btnRun.disabled = false;

      // Slight delay for visual satisfaction
      await sleep(600);
      dom.loadingScreen.classList.add("hidden");
      dom.appContainer.classList.add("visible");

    } catch (err) {
      console.error("Pyodide init failed:", err);
      dom.statusText.textContent = "Init Failed";
      showToast("❌ Failed to initialize Python environment. Please refresh.", "error");

      // Show app anyway so user can see the error
      await sleep(1000);
      dom.loadingScreen.classList.add("hidden");
      dom.appContainer.classList.add("visible");
    }
  }

  function createPlaceholderDataset(name) {
    let csv = "";
    if (name === "ecommerce_transactions.csv") {
      csv = `transaction_id,customer_id,date,product,category,price,quantity,payment_method
1,C001,2023-01-05,Widget A,Electronics,29.99,2,Credit Card
2,C002,2023-01-06,Gadget B,Electronics,49.99,1,PayPal
3,C003,2023-01-06,Shirt C,Clothing,19.99,3,Credit Card
4,C001,2023-01-10,Widget D,Electronics,99.99,1,Debit Card
5,C004,2023-01-12,Pants E,Clothing,39.99,2,Credit Card
6,C002,2023-02-01,Gadget F,Electronics,149.99,1,PayPal
7,C005,2023-02-05,Shoes G,Clothing,59.99,1,Credit Card
8,C003,2023-02-08,Widget A,Electronics,29.99,4,Credit Card
9,C001,2023-02-15,Book H,Books,12.99,2,Debit Card
10,C006,2023-03-01,Widget A,Electronics,29.99,1,Credit Card
11,C004,2023-03-05,Gadget B,Electronics,49.99,2,PayPal
12,C002,2023-03-10,Shirt I,Clothing,24.99,1,Credit Card
13,C005,2023-03-15,Book J,Books,15.99,3,Debit Card
14,C007,2023-04-01,Widget D,Electronics,99.99,1,Credit Card
15,C003,2023-04-10,Shoes K,Clothing,79.99,1,PayPal
16,C001,2023-04-20,Gadget F,Electronics,149.99,1,Credit Card
17,C006,2023-05-01,Shirt C,Clothing,19.99,2,Debit Card
18,C008,2023-05-12,Widget A,Electronics,29.99,5,Credit Card
19,C002,2023-05-20,Book L,Books,22.99,1,PayPal
20,C004,2023-06-01,Gadget B,Electronics,49.99,3,Credit Card`;
    } else if (name === "health_risk_data.csv") {
      csv = `patient_id,age,gender,bmi,blood_pressure_systolic,blood_pressure_diastolic,cholesterol,glucose,smoking,exercise_hours_per_week,family_history,risk_level
P001,45,Male,27.5,130,85,210,95,Yes,2.5,Yes,High
P002,32,Female,22.1,118,75,180,88,No,5.0,No,Low
P003,58,Male,31.2,145,92,250,110,Yes,1.0,Yes,High
P004,41,Female,25.8,125,80,195,92,No,3.5,No,Medium
P005,67,Male,29.3,155,95,230,105,No,1.5,Yes,High
P006,28,Female,21.5,112,70,165,82,No,6.0,No,Low
P007,53,Male,28.7,138,88,220,100,Yes,2.0,Yes,High
P008,36,Female,24.3,120,76,185,90,No,4.5,No,Low
P009,49,Male,26.9,132,84,205,98,No,3.0,Yes,Medium
P010,62,Female,30.1,148,91,240,108,No,1.0,Yes,High
P011,38,Male,23.8,122,78,178,86,No,5.5,No,Low
P012,55,Female,27.2,135,86,215,102,Yes,2.0,Yes,High
P013,44,Male,25.5,128,82,200,94,No,3.5,No,Medium
P014,71,Female,29.8,152,93,245,112,No,0.5,Yes,High
P015,33,Male,22.8,116,74,172,84,No,6.0,No,Low
P016,50,Female,26.4,130,83,208,96,Yes,2.5,Yes,Medium
P017,39,Male,24.0,124,79,188,91,No,4.0,No,Low
P018,61,Female,28.5,142,90,235,106,No,1.5,Yes,High
P019,47,Male,27.0,133,85,212,99,Yes,2.0,No,Medium
P020,56,Female,25.2,136,87,218,101,No,3.0,Yes,Medium`;
    } else if (name === "stock_market_data.csv") {
      csv = `date,ticker,open,high,low,close,volume
2023-01-03,AAPL,130.28,131.74,129.64,131.12,112117500
2023-01-04,AAPL,131.25,133.51,130.06,132.94,89113600
2023-01-05,AAPL,132.69,133.41,129.89,130.15,80962700
2023-01-06,AAPL,130.57,131.63,128.12,131.56,87754700
2023-01-09,AAPL,131.79,134.92,131.66,134.68,70790800
2023-01-03,GOOGL,89.56,90.40,88.57,89.70,26234300
2023-01-04,GOOGL,89.57,90.18,88.40,89.95,21786700
2023-01-05,GOOGL,89.66,90.31,88.09,88.37,23827100
2023-01-06,GOOGL,88.13,89.99,87.91,89.58,23894600
2023-01-09,GOOGL,90.14,91.40,89.88,91.26,23447200
2023-01-03,MSFT,243.08,245.75,241.28,244.48,25740000
2023-01-04,MSFT,244.73,246.44,240.89,241.22,21996100
2023-01-05,MSFT,240.41,242.04,237.40,239.23,23737200
2023-01-06,MSFT,239.25,243.30,238.16,243.08,23353000
2023-01-09,MSFT,244.00,247.16,243.32,246.67,20200400
2023-01-03,AMZN,85.46,86.96,84.72,85.82,59167900
2023-01-04,AMZN,86.13,87.45,85.46,86.39,44862000
2023-01-05,AMZN,85.53,86.60,83.36,83.12,44953500
2023-01-06,AMZN,83.00,86.42,82.60,86.08,53096900
2023-01-09,AMZN,87.17,89.15,86.60,88.83,42476000
2023-01-03,TSLA,118.47,119.93,107.23,108.10,234815400
2023-01-04,TSLA,109.11,114.59,107.52,113.64,180660500
2023-01-05,TSLA,110.51,114.17,107.16,110.34,157234200
2023-01-06,TSLA,103.00,114.39,101.81,113.06,221564800
2023-01-09,TSLA,118.96,123.52,117.11,119.77,190887900`;
    }
    state.pyodide.FS.writeFile(`/data/${name}`, csv);
  }

  // ── Loading Helpers ────────────────────────────────────────
  function updateLoadingStep(index, status) {
    const step = dom.loadingSteps[index];
    if (!step) return;
    step.classList.remove("active", "done");
    step.classList.add(status);
    const icon = step.querySelector(".step-icon");
    if (status === "done" && icon) icon.textContent = "✓";
    if (status === "active" && icon) icon.textContent = "⟳";
  }

  function updateProgress(percent) {
    dom.loadingProgressBar.style.width = percent + "%";
  }

  // ── Project Tab Switching ──────────────────────────────────
  function switchProject(projectKey) {
    state.activeProject = projectKey;
    state.activeChallenge = null;

    // Update tab UI
    dom.projectTabs.forEach((tab) => {
      tab.classList.toggle("active", tab.dataset.project === projectKey);
    });

    const project = CHALLENGES[projectKey];
    dom.sidebarProjectName.textContent = `${project.icon} ${project.name}`;

    renderChallengesList(project);
    showWelcome();
  }

  function renderChallengesList(project) {
    dom.challengesList.innerHTML = "";

    project.challenges.forEach((ch, index) => {
      const card = document.createElement("div");
      card.className = "challenge-card";
      card.dataset.index = index;

      const completedKey = `${state.activeProject}-${index}`;
      if (state.completedChallenges.has(completedKey)) {
        card.classList.add("completed");
      }

      card.innerHTML = `
        <div class="challenge-number">${index + 1}</div>
        <div class="title">${ch.title}</div>
        <div class="subtitle">${ch.subtitle}</div>
      `;

      card.addEventListener("click", () => selectChallenge(index));
      dom.challengesList.appendChild(card);
    });
  }

  // ── Challenge Selection ────────────────────────────────────
  function selectChallenge(index) {
    const project = CHALLENGES[state.activeProject];
    if (!project) return;

    state.activeChallenge = index;
    const challenge = project.challenges[index];

    // Update sidebar active state
    dom.challengesList.querySelectorAll(".challenge-card").forEach((c, i) => {
      c.classList.toggle("active", i === index);
    });

    // Show challenge info
    dom.challengeTitle.textContent = `${challenge.subtitle} — ${challenge.title}`;
    dom.challengeDesc.textContent = challenge.description;
    dom.challengeInfoBar.style.display = "flex";
    dom.hintPopup.classList.remove("visible");
    dom.hintPopup.textContent = challenge.hint;

    // Load starter code
    state.editor.setValue(challenge.starterCode);
    state.editor.refresh();

    // Show editor, hide welcome
    dom.welcomeState.style.display = "none";
    dom.editorPanel.style.display = "flex";

    // Clear output
    clearOutput();
  }

  function showWelcome() {
    dom.welcomeState.style.display = "flex";
    dom.editorPanel.style.display = "none";
    dom.challengeInfoBar.style.display = "none";
    dom.hintPopup.classList.remove("visible");
    clearOutput();
  }

  // ── Run Code ───────────────────────────────────────────────
  async function runCode() {
    if (!state.pyodideReady || state.running) return;

    const code = state.editor.getValue();
    if (!code.trim()) {
      showToast("⚠️ No code to run", "error");
      return;
    }

    state.running = true;
    dom.btnRun.disabled = true;
    dom.outputContent.innerHTML = `
      <div class="output-running">
        <div class="mini-spinner"></div>
        <span>Running code...</span>
      </div>`;

    state.lastOutput = "";
    state.lastHasChart = false;

    try {
      // Capture stdout
      await state.pyodide.runPythonAsync(`
import sys, io
sys.stdout = io.StringIO()
sys.stderr = io.StringIO()
      `);

      // Clear any previous chart
      await state.pyodide.runPythonAsync(`
import matplotlib.pyplot as plt
plt.close('all')

# Clear output dir
import os
for f in os.listdir('/output'):
    os.remove(os.path.join('/output', f))
      `);

      // Run user code
      await state.pyodide.runPythonAsync(code);

      // Capture output
      const stdout = await state.pyodide.runPythonAsync(`sys.stdout.getvalue()`);
      const stderr = await state.pyodide.runPythonAsync(`sys.stderr.getvalue()`);

      // Check for chart
      let chartBase64 = null;
      try {
        const hasChart = await state.pyodide.runPythonAsync(`
import os
os.path.exists('/output/chart.png')
        `);

        if (hasChart) {
          chartBase64 = await state.pyodide.runPythonAsync(`
import base64
with open('/output/chart.png', 'rb') as f:
    base64.b64encode(f.read()).decode('utf-8')
          `);
        }
      } catch (e) {
        // No chart, that's fine
      }

      // Also try to get chart via savefig in memory if no file output
      if (!chartBase64) {
        try {
          chartBase64 = await state.pyodide.runPythonAsync(`
import matplotlib.pyplot as plt
import io, base64
fig = plt.gcf()
if fig.get_axes():
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight',
                facecolor='none', edgecolor='none')
    buf.seek(0)
    base64.b64encode(buf.read()).decode('utf-8')
else:
    ''
          `);
          if (chartBase64 === "") chartBase64 = null;
        } catch (e) {
          // No chart
        }
      }

      // Build output HTML
      let html = "";

      if (stdout && stdout.trim()) {
        state.lastOutput = stdout;
        html += `<div class="output-text">${escapeHtml(stdout)}</div>`;
      }

      if (stderr && stderr.trim()) {
        html += `<div class="output-error">${escapeHtml(stderr)}</div>`;
      }

      if (chartBase64) {
        state.lastHasChart = true;
        html += `<img class="output-chart" src="data:image/png;base64,${chartBase64}" alt="Chart output" />`;
      }

      if (!html) {
        html = `<div class="output-text" style="color: var(--text-muted);">Code executed successfully (no output).</div>`;
      }

      dom.outputContent.innerHTML = html;

    } catch (err) {
      const errorMsg = err.message || String(err);
      state.lastOutput = errorMsg;
      dom.outputContent.innerHTML = `<div class="output-error">${escapeHtml(errorMsg)}</div>`;
    } finally {
      state.running = false;
      dom.btnRun.disabled = false;

      // Restore stdout
      try {
        await state.pyodide.runPythonAsync(`
import sys
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__
        `);
      } catch (e) { /* ignore */ }
    }
  }

  // ── Check Answer ───────────────────────────────────────────
  function checkAnswer() {
    if (state.activeProject === null || state.activeChallenge === null) {
      showToast("⚠️ Select a challenge first", "error");
      return;
    }

    if (!state.lastOutput && !state.lastHasChart) {
      showToast("⚠️ Run your code first before checking", "error");
      return;
    }

    const result = validateChallenge(
      state.activeProject,
      state.activeChallenge,
      state.lastOutput,
      state.lastHasChart
    );

    // Show validation result in output
    const existingValidation = dom.outputContent.querySelector(".validation-result");
    if (existingValidation) existingValidation.remove();

    const div = document.createElement("div");
    div.className = `validation-result ${result.valid ? "success" : "fail"}`;
    div.textContent = result.message;
    dom.outputContent.appendChild(div);

    if (result.valid) {
      const key = `${state.activeProject}-${state.activeChallenge}`;
      state.completedChallenges.add(key);

      // Update sidebar card
      const cards = dom.challengesList.querySelectorAll(".challenge-card");
      if (cards[state.activeChallenge]) {
        cards[state.activeChallenge].classList.add("completed");
      }

      showToast("🎉 Challenge completed!", "success");
    }
  }

  // ── Clear Output ───────────────────────────────────────────
  function clearOutput() {
    state.lastOutput = "";
    state.lastHasChart = false;
    dom.outputContent.innerHTML = `
      <div class="output-placeholder">
        <div class="output-placeholder-icon">⚡</div>
        <div class="output-placeholder-text">Run your code to see results here</div>
      </div>`;
  }

  // ── Hint Toggle ────────────────────────────────────────────
  function toggleHint() {
    dom.hintPopup.classList.toggle("visible");
  }

  // ── Toast Notifications ────────────────────────────────────
  function showToast(message, type = "info") {
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    toast.textContent = message;
    dom.toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.style.animation = "toastOut 0.3s ease forwards";
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  }

  // ── Utilities ──────────────────────────────────────────────
  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  // ── Event Listeners ────────────────────────────────────────
  function bindEvents() {
    // Project tabs
    dom.projectTabs.forEach((tab) => {
      tab.addEventListener("click", () => switchProject(tab.dataset.project));
    });

    // Buttons
    dom.btnRun.addEventListener("click", runCode);
    dom.btnCheck.addEventListener("click", checkAnswer);
    dom.btnClear.addEventListener("click", clearOutput);
    dom.hintBtn.addEventListener("click", toggleHint);

    // Keyboard shortcuts
    document.addEventListener("keydown", (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        e.preventDefault();
        runCode();
      }
    });
  }

  // ── Bootstrap ──────────────────────────────────────────────
  function init() {
    initEditor();
    bindEvents();

    // Default project
    switchProject("ecommerce");

    // Start Pyodide initialization
    initPyodide();
  }

  // Start when DOM is ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
