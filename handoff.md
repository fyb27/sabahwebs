# SabahWebs — Design & Build Handoff

A complete record of the design language, principles, and techniques used to build this site.
Live: **https://fyb27.github.io/sabahwebs/** · Repo: **https://github.com/fyb27/sabahwebs**

---

## 1. Design philosophy

The whole site follows one idea borrowed from the `DESIGN.md` reference (a Hyperstudio-style
"designer's midnight gallery"): **typography carries the weight, colour is rationed, depth comes
from greys not shadows.** It reads top-to-bottom like a printed manifesto rather than a busy
landing page.

Guiding principles applied throughout:

- **Restraint over decoration.** One accent colour, one filled button per screen, no gradients-as-ornament.
- **Hierarchy through type, not boxes.** Size, weight and spacing do the work before any container does.
- **Flat, architectural surfaces.** Separation comes from a 4-step grey stack + 1px hairlines, never drop shadows.
- **Whitespace is a feature.** Generous 120px section rhythm; content is allowed to breathe.
- **Progressive enhancement.** It reads fine with no JS; motion and interaction are layered on top.
- **Honest performance.** Hand-built, lightweight, modern image formats — fast on mobile data.

---

## 2. Design tokens (the system)

Everything is driven by CSS custom properties in `:root` (see `css/styles.css`) so the look is
consistent and changeable from one place.

### Colour
| Role | Value |
|------|-------|
| Canvas (page background) | `#101010` |
| Void (deepest / hero canvas) | `#080808` |
| Surface (cards) | `#212121` |
| Elevated | `#333333` |
| Primary text (frost) | `#f3f3f3` (off-white, softer than pure white) |
| Secondary / muted text | `#949494` / `#bdbdbd` |
| Tertiary (labels, meta) | `#888888` |
| **Amber Whisper (sole accent)** | `#e7c59a` |

- **Accent economy:** the amber appears at most once per viewport — the word "Sabah" in the hero,
  the featured pricing tier, the active client row, hover states. Never as filler.
- **Warm black:** canvas is `#101010`, not pure `#000`, so the dark feels warm, not digital.

### Typography
- **Display / UI:** Inter (a stand-in for Aeonik) at **400 and 700 only**.
- **Labels / meta / numbers:** JetBrains Mono (stand-in for Input) — used *only* for micro-labels,
  timestamps, categories, technical text.
- **Whisper-weight headlines:** big headings are weight **400**, not bold — the signature move.
  700 is reserved for small uppercase "stencil" labels (OUR CLIENTS, WHY CHOOSE US…).
- **Negative tracking everywhere:** letter-spacing is always negative (≈ −0.011em on Inter,
  tighter on the mono face). No `0` or positive tracking.
- **Fluid type:** key headings use `clamp()` so they scale smoothly between mobile and desktop.
- A defined type scale (caption 13 → display 63px) keeps sizes intentional, not arbitrary.

### Spacing, shape & layout
- 4px base spacing scale.
- **Three corner radii, used semantically:** 8px (buttons/badges), 20px (cards), 99px (pill CTAs).
- Page container: `max-width 1560px`, 48px side padding (20px on mobile), centred.
- Section rhythm: 120px vertical gaps (80px on mobile).

### Elevation
- **No drop shadows for structure.** Depth = the grey surface stack (`#080808 → #101010 → #212121 → #333333`)
  plus 1px `#212121` hairline borders. (One soft shadow is used only on the floating hover preview,
  because it genuinely floats above the page.)

---

## 3. Layout & composition techniques

- **Centred, symmetrical, vertical rhythm** — the page is read like a column.
- **Hairline grids, not card grids.** The "Why choose us" 2×2 shares 1px borders between cells
  rather than sitting as separate floating cards.
- **Full-bleed hero vs contained content.** The hero spans the whole viewport; the header and
  sections align to the wide 1560px container so they feel connected to it.
- **Readable measure for long-form.** Blog article bodies are deliberately kept to ~720px wide for
  comfortable reading, even though the rest of the site is wide.
- **Editorial index pattern** for the client list (see §6).

---

## 4. The hero (signature piece)

- **Canvas-rendered dot-matrix Mount Kinabalu** (`js/hero-mountk.js`) — a point cloud drawn as
  shimmering diamonds, decoded from embedded data (no external image request).
- **Parallax depth:** on scroll the mountain layer translates slower than the page, and the copy
  lifts and fades — communicating depth without a literal image.
- **Composition:** headline/CTAs anchored to the upper band, the mountain rising from the bottom,
  so type and art never fight for the same space.
- **Legibility overlay:** a top-down gradient darkens only the upper band behind the headline, so
  text stays readable while the mountain shows through clean below.
- **Mouse interaction:** points gently push away from the cursor — a subtle "alive" detail.
- **Reduced-motion aware:** the shimmer/animation is disabled for users who prefer no motion
  (the mountain still renders, just still).

---

## 5. Motion & micro-interactions

Motion is purposeful, fast, and consistent — never bouncy or gratuitous.

- **Shared easing:** a custom `cubic-bezier(.2,.7,.3,1)` ("ease-out-ish") is used across the site
  so everything feels like one hand.
- **Scroll reveal:** elements fade + rise into place via `IntersectionObserver`, with **staggered
  delays** (`data-delay`) so groups cascade rather than pop all at once. Observer unobserves after
  firing (no wasted work).
- **Hover micro-interactions:**
  - nav links: an amber underline grows from the left.
  - buttons: a 2px lift, arrow icons slide right, the primary button warms to amber.
  - client rows: padding shifts right, name/number turn amber, siblings dim.
  - cards: subtle border lighten + image scale.
