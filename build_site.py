import json
import os
import html as html_lib

ROOT_DIR = "/Users/fds_2023_1/.gemini/antigravity/scratch/tairyoku-creative-team"
DATA_PATH = os.path.join(ROOT_DIR, "site_data.json")
SITE_ORIGIN = "https://tairyoku.jp"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    SITE_DATA = json.load(f)

STYLES_CSS = r"""/* ==========================================================================
   TAIRYOKU (体力) — Contemporary Artist Archive / Kinetic Contact Wall
   Single-Color Ink System (Violet / Ultramarine / Cobalt) + Raw HTML UI
   ========================================================================== */

:root {
  /* Default Ink: Electric Ultramarine Violet */
  --ink: #3519e8;
  --ink-rgb: 53, 25, 232;
  --ink-soft: rgba(53, 25, 232, 0.12);
  --ink-mid: rgba(53, 25, 232, 0.38);
  --bg: #faf9ff;
  --bg-rgb: 250, 249, 255;
  --font-raw: "Times New Roman", Times, "Hiragino Mincho ProN", "YuMincho", serif;
  --font-mono: ui-monospace, "SFMono-Regular", Menlo, Monaco, Consolas, "Courier New", monospace;
  --font-sans: "Helvetica Neue", Arial, "Hiragino Kaku Gothic ProN", "Noto Sans JP", sans-serif;
  --tile-min: 265px;
  --grid-gap: 1px;
}

html[data-ink="ultramarine"] {
  --ink: #1424f5;
  --ink-rgb: 20, 36, 245;
  --ink-soft: rgba(20, 36, 245, 0.12);
  --ink-mid: rgba(20, 36, 245, 0.38);
  --bg: #f8faff;
  --bg-rgb: 248, 250, 255;
}

html[data-ink="purple"] {
  --ink: #5a12d9;
  --ink-rgb: 90, 18, 217;
  --ink-soft: rgba(90, 18, 217, 0.12);
  --ink-mid: rgba(90, 18, 217, 0.38);
  --bg: #fcf9ff;
  --bg-rgb: 252, 249, 255;
}

html[data-ink="night"] {
  --ink: #b6a8ff;
  --ink-rgb: 182, 168, 255;
  --ink-soft: rgba(182, 168, 255, 0.14);
  --ink-mid: rgba(182, 168, 255, 0.42);
  --bg: #0c0721;
  --bg-rgb: 12, 7, 33;
}

html[data-size="s"] { --wall-cols: 6; }
html[data-size="m"] { --wall-cols: 4; }
html[data-size="l"] { --wall-cols: 3; }

[hidden] {
  display: none !important;
}

* {
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: var(--font-sans);
  font-size: 13px;
  line-height: 1.45;
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}

::selection {
  background: var(--ink);
  color: var(--bg);
}

/* Raw HTML Link & Button Reset */
a, .raw-btn {
  color: var(--ink);
  background: transparent;
  border: 0;
  padding: 0 2px;
  margin: 0;
  font: inherit;
  text-decoration: underline;
  text-underline-offset: 2px;
  text-decoration-thickness: 1px;
  cursor: pointer;
  display: inline;
}

a:hover,
.raw-btn:hover,
a[aria-current="page"],
a[aria-pressed="true"],
.raw-btn[aria-pressed="true"],
.raw-btn.is-active {
  background: var(--ink);
  color: var(--bg);
  text-decoration: none;
}

a:focus-visible,
.raw-btn:focus-visible {
  outline: 1px dashed var(--ink);
  outline-offset: 2px;
}

/* Hidden inline SVG filter container */
.svg-defs {
  position: absolute;
  width: 0;
  height: 0;
  overflow: hidden;
  pointer-events: none;
}

/* ==========================================================================
   TOP RAW HTML HEADER & DIRECTORY BAR
   ========================================================================== */
.raw-header {
  position: sticky;
  top: 0;
  z-index: 60;
  background: rgba(var(--bg-rgb), 0.94);
  backdrop-filter: blur(4px);
  border-bottom: 1px solid var(--ink);
}

.raw-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  justify-content: space-between;
  gap: 6px 18px;
  padding: 7px 10px;
  border-bottom: 1px solid var(--ink);
}

.brand-cluster {
  display: inline-flex;
  align-items: baseline;
  gap: 8px;
  flex-wrap: wrap;
}

.brand-link,
.brand-link:hover,
.brand-link[aria-pressed="true"] {
  font-family: var(--font-raw);
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 0.02em;
  text-decoration: none;
  background: transparent;
  color: var(--ink);
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.brand-logo-mini {
  width: 18px;
  height: 18px;
  object-fit: contain;
  filter: url(#tairyoku-duotone);
  transition: transform 0.35s ease;
  vertical-align: middle;
}

.brand-link:hover .brand-logo-mini {
  transform: rotate(18deg) scale(1.15);
}

.raw-meta {
  font-family: var(--font-mono);
  font-size: 11px;
  opacity: 0.85;
}

.raw-nav {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 4px 10px;
  font-family: var(--font-raw);
  font-size: 14px;
}

.raw-sep {
  opacity: 0.45;
  user-select: none;
  font-family: var(--font-mono);
  font-size: 11px;
}

.raw-controls {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 4px 12px;
  padding: 5px 10px;
  font-family: var(--font-mono);
  font-size: 11px;
  background: var(--bg);
}

.ctrl-group {
  display: inline-flex;
  align-items: baseline;
  gap: 4px;
  flex-wrap: wrap;
}

.ctrl-label {
  opacity: 0.65;
}

/* ==========================================================================
   COLLAPSIBLE RAW HTML INDEX LIST (Top Directory)
   ========================================================================== */
.raw-directory {
  border-bottom: 1px solid var(--ink);
  background: var(--bg);
  padding: 8px 10px 10px;
  font-family: var(--font-raw);
  font-size: 13.5px;
  line-height: 1.5;
}

.raw-directory[hidden] {
  display: none;
}

.directory-columns {
  display: flex;
  flex-wrap: wrap;
  gap: 2px 18px;
  align-items: baseline;
}

.dir-item {
  display: inline-flex;
  align-items: baseline;
  gap: 4px;
  white-space: nowrap;
}

.dir-num {
  font-family: var(--font-mono);
  font-size: 10.5px;
  opacity: 0.7;
  text-decoration: none;
}

.dir-cat {
  font-family: var(--font-mono);
  font-size: 10px;
  opacity: 0.65;
}

.dir-item.is-highlighted a {
  background: var(--ink);
  color: var(--bg);
  text-decoration: none;
}

/* ==========================================================================
   WALL OF IMAGES (Contact Sheet / Edge-to-Edge Tiled Grid)
   ========================================================================== */
.stage-wrap {
  position: relative;
  min-height: calc(100vh - 90px);
  width: 100%;
}

.wall-grid {
  display: grid;
  grid-template-columns: repeat(var(--wall-cols, 4), minmax(0, 1fr));
  gap: 0;
  background: var(--bg);
  border-bottom: 1px solid var(--ink);
  will-change: transform;
  transition: transform 0.18s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.wall-tile {
  position: relative;
  aspect-ratio: 1 / 1;
  background: transparent;
  overflow: visible;
  cursor: pointer;
  display: block;
  padding: 0;
  text-decoration: none;
  user-select: none;
  z-index: 1;
}

.wall-tile:hover,
.wall-tile:focus-visible,
.wall-tile.is-project-match {
  z-index: 45;
  background: transparent;
  color: var(--ink);
}

.wall-tile-card {
  position: relative;
  width: 100%;
  height: 100%;
  background: var(--bg);
  padding: 6px;
  overflow: hidden;
  border-right: 1px solid var(--ink);
  border-bottom: 1px solid var(--ink);
  transform: scale(1);
  transform-origin: center center;
  transition:
    transform 0.28s cubic-bezier(0.16, 1, 0.3, 1),
    box-shadow 0.28s ease,
    border-color 0.2s ease,
    background-color 0.25s ease;
}

.wall-tile:hover .wall-tile-card,
.wall-tile:focus-visible .wall-tile-card,
.wall-tile.is-project-match .wall-tile-card {
  transform: scale(1.26);
  border: 1px solid var(--ink);
  box-shadow: 10px 10px 0 var(--ink);
  background: var(--bg);
}

.wall-tile-inner {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.wall-tile img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  /* Single-color purple/blue ink duotone by default */
  filter: url(#tairyoku-duotone) contrast(1.06);
  transition:
    filter 0.3s ease,
    opacity 0.25s ease;
}

.wall-tile[data-group="zine"] img,
.wall-tile[data-group="commission"] img {
  object-fit: contain;
  padding: 4px;
}

/* Reveal full original color on hover, afterglow wake, sibling resonance, or all-color mode */
.wall-tile:hover img,
.wall-tile:focus-visible img,
.wall-tile.is-awake img,
.wall-tile.is-project-match img,
html[data-color="color"] .wall-tile img {
  filter: none;
}

/* Dim non-matching tiles when hovering a project in the index list */
.wall-grid.has-project-focus .wall-tile:not(.is-project-match) {
  opacity: 0.25;
}

.wall-grid.has-project-focus .wall-tile.is-project-match .wall-tile-card {
  outline: 2px solid var(--ink);
  outline-offset: -2px;
}

/* Tiny raw HTML frame numbers and hover label on each tile */
.tile-idx {
  position: absolute;
  top: 5px;
  left: 6px;
  z-index: 4;
  font-family: var(--font-mono);
  font-size: 10px;
  line-height: 1.1;
  color: var(--ink);
  background: rgba(var(--bg-rgb), 0.88);
  padding: 2px 4px;
  pointer-events: none;
  border: 1px solid rgba(var(--ink-rgb), 0.25);
}

.wall-tile:hover .tile-idx {
  background: var(--ink);
  color: var(--bg);
  border-color: var(--ink);
}

.tile-caption {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 4;
  background: var(--ink);
  color: var(--bg);
  font-family: var(--font-mono);
  font-size: 10.5px;
  line-height: 1.3;
  padding: 4px 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  opacity: 0;
  transform: translateY(100%);
  transition: opacity 0.16s ease, transform 0.16s ease;
  pointer-events: none;
}

.wall-tile:hover .tile-caption,
.wall-tile:focus-visible .tile-caption,
.wall-tile.is-project-match .tile-caption {
  opacity: 1;
  transform: translateY(0);
}

/* ==========================================================================
   MODE 2: KINETIC DRIFT CONVEYOR (view="drift")
   ========================================================================== */
.drift-stage {
  display: none;
  flex-direction: column;
  gap: 0;
  background: var(--bg);
  border-bottom: 1px solid var(--ink);
  overflow: hidden;
  padding: 28px 0;
}

html[data-view="drift"] .wall-grid { display: none; }
html[data-view="drift"] .drift-stage { display: flex; }

.drift-row {
  display: flex;
  width: max-content;
  background: var(--bg);
  border-top: 1px solid var(--ink);
  gap: 0;
  will-change: transform;
}

.drift-row .wall-tile {
  width: clamp(230px, 24vw, 340px);
  height: clamp(230px, 24vw, 340px);
  flex: 0 0 auto;
}

.drift-row .wall-tile:hover .wall-tile-card {
  transform: scale(1.16);
}

/* ==========================================================================
   MODE 3: ARTIST STUDIO SCATTER CANVAS (view="scatter")
   ========================================================================== */
.scatter-stage {
  display: none;
  position: relative;
  width: 100%;
  height: calc(100vh - 92px);
  min-height: 620px;
  overflow: hidden;
  background:
    radial-gradient(var(--ink-mid) 1px, transparent 1px) 0 0 / 24px 24px,
    var(--bg);
  border-bottom: 1px solid var(--ink);
}

html[data-view="scatter"] .wall-grid { display: none; }
html[data-view="scatter"] .scatter-stage { display: block; }

.scatter-toolbar {
  position: absolute;
  top: 8px;
  left: 10px;
  z-index: 40;
  background: rgba(var(--bg-rgb), 0.9);
  border: 1px solid var(--ink);
  padding: 4px 8px;
  font-family: var(--font-mono);
  font-size: 11px;
  display: flex;
  gap: 10px;
  align-items: center;
}

.scatter-card {
  position: absolute;
  width: clamp(170px, 19vw, 260px);
  background: var(--bg);
  border: 1px solid var(--ink);
  padding: 4px 4px 18px;
  cursor: grab;
  user-select: none;
  touch-action: none;
  box-shadow: 3px 3px 0 var(--ink);
  transition: box-shadow 0.2s ease;
}

.scatter-card:active {
  cursor: grabbing;
  box-shadow: 7px 7px 0 var(--ink);
}

.scatter-card:hover {
  box-shadow: 9px 9px 0 var(--ink);
}

.scatter-card img {
  width: 100%;
  height: auto;
  max-height: 240px;
  object-fit: contain;
  display: block;
  pointer-events: none;
  filter: url(#tairyoku-duotone) contrast(1.06);
  transition: filter 0.3s ease, transform 0.25s ease;
}

.scatter-card:hover img {
  transform: scale(1.04);
}

.scatter-card:hover img,
.scatter-card.is-awake img,
html[data-color="color"] .scatter-card img {
  filter: none;
}

.scatter-meta {
  position: absolute;
  left: 4px;
  right: 4px;
  bottom: 2px;
  font-family: var(--font-mono);
  font-size: 9.5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ==========================================================================
   MODE 4: RAW HTML TABLE VIEW (view="table")
   ========================================================================== */
.table-stage {
  display: none;
  padding: 14px 10px 60px;
}

html[data-view="table"] .wall-grid { display: none; }
html[data-view="table"] .table-stage { display: block; }

.raw-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid var(--ink);
  font-family: var(--font-raw);
  font-size: 14px;
}

.raw-table th,
.raw-table td {
  border: 1px solid var(--ink);
  padding: 6px 8px;
  text-align: left;
  vertical-align: top;
}

.raw-table th {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 400;
  text-transform: uppercase;
  background: var(--ink-soft);
}

.raw-table tbody tr {
  cursor: pointer;
}

.raw-table tbody tr:hover {
  background: var(--ink);
  color: var(--bg);
}

.raw-table tbody tr:hover a,
.raw-table tbody tr:hover .raw-btn {
  color: var(--bg);
}

.table-thumb-strip {
  display: inline-flex;
  gap: 4px;
  flex-wrap: wrap;
  vertical-align: middle;
}

.table-thumb-strip img {
  width: 52px;
  height: 52px;
  object-fit: cover;
  border: 1px solid currentColor;
  filter: url(#tairyoku-duotone);
}

.raw-table tbody tr:hover .table-thumb-strip img {
  filter: none;
}

/* ==========================================================================
   EDITORIAL RAW HTML SECTIONS (ABOUT / CREATORS / CONTACT)
   ========================================================================== */
.raw-section {
  border-bottom: 1px solid var(--ink);
  padding: 24px 12px 36px;
  position: relative;
  background: var(--bg);
}

.raw-section-inner {
  max-width: 1080px;
}

.raw-h1 {
  font-family: var(--font-raw);
  font-size: clamp(22px, 3vw, 34px);
  font-weight: 400;
  margin: 0 0 14px;
  letter-spacing: -0.01em;
}

.raw-lead {
  font-family: var(--font-raw);
  font-size: clamp(16px, 2vw, 22px);
  line-height: 1.45;
  margin: 0 0 12px;
}

.raw-p {
  margin: 0 0 12px;
  max-width: 68ch;
  font-size: 13.5px;
  line-height: 1.65;
}

.raw-grid-2 {
  display: grid;
  grid-template-columns: minmax(250px, 340px) minmax(0, 1fr);
  gap: 22px 26px;
  align-items: start;
  margin-top: 18px;
}

.chronology-col {
  min-width: 0;
}

.chronology-head {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  justify-content: space-between;
  gap: 6px 12px;
  margin: 0 0 6px;
}

.chronology-label {
  font-family: var(--font-mono);
  font-size: 11px;
  margin: 0;
}

.chronology-scroll {
  max-height: clamp(280px, 44vh, 400px);
  overflow-y: auto;
  overflow-x: hidden;
  border: 1px solid var(--ink);
  background: var(--bg);
  scrollbar-width: thin;
  scrollbar-color: var(--ink) transparent;
}

.chronology-scroll.is-expanded {
  max-height: none;
  overflow-y: visible;
}

.chronology-scroll::-webkit-scrollbar {
  width: 6px;
}

.chronology-scroll::-webkit-scrollbar-thumb {
  background: var(--ink);
}

.chronology-table {
  width: 100%;
  border: 0;
  border-collapse: separate;
  border-spacing: 0;
  table-layout: fixed;
}

.chronology-table th,
.chronology-table td {
  border: 0;
  border-right: 1px solid var(--ink);
  border-bottom: 1px solid var(--ink);
  line-height: 1.5;
  overflow-wrap: anywhere;
  word-break: break-word;
}

.chronology-table th:last-child,
.chronology-table td:last-child {
  border-right: 0;
}

.chronology-table tbody tr:last-child td {
  border-bottom: 0;
}

.chronology-table thead th {
  position: sticky;
  top: 0;
  z-index: 2;
  background: linear-gradient(var(--ink-soft), var(--ink-soft)), var(--bg);
}

.chronology-table tbody tr {
  cursor: default;
}

.chronology-table tbody tr:hover {
  background: var(--ink-soft);
  color: var(--ink);
}

.chronology-table tbody tr:hover a {
  color: var(--ink);
}

.chronology-col-date {
  width: 108px;
}

.chronology-col-loc {
  width: 34%;
}

.chronology-note {
  margin-top: 4px;
  font-size: 12px;
  line-height: 1.5;
  opacity: 0.85;
}

.stamp-zone {
  margin-top: 16px;
  padding: 12px 14px;
  border: 1px dashed var(--ink);
  font-family: var(--font-mono);
  font-size: 11px;
  display: inline-flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  user-select: none;
  background: var(--bg);
  transition: transform 0.16s cubic-bezier(0.2, 1.6, 0.4, 1), background-color 0.15s ease, box-shadow 0.15s ease;
}

.stamp-zone:hover {
  background: var(--ink-soft);
  border-style: solid;
  box-shadow: 3px 3px 0 var(--ink);
}

.stamp-zone:active,
.stamp-zone.is-popping {
  transform: scale(0.94);
}

.stamp-zone img {
  width: 52px;
  height: 52px;
  filter: url(#tairyoku-duotone);
  transition: transform 0.24s cubic-bezier(0.18, 1.8, 0.35, 1);
}

.stamp-zone:hover img {
  transform: scale(1.12) rotate(-4deg);
}

.stamp-zone.is-popping img {
  transform: scale(1.36) rotate(8deg);
}

.contact-split {
  display: grid;
  grid-template-columns: minmax(280px, 1fr) minmax(230px, 320px);
  gap: 28px;
  align-items: center;
  justify-content: space-between;
}

.contact-table {
  max-width: 560px;
}

.contact-video-frame {
  margin: 0;
  width: 100%;
  max-width: 320px;
  justify-self: end;
  border: 1px solid var(--ink);
  background: var(--bg);
  overflow: hidden;
  line-height: 0;
}

.contact-video {
  display: block;
  width: 100%;
  height: auto;
  aspect-ratio: 4 / 5;
  object-fit: cover;
  filter: contrast(1.16) brightness(1.05) url(#tairyoku-duotone);
  transition: filter 0.28s ease;
}

html[data-color="color"] .contact-video,
html[data-color="hover"] .contact-video-frame:hover .contact-video {
  filter: none;
}

/* ==========================================================================
   PROJECT DETAIL OVERLAY / MODAL SHEET
   ========================================================================== */
.detail-sheet {
  position: fixed;
  inset: 0;
  z-index: 100;
  background: rgba(var(--bg-rgb), 0.97);
  overflow-y: auto;
  padding: 0;
}

.detail-sheet[hidden] {
  display: none;
}

.detail-topbar {
  position: sticky;
  top: 0;
  z-index: 10;
  background: var(--bg);
  border-bottom: 1px solid var(--ink);
  padding: 8px 12px;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: baseline;
  gap: 10px;
  font-family: var(--font-mono);
  font-size: 12px;
}

.detail-body {
  padding: 16px 12px 64px;
  display: grid;
  grid-template-columns: minmax(260px, 370px) minmax(0, 1fr);
  gap: 24px;
  align-items: start;
}

.detail-meta-col {
  position: sticky;
  top: 46px;
}

.detail-title {
  font-family: var(--font-raw);
  font-size: clamp(22px, 2.8vw, 32px);
  font-weight: 400;
  margin: 0 0 12px;
  line-height: 1.2;
}

.detail-desc {
  margin: 14px 0;
  font-size: 13.5px;
  line-height: 1.65;
}

.detail-desc p {
  margin: 0 0 10px;
}

.detail-images-col {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 12px;
}

.detail-figure {
  margin: 0;
  border: 1px solid var(--ink);
  background: var(--bg);
  padding: 8px;
}

.detail-figure img {
  width: 100%;
  height: auto;
  display: block;
  filter: none;
  transition: filter 0.3s ease;
}

.detail-figure.is-duotone img {
  filter: url(#tairyoku-duotone);
}

.detail-figure.is-duotone:hover img {
  filter: none;
}

.detail-figcap {
  margin-top: 6px;
  font-family: var(--font-mono);
  font-size: 10.5px;
  display: flex;
  justify-content: space-between;
  opacity: 0.8;
}

/* ==========================================================================
   FLOATING KINETIC CURSOR TAG & BOTTOM STATUS TICKER
   ========================================================================== */
.cursor-tag {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 90;
  pointer-events: none;
  background: var(--ink);
  color: var(--bg);
  font-family: var(--font-mono);
  font-size: 10.5px;
  padding: 2px 6px;
  white-space: nowrap;
  opacity: 0;
  transform: translate(-50%, -140%);
  transition: opacity 0.12s ease;
}

.cursor-tag.is-visible {
  opacity: 1;
}

.raw-footer {
  position: sticky;
  bottom: 0;
  z-index: 50;
  background: var(--bg);
  border-top: 1px solid var(--ink);
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-family: var(--font-mono);
  font-size: 11px;
  overflow: hidden;
}

.raw-marquee {
  flex: 1;
  overflow: hidden;
  white-space: nowrap;
  padding: 4px 0;
}

.raw-marquee-track {
  display: inline-block;
  white-space: nowrap;
  animation: raw-scroll 32s linear infinite;
}

.raw-marquee:hover .raw-marquee-track {
  animation-play-state: paused;
}

@keyframes raw-scroll {
  from { transform: translateX(0); }
  to { transform: translateX(-50%); }
}

.footer-status {
  padding: 4px 10px;
  border-left: 1px solid var(--ink);
  background: var(--bg);
  white-space: nowrap;
}

/* Stamp clones created on click — large random full-window stamps */
.ink-stamp {
  position: fixed;
  width: var(--stamp-size, 200px);
  height: var(--stamp-size, 200px);
  pointer-events: none;
  z-index: 95;
  filter: url(#tairyoku-duotone);
  transform-origin: center center;
  will-change: transform, opacity;
  animation: tairyoku-stamp-pop var(--stamp-dur, 2300ms) cubic-bezier(0.16, 1, 0.3, 1) var(--stamp-delay, 0ms) both;
}

@keyframes tairyoku-stamp-pop {
  0% {
    opacity: 0;
    transform: translate(-50%, -50%) rotate(var(--r0, 0deg)) scale(0.2);
  }
  15% {
    opacity: 1;
    transform: translate(-50%, -50%) rotate(var(--r1, -6deg)) scale(var(--s-pop, 1.35));
  }
  28% {
    opacity: 0.95;
    transform: translate(-50%, -50%) rotate(var(--r2, -4deg)) scale(var(--s-land, 1));
  }
  78% {
    opacity: 0.9;
    transform: translate(-50%, -50%) rotate(var(--r2, -4deg)) scale(var(--s-land, 1));
  }
  100% {
    opacity: 0;
    transform: translate(-50%, -50%) rotate(var(--r2, -4deg)) scale(calc(var(--s-land, 1) * 0.96));
  }
}

@media (max-width: 1120px) {
  html[data-size="s"] { --wall-cols: 4; }
  html[data-size="m"] { --wall-cols: 3; }
  html[data-size="l"] { --wall-cols: 2; }
}

@media (max-width: 780px) {
  html[data-size="s"] { --wall-cols: 3; }
  html[data-size="m"] { --wall-cols: 2; }
  html[data-size="l"] { --wall-cols: 1; }
  .wall-tile:hover .wall-tile-card {
    transform: scale(1.08);
  }
  .detail-body {
    grid-template-columns: 1fr;
  }
  .detail-meta-col {
    position: static;
  }
  .detail-images-col {
    grid-template-columns: 1fr;
  }
  .cursor-tag {
    display: none;
  }
  .contact-split {
    grid-template-columns: 1fr;
    gap: 18px;
  }
  .contact-video-frame {
    justify-self: center;
    max-width: 300px;
    margin-top: 4px;
  }
}

@media (max-width: 860px) {
  .raw-grid-2 {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 600px) {
  .chronology-table colgroup,
  .chronology-table thead {
    display: none;
  }
  .chronology-table,
  .chronology-table tbody,
  .chronology-table tr,
  .chronology-table td {
    display: block;
    width: 100%;
  }
  .chronology-table tbody tr {
    padding: 8px 10px;
    border-bottom: 1px solid var(--ink);
  }
  .chronology-table tbody tr:last-child {
    border-bottom: 0;
  }
  .chronology-table td {
    border: 0;
    padding: 0;
  }
  .chronology-table td.chronology-date {
    font-size: 11px;
    opacity: 0.78;
    margin-bottom: 2px;
  }
  .chronology-table td.chronology-title {
    font-size: 14px;
    margin-bottom: 2px;
  }
  .chronology-table td.chronology-loc {
    font-size: 12px;
    opacity: 0.85;
  }
}
"""

