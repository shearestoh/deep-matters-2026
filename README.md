# Deep Matters 2026: Agents for Science

Website for the Deep Matters 2026 conference — Thursday 26 November 2026, Institute of Physics, London.
Previous edition: [Deep Matters: Foundations 2025](https://tldr-group.github.io/deep-matters/).

```
site/                  published as-is to GitHub Pages
  index.html           page structure
  css/style.css        styling
  js/main.js           renders the page from content.json
  data/content.json    ALL event content — the only file you normally edit
  images/              logo, favicon, link-preview card, people/, logos/
assets/people/         original photos (not published)
tools/make_images.py   photo resizing, link-preview card, speaker share cards
```

## Preview locally

```bash
python3 -m http.server -d site 8000   # then open http://localhost:8000
```

Opening `index.html` directly from disk won't work, because the page loads `data/content.json`.

## Editing content (`site/data/content.json`)

- **Event details**: `event` and `venue`. `event.registerUrl` is the Luma page, and `event.lumaEventId`
  (from Luma's "Embed" code) opens Luma's checkout as a pop-up on the site instead of a new tab. Clear
  `registerUrl` and the register buttons go back to "Registration opens soon".
- **People**: add speakers and organizers to `people`, keyed by an id such as `"jane-doe"`. Fields are
  `name`, `affiliation`, and optionally `role`, `photo`, `logo` (institution logo shown on the card),
  `linkedin` and `website`. The whole card links to LinkedIn, or to the website if there's no LinkedIn.
  Anyone without a photo gets an initials avatar.
- **Agenda**: set `agenda.start`, then list `items` in order. Times are calculated automatically from
  `minutes` (talks default to `talkMinutes`). To fill in a talk:

  ```json
  { "type": "talk", "title": "…", "speakers": ["jane-doe"], "abstract": "…" }
  ```

  Speakers appear in the Speakers section automatically, in agenda order. Until the programme is final,
  use talk blocks for unconfirmed periods, e.g. `{ "type": "block", "title": "Morning talks", "minutes": 120,
  "description": "Speakers to be announced soon." }`: they show one time range without individual slots, and
  the Speakers section adds a single "More speakers to be announced soon" card. As speakers are confirmed,
  shrink the block's `minutes` and add their `talk` items.
- **Logos**: `partners` is a list of labelled groups (Host, Venue, Sponsors), each with `orgs`. Logos are sized automatically to look equally weighted. Crop each file
  tightly with no padding, and use the optional `scale` (e.g. `1.2`) to fine-tune one logo.
- **FAQ**: `faq` list of `{ "q", "a" }`.
- **Gallery**: `gallery.title` plus `gallery.photos` (`src`, `alt`), shown as a continuously scrolling strip. Remove `gallery` to hide the section.

## Images

```bash
pip install pillow
cp ~/Downloads/jane.jpg assets/people/jane-doe.jpg   # file name = person id
python3 tools/make_images.py                         # all steps, or: photos | gallery | og | cards
```

- `photos`: crops and resizes everything in `assets/people/` into `site/images/people/<id>.jpg`.
  Set `"photo": "images/people/<id>.jpg"` for that person.
- `gallery`: resizes the full-size photos in `assets/gallery/` into `site/images/gallery/` (960×640).
  The originals are git-ignored because they're about 6MB each.
- `og`: regenerates `site/images/og-card.png`, the image shown when the link is shared. Run it if the
  title, date or venue changes.
- `cards`: makes LinkedIn announcement images for each speaker in `share/` (not committed).

## Deploying

Every push to `main` deploys `site/` through `.github/workflows/pages.yml`. One-time setup: repo
**Settings → Pages → Source: GitHub Actions**.

### Moving to tldr-group

1. Transfer the repo (**Settings → Transfer ownership**), or push it to a new `tldr-group/deep-matters-2026` repo.
2. Ask an org admin to enable Pages (Source: GitHub Actions).
3. In `site/index.html`, change the two absolute URLs in the link-preview tags (`og:url`, `og:image`) to
   `https://tldr-group.github.io/deep-matters-2026/`. Everything else uses relative paths.