- **Status pulse:** the availability/green dot pattern uses a soft expanding ring.
- **Sticky header:** transparent over the hero, then blurs + gains a hairline once you scroll
  (`.scrolled` state).
- **Performance:** transforms/opacity only (GPU-friendly), `will-change` where it counts, scroll
  work throttled with `requestAnimationFrame`.
- **`prefers-reduced-motion`:** globally honoured — all animation/transition is cut for those users.

---

## 6. Client section — editorial hover index

A deliberately "studio-grade" pattern instead of a screenshot grid:

- Clients are a **numbered typographic list** (01–05) with big names + mono category labels,
  separated by hairlines.
- **Hover:** non-hovered rows dim (focus), the active row's name + number go amber, and a **live
  screenshot of that client's site floats in following the cursor**.
- Preview position is **clamped** so it never runs off-screen.
- **Touch/mobile fallback:** no cursor → it becomes clean stacked rows with the screenshot shown
  inline, so the visuals are never lost. Driven by `@media (hover: none)` + width breakpoints.

---

## 7. Components

- **Buttons:** exactly one white filled CTA per view (highest emphasis), outlined secondary
  buttons, and a 99px pill for the conversational "Let's chat".
- **Pricing cards:** flat surfaces; the recommended tier is distinguished by an amber border +
  faint amber wash (the single accent), not by size or shadow.
- **Blog:** kept as a simple text list (no picture cards) on its own page; individual articles use
  a clean long-form prose template.

---

## 8. Performance techniques

- **Modern image formats with fallback:** responsive `<picture>` serving **AVIF → WebP → JPEG**,
  at multiple widths via `srcset`, so the browser picks the smallest it supports for the screen.
- **Sharpening pipeline:** the source mountain image was upscaled + unsharp-masked for crisp
  wireframe lines before export.
- **Lightweight by hand:** no page-builder bloat; minimal third-party scripts.
- **Loading hints:** `fetchpriority="high"` on the hero, `loading="lazy"` on below-the-fold images,
  `decoding="async"`, and `preconnect` to the font host.
- **Canvas hero** ships its geometry as inline data — zero extra image requests for the hero visual.

---

## 9. Responsive & accessibility

- **Breakpoints:** ~1100px (grid reflow) and 860px (mobile). Fluid `clamp()` type in between.
- **Mobile nav:** hamburger toggle with an accessible `aria-expanded` state; links close the menu.
- **Touch handling:** `@media (hover: none)` swaps hover-only interactions for tap-friendly ones.
- **Semantics:** one `<h1>` per page, real `<header>/<section>/<footer>` landmarks, `<article>`
  for posts, meaningful heading order.
- **Labels & alt text:** `aria-label` on icon links, `aria-hidden` on decorative SVGs/canvas,
  descriptive `alt` on every content image.
- **Contrast:** off-white on warm-black sits comfortably above WCAG body-text thresholds.
- **Reduced motion** respected site-wide.

---

## 10. SEO & content integrity

- **URL/slug preservation:** the inherited blog posts keep their exact `blog/<slug>.html` URLs, so
  existing inbound links and rankings are not lost.
- **Canonical content untouched:** original post titles, meta descriptions, headings, structured
  content and images are preserved byte-for-byte; only the *theme* (colours) was overlaid.
- **Self-contained:** the live posts + their assets were mirrored into the repo so the whole site
  deploys as one unit.
- **Per-page metadata:** unique `<title>` + `meta description`, Open Graph tags, `theme-color`,
  `lang`, and an OG share image generated from the brand mark.
- **Clean copy:** em-dashes removed site-wide per brand voice; consistent contact details
  (`hello@sabahwebs.com`).

---

## 11. Inheriting the old (Webflow) blog cleanly

- **Dark-theme overlay** (`blog/dark-theme.css`): a scoped override that flips the old light Webflow
  palette to the SabahWebs dark canvas **without editing the original markup** — done by targeting
  structural classes and being careful about variables used in two roles (so the footer didn't break).
- **One-file logo swap:** every inherited post referenced a single logo image, so replacing that one
  file updated the nav + footer logo across all posts at once (new transparent mountain mark).
- **Subpath-safe paths:** root-absolute `/...` links were rewritten to relative paths so everything
  works under the GitHub Pages `/sabahwebs/` subpath.

---

## 12. Tooling & deployment

- **Stack:** hand-written semantic HTML, a single CSS file driven by tokens, vanilla JS (no framework).
- **Fonts:** Google Fonts (Inter + JetBrains Mono) with `preconnect`.
- **Version control:** Git, hosted on GitHub.
- **Hosting:** GitHub Pages, auto-deploys on every push to `main` (rebuild in ~1–2 min).
- **Favicon set** generated from the Mount Kinabalu peak (ICO + multiple PNG sizes + Apple touch icon).

---

## 13. File map

```
index.html              Landing page (hero, clients index, why-us, about, pricing, contact)
blog.html               Blog list (simple, text-led)
blog/<slug>.html        Inherited posts (SEO-preserved) + 4 new studio articles (dark style)
blog/dark-theme.css     Dark overlay for the inherited Webflow posts
css/styles.css          The whole design system + components + responsive
js/main.js              Header state, parallax, scroll reveal, mobile nav, client hover preview
js/hero-mountk.js        Canvas dot-matrix Mount Kinabalu hero
assets/                 Favicons, OG image, client screenshots, (legacy) hero image set
cdn.prod.website-files.com/ …  Mirrored assets for the inherited posts
```

---

*Built for SabahWebs — websites & SEO from Sabah.*
