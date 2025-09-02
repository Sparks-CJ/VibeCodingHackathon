// static/script.js

const journalForm = document.getElementById("journalForm");
const journalEntry = document.getElementById("journalEntry");
const journalHistory = document.getElementById("journalHistory");
const moodChartCtx = document.getElementById("moodChart").getContext("2d");

const payForm = document.getElementById("payForm");
const phoneInput = document.getElementById("phoneNumber");

// Base API URL (adjust if hosted)
const API_BASE = "http://localhost:5000";

// Mood chart instance
let moodChart = new Chart(moodChartCtx, {
    type: "line",
    data: {
        labels: [],
        datasets: [
            {
                label: "Happiness (%)",
                data: [],
                borderColor: "green",
                fill: false,
            },
            {
                label: "Sadness (%)",
                data: [],
                borderColor: "blue",
                fill: false,
            },
            {
                label: "Anger (%)",
                data: [],
                borderColor: "red",
                fill: false,
            },
        ],
    },
    options: {
        responsive: true,
        plugins: {
            legend: { position: "top" },
        },
    },
});

// Submit a new journal entry
journalForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const entry = journalEntry.value.trim();
    if (!entry) return;

    const res = await fetch(`${API_BASE}/journal`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ entry }),
    });

    const data = await res.json();
    alert(`Sentiment saved: ${JSON.stringify(data.sentiment)}`);
    journalEntry.value = "";
    loadHistory();
});

// Load history and update chart
async function loadHistory() {
    const res = await fetch(`${API_BASE}/journal`);
    const data = await res.json();

    journalHistory.innerHTML = "";
    const labels = [];
    const happy = [];
    const sad = [];
    const angry = [];

    data.forEach((row) => {
        const date = new Date(row.created_at).toLocaleDateString();
        labels.push(date);
        happy.push(row.sentiment.happy || 0);
        sad.push(row.sentiment.sad || 0);
        angry.push(row.sentiment.angry || 0);

        const li = document.createElement("li");
        li.textContent = `${date}: ${row.entry} → ${JSON.stringify(row.sentiment)}`;
        journalHistory.appendChild(li);
    });

    moodChart.data.labels = labels;
    moodChart.data.datasets[0].data = happy;
    moodChart.data.datasets[1].data = sad;
    moodChart.data.datasets[2].data = angry;
    moodChart.update();
}

// Handle IntaSend payment
payForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const phone = phoneInput.value.trim();
    if (!phone) return alert("Enter phone number");

    const res = await fetch(`${API_BASE}/pay`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ phone }),
    });

    const data = await res.json();
    alert(`Payment initiated. Checkout ID: ${data.checkout_id}`);
});

// Initial load
loadHistory();
