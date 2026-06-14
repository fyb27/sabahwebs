# SabahWebs — Design & Build Handoff

A complete record of the design language, principles, and techniques used to build this site.
Live: **https://sabahwebs.com** · Repo: **https://github.com/fyb27/sabahwebs**

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
- **Off-screen pause:** an `IntersectionObserver` stops the render loop the moment the hero scrolls
  out of view, and a `visibilitychange` listener pauses it when the tab is hidden — so it costs
  zero main-thread time for the rest of the session (the original loop ran forever).
- **Low-power skip:** on data-saver, 2G/3G, ≤4-core, or ≤4 GB devices it paints a single static
  frame and never animates — keeping mobile/budget phones fast.

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
- **Lightweight by hand:** no page-builder bloat; **zero third-party scripts** (the old Webflow
  Google Analytics, reCAPTCHA and WebFont loader were removed site-wide — see §11).
- **Non-render-blocking fonts:** Google Fonts load via the `media="print"`/`onload` swap with a
  `<noscript>` fallback, so first paint never waits on the font request.
- **Loading hints:** `loading="lazy"` on below-the-fold images, `decoding="async"` and explicit
  `width`/`height` on logos (no layout shift), `preconnect` to the font host.
- **Canvas hero** ships its geometry as inline data — zero extra image requests — and is render-loop
  gated (off-screen pause + low-power skip, see §4).
- **Scores:** mobile PageSpeed went from poor to good after gating the hero loop and unblocking fonts.

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

## 10. SEO

Target keyword: **"web design sabah"** (+ web design Kota Kinabalu, SEO Sabah). The site is a
local-services business, so local intent drives the on-page strategy.

- **Keyword-led homepage:** `<title>` = *Web Design Sabah | Affordable Websites & SEO — SabahWebs*,
  meta description opens with "Web design & SEO in Sabah…", and the H1 is "Web design & SEO, built
  from Sabah". `geo.region` (`MY-12`) + `geo.placename` meta reinforce location.
- **Structured data (JSON-LD):**
  - Homepage: a `@graph` of **`ProfessionalService`** (areaServed Sabah/Malaysia, Kota Kinabalu
    address, email + phone, `makesOffer` for the three pricing tiers) + **`WebSite`**.
  - Every post: **`BlogPosting`** with `headline`, `description`, real `datePublished`/`dateModified`,
    `author`/`publisher` (SabahWebs + logo), and `isPartOf` the WebSite node.
  - Client local-guide posts (the Permai Polyclinics Fortuna pair) also carry an **`about`
    `MedicalClinic`** node (full NAP, `geo`, 24h `openingHours`, `sameAs` → the client's domain +
    Instagram + Facebook), so the article is tied to the client as a recognised entity.
- **Canonical + social on every page:** absolute `rel="canonical"`, full Open Graph + Twitter
  summary-large-image cards, `og:locale en_MY`, `theme-color`, `lang`.
- **`sitemap.xml`** (17 URLs: home + blog hub + 15 posts, all matching their canonicals) and
  **`robots.txt`** pointing to it. Submitted to Google Search Console (Domain property, DNS-verified).
- **URL/slug preservation:** every post kept its exact `blog/<slug>.html` URL through the rebuild and
  domain move, so inbound links and rankings carry over with no redirects needed.
- **Clean copy & contacts:** consistent `hello@sabahwebs.com` + WhatsApp `+60 16-843 0891` site-wide.
- **Client local-guide posts (Permai Polyclinics Fortuna):** two posts double as a service to the
  client — the 24-hour clinic guide and a `knee-injection-kota-kinabalu.html` post targeting
  "knee injection Kota Kinabalu / suntikan lutut". Both carry **followed** links (`rel="noopener"`
  only, no `nofollow`) to the client's own domain **https://permaipolyclinicsfortuna.com/** with
  descriptive anchor text, plus the `MedicalClinic` schema above. They **interlink** (each links the
  other) to share ranking signal. The knee post is the traffic-capture play; the link equity is a
  secondary, one-domain-level benefit. NAP in both matches the client's site exactly.

---

## 11. Blog rebuild & old-mirror removal

The site originally shipped as a **hybrid**: 4 hand-built posts alongside a full mirror of the old
Webflow site (an old `blog/index.html` hub + 10 mirrored posts that pulled CSS/images from
`cdn.prod.website-files.com` and still loaded **old Google Analytics `G-BK1FVF46K5`, reCAPTCHA, a
WebFont loader and Webflow JS**). That has been fully resolved:

- **Lossless rebuild:** each mirrored post's body lived in a single `.w-richtext` container of clean
  semantic tags (h2/h3/h4/p/ul/strong/a) with **no inline images**, so the text was extracted and
  poured into the hand-built dark template — content preserved verbatim, same URLs.
- **All trackers gone:** no Google Analytics, reCAPTCHA, WebFont loader or Webflow CSS/JS anywhere on
  the site now; every page is self-contained on `css/styles.css` + `js/main.js`.
- **Mirror deleted:** the old `blog/index.html` hub, `mirror.py`, the orphaned `blog/dark-theme.css`,
  and all mirror directories (`cdn.prod.website-files.com`, `ajax.googleapis.com`, `www.google.com`,
  `www.googletagmanager.com`, `analytics.ahrefs.com`, cloudfront, first-party GA dir) were removed
  (~3.5k lines). The blog is now one consistent, fully owned set of posts (15 as of this writing).

---

## 12. Tooling & deployment

- **Stack:** hand-written semantic HTML, a single CSS file driven by tokens, vanilla JS (no framework).
- **Fonts:** Google Fonts (Inter + JetBrains Mono), `preconnect` + non-render-blocking load (§8).
- **Version control:** Git, hosted on GitHub (repo `fyb27/sabahwebs`).
- **Hosting:** GitHub Pages, auto-deploys on every push to `main` (rebuild in ~1–2 min).
- **Custom domain:** **sabahwebs.com** via a `CNAME` file in the repo. GoDaddy DNS points the apex
  to the four GitHub Pages A-records (`185.199.108–111.153`) and `www` → `fyb27.github.io` (301 → apex).
  HTTPS enforced (GitHub-provisioned cert). The domain was released from the old `sabahwebs-exact`
  repo first so this repo could claim it. Serving at the domain root (no `/sabahwebs/` subpath).
- **Favicon set** generated from the Mount Kinabalu peak (ICO + multiple PNG sizes + Apple touch icon).

---

## 13. File map

```
index.html              Landing page (hero, clients index, why-us, about, pricing, contact)
blog.html               Blog list (simple, text-led)
blog/<slug>.html        15 posts, all hand-built on the dark template (same URLs throughout)
css/styles.css          The whole design system + components + responsive
js/main.js              Header state, parallax, scroll reveal, mobile nav, client hover preview
js/hero-mountk.js       Canvas dot-matrix Mount Kinabalu hero (off-screen + low-power gated)
assets/                 Favicons, OG image, client screenshots, (legacy) hero image set
CNAME                   Custom domain (sabahwebs.com) for GitHub Pages
robots.txt              Allow-all + sitemap pointer
sitemap.xml             17 URLs (home + blog hub + 15 posts)
```

---

*Built for SabahWebs — websites & SEO from Sabah.*
