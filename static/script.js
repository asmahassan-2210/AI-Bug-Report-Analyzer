document.addEventListener('DOMContentLoaded', () => {
    // Initialize Lucide icons
    lucide.createIcons();

    const sampleBug = "When users click the 'Checkout' button on mobile viewports while having an empty cart, the app freezes for 5 seconds and throws an unhandled TypeError: Cannot read properties of undefined (reading 'items') in cartSlice.js.";

    const loadSampleBtn = document.getElementById('load-sample');
    const descriptionInput = document.getElementById('description-input');
    const bugForm = document.getElementById('bug-form');
    const submitBtn = document.getElementById('submit-btn');
    const pipelineSteps = document.querySelectorAll('.step-item');
    
    const emptyState = document.getElementById('empty-state');
    const resultContainer = document.getElementById('result-container');
    const outputActions = document.getElementById('output-actions');
    const severityBadge = document.getElementById('severity-badge');
    const copyBtn = document.getElementById('copy-btn');
    const copyText = document.getElementById('copy-text');
    const resFeature = document.getElementById('res-feature');
    const resTitle = document.getElementById('res-title');
    const resReport = document.getElementById('res-report');

    let latestReportMarkdown = '';

    loadSampleBtn.addEventListener('click', () => {
        descriptionInput.value = sampleBug;
    });

    bugForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const description = descriptionInput.value.trim();
        if (!description) return;

        // Reset UI & set loading state
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<div class="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin"></div> Running LangGraph Pipeline...`;
        emptyState.classList.remove('hidden');
        resultContainer.classList.add('hidden');
        outputActions.classList.add('hidden');

        let currentStep = 0;
        updatePipelineUI(currentStep, true);

        const stepInterval = setInterval(() => {
            if (currentStep < 3) {
                currentStep++;
                updatePipelineUI(currentStep, true);
            }
        }, 600);

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ description })
            });

            if (!response.ok) throw new Error('Failed to analyze bug report');
            const data = await response.json();

            clearInterval(stepInterval);
            updatePipelineUI(3, false, true);

            setTimeout(() => {
                displayResult(data);
                submitBtn.disabled = false;
                submitBtn.innerHTML = `<i data-lucide="play" class="w-4 h-4 fill-current"></i> Analyze Bug Report`;
                lucide.createIcons();
            }, 300);

        } catch (err) {
            clearInterval(stepInterval);
            alert("Error connecting to backend: " + err.message);
            submitBtn.disabled = false;
            submitBtn.innerHTML = `<i data-lucide="play" class="w-4 h-4 fill-current"></i> Analyze Bug Report`;
            updatePipelineUI(-1, false, false);
            lucide.createIcons();
        }
    });

    function updatePipelineUI(activeIndex, isLoading, isComplete = false) {
        pipelineSteps.forEach((step, idx) => {
            const iconContainer = step.querySelector('div');
            if (isComplete || idx < activeIndex || (idx === activeIndex && !isLoading)) {
                step.className = "step-item flex items-start gap-3 p-3 rounded-xl border bg-indigo-950/20 border-indigo-500/30 text-indigo-200 transition-all";
                iconContainer.innerHTML = `<i data-lucide="check-circle-2" class="w-4 h-4 text-indigo-400"></i>`;
            } else if (idx === activeIndex && isLoading) {
                step.className = "step-item flex items-start gap-3 p-3 rounded-xl border bg-slate-800 border-slate-700 text-white animate-pulse transition-all";
                iconContainer.innerHTML = `<div class="w-4 h-4 rounded-full border-2 border-indigo-500 border-t-transparent animate-spin"></div>`;
            } else {
                step.className = "step-item flex items-start gap-3 p-3 rounded-xl border bg-slate-950/50 border-slate-900 text-slate-500 transition-all";
                iconContainer.innerHTML = `<div class="w-4 h-4 rounded-full border border-slate-700 flex items-center justify-center text-[10px]">${idx + 1}</div>`;
            }
        });
        lucide.createIcons();
    }

    function displayResult(data) {
        latestReportMarkdown = data.formatted_report;
        resFeature.textContent = data.affected_feature;
        resTitle.textContent = data.title;
        resReport.textContent = data.formatted_report;

        // Set Severity Badge Styles
        const severity = data.severity;
        severityBadge.textContent = `${severity} Severity`;
        const colors = {
            Critical: "bg-red-500/20 text-red-400 border-red-500/30",
            High: "bg-orange-500/20 text-orange-400 border-orange-500/30",
            Medium: "bg-amber-500/20 text-amber-400 border-amber-500/30",
            Low: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30"
        };
        severityBadge.className = `text-xs px-3 py-1 rounded-full border font-medium ${colors[severity] || "bg-blue-500/20 text-blue-400 border-blue-500/30"}`;

        emptyState.classList.add('hidden');
        resultContainer.classList.remove('hidden');
        outputActions.classList.remove('hidden');
        outputActions.classList.add('flex');
    }

    copyBtn.addEventListener('click', () => {
        if (latestReportMarkdown) {
            navigator.clipboard.writeText(latestReportMarkdown);
            copyText.textContent = 'Copied';
            copyBtn.querySelector('i').setAttribute('data-lucide', 'check');
            lucide.createIcons();
            setTimeout(() => {
                copyText.textContent = 'Copy Report';
                copyBtn.querySelector('i').setAttribute('data-lucide', 'copy');
                lucide.createIcons();
            }, 2000);
        }
    });
});