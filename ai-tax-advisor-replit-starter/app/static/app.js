
const $ = (s) => document.querySelector(s);
const statusEl = $("#status");
const formsEl = $("#forms");
const recsEl = $("#recs");

$("#btn").addEventListener("click", async () => {
  const f = $("#file").files[0];
  if (!f) { alert("PDF를 선택하세요."); return; }
  statusEl.textContent = "업로드/분석 중…";
  formsEl.textContent = "";
  recsEl.innerHTML = "";

  const fd = new FormData();
  fd.append("file", f);

  try {
    const res = await fetch("/upload", { method: "POST", body: fd });
    if (!res.ok) throw new Error("Upload failed");
    const data = await res.json();
    statusEl.textContent = `분석 완료: ${data.filename}`;
    formsEl.textContent = (data.forms_detected || []).join(", ") || "None";

    (data.recommendations || []).forEach((r) => {
      const el = document.createElement("div");
      el.className = "card";
      el.innerHTML = `
        <div class="pill">${r.category}</div>
        <h4>${r.title}</h4>
        <div class="muted small">${r.reason}</div>
        <div class="small">잠재 절감: $${r.estimate_savings_range[0]} – $${r.estimate_savings_range[1]}</div>
        <div class="small muted">신뢰도: ${(r.confidence * 100).toFixed(0)}%</div>
        <div class="small">조치: ${(r.actions || []).join(" · ")}</div>
      `;
      recsEl.appendChild(el);
    });

    if (!data.recommendations || data.recommendations.length === 0) {
      const el = document.createElement("div");
      el.className = "muted small";
      el.textContent = "추천 없음 (샘플 규칙을 충족하지 않음)";
      recsEl.appendChild(el);
    }
  } catch (e) {
    console.error(e);
    statusEl.textContent = "분석 실패 — 콘솔 확인";
    alert("에러가 발생했습니다.");
  }
});