def build_svg_filter():
    return """<svg class="svg-defs" aria-hidden="true">
  <defs>
    <filter id="tairyoku-duotone" color-interpolation-filters="sRGB">
      <feColorMatrix type="matrix" values="
        0.299 0.587 0.114 0 0
        0.299 0.587 0.114 0 0
        0.299 0.587 0.114 0 0
        0     0     0     1 0" result="gray"/>
      <feComponentTransfer in="gray" result="duotone">
        <feFuncR id="duotone-r" type="table" tableValues="0.208 0.980"/>
        <feFuncG id="duotone-g" type="table" tableValues="0.098 0.976"/>
        <feFuncB id="duotone-b" type="table" tableValues="0.910 1.000"/>
      </feComponentTransfer>
    </filter>
  </defs>
</svg>"""

def build_all_tiles(projects):
    tiles = []
    for idx, p in enumerate(projects, 1):
        photos = p["photos"]
        cover = photos[0] if photos else {"src": "/assets/tairyoku-logo.png", "alt": p["title"]}
        tiles.append({
            "frame": idx,
            "frame_code": p["code"],
            "project_id": p["id"],
            "project_code": p["code"],
            "project_title": p["title"],
            "project_url": p["url"],
            "section": p["section"],
            "group": p["group"],
            "year": p["year"],
            "category_label": p["category_label"],
            "src": cover["src"],
            "alt": f"{p['title']} — {cover.get('alt') or 'cover'}",
            "photo_index": 1,
            "photo_total": len(photos),
        })
    return tiles

