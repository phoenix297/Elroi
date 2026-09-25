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
| `blog.html` | News |
| `faq.html` | FAQ |
| `contact.html` | Contact (form, offices, map) |
| `quote.html` | Quote request form (pre-fills from the calculator) |
| `book.html` | Booking form |
| `calculator.html` | Rough cost calculator |
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

## Calculator

Rates live in `assets/script.js` (`baseRates` per kg and `destMultiplier` per route), with a 50 kg minimum.
Results are rough estimates and the page says so.

## Claude Code skill

`.claude/skills/scroll-world/` is the [scroll-world](https://github.com/oso95/scroll-world) skill (MIT),
kept here so it loads in Claude Code sessions for this repo. It is not part of the website; leave it
out when uploading the site to a host.
