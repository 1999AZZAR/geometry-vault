# Design System Specification: Swiss-Archival (v1.7.0)
**System Identity:** Glass Gallery Digital Archive  
**Lead Architect:** Mema  
**Philosophy:** Technical Minimalism, Structural Honesty, and Physicality.

---

## 1. Architectural Principles

### 1.1 The Grid as Foundation
The interface is anchored by the **Blueprint Grid**, a visible 1px vertical boundary system (RGBA 191, 182, 166, 0.2). This grid grounds the content within an 80rem (1280px) container, ensuring that every element feels "drafted" onto a technical canvas.

### 1.2 Tactility & Materiality
To counteract digital flatness, the system employs a **Fixed SVG Fractal Noise Filter**.
*   **Implementation:** `feTurbulence` with `fractalNoise` type, `baseFrequency="0.65"`, and `opacity="0.04"`.
*   **Result:** A persistent organic grain that mimics 300gsm matte-printed archival paper.

### 1.3 State-Driven Motion
All animations are functional indicators of system state or navigation intent. To maintain a "liquid" but high-performance feel, the system uses a global **Snappy Motion Ratio of 0.75x**, effectively reducing standard web animation durations by 25%.

---

## 2. Color Language & Semantic Roles

| Token | Hex/RGBA | Semantic Role | Design Intent |
| :--- | :--- | :--- | :--- |
| **Background** | `#E8E0D0` | Primary Canvas | Warm Cream; reduces eye strain and implies age/value. |
| **Foreground** | `#2A2520` | Core Content | Deep Coffee; used for narrative text and primary structure. |
| **Card / Surface** | `#EFE9DC` | Elevation | Soft Pearl; used for interactive entries and sidebars. |
| **Accent** | `#8B1A1A` | Focus & Action | Burgundy; signifies interactive elements and data points. |
| **Muted** | `#DDD5C5` | Inactive/Structural | Earthy Neutral; used for borders, rules, and placeholders. |
| **Muted FG** | `#7A7068` | Meta / Technical | Ash Gray; used for technical labels and metadata. |
| **Selection** | `RGBA(139, 26, 26, 1)`| Interaction | Branded highlighting for all text selections. |

---

## 3. Typographic System

### 3.1 Narrative Layer: Plus Jakarta Sans
*   **Usage:** Headings, Body Content, and Primary Identity.
*   **Headings (700):** Feature tight tracking (`-0.03em`) and tight leading (`1.05`) to simulate traditional hot-press typesetting.
*   **Body (400/500):** Standardized leading (`1.6`) for long-form archival legibility.

### 3.2 Technical Layer: JetBrains Mono
*   **Usage:** Metadata, Navigation, Labels, and UI Controls.
*   **Styling:** Semibold (600), fixed `0.75rem` sizing, technical uppercase, and wide tracking (`0.1em`).
*   **Rationale:** Creates a "Museum Label" aesthetic, distinguishing raw data from narrative content.

---

## 4. Interaction Engine (Keyboard UI)

The system features a **Low-Latency Archival Command Engine**. All shortcuts are automatically disabled within input/textarea contexts.

### 4.1 Global Command Set
| Trigger | Technical Action | Logic Reference |
| :--- | :--- | :--- |
| **`?`** | `openShortcuts()` | Reveals global Command Index overlay. |
| **`CTRL + K`** | `openSearch()` | Focuses the glassmorphic Search Index. |
| **`SHIFT + H`** | `triggerTransition("/")`| Forced return to Archive Index. |
| **`ESC`** | `closeAllOverlays()` | Universal state reset for all modals. |
| **`J` / `K`** | `window.scrollBy()` | Precision 150px smooth vertical movement. |

### 4.2 Navigation Contexts
| Trigger | Action (Index View) | Action (Single View) |
| :--- | :--- | :--- |
| **`[` / `]`** | Prev / Next Page | Prev / Next Archive Entry |
| **`W` / `S`** | Move Entry Focus (Grid) | Move Entry Focus (Sidebar) |
| **`ENTER`** | Open Focused Entry | Open Focused Recommendation |
| **`C`** | N/A | Trigger Citation Specimen Modal |

---

## 5. UI Component Specifications

### 5.1 Contextual Header (Intelligent Identity)
A Grid-Stack component that vertically swaps the Site Identity with a contextual reference on scroll.
*   **Logic:** Detects `winScroll > 400px` to apply the `.scrolled` state.
*   **Single View:** Displays `[ CATEGORIES: NAME ]` with multi-line wrapping and a return-home link.
*   **Index View:** Displays `[ ARCHIVE_TAGLINE: TEXT ]` to reinforce site mission.

### 5.2 Citation Specimen Utility
A high-end archival tool for content referencing.
*   **Formats:** APA, MLA, BibTeX, and TECHNICAL_REF.
*   **Global Feedback:** Integrated with the Toast Notification system for archival confirmation.
*   **Feedback:** Card-level border pulse and technical `[ SUCCESS ]` label update upon data transfer.
*   **UI:** Glassmorphic modal (`backdrop-blur: 12px`) with a technical dark-mode help overlay.

### 5.3 Physical Print Layer
Advanced reformatting for physical preservation.
*   **Media:** `@media print`.
*   **Formatting:** A4 size, 2cm technical margins, removal of all digital UI (nav, buttons, cursor).
*   **Identifiers:** Adds a technical `[ ARCHIVAL_PRINT_SPECIMEN ]` footer to every physical page.

### 5.4 Liquid Navigation & Transitions
A three-stage process to eliminate browser "jank."
*   **Stage 1 (Exit):** Soft dissolve, 4px blur, and 5px upward drift.
*   **Stage 2 (Transition):** Centered technical `[ ACCESSING_ARCHIVE ]` label with 0.8s spinning bracket.
*   **Stage 3 (Reveal):** Robust `pageshow` event handling to clear loading states during back-navigation.

---

## 6. Technical Maintenance & Performance
*   **Media Loading:** All generative shapes (DiceBear API) utilize `loading="lazy"` to optimize initial index retrieval.
*   **Visual Assets:** Generative shapes are strictly color-locked to the brand palette (Burgundy/Coffee/Gray).
*   **Mobile Interface:** The Custom Cursor and all tactile trailing effects are hardware-disabled on touch-start devices.

---
**Version 1.7.0 Final**  
**Document Status: APPROVED**  
**Developed by Mema**
