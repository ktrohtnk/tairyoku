/* ==========================================================================
   TAIRYOKU (体力) — Kinetic Archive & Single-Ink Wall Controller
   ========================================================================== */
(function () {
  const DATA = window.TAIRYOKU_DATA || { projects: [] };
  const PREFIX = window.ASSET_PREFIX || ".";
  const projectsById = {};
  DATA.projects.forEach((p) => { projectsById[p.id] = p; });

  function resolvePath(relPath) {
    if (!relPath) return "";
    if (relPath.startsWith("http://") || relPath.startsWith("https://") || relPath.startsWith("data:")) return relPath;
    const clean = relPath.replace(/^\.\//, "");
    if (window.location && window.location.protocol !== "file:") {
      return clean.startsWith("/") ? clean : "/" + clean;
    }
    return PREFIX + (clean.startsWith("/") ? clean : "/" + clean);
  }

  function escHtml(str) {
    return String(str ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  const htmlEl = document.documentElement;
  const wallGrid = document.getElementById("wall-grid");
  const driftStage = document.getElementById("drift-stage");
  const scatterStage = document.getElementById("scatter-stage");
  const cursorTag = document.getElementById("cursor-tag");
  const statusReadout = document.getElementById("status-readout");
  const detailSheet = document.getElementById("detail-sheet");
  const directoryEl = document.getElementById("raw-directory");

  /* --------------------------------------------------------------------------
     1. INK COLOR PALETTE & DYNAMIC SVG DUOTONE FILTER
     -------------------------------------------------------------------------- */
  const INK_PALETTES = {
    violet:      { ink: [0.208, 0.098, 0.910], bg: [0.980, 0.976, 1.000] }, // #3519e8
    ultramarine: { ink: [0.078, 0.141, 0.961], bg: [0.973, 0.980, 1.000] }, // #1424f5
    purple:      { ink: [0.353, 0.071, 0.851], bg: [0.988, 0.976, 1.000] }, // #5a12d9
    night:       { ink: [0.047, 0.027, 0.129], bg: [0.714, 0.659, 1.000] }  // dark violet
  };

  function applyInk(inkKey) {
    const pal = INK_PALETTES[inkKey] || INK_PALETTES.violet;
    htmlEl.setAttribute("data-ink", inkKey);
    const fR = document.getElementById("duotone-r");
    const fG = document.getElementById("duotone-g");
    const fB = document.getElementById("duotone-b");
    if (fR && fG && fB) {
      fR.setAttribute("tableValues", `${pal.ink[0]} ${pal.bg[0]}`);
      fG.setAttribute("tableValues", `${pal.ink[1]} ${pal.bg[1]}`);
      fB.setAttribute("tableValues", `${pal.ink[2]} ${pal.bg[2]}`);
    }
    document.querySelectorAll("[data-set-ink]").forEach((btn) => {
      btn.setAttribute("aria-pressed", String(btn.dataset.setInk === inkKey));
    });
  }

  document.querySelectorAll("[data-set-ink]").forEach((btn) => {
    btn.addEventListener("click", () => applyInk(btn.dataset.setInk));
  });

  /* --------------------------------------------------------------------------
     2. VIEW MODE, COLOR MODE, DENSITY & CATEGORY FILTERING
     -------------------------------------------------------------------------- */
  let currentView = htmlEl.getAttribute("data-view") || "wall";
  let currentFilter = htmlEl.getAttribute("data-filter") || "all";

  function setView(mode) {
    currentView = mode;
    htmlEl.setAttribute("data-view", mode);
    document.querySelectorAll("[data-set-view]").forEach((btn) => {
      btn.setAttribute("aria-pressed", String(btn.dataset.setView === mode));
    });
    if (mode === "drift") initDriftStage();
    if (mode === "scatter") initScatterStage();
  }

  document.querySelectorAll("[data-set-view]").forEach((btn) => {
    btn.addEventListener("click", () => setView(btn.dataset.setView));
  });

  document.querySelectorAll("[data-set-color]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const c = btn.dataset.setColor;
      htmlEl.setAttribute("data-color", c);
      document.querySelectorAll("[data-set-color]").forEach((b) => {
        b.setAttribute("aria-pressed", String(b === btn));
      });
    });
  });

  document.querySelectorAll("[data-set-size]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const s = btn.dataset.setSize;
      htmlEl.setAttribute("data-size", s);
      document.querySelectorAll("[data-set-size]").forEach((b) => {
        b.setAttribute("aria-pressed", String(b === btn));
      });
    });
  });

  function applyFilter(filterKey) {
    currentFilter = filterKey;
    htmlEl.setAttribute("data-filter", filterKey);
    document.querySelectorAll("[data-filter-btn]").forEach((btn) => {
      btn.setAttribute("aria-pressed", String(btn.dataset.filterBtn === filterKey));
    });
    let visibleCount = 0;
    document.querySelectorAll("#wall-grid .wall-tile").forEach((tile) => {
      const match =
        filterKey === "all" ||
        tile.dataset.section === filterKey ||
        tile.dataset.group === filterKey;
      tile.hidden = !match;
      if (match) visibleCount++;
    });
    document.querySelectorAll(".raw-table tbody tr[data-project-id]").forEach((row) => {
      const match =
        filterKey === "all" ||
        row.dataset.section === filterKey ||
        row.dataset.group === filterKey;
      row.hidden = !match;
    });
    if (driftInitialized) {
      buildDriftRows();
    }
    if (scatterInitialized) {
      scatterBodies.forEach((b) => {
        const match =
          filterKey === "all" ||
          b.section === filterKey ||
          b.group === filterKey;
        b.el.hidden = !match;
      });
    }
    if (statusReadout) {
      statusReadout.textContent = `SHOWING ${visibleCount} PROJECTS [${filterKey.toUpperCase()}]`;
    }
  }

  document.querySelectorAll("[data-filter-btn]").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      closeDetailSheet(false);
      applyFilter(btn.dataset.filterBtn);
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  });

  // Smooth jump to anchor sections (e.g. #about-section, #contact-section)
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", (e) => {
      const id = anchor.getAttribute("href").slice(1);
      const target = id ? document.getElementById(id) : null;
      if (target) {
        e.preventDefault();
        closeDetailSheet(false);
        target.scrollIntoView({ behavior: "smooth" });
      }
    });
  });

  // Toggle collapsible raw index directory
  const toggleDirBtn = document.getElementById("toggle-dir-btn");
  function syncDirBtnLabel() {
    if (!toggleDirBtn || !directoryEl) return;
    const isOpen = !directoryEl.hasAttribute("hidden");
    toggleDirBtn.setAttribute("aria-pressed", String(isOpen));
    toggleDirBtn.textContent = isOpen ? "index (18) [-]" : "index (18) [+]";
  }
  if (toggleDirBtn && directoryEl) {
    syncDirBtnLabel();
    toggleDirBtn.addEventListener("click", () => {
      if (directoryEl.hasAttribute("hidden")) {
        directoryEl.removeAttribute("hidden");
      } else {
        directoryEl.setAttribute("hidden", "");
      }
      syncDirBtnLabel();
    });
  }

  /* --------------------------------------------------------------------------
     3. WET-INK AFTERGLOW TRAIL, FLIPBOOK PREVIEW & EDGE-AWARE EXPANSION
     -------------------------------------------------------------------------- */
  const wakeTimers = new WeakMap();
  const flipTimers = new WeakMap();
  const imgCache = {};
  const preloadedProjects = {};

  function preloadSrc(src) {
    const url = resolvePath(src);
    if (!url) return null;
    if (!imgCache[url]) {
      const im = new Image();
      im.decoding = "async";
      im.src = url;
      imgCache[url] = im;
    }
    return imgCache[url];
  }

  function preloadProjectPhotos(pid) {
    if (preloadedProjects[pid]) return;
    const p = projectsById[pid];
    if (!p || !p.photos) return;
    preloadedProjects[pid] = true;
    p.photos.forEach((ph) => preloadSrc(ph.src));
  }

  // Gently warm all project frames in background after page load so flipbook is instant
  window.addEventListener("load", () => {
    setTimeout(() => {
      DATA.projects.forEach((p, idx) => {
        setTimeout(() => preloadProjectPhotos(p.id), idx * 140);
      });
    }, 500);
  });

  function wakeTile(tile, durationMs = 1350) {
    if (!tile) return;
    tile.classList.add("is-awake");
    const prev = wakeTimers.get(tile);
    if (prev) clearTimeout(prev);
    const tid = setTimeout(() => {
      tile.classList.remove("is-awake");
    }, durationMs);
    wakeTimers.set(tile, tid);
  }

  function updateExpandOrigin(tile) {
    const card = tile.querySelector(".wall-tile-card");
    if (!card) return;
    const r = tile.getBoundingClientRect();
    let ox = "center";
    let oy = "center";
    if (r.left < 90) ox = "left";
    else if (window.innerWidth - r.right < 90) ox = "right";
    if (r.top < 160) oy = "top";
    else if (window.innerHeight - r.bottom < 100) oy = "bottom";
    card.style.transformOrigin = `${ox} ${oy}`;
  }

  function setTileFrame(tile, frameIdx) {
    const pid = tile.dataset.projectId;
    const p = projectsById[pid];
    if (!p || !p.photos.length) return;
    const imgEl = tile.querySelector("img");
    const badgeEl = tile.querySelector(".tile-idx");
    const capEl = tile.querySelector(".tile-caption");
    const total = p.photos.length;
    const idx = ((frameIdx % total) + total) % total;
    const targetPhoto = p.photos[idx];
    const targetUrl = resolvePath(targetPhoto.src);

    // Ensure cached before swapping so flipbook never flashes blank
    const cached = preloadSrc(targetPhoto.src);
    if (imgEl) {
      if (!cached || cached.complete || idx === 0) {
        imgEl.src = targetUrl;
      } else {
        cached.onload = () => {
          if (tile.dataset.isHovering === "1") {
            imgEl.src = targetUrl;
          }
        };
      }
    }
    tile.dataset.activePhotoIndex = String(idx);
    if (badgeEl) {
      badgeEl.textContent = idx === 0 && tile.dataset.isHovering !== "1"
        ? `#${p.code} [${total}p]`
        : `#${p.code} [${String(idx + 1).padStart(2, "0")}/${String(total).padStart(2, "0")}]`;
    }
    if (capEl) {
      capEl.textContent = `#${p.code} ${p.title} (${idx + 1}/${total})`;
    }
  }

  function startFlipbook(tile, intervalMs = 360) {
    const pid = tile.dataset.projectId;
    const p = projectsById[pid];
    if (!p || !p.photos.length) return;
    preloadProjectPhotos(pid);
    tile.dataset.isHovering = "1";
    stopFlipbook(tile, false);

    let frameIdx = 0;
    const total = p.photos.length;
    if (total <= 1) {
      setTileFrame(tile, 0);
      return;
    }

    // Immediate quick flip to frame 2 so user feels the flipbook instantly
    const step = () => {
      if (tile.dataset.isHovering !== "1") return;
      frameIdx = (frameIdx + 1) % total;
      setTileFrame(tile, frameIdx);
      if (statusReadout) {
        statusReadout.textContent = `#${p.code} — ${p.title} [${frameIdx + 1}/${total}]`;
      }
    };

    setTileFrame(tile, 0);
    const firstTick = setTimeout(() => {
      step();
      const loopId = setInterval(step, intervalMs);
      flipTimers.set(tile, { firstTick: null, loopId });
    }, 200);
    flipTimers.set(tile, { firstTick, loopId: null });
  }

  function stopFlipbook(tile, resetToCover = true) {
    const state = flipTimers.get(tile);
    if (state) {
      if (state.firstTick) clearTimeout(state.firstTick);
      if (state.loopId) clearInterval(state.loopId);
      flipTimers.delete(tile);
    }
    if (resetToCover) {
      tile.dataset.isHovering = "0";
      setTileFrame(tile, 0);
    }
  }

  function bindTileInteractions(container) {
    if (!container) return;
    container.querySelectorAll(".wall-tile").forEach((tile) => {
      tile.addEventListener("pointerenter", () => {
        wakeTile(tile, 1500);
        updateExpandOrigin(tile);
        startFlipbook(tile, 360);
        const pid = tile.dataset.projectId;
        const pTitle = tile.dataset.projectTitle;
        const fCode = tile.dataset.frameCode;
        const pCat = tile.dataset.category;
        if (cursorTag) {
          cursorTag.textContent = `#${fCode} ${pTitle} [${pCat}]`;
          cursorTag.classList.add("is-visible");
        }
        if (statusReadout) {
          statusReadout.textContent = `#${fCode} — ${pTitle} (${tile.dataset.year})`;
        }
        document.querySelectorAll(".dir-item").forEach((item) => {
          item.classList.toggle("is-highlighted", item.dataset.projectId === pid);
        });
      });

      tile.addEventListener("pointerleave", () => {
        stopFlipbook(tile, true);
        wakeTile(tile, 1100);
        if (cursorTag) cursorTag.classList.remove("is-visible");
      });

      tile.addEventListener("click", (e) => {
        const pid = tile.dataset.projectId;
        const activeIdx = parseInt(tile.dataset.activePhotoIndex || "0", 10);
        if (pid && projectsById[pid]) {
          e.preventDefault();
          triggerColorRipple(tile);
          openDetailSheet(pid, activeIdx, true);
        }
      });
    });
  }

  bindTileInteractions(wallGrid);

  function triggerColorRipple(originTile) {
    if (!wallGrid) return;
    const rect0 = originTile.getBoundingClientRect();
    const cx0 = rect0.left + rect0.width / 2;
    const cy0 = rect0.top + rect0.height / 2;
    wallGrid.querySelectorAll(".wall-tile:not([hidden])").forEach((t) => {
      const r = t.getBoundingClientRect();
      if (r.bottom < 0 || r.top > window.innerHeight) return;
      const dist = Math.hypot(r.left + r.width / 2 - cx0, r.top + r.height / 2 - cy0);
      if (dist < 620) {
        setTimeout(() => wakeTile(t, 1200), dist * 0.7);
      }
    });
  }

  const shuffleBtn = document.getElementById("shuffle-wall-btn");
  if (shuffleBtn && wallGrid) {
    shuffleBtn.addEventListener("click", () => {
      const tiles = Array.from(wallGrid.children);
      for (let i = tiles.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        wallGrid.appendChild(tiles[j]);
      }
      tiles.forEach((t, idx) => setTimeout(() => wakeTile(t, 1200), idx * 45));
    });
  }

  let lastPointerMove = Date.now();
  window.addEventListener("pointermove", (e) => {
    lastPointerMove = Date.now();
    if (cursorTag && cursorTag.classList.contains("is-visible")) {
      cursorTag.style.left = `${e.clientX}px`;
      cursorTag.style.top = `${e.clientY}px`;
    }
  }, { passive: true });

  // Subtle autonomous color & flip pulse when idle
  setInterval(() => {
    if (document.hidden || !detailSheet.hasAttribute("hidden")) return;
    if (Date.now() - lastPointerMove < 2200) return;
    const visibleTiles = Array.from(
      document.querySelectorAll("#wall-grid .wall-tile:not([hidden])")
    ).filter((t) => {
      if (t.dataset.isHovering === "1") return false;
      const r = t.getBoundingClientRect();
      return r.bottom > 0 && r.top < window.innerHeight;
    });
    if (!visibleTiles.length) return;
    const pick = visibleTiles[Math.floor(Math.random() * visibleTiles.length)];
    wakeTile(pick, 1900);
    const p = projectsById[pick.dataset.projectId];
    if (p && p.photos.length > 1) {
      preloadProjectPhotos(p.id);
      setTileFrame(pick, 1);
      setTimeout(() => {
        if (pick.dataset.isHovering !== "1") setTileFrame(pick, 2 % p.photos.length);
      }, 450);
      setTimeout(() => {
        if (pick.dataset.isHovering !== "1") setTileFrame(pick, 0);
      }, 1150);
    }
  }, 1900);

  /* --------------------------------------------------------------------------
     4. DIRECTORY LIST HOVER -> FULL-COLOR ENLARGED FLIPBOOK RESONANCE ON WALL
     -------------------------------------------------------------------------- */
  document.querySelectorAll(".dir-item").forEach((item) => {
    const pid = item.dataset.projectId;
    item.addEventListener("pointerenter", () => {
      if (!wallGrid) return;
      wallGrid.classList.add("has-project-focus");
      wallGrid.querySelectorAll(".wall-tile").forEach((tile) => {
        const match = tile.dataset.projectId === pid;
        tile.classList.toggle("is-project-match", match);
        if (match) {
          updateExpandOrigin(tile);
          wakeTile(tile, 2000);
          startFlipbook(tile, 360);
        }
      });
    });
    item.addEventListener("pointerleave", () => {
      if (!wallGrid) return;
      wallGrid.classList.remove("has-project-focus");
      wallGrid.querySelectorAll(".wall-tile.is-project-match").forEach((tile) => {
        tile.classList.remove("is-project-match");
        stopFlipbook(tile, true);
      });
    });
    const link = item.querySelector("a");
    if (link) {
      link.addEventListener("click", (e) => {
        if (pid && projectsById[pid]) {
          e.preventDefault();
          openDetailSheet(pid, 0, true);
        }
      });
    }
  });

  document.querySelectorAll(".raw-table tbody tr[data-project-id]").forEach((row) => {
    row.addEventListener("click", (e) => {
      const pid = row.dataset.projectId;
      if (pid && projectsById[pid]) {
        e.preventDefault();
        openDetailSheet(pid, 0, true);
      }
    });
  });

  /* --------------------------------------------------------------------------
     5. SCROLL-VELOCITY KINETIC SKEW (Wall Mode)
     -------------------------------------------------------------------------- */
  let lastScrollY = window.scrollY;
  let currentSkew = 0;
  function updateScrollSkew() {
    if (currentView === "wall" && wallGrid) {
      const dy = window.scrollY - lastScrollY;
      lastScrollY = window.scrollY;
      const targetSkew = Math.max(-2.2, Math.min(2.2, dy * 0.045));
      currentSkew += (targetSkew - currentSkew) * 0.22;
      if (Math.abs(currentSkew) > 0.02) {
        wallGrid.style.transform = `skewY(${currentSkew.toFixed(3)}deg)`;
      } else {
        wallGrid.style.transform = "";
      }
    }
    requestAnimationFrame(updateScrollSkew);
  }
  requestAnimationFrame(updateScrollSkew);

  /* --------------------------------------------------------------------------
     6. MODE 2: KINETIC DRIFT CONVEYOR ENGINE
     -------------------------------------------------------------------------- */
  let driftInitialized = false;
  let driftAnimating = false;
  const driftTracks = [];

  function buildDriftRows() {
    if (!driftStage || !wallGrid) return;
    driftStage.innerHTML = "";
    driftTracks.length = 0;
    const sourceTiles = Array.from(wallGrid.querySelectorAll(".wall-tile:not([hidden])"));
    const pool = sourceTiles.length ? sourceTiles : Array.from(wallGrid.querySelectorAll(".wall-tile"));
    const numRows = Math.min(4, Math.max(1, pool.length));
    for (let r = 0; r < numRows; r++) {
      const rowEl = document.createElement("div");
      rowEl.className = "drift-row";
      let slice = pool.filter((_, idx) => idx % numRows === r);
      while (slice.length < 6) slice = slice.concat(slice);
      [...slice, ...slice].forEach((orig) => {
        const clone = orig.cloneNode(true);
        clone.hidden = false;
        rowEl.appendChild(clone);
      });
      driftStage.appendChild(rowEl);
      bindTileInteractions(rowEl);
      const speed = (r % 2 === 0 ? 1 : -1) * (0.45 + r * 0.14);
      const trackObj = { el: rowEl, x: r % 2 === 0 ? 0 : -600, speed, paused: false };
      rowEl.addEventListener("pointerenter", () => { trackObj.paused = true; });
      rowEl.addEventListener("pointerleave", () => { trackObj.paused = false; });
      driftTracks.push(trackObj);
    }
  }

  function initDriftStage() {
    if (!driftStage || driftInitialized) return;
    driftInitialized = true;
    buildDriftRows();
    if (!driftAnimating) {
      driftAnimating = true;
      function stepDrift() {
        if (currentView === "drift") {
          driftTracks.forEach((tr) => {
            if (!tr.paused) {
              tr.x -= tr.speed;
              const halfW = tr.el.scrollWidth / 2;
              if (halfW > 0) {
                if (tr.x <= -halfW) tr.x += halfW;
                if (tr.x > 0) tr.x -= halfW;
              }
              tr.el.style.transform = `translate3d(${tr.x.toFixed(2)}px, 0, 0)`;
            }
          });
        }
        requestAnimationFrame(stepDrift);
      }
      requestAnimationFrame(stepDrift);
    }
  }

  /* --------------------------------------------------------------------------
     7. MODE 3: INTERACTIVE ARTIST STUDIO SCATTER CANVAS (Physics & Drag)
     -------------------------------------------------------------------------- */
  let scatterInitialized = false;
  const scatterBodies = [];
  let topZ = 10;

  function initScatterStage() {
    if (!scatterStage || scatterInitialized) return;
    scatterInitialized = true;
    const stageRect = scatterStage.getBoundingClientRect();
    const W = Math.max(stageRect.width, window.innerWidth);
    const H = Math.max(stageRect.height, 620);

    const sourceTiles = Array.from(wallGrid.querySelectorAll(".wall-tile"));
    sourceTiles.forEach((tile, i) => {
      const pid = tile.dataset.projectId;
      const p = projectsById[pid];
      const card = document.createElement("div");
      card.className = "scatter-card";
      card.dataset.projectId = pid;
      card.style.zIndex = String(++topZ);
      const img = tile.querySelector("img").cloneNode(true);
      const meta = document.createElement("div");
      meta.className = "scatter-meta";
      meta.textContent = `#${tile.dataset.frameCode} ${tile.dataset.projectTitle}`;
      card.appendChild(img);
      card.appendChild(meta);
      scatterStage.appendChild(card);

      const body = {
        el: card,
        projectId: pid,
        section: tile.dataset.section,
        group: tile.dataset.group,
        photoIndex: 0,
        hovering: false,
        flipId: null,
        x: 30 + ((i * 155) % Math.max(200, W - 260)),
        y: 44 + ((i * 97) % Math.max(180, H - 270)),
        vx: (Math.random() - 0.5) * 0.55,
        vy: (Math.random() - 0.5) * 0.55,
        rot: (Math.random() - 0.5) * 14,
        dragging: false
      };
      if (currentFilter !== "all" && body.section !== currentFilter && body.group !== currentFilter) {
        card.hidden = true;
      }
      scatterBodies.push(body);

      card.addEventListener("pointerenter", () => {
        body.hovering = true;
        card.style.zIndex = String(++topZ);
        if (p && p.photos.length > 1) {
          preloadProjectPhotos(pid);
          let fi = 0;
          if (body.flipId) clearInterval(body.flipId);
          body.flipId = setInterval(() => {
            if (!body.hovering) return;
            fi = (fi + 1) % p.photos.length;
            body.photoIndex = fi;
            img.src = resolvePath(p.photos[fi].src);
            meta.textContent = `#${p.code} ${p.title} (${fi + 1}/${p.photos.length})`;
          }, 360);
        }
      });

      card.addEventListener("pointerleave", () => {
        body.hovering = false;
        if (body.flipId) {
          clearInterval(body.flipId);
          body.flipId = null;
        }
        if (p && p.photos.length) {
          body.photoIndex = 0;
          img.src = resolvePath(p.photos[0].src);
          meta.textContent = `#${p.code} ${p.title}`;
        }
      });

      let startX = 0, startY = 0, moved = false;
      card.addEventListener("pointerdown", (e) => {
        card.setPointerCapture(e.pointerId);
        body.dragging = true;
        moved = false;
        startX = e.clientX - body.x;
        startY = e.clientY - body.y;
        card.style.zIndex = String(++topZ);
        card.classList.add("is-awake");
      });
      card.addEventListener("pointermove", (e) => {
        if (!body.dragging) return;
        const nx = e.clientX - startX;
        const ny = e.clientY - startY;
        if (Math.hypot(nx - body.x, ny - body.y) > 5) moved = true;
        body.vx = (nx - body.x) * 0.35;
        body.vy = (ny - body.y) * 0.35;
        body.x = nx;
        body.y = ny;
      });
      card.addEventListener("pointerup", () => {
        body.dragging = false;
        if (!moved && body.projectId) {
          openDetailSheet(body.projectId, body.photoIndex, true);
        }
      });
    });

    const rescatterBtn = document.getElementById("rescatter-btn");
    if (rescatterBtn) {
      rescatterBtn.addEventListener("click", () => {
        const bW = scatterStage.clientWidth || window.innerWidth;
        const bH = scatterStage.clientHeight || 640;
        scatterBodies.forEach((b) => {
          b.x = 24 + Math.random() * Math.max(120, bW - 200);
          b.y = 44 + Math.random() * Math.max(120, bH - 220);
          b.vx = (Math.random() - 0.5) * 3.2;
          b.vy = (Math.random() - 0.5) * 3.2;
          b.rot = (Math.random() - 0.5) * 18;
          b.el.classList.add("is-awake");
          setTimeout(() => b.el.classList.remove("is-awake"), 1200);
        });
      });
    }

    function stepScatter() {
      if (currentView === "scatter") {
        const bW = scatterStage.clientWidth || window.innerWidth;
        const bH = scatterStage.clientHeight || 640;
        scatterBodies.forEach((b) => {
          if (!b.dragging) {
            b.x += b.vx;
            b.y += b.vy;
            b.vx *= 0.985;
            b.vy *= 0.985;
            if (Math.hypot(b.vx, b.vy) < 0.18) {
              b.vx += (Math.random() - 0.5) * 0.04;
              b.vy += (Math.random() - 0.5) * 0.04;
            }
            if (b.x < 8) { b.x = 8; b.vx *= -0.8; }
            if (b.x > bW - 180) { b.x = bW - 180; b.vx *= -0.8; }
            if (b.y < 38) { b.y = 38; b.vy *= -0.8; }
            if (b.y > bH - 190) { b.y = bH - 190; b.vy *= -0.8; }
          }
          const sc = bodyHoverScale(b);
          b.el.style.transform = `translate3d(${b.x.toFixed(1)}px, ${b.y.toFixed(1)}px, 0) rotate(${b.hovering ? 0 : b.rot.toFixed(1)}deg) scale(${sc})`;
        });
      }
      requestAnimationFrame(stepScatter);
    }
    function bodyHoverScale(b) {
      return b.hovering && !b.dragging ? 1.22 : 1;
    }
    requestAnimationFrame(stepScatter);
  }

  /* --------------------------------------------------------------------------
     8. PROJECT DETAIL SHEET (Modal & Standalone History Support)
     -------------------------------------------------------------------------- */
  function openDetailSheet(projectId, startPhotoIndex = 0, pushState = true) {
    const p = projectsById[projectId];
    if (!p || !detailSheet) return;

    preloadProjectPhotos(projectId);

    const codeEl = document.getElementById("detail-code");
    const titleEl = document.getElementById("detail-title");
    const specsBody = document.getElementById("detail-specs-body");
    const descEl = document.getElementById("detail-desc");
    const shopWrap = document.getElementById("detail-shop-wrap");
    const imagesCol = document.getElementById("detail-images-col");

    if (codeEl) codeEl.textContent = `INDEX #${p.code} / ${p.section.toUpperCase()} / ${p.year}`;
    if (titleEl) titleEl.textContent = p.title;

    if (specsBody) {
      specsBody.innerHTML = p.specs
        .map((s) => `<tr><th>${escHtml(s.label)}</th><td>${escHtml(s.value).replace(/\n/g, "<br>")}</td></tr>`)
        .join("");
    }

    if (descEl) {
      descEl.innerHTML = p.description.map((para) => `<p>${escHtml(para)}</p>`).join("");
    }

    if (shopWrap) {
      if (p.shop_url) {
        shopWrap.innerHTML = `<p><a href="${escHtml(p.shop_url)}" target="_blank" rel="noreferrer">[${escHtml(p.shop_label || "View in shop ↗")}]</a></p>`;
      } else {
        shopWrap.innerHTML = "";
      }
    }

    if (imagesCol) {
      imagesCol.innerHTML = p.photos
        .map(
          (ph, idx) => `
          <figure class="detail-figure" id="detail-fig-${idx}">
            <img src="${resolvePath(ph.src)}" alt="${escHtml(p.title)} — ${escHtml(ph.alt || idx + 1)}" loading="eager" decoding="async">
            <figcaption class="detail-figcap">
              <span>[${String(idx + 1).padStart(2, "0")}/${String(p.photos.length).padStart(2, "0")}]</span>
              <span>${escHtml(ph.alt || p.title)}</span>
            </figcaption>
          </figure>`
        )
        .join("");
    }

    const curIdx = DATA.projects.findIndex((item) => item.id === projectId);
    const prevP = DATA.projects[(curIdx - 1 + DATA.projects.length) % DATA.projects.length];
    const nextP = DATA.projects[(curIdx + 1) % DATA.projects.length];
    const prevBtn = document.getElementById("detail-prev-btn");
    const nextBtn = document.getElementById("detail-next-btn");
    if (prevBtn && prevP) {
      prevBtn.onclick = () => openDetailSheet(prevP.id, 0, true);
      prevBtn.textContent = `← prev [#${prevP.code}]`;
    }
    if (nextBtn && nextP) {
      nextBtn.onclick = () => openDetailSheet(nextP.id, 0, true);
      nextBtn.textContent = `next [#${nextP.code}] →`;
    }

    detailSheet.removeAttribute("hidden");
    document.body.style.overflow = "hidden";

    if (startPhotoIndex > 0) {
      const targetFig = document.getElementById(`detail-fig-${startPhotoIndex}`);
      if (targetFig) targetFig.scrollIntoView({ behavior: "smooth", block: "center" });
    } else {
      detailSheet.scrollTop = 0;
    }

    if (pushState && window.history && window.history.pushState) {
      try {
        if (window.location.protocol === "file:") {
          window.history.pushState({ projectId }, `${p.title} — TAIRYOKU`, `#${projectId}`);
        } else {
          window.history.pushState({ projectId }, `${p.title} — TAIRYOKU`, p.url);
        }
      } catch (_e) {}
    }
  }

  function closeDetailSheet(pushState = true) {
    if (!detailSheet || detailSheet.hasAttribute("hidden")) return;
    detailSheet.setAttribute("hidden", "");
    document.body.style.overflow = "";
    if (pushState && window.history && window.history.pushState) {
      try {
        if (window.location.protocol === "file:") {
          window.history.pushState({}, "TAIRYOKU — Creative Team", window.location.pathname);
        } else {
          window.history.pushState({}, "TAIRYOKU — Creative Team", "/");
        }
      } catch (_e) {}
    }
  }

  const closeBtn = document.getElementById("detail-close-btn");
  if (closeBtn) closeBtn.addEventListener("click", () => closeDetailSheet(true));

  const toggleDetailToneBtn = document.getElementById("detail-tone-btn");
  if (toggleDetailToneBtn) {
    toggleDetailToneBtn.addEventListener("click", () => {
      document.querySelectorAll(".detail-figure").forEach((fig) => {
        fig.classList.toggle("is-duotone");
      });
    });
  }

  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeDetailSheet(true);
  });

  window.addEventListener("popstate", (e) => {
    if (e.state && e.state.projectId) {
      openDetailSheet(e.state.projectId, 0, false);
    } else {
      closeDetailSheet(false);
    }
  });

  /* --------------------------------------------------------------------------
     9. INTERACTIVE LOGO STAMP (Playful Artist Signature in About Section)
     -------------------------------------------------------------------------- */
  const stampBtn = document.getElementById("stamp-trigger");
  if (stampBtn) {
    const triggerStampBurst = (e) => {
      const vw = window.innerWidth || 1200;
      const vh = window.innerHeight || 800;
      const isNarrow = vw < 640;
      const logoEl = stampBtn.querySelector("img") || stampBtn;
      const rect = logoEl.getBoundingClientRect ? logoEl.getBoundingClientRect() : null;
      const fallbackX = rect ? rect.left + rect.width / 2 : vw / 2;
      const fallbackY = rect ? rect.top + rect.height / 2 : vh / 2;
      const ox = e && e.clientX > 0 ? e.clientX : fallbackX;
      const oy = e && e.clientY > 0 ? e.clientY : fallbackY;

      stampBtn.classList.remove("is-popping");
      if (stampBtn.offsetWidth >= 0) stampBtn.classList.add("is-popping");
      setTimeout(() => stampBtn.classList.remove("is-popping"), 220);

      const count = 7;
      const maxRX = Math.min(vw * 0.42, 420);
      const maxRY = Math.min(vh * 0.36, 300);

      for (let i = 0; i < count; i++) {
        const st = document.createElement("img");
        st.src = resolvePath("/assets/tairyoku-logo.png");
        st.alt = "";
        st.className = "ink-stamp";

        const isHero = i === 0;
        const size = isHero
          ? (isNarrow ? 185 : 265) + Math.random() * 65
          : (isNarrow ? 115 : 150) + Math.random() * (isNarrow ? 75 : 120);

        let dx;
        let dy;
        if (isHero) {
          dx = (Math.random() - 0.5) * 70;
          dy = -36 - Math.random() * 64;
        } else {
          const angle = ((i - 1) / (count - 1)) * Math.PI * 2 + (Math.random() - 0.5) * 0.55;
          const dist = 0.42 + Math.random() * 0.58;
          dx = Math.cos(angle) * maxRX * dist;
          dy = Math.sin(angle) * maxRY * dist - 55;
        }

        const margin = Math.min(size * 0.38, 110);
        const tx = Math.max(margin, Math.min(vw - margin, ox + dx));
        const ty = Math.max(margin, Math.min(vh - margin, oy + dy));
        const r0 = (Math.random() - 0.5) * 28;
        const r1 = r0 + (Math.random() - 0.5) * 32;
        const r2 = r1 + (Math.random() - 0.5) * 16;
        const sPop = isHero ? 1.42 : 1.24 + Math.random() * 0.24;
        const sLand = isHero ? 1.08 : 0.94 + Math.random() * 0.18;
        const delay = i * 28;
        const dur = (isHero ? 2500 : 2150) + Math.floor(Math.random() * 420);

        st.style.left = `${ox}px`;
        st.style.top = `${oy}px`;
        st.style.setProperty("--stamp-size", `${Math.round(size)}px`);
        st.style.setProperty("--dx", `${Math.round(tx - ox)}px`);
        st.style.setProperty("--dy", `${Math.round(ty - oy)}px`);
        st.style.setProperty("--r0", `${r0.toFixed(1)}deg`);
        st.style.setProperty("--r1", `${r1.toFixed(1)}deg`);
        st.style.setProperty("--r2", `${r2.toFixed(1)}deg`);
        st.style.setProperty("--s-pop", sPop.toFixed(2));
        st.style.setProperty("--s-land", sLand.toFixed(2));
        st.style.setProperty("--stamp-delay", `${delay}ms`);
        st.style.setProperty("--stamp-dur", `${dur}ms`);

        document.body.appendChild(st);
        setTimeout(() => st.remove(), delay + dur + 100);
      }
    };

    stampBtn.addEventListener("click", triggerStampBurst);
    stampBtn.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        triggerStampBurst(null);
      }
    });
  }

  if (window.INITIAL_PROJECT_ID) {
    openDetailSheet(window.INITIAL_PROJECT_ID, 0, false);
  }
  if (window.INITIAL_FILTER) {
    applyFilter(window.INITIAL_FILTER);
  }
  if (window.INITIAL_SCROLL_TARGET) {
    const el = document.getElementById(window.INITIAL_SCROLL_TARGET);
    if (el) setTimeout(() => el.scrollIntoView({ behavior: "smooth" }), 80);
  }
})();
