# EL-ROI Shipping Services — website

Static website for EL-ROI Shipping Services (Essen, Germany → Lagos, Nigeria & worldwide).
Design: marine navy, brass gold, steel blue and ivory, set in Fraunces and Inter.
Plain HTML, CSS and JavaScript. There is no build step, so any static host works (Netlify, GitHub Pages, cPanel…).

## Pages

| File | Page |
| --- | --- |
| `index.html` | Home |
| `services.html` | Services |
| `routes.html` | Routes (route table + route map) |
| `gallery.html` | Photo gallery with filters and lightbox |
| `about.html` | About |
| `blog.html` | Shipping guides & news |
| `guide-*.html` | SEO guides: car to Nigeria, Form M, 20ft vs 40ft containers, what to prepare |
| `faq.html` | FAQ |
| `contact.html` | Contact (form, offices, map) |
| `quote.html` | Quote request form (pre-fills from the calculator) |
| `book.html` | Booking form |
| `calculator.html` | Rough cost calculator |
| `privacy.html` | Privacy policy (GDPR), linked in every footer and under each form |
| `terms.html` | Terms & conditions, linked in every footer and under the quote and booking forms |
| `404.html` | Not-found page |

Shared styles live in `assets/style.css`, interactions in `assets/script.js`, photos in `assets/img/`.
The header and footer are repeated in every page, so a change to either needs making in each file.

## Home page hero

- **3D globe** (`assets/globe.js` + `assets/globe-land.js`): a dependency-free canvas globe showing
  the routes from Essen. Visitors can drag it to spin. Routes and colours are at the top of `globe.js`.
- **Live truck background**: the hero photo drifts slowly and shifts with scroll. To use a real video
  instead, add a short muted MP4 (for example `assets/video/hero.mp4`, ideally under 8 MB) and set
  `data-video="assets/video/hero.mp4"` on the `.hero-media` element in `index.html`. The photo stays as
  the fallback while the video loads, and for visitors with reduced motion or data saver turned on.

- **Scroll journey** ("How it works" on the home page): the section pins while you scroll over a real world
  chart. It starts close on Europe (Essen, and the major routes to Belgium, Holland and Austria), a truck drives to
  the port, then the camera pulls back and container ships sail real sea lanes to the Americas, South America,
  Lagos, Southern Africa, the Middle East and Asia. Lanes and labels live at the top of the journey code in
  `assets/script.js`; the land outline is Natural Earth 1:50m (public domain).
- **Scroll animations**: sections fade and slide in as they enter and fade out as they leave, photos wipe open,
  headings reveal word by word (and replay when you scroll back), and the hero drifts away as you scroll.
  Browsers with CSS scroll-driven animations get scroll-linked motion; others (for example Firefox) get the same
  effect triggered on entry/exit. Forms and the calculator only fade in. Everything is off with reduced motion.
- **Scroll progress bar**: the thin gold line at the top of every page.

## SEO

- Every page has a keyword title and description, a canonical link, Open Graph tags and structured data
  (LocalBusiness on Home/About/Contact, BreadcrumbList on inner pages, FAQPage on the FAQ and guides, Article on guides).
- `sitemap.xml` and `robots.txt` are generated at the site root.
- **Moving to the custom domain:** all absolute URLs come from one address (`https://phoenix297.github.io/Elroi/`).
  When the domain is live, replace that address everywhere (canonical, `og:url`, `og:image`, structured data,
  `sitemap.xml`, `robots.txt`), add a `CNAME` file containing the domain, then submit `sitemap.xml` in Google Search Console.
- After launch: create a Google Business Profile for the Essen address, and ask happy customers for Google reviews.

## Fonts and link previews

- Fonts (Fraunces and Inter, SIL Open Font License) are self-hosted in `assets/fonts/` via `assets/fonts.css`.
  Nothing is loaded from Google Fonts, which matters for GDPR in Germany.
- `assets/og-image.jpg` (1200x630) is the preview shown when a page link is shared on WhatsApp, Facebook, LinkedIn etc.
  The `og:` tags use `https://phoenix297.github.io/Elroi/`. When the site moves to its own domain, update the address in
  every page's `og:url` and `og:image` tags.

## Adding photos

1. Put the image in `assets/img/` (JPG, ideally no wider than 1600px).
2. In `gallery.html`, copy one `<figure>` block inside `<div class="masonry">` and change the
   `href`, `src`, `alt`, `width`/`height`, caption text and `data-cat`
   (`vehicles`, `machinery` or `containers`, and the filter buttons pick it up automatically).

## Forms

The contact, quote and booking forms post to Formspree. Until a real form ID is set, submitting
opens WhatsApp (+49 1521 9521826) with the form details pre-filled, so no enquiry is lost.

To switch to email delivery, create a form at [formspree.io](https://formspree.io) and replace
`YOUR_FORM_ID` in the `action` of the forms in `contact.html`, `quote.html` and `book.html`.

## Placeholders to replace

- **Testimonials** on the home page (`index.html`, section 05) use placeholder names. Swap in real client quotes.
- **Logo**: the gold "ER" monogram in the header, footer and `assets/favicon.svg` is a placeholder until the real logo file is ready.

## Photos and privacy

Licence plates, trailer ID numbers and visible faces are blurred in `assets/img/`. Blur them in any new photo before adding it.

The privacy policy and terms & conditions are solid starting points, but have a lawyer review both before launch (in particular whether to use the ADSp 2017, the liability limits, quote validity and cancellation charges). German sites also normally need an Impressum (legal notice).

## Calculator

Rates live in `assets/script.js` (`baseRates` per kg and `destMultiplier` per route), with a 50 kg minimum.
Results are rough estimates and the page says so.

## Claude Code skill

`.claude/skills/scroll-world/` is the [scroll-world](https://github.com/oso95/scroll-world) skill (MIT),
kept here so it loads in Claude Code sessions for this repo. It is not part of the website; leave it
out when uploading the site to a host.
