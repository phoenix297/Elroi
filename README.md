# EL-ROI Shipping Services — website

Static website for EL-ROI Shipping Services (Essen, Germany → Lagos, Nigeria & worldwide).
Plain HTML, CSS and JavaScript. There is no build step, so any static host works (Netlify, GitHub Pages, cPanel…).

## Pages

| File | Page |
| --- | --- |
| `index.html` | Home |
| `services.html` | Services |
| `routes.html` | Routes (departure board + route map) |
| `gallery.html` | Photo gallery with filters and lightbox |
| `about.html` | About |
| `blog.html` | News |
| `faq.html` | FAQ |
| `contact.html` | Contact |
| `quote.html` | Quote request form (pre-fills from the calculator) |
| `book.html` | Booking form |
| `calculator.html` | Rough cost calculator |
| `404.html` | Not-found page |

Shared styles live in `assets/style.css`, interactions in `assets/script.js`, photos in `assets/img/`.
The header and footer are repeated in every page, so a change to either needs making in each file.

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

## Calculator

Rates live in `assets/script.js` (`baseRates` per kg and `destMultiplier` per route), with a 50 kg minimum.
Results are rough estimates and the page says so.