ALL_TILES = build_all_tiles(SITE_DATA["projects"])

APP_JS = r"""/* ==========================================================================
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
      if (btn.classList && btn.classList.contains("brand-link")) return;
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
    const triggerStampBurst = () => {
      const vw = window.innerWidth || 1200;
      const vh = window.innerHeight || 800;
      const isNarrow = vw < 640;

      stampBtn.classList.remove("is-popping");
      if (stampBtn.offsetWidth >= 0) stampBtn.classList.add("is-popping");
      setTimeout(() => stampBtn.classList.remove("is-popping"), 220);

      const count = 7;
      const placed = [];
      const minDist = Math.min(vw, vh) * 0.22;

      for (let i = 0; i < count; i++) {
        const st = document.createElement("img");
        st.src = resolvePath("/assets/tairyoku-logo.png");
        st.alt = "";
        st.className = "ink-stamp";

        const isHero = i === 0;
        const size = isHero
          ? (isNarrow ? 190 : 270) + Math.random() * 70
          : (isNarrow ? 120 : 165) + Math.random() * (isNarrow ? 75 : 130);

        const padX = Math.min(size * 0.42, vw * 0.14);
        const padY = Math.min(size * 0.42, vh * 0.14);
        let rx = vw / 2;
        let ry = vh / 2;
        for (let attempt = 0; attempt < 8; attempt++) {
          const candX = padX + Math.random() * Math.max(40, vw - padX * 2);
          const candY = padY + Math.random() * Math.max(40, vh - padY * 2);
          const tooClose = placed.some((p) => Math.hypot(candX - p.x, candY - p.y) < minDist);
          rx = candX;
          ry = candY;
          if (!tooClose) break;
        }
        placed.push({ x: rx, y: ry });

        const baseRot = (Math.random() - 0.5) * 44;
        const r0 = baseRot + (Math.random() - 0.5) * 18;
        const r1 = baseRot + (Math.random() - 0.5) * 8;
        const r2 = baseRot;
        const sPop = isHero ? 1.42 : 1.28 + Math.random() * 0.22;
        const sLand = isHero ? 1.08 : 0.96 + Math.random() * 0.16;
        const delay = i * 55;
        const dur = (isHero ? 2450 : 2100) + Math.floor(Math.random() * 420);

        st.style.left = `${Math.round(rx)}px`;
        st.style.top = `${Math.round(ry)}px`;
        st.style.setProperty("--stamp-size", `${Math.round(size)}px`);
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
        triggerStampBurst();
      }
    });
  }

  document.querySelectorAll("video[autoplay]").forEach((v) => {
    v.muted = true;
    const p = v.play && v.play();
    if (p && typeof p.catch === "function") p.catch(() => {});
  });

  const chronologyScroll = document.getElementById("chronology-scroll");
  const chronologyToggleBtn = document.getElementById("chronology-toggle-btn");
  if (chronologyScroll && chronologyToggleBtn) {
    const totalCount = chronologyScroll.querySelectorAll("tbody tr").length;
    const syncChronologyToggle = () => {
      const isExpanded = chronologyScroll.classList.contains("is-expanded");
      const overflows = chronologyScroll.scrollHeight > chronologyScroll.clientHeight + 4;
      chronologyToggleBtn.hidden = !isExpanded && !overflows;
      chronologyToggleBtn.setAttribute("aria-expanded", String(isExpanded));
      chronologyToggleBtn.textContent = isExpanded
        ? "[collapse ↑]"
        : `[expand all (${totalCount}) ↕]`;
    };
    chronologyToggleBtn.addEventListener("click", () => {
      chronologyScroll.classList.toggle("is-expanded");
      syncChronologyToggle();
    });
    window.addEventListener("resize", syncChronologyToggle);
    syncChronologyToggle();
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
"""

