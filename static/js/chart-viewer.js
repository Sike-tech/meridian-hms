/* Chart Viewer — zoom, pan, download */
(function () {
  let scale = 1;
  let rotation = 0;
  let panX = 0, panY = 0;
  let isDragging = false;
  let startX, startY;

  const overlay = document.getElementById("chart-viewer-overlay");
  const body = overlay.querySelector(".chart-viewer-body");
  const img = body.querySelector("img");
  const title = overlay.querySelector(".chart-viewer-header h3");
  const zoomLabel = overlay.querySelector(".zoom-label");

  function updateTransform() {
    img.style.transform =
      `translate(${panX}px, ${panY}px) scale(${scale}) rotate(${rotation}deg)`;
    zoomLabel.textContent = Math.round(scale * 100) + "%";
  }

  function openViewer(src, chartTitle) {
    img.src = src;
    title.textContent = chartTitle;
    scale = 1;
    rotation = 0;
    panX = 0;
    panY = 0;
    updateTransform();
    overlay.classList.add("active");
    document.body.style.overflow = "hidden";
  }

  function closeViewer() {
    overlay.classList.remove("active");
    document.body.style.overflow = "";
  }

  /* ── Click chart card to open ──────────────────────────── */
  document.querySelectorAll(".chart-card").forEach(function (card) {
    card.addEventListener("click", function () {
      var imgEl = card.querySelector("img");
      var titleEl = card.querySelector("h3");
      if (imgEl && titleEl) {
        openViewer(imgEl.src, titleEl.textContent.trim());
      }
    });
  });

  /* ── Close ─────────────────────────────────────────────── */
  overlay.querySelector(".chart-viewer-close").addEventListener("click", closeViewer);
  overlay.addEventListener("click", function (e) {
    if (e.target === overlay) closeViewer();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeViewer();
  });

  /* ── Zoom buttons (10% step) ───────────────────────────── */
  overlay.querySelector(".zoom-in").addEventListener("click", function () {
    scale = Math.min(scale + 0.10, 5);
    updateTransform();
  });
  overlay.querySelector(".zoom-out").addEventListener("click", function () {
    scale = Math.max(scale - 0.10, 0.25);
    updateTransform();
  });
  overlay.querySelector(".zoom-rotate").addEventListener("click", function () {
    rotation = (rotation + 90) % 360;
    updateTransform();
  });
  overlay.querySelector(".zoom-reset").addEventListener("click", function () {
    scale = 1; rotation = 0; panX = 0; panY = 0;
    updateTransform();
  });

  /* ── Mouse wheel zoom ──────────────────────────────────── */
  body.addEventListener("wheel", function (e) {
    e.preventDefault();
    var delta = e.deltaY > 0 ? -0.15 : 0.15;
    scale = Math.min(Math.max(scale + delta, 0.25), 5);
    updateTransform();
  }, { passive: false });

  /* ── Pan (drag) ────────────────────────────────────────── */
  body.addEventListener("mousedown", function (e) {
    if (e.target === img || e.target === body) {
      e.preventDefault();
      isDragging = true;
      startX = e.clientX - panX;
      startY = e.clientY - panY;
      body.classList.add("dragging");
    }
  });
  img.addEventListener("dragstart", function (e) { e.preventDefault(); });
  document.addEventListener("mousemove", function (e) {
    if (!isDragging) return;
    panX = e.clientX - startX;
    panY = e.clientY - startY;
    updateTransform();
  });
  document.addEventListener("mouseup", function () {
    isDragging = false;
    body.classList.remove("dragging");
  });

  /* ── Download ──────────────────────────────────────────── */
  overlay.querySelector(".zoom-download").addEventListener("click", function () {
    var a = document.createElement("a");
    a.href = img.src;
    a.download = title.textContent.replace(/\s+/g, "_") + ".png";
    a.click();
  });
})();
