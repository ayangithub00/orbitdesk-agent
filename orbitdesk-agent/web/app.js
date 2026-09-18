const question = document.querySelector("#question");
const askButton = document.querySelector("#ask-button");
const characterCount = document.querySelector("#character-count");
const response = document.querySelector("#response");
const loading = document.querySelector("#loading");

function setQuestion(value) { question.value = value; characterCount.textContent = `${question.value.length.toLocaleString()} / 1,500`; question.focus(); }
function setLoading(isLoading) { loading.classList.toggle("hidden", !isLoading); askButton.disabled = isLoading; askButton.innerHTML = isLoading ? "Checking…" : "Ask OrbitDesk <span aria-hidden=\"true\">→</span>"; }
function renderAnswer(text) { const target = document.querySelector("#answer"); target.replaceChildren(); text.split("\n").filter(Boolean).forEach((line) => { const paragraph = document.createElement("p"); paragraph.textContent = line; target.append(paragraph); }); }
function displayResult(result) {
  renderAnswer(result.answer);
  const classification = document.querySelector("#classification"); classification.textContent = (result.classification || "safe_failure").replaceAll("_", " "); classification.className = `classification ${result.classification || "safe_failure"}`;
  document.querySelector("#confidence").textContent = `${Math.round((result.confidence || 0) * 100)}%`;
  document.querySelector("#reason").textContent = result.reason || "Response complete.";
  const sources = document.querySelector("#sources"); const sourcesSection = document.querySelector("#sources-section"); sources.replaceChildren();
  (result.sources || []).forEach((source) => { const item = document.createElement("li"); item.textContent = source.source_id || source.passage; sources.append(item); });
  sourcesSection.classList.toggle("hidden", !sources.children.length); response.classList.remove("hidden"); response.scrollIntoView({ behavior: "smooth", block: "start" });
}
async function ask() {
  const text = question.value.trim(); if (!text) { question.focus(); question.setAttribute("aria-invalid", "true"); return; }
  question.removeAttribute("aria-invalid"); response.classList.add("hidden"); setLoading(true);
  try {
    const request = await fetch("/api/ask", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ question: text }) });
    const result = await request.json(); if (!request.ok) throw new Error(result.error || "Unable to complete that request."); displayResult(result);
  } catch (error) { displayResult({ classification: "safe_failure", answer: error.message, confidence: 0, reason: "The local agent was unavailable.", sources: [] }); } finally { setLoading(false); }
}
question.addEventListener("input", () => { if (question.value.length > 1500) question.value = question.value.slice(0, 1500); characterCount.textContent = `${question.value.length.toLocaleString()} / 1,500`; });
question.addEventListener("keydown", (event) => { if ((event.metaKey || event.ctrlKey) && event.key === "Enter") ask(); });
askButton.addEventListener("click", ask);
document.querySelectorAll("[data-question]").forEach((button) => button.addEventListener("click", () => setQuestion(button.dataset.question)));