def render_page_html(
    title="TAIRYOKU — Creative Team (体力)",
    initial_project_id=None,
    initial_filter="all",
    initial_scroll=None,
    prefix=".",
    canonical_path="/",
    og_image="/assets/tairyoku-logo.png",
    description=None,
):
    projects = SITE_DATA["projects"]
    team = SITE_DATA["team"]

    canonical_url = f"{SITE_ORIGIN}{canonical_path}"
    og_image_url = og_image if og_image.startswith("http") else f"{SITE_ORIGIN}{og_image if og_image.startswith('/') else '/' + og_image}"
    meta_desc = description or (
        "TAIRYOKU (体力) — Creative team based in Fukuoka, Japan. "
        "ZINEs, clothing, printed matter, exhibitions and visual artwork."
    )

    def p_url(rel):
        return f"{prefix}{rel}" if rel.startswith("/") else f"{prefix}/{rel}"

    # Directory items (01..18)
    dir_items_html = []
    for p in projects:
        dir_items_html.append(
            f'<span class="dir-item" data-project-id="{p["id"]}">'
            f'<span class="dir-num">{p["code"]}.</span>'
            f'<a href="{p_url(p["url"])}">{html_lib.escape(p["title"])}</a>'
            f'<span class="dir-cat">[{html_lib.escape(p["category_label"])},{len(p["photos"])}]</span>'
            f'</span>'
        )

    # Wall tiles (18 projects — 1 cover tile per project, flipbook on hover)
    wall_tiles_html = []
    for t in ALL_TILES:
        wall_tiles_html.append(
            f'<a class="wall-tile" href="{p_url(t["project_url"])}" '
            f'data-frame-code="{t["frame_code"]}" '
            f'data-project-id="{t["project_id"]}" '
            f'data-project-title="{html_lib.escape(t["project_title"])}" '
            f'data-section="{t["section"]}" '
            f'data-group="{t["group"]}" '
            f'data-category="{html_lib.escape(t["category_label"])}" '
            f'data-year="{t["year"]}" '
            f'data-photo-index="1" '
            f'data-active-photo-index="0">'
            f'<div class="wall-tile-card">'
            f'<span class="tile-idx">#{t["project_code"]} [{t["photo_total"]}p]</span>'
            f'<div class="wall-tile-inner">'
            f'<img src="{p_url(t["src"])}" alt="{html_lib.escape(t["alt"])}" loading="eager">'
            f'</div>'
            f'<span class="tile-caption">#{t["project_code"]} {html_lib.escape(t["project_title"])} (1/{t["photo_total"]})</span>'
            f'</div>'
            f'</a>'
        )

    # Table rows (18 projects)
    table_rows_html = []
    for p in projects:
        thumbs = "".join(
            f'<img src="{p_url(ph["src"])}" alt="" loading="lazy">'
            for ph in p["photos"][:5]
        )
        shop_cell = f'<a href="{p["shop_url"]}" target="_blank" rel="noreferrer">shop ↗</a>' if p["shop_url"] else "—"
        table_rows_html.append(
            f'<tr data-project-id="{p["id"]}" data-section="{p["section"]}" data-group="{p["group"]}">'
            f'<td style="font-family:var(--font-mono)">{p["code"]}</td>'
            f'<td style="font-family:var(--font-mono)">{p["year"]}</td>'
            f'<td><a href="{p_url(p["url"])}">{html_lib.escape(p["title"])}</a></td>'
            f'<td>{html_lib.escape(p["category_label"])}</td>'
            f'<td><div class="table-thumb-strip">{thumbs}</div> <span style="font-family:var(--font-mono);font-size:11px">({len(p["photos"])})</span></td>'
            f'<td>{shop_cell}</td>'
            f'</tr>'
        )

    members_rows = "".join(
        f'<tr><td>{html_lib.escape(m["name"])}</td><td><a href="{m["url"]}" target="_blank" rel="noreferrer">{html_lib.escape(m["handle"])} ↗</a></td></tr>'
        for m in team["members"]
    )

    def fmt_multiline(text):
        return html_lib.escape(text).replace("\n", "<br>")

    history_rows_list = []
    for h in team["history"]:
        title_html = fmt_multiline(h["title"])
        if h.get("url"):
            title_html = f'<a href="{html_lib.escape(h["url"])}" target="_blank" rel="noreferrer">{title_html} ↗</a>'
        note_html = f'<div class="chronology-note">{fmt_multiline(h["note"])}</div>' if h.get("note") else ""
        history_rows_list.append(
            f'<tr>'
            f'<td class="chronology-date" style="font-family:var(--font-mono)">{fmt_multiline(h["date"])}</td>'
            f'<td class="chronology-title">{title_html}{note_html}</td>'
            f'<td class="chronology-loc">{fmt_multiline(h["place"])}</td>'
            f'</tr>'
        )
    history_rows = "".join(history_rows_list)

    init_script = f"""<script>
window.ASSET_PREFIX = {json.dumps(prefix)};
window.TAIRYOKU_DATA = {json.dumps(SITE_DATA, ensure_ascii=False)};
window.INITIAL_PROJECT_ID = {json.dumps(initial_project_id)};
window.INITIAL_FILTER = {json.dumps(initial_filter)};
window.INITIAL_SCROLL_TARGET = {json.dumps(initial_scroll)};
</script>"""

    return f"""<!doctype html>
<html lang="ja" data-ink="violet" data-view="wall" data-color="hover" data-size="m" data-filter="{initial_filter}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{html_lib.escape(title)}</title>
  <meta name="description" content="{html_lib.escape(meta_desc)}">
  <link rel="canonical" href="{html_lib.escape(canonical_url)}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="TAIRYOKU (体力)">
  <meta property="og:title" content="{html_lib.escape(title)}">
  <meta property="og:description" content="{html_lib.escape(meta_desc)}">
  <meta property="og:url" content="{html_lib.escape(canonical_url)}">
  <meta property="og:image" content="{html_lib.escape(og_image_url)}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html_lib.escape(title)}">
  <meta name="twitter:description" content="{html_lib.escape(meta_desc)}">
  <meta name="twitter:image" content="{html_lib.escape(og_image_url)}">
  <link rel="icon" href="{p_url('/favicon.svg')}">
  <link rel="stylesheet" href="{p_url('/styles.css')}?v=10">
</head>
<body>
{build_svg_filter()}

<!-- RAW HTML TOP HEADER -->
<header class="raw-header">
  <div class="raw-bar">
    <div class="brand-cluster">
      <a class="brand-link" href="{p_url('/index.html')}" data-filter-btn="all">
        <img class="brand-logo-mini" src="{p_url('/assets/tairyoku-logo.png')}" alt="" width="18" height="18">
        <span>TAIRYOKU (体力)</span>
      </a>
      <span class="raw-meta">Fukuoka, JP [{team["coords"]}]</span>
    </div>

    <nav class="raw-nav" aria-label="Primary navigation">
      <a href="{p_url('/index.html')}" data-filter-btn="all" aria-pressed="true">all ({len(ALL_TILES)})</a>
      <span class="raw-sep">/</span>
      <a href="{p_url('/works.html')}" data-filter-btn="works">works (13)</a>
      <span class="raw-sep">/</span>
      <a href="{p_url('/exhibitions.html')}" data-filter-btn="exhibitions">exhibitions (5)</a>
      <span class="raw-sep">/</span>
      <button type="button" class="raw-btn" id="toggle-dir-btn" aria-pressed="false" aria-controls="raw-directory">index (18) [+]</button>
      <span class="raw-sep">/</span>
      <a href="#about-section">about &amp; creators</a>
      <span class="raw-sep">/</span>
      <a href="#contact-section">contact</a>
      <span class="raw-sep">/</span>
      <a href="{team["shop"]}" target="_blank" rel="noreferrer">shop ↗</a>
      <span class="raw-sep">/</span>
      <a href="{team["instagram"]}" target="_blank" rel="noreferrer">ig ↗</a>
    </nav>
  </div>

  <!-- RAW HTML ARCHIVE CONTROLS -->
  <div class="raw-controls" role="toolbar" aria-label="Archive display controls">
    <div class="ctrl-group">
      <span class="ctrl-label">view:</span>
      <button type="button" class="raw-btn" data-set-view="wall" aria-pressed="true">[wall]</button>
      <button type="button" class="raw-btn" data-set-view="drift" aria-pressed="false">[kinetic-drift]</button>
      <button type="button" class="raw-btn" data-set-view="scatter" aria-pressed="false">[scatter-desk]</button>
      <button type="button" class="raw-btn" data-set-view="table" aria-pressed="false">[html-table]</button>
      <button type="button" class="raw-btn" id="shuffle-wall-btn" title="Shuffle wall tiles">[shuffle ↻]</button>
    </div>

    <div class="ctrl-group">
      <span class="ctrl-label">category:</span>
      <button type="button" class="raw-btn" data-filter-btn="all" aria-pressed="true">all</button>
      <button type="button" class="raw-btn" data-filter-btn="zine" aria-pressed="false">zine</button>
      <button type="button" class="raw-btn" data-filter-btn="apparel" aria-pressed="false">clothing/bag</button>
      <button type="button" class="raw-btn" data-filter-btn="exhibition" aria-pressed="false">exhibition</button>
      <button type="button" class="raw-btn" data-filter-btn="commission" aria-pressed="false">cd</button>
    </div>

    <div class="ctrl-group">
      <span class="ctrl-label">color:</span>
      <button type="button" class="raw-btn" data-set-color="hover" aria-pressed="true">mono→hover-color</button>
      <button type="button" class="raw-btn" data-set-color="color" aria-pressed="false">all-color</button>
    </div>

    <div class="ctrl-group">
      <span class="ctrl-label">ink:</span>
      <button type="button" class="raw-btn" data-set-ink="violet" aria-pressed="true">violet</button>
      <button type="button" class="raw-btn" data-set-ink="ultramarine" aria-pressed="false">ultramarine</button>
      <button type="button" class="raw-btn" data-set-ink="purple" aria-pressed="false">purple</button>
      <button type="button" class="raw-btn" data-set-ink="night" aria-pressed="false">invert</button>
    </div>

    <div class="ctrl-group">
      <span class="ctrl-label">grid:</span>
      <button type="button" class="raw-btn" data-set-size="s" aria-pressed="false">S</button>
      <button type="button" class="raw-btn" data-set-size="m" aria-pressed="true">M</button>
      <button type="button" class="raw-btn" data-set-size="l" aria-pressed="false">L</button>
    </div>
  </div>

  <!-- COLLAPSIBLE RAW HTML INDEX LIST -->
  <section class="raw-directory" id="raw-directory" hidden aria-label="Index of works and exhibitions">
    <div class="directory-columns">
      {" ".join(dir_items_html)}
    </div>
  </section>
</header>

<!-- MAIN ARCHIVE STAGE -->
<main id="main" class="stage-wrap">
  <!-- MODE 1: WALL-TO-WALL TILED CONTACT SHEET -->
  <section class="wall-grid" id="wall-grid" aria-label="Tiled artwork wall">
    {"".join(wall_tiles_html)}
  </section>

  <!-- MODE 2: KINETIC DRIFT CONVEYOR -->
  <section class="drift-stage" id="drift-stage" aria-label="Kinetic drifting wall"></section>

  <!-- MODE 3: INTERACTIVE SCATTER STUDIO TABLE -->
  <section class="scatter-stage" id="scatter-stage" aria-label="Draggable studio table">
    <div class="scatter-toolbar">
      <span>DRAG &amp; THROW IMAGES / CLICK TO INSPECT</span>
      <button type="button" class="raw-btn" id="rescatter-btn">[re-scatter ↻]</button>
    </div>
  </section>

  <!-- MODE 4: PURE RAW HTML TABLE DIRECTORY -->
  <section class="table-stage" id="table-stage" aria-label="Raw HTML archive table">
    <table class="raw-table">
      <thead>
        <tr>
          <th>No.</th>
          <th>Year</th>
          <th>Title</th>
          <th>Category / Format</th>
          <th>Contact Preview</th>
          <th>Shop</th>
        </tr>
      </thead>
      <tbody>
        {"".join(table_rows_html)}
      </tbody>
    </table>
  </section>

  <!-- ABOUT & CREATORS SECTION (RAW HTML EDITORIAL) -->
  <section class="raw-section" id="about-section">
    <div class="raw-section-inner">
      <h1 class="raw-h1">ABOUT / CREATORS — TAIRYOKU (体力)</h1>
      <p class="raw-lead">{html_lib.escape(team["lead_en"])}</p>
      <p class="raw-p">{html_lib.escape(team["body_en"])}</p>
      <p class="raw-p" lang="ja">{html_lib.escape(team["body_jp"])}</p>

      <div class="raw-grid-2">
        <div>
          <p style="font-family:var(--font-mono);font-size:11px;margin:0 0 6px;">CREATORS / MEMBERS:</p>
          <table class="raw-table">
            <thead>
              <tr><th>Name</th><th>Instagram</th></tr>
            </thead>
            <tbody>{members_rows}</tbody>
          </table>

          <div class="stamp-zone" id="stamp-trigger" role="button" tabindex="0" title="Click to stamp TAIRYOKU mark">
            <img src="{p_url('/assets/tairyoku-logo.png')}" alt="TAIRYOKU mark">
            <span>[click to stamp TAIRYOKU mark ✦]</span>
          </div>
        </div>

        <div class="chronology-col">
          <div class="chronology-head">
            <p class="chronology-label">EXHIBITIONS &amp; CHRONOLOGY (2024—NOW):</p>
            <button type="button" class="raw-btn" id="chronology-toggle-btn" hidden aria-expanded="false">[expand all ({len(team["history"])}) ↕]</button>
          </div>
          <div class="chronology-scroll" id="chronology-scroll">
            <table class="raw-table chronology-table">
              <colgroup>
                <col class="chronology-col-date">
                <col class="chronology-col-title">
                <col class="chronology-col-loc">
              </colgroup>
              <thead>
                <tr><th>Date</th><th>Event / Work</th><th>Location</th></tr>
              </thead>
              <tbody>{history_rows}</tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- CONTACT SECTION (RAW HTML) -->
  <section class="raw-section" id="contact-section">
    <div class="raw-section-inner contact-split">
      <div class="contact-info-col">
        <h2 class="raw-h1">CONTACT / LINKS</h2>
        <p class="raw-p">For exhibitions, collaborations and commissions.<br>展示、コラボレーション、制作のご相談はメールまたはInstagramのDMで受け付けています。</p>
        <table class="raw-table contact-table">
          <tbody>
            <tr>
              <th>EMAIL</th>
              <td><a href="mailto:{team["email"]}">{team["email"]} ↗</a></td>
            </tr>
            <tr>
              <th>INSTAGRAM</th>
              <td><a href="{team["instagram"]}" target="_blank" rel="noreferrer">{team["instagram_handle"]} ↗</a></td>
            </tr>
            <tr>
              <th>ONLINE SHOP</th>
              <td><a href="{team["shop"]}" target="_blank" rel="noreferrer">TAIRYOKU BASE SHOP ↗</a></td>
            </tr>
          </tbody>
        </table>
      </div>

      <figure class="contact-video-frame">
        <video class="contact-video" src="{p_url('/assets/contact-motion.mp4')}" autoplay loop muted playsinline preload="metadata" width="720" height="900"></video>
      </figure>
    </div>
  </section>
</main>

<!-- PROJECT DETAIL OVERLAY SHEET -->
<aside class="detail-sheet" id="detail-sheet" hidden aria-label="Project details">
  <div class="detail-topbar">
    <div>
      <button type="button" class="raw-btn" id="detail-close-btn">[← close / back to wall (ESC)]</button>
      <span class="raw-sep">|</span>
      <span id="detail-code">INDEX #01</span>
    </div>
    <div>
      <button type="button" class="raw-btn" id="detail-tone-btn">[toggle duotone/color]</button>
      <span class="raw-sep">|</span>
      <button type="button" class="raw-btn" id="detail-prev-btn">← prev</button>
      <button type="button" class="raw-btn" id="detail-next-btn">next →</button>
    </div>
  </div>
  <div class="detail-body">
    <div class="detail-meta-col">
      <h2 class="detail-title" id="detail-title"></h2>
      <table class="raw-table">
        <tbody id="detail-specs-body"></tbody>
      </table>
      <div class="detail-desc" id="detail-desc"></div>
      <div id="detail-shop-wrap"></div>
    </div>
    <div class="detail-images-col" id="detail-images-col"></div>
  </div>
</aside>

<!-- FLOATING CURSOR TAG -->
<div class="cursor-tag" id="cursor-tag" aria-hidden="true"></div>

<!-- BOTTOM KINETIC STATUS TICKER -->
<footer class="raw-footer">
  <div class="raw-marquee" aria-hidden="true">
    <div class="raw-marquee-track">
      <span>TAIRYOKU (体力) — FUKUOKA CREATIVE TEAM — DRAWING / GRAPHIC DESIGN / ZINE / CLOTHING / EXHIBITION — HOVER WALL TO WAKE COLOR — </span>
      <span>TAIRYOKU (体力) — FUKUOKA CREATIVE TEAM — DRAWING / GRAPHIC DESIGN / ZINE / CLOTHING / EXHIBITION — HOVER WALL TO WAKE COLOR — </span>
    </div>
  </div>
  <div class="footer-status" id="status-readout">18 PROJECTS / 83 FRAMES READY [SINGLE-INK WALL]</div>
</footer>

{init_script}
<script src="{p_url('/app.js')}?v=10"></script></script>
</body>
</html>
"""

def main():
    with open(os.path.join(ROOT_DIR, "styles.css"), "w", encoding="utf-8") as f:
        f.write(STYLES_CSS)
    with open(os.path.join(ROOT_DIR, "app.js"), "w", encoding="utf-8") as f:
        f.write(APP_JS)

    sitemap_paths = ["/"]
    with open(os.path.join(ROOT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_page_html(prefix=".", canonical_path="/"))

    section_pages = [
        ("works.html", "Works — TAIRYOKU", None, "works", None),
        ("exhibitions.html", "Exhibitions — TAIRYOKU", None, "exhibitions", None),
        ("about.html", "About — TAIRYOKU", None, "all", "about-section"),
        ("creators.html", "Creators — TAIRYOKU", None, "all", "about-section"),
        ("contact.html", "Contact — TAIRYOKU", None, "all", "contact-section"),
    ]
    for filename, title, pid, flt, scroll_id in section_pages:
        clean_path = "/" + filename[:-5]
        sitemap_paths.append(clean_path)
        with open(os.path.join(ROOT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_page_html(
                title=title,
                initial_project_id=pid,
                initial_filter=flt,
                initial_scroll=scroll_id,
                prefix=".",
                canonical_path=clean_path,
            ))

    for p in SITE_DATA["projects"]:
        rel_path = p["url"].lstrip("/")
        clean_path = p["url"][:-5] if p["url"].endswith(".html") else p["url"]
        sitemap_paths.append(clean_path)
        og_img = p["photos"][0]["src"] if p["photos"] else "/assets/tairyoku-logo.png"
        desc_text = p["description"][0] if p["description"] else f"{p['title']} — {p['category_label']} ({p['year']}) / TAIRYOKU (体力)"
        full_path = os.path.join(ROOT_DIR, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(render_page_html(
                title=f"{p['title']} — TAIRYOKU",
                initial_project_id=p["id"],
                initial_filter="all",
                prefix="..",
                canonical_path=clean_path,
                og_image=og_img,
                description=desc_text,
            ))

    robots_txt = f"User-agent: *\nAllow: /\n\nSitemap: {SITE_ORIGIN}/sitemap.xml\n"
    with open(os.path.join(ROOT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_txt)

    url_entries = "\n".join(
        f"  <url><loc>{html_lib.escape(SITE_ORIGIN + path)}</loc></url>"
        for path in sitemap_paths
    )
    sitemap_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{url_entries}\n"
        "</urlset>\n"
    )
    with open(os.path.join(ROOT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_xml)

    print("Successfully built relative-path compatible TAIRYOKU site.")

if __name__ == "__main__":
    main()
