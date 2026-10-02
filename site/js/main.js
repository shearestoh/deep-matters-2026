// Renders the page from data/content.json. Edit that file, not this one, to change content.

const esc = (s = "") =>
  String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);

const ICONS = {
  linkedin: '<svg viewBox="0 0 24 24" aria-hidden="true"><path class="fill" d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.75h4v11H3v-11zm6.5 0h3.8v1.5h.06c.53-1 1.83-2.05 3.77-2.05 4.03 0 4.77 2.65 4.77 6.1v5.45h-4v-4.83c0-1.15-.02-2.63-1.6-2.63-1.6 0-1.85 1.25-1.85 2.55v4.91h-3.95v-11z"/></svg>',
  website: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>',
  person: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg>',
};

const initials = (name) => {
  const words = name.replace(/^(dr|prof)\.?\s+/i, "").split(/\s+/);
  return (words[0][0] + (words.length > 1 ? words[words.length - 1][0] : "")).toUpperCase();
};

const avatar = (p) =>
  !p ? `<div class="avatar ghost">${ICONS.person}</div>`
  : p.photo ? `<img class="avatar" src="${esc(p.photo)}" alt="" loading="lazy" />`
  : `<div class="avatar" aria-hidden="true">${esc(initials(p.name))}</div>`;

const profileLinks = (p) => {
  const links = [
    p.linkedin && `<a href="${esc(p.linkedin)}" target="_blank" rel="noopener" aria-label="${esc(p.name)} on LinkedIn">${ICONS.linkedin}</a>`,
    p.website && `<a href="${esc(p.website)}" target="_blank" rel="noopener" aria-label="${esc(p.name)}'s website">${ICONS.website}</a>`,
  ].filter(Boolean);
  return links.length ? `<div class="links">${links.join("")}</div>` : "";
};

// Front: photo, name, role and institution (logo if available, else text).
// Hover/tap (or keyboard focus) reveals the short bio with LinkedIn/website buttons.
// domId is set for speaker cards so agenda rows can link to them.
function personCard(p, domId) {
  if (!p) return `<article class="person tba">${avatar()}<h3>To be announced</h3></article>`;
  const links = profileLinks(p);
  const back = p.bio || links ? `<div class="person-back">${p.bio ? `<p>${esc(p.bio)}</p>` : ""}${links}</div>` : "";
  const org = p.logo
    ? `<img class="org-logo" src="${esc(p.logo)}" alt="${esc(p.affiliation)}" loading="lazy" />`
    : `<p>${esc(p.affiliation)}</p>`;
  return `<article class="person${back ? " has-back" : ""}"${domId ? ` id="${esc(domId)}"` : ""}${back ? ' tabindex="0"' : ""}>
    ${avatar(p)}
    <h3>${esc(p.name)}</h3>
    ${p.role ? `<p class="role">${esc(p.role)}</p>` : ""}
    ${org}
    ${back}
  </article>`;
}

// "09:30" + minutes -> "10:10"
const addMinutes = (hhmm, mins) => {
  const [h, m] = hhmm.split(":").map(Number);
  const t = h * 60 + m + mins;
  return `${String(Math.floor(t / 60)).padStart(2, "0")}:${String(t % 60).padStart(2, "0")}`;
};

function renderAgenda({ start, talkMinutes, items }, people) {
  let clock = start;
  return items.map((item) => {
    const minutes = item.minutes ?? (item.type === "talk" ? talkMinutes : 0);
    const end = minutes ? addMinutes(clock, minutes) : null;
    const time = end ? `${clock} – ${end}` : clock;  // no duration = a single point in time
    clock = end || clock;

    if (item.type !== "talk") {
      const cls = item.type === "break" ? "slot slot-break" : "slot slot-session";
      const desc = item.description ? `<p class="abstract">${esc(item.description)}</p>` : "";
      return `<li class="${cls}"><time>${time}</time><div><h3>${esc(item.title)}</h3>${desc}</div></li>`;
    }

    const ids = (item.speakers || []).filter((id) => people[id]);
    const chips = ids.length
      ? ids.map((id) => `<a class="chip" href="#speaker-${esc(id)}">${avatar(people[id])}<div><strong>${esc(people[id].name)}</strong><span>${esc(people[id].affiliation)}</span></div></a>`).join("")
      : `<div class="chip">${avatar()}<div><span>Speaker to be announced</span></div></div>`;
    const link = ids.length ? ` data-speaker="${esc(ids[0])}"` : "";
    return `<li class="slot${item.title ? "" : " tba"}${ids.length ? " slot-link" : ""}"${link}>
      <time>${time}</time>
      <div>
        <h3>${esc(item.title || "To be announced soon")}</h3>
        <div class="speaker-chips">${chips}</div>
        ${item.abstract ? `<p class="abstract">${esc(item.abstract)}</p>` : ""}
      </div>
    </li>`;
  }).join("");
}

// Infinite marquee: the photo set is rendered twice and the track slides by exactly one set width.
function renderGallery(gallery) {
  const section = document.getElementById("gallery");
  if (!gallery?.photos?.length) { section.hidden = true; return; }
  const imgs = (hidden) => gallery.photos.map((ph) =>
    `<img src="${esc(ph.src)}" alt="${hidden ? "" : esc(ph.alt)}" loading="lazy" width="960" height="640" />`).join("");
  const track = document.getElementById("gallery-track");
  track.innerHTML = `<div class="marquee-set">${imgs(false)}</div><div class="marquee-set" aria-hidden="true">${imgs(true)}</div>`;
  track.style.setProperty("--duration", `${gallery.photos.length * 6}s`);
}

// Clicking a talk row (or a speaker in it) scrolls to that speaker's card and opens its bio panel
// (.open); the panel closes when the visitor clicks anywhere outside the card.
function openSpeaker(id) {
  const card = document.getElementById(`speaker-${id}`);
  if (!card) return;
  card.scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "center" });
  document.querySelectorAll(".person.open").forEach((c) => c.classList.remove("open"));
  card.classList.add("open");
  card.focus({ preventScroll: true });
  card.classList.remove("flash");
  void card.offsetWidth; // restart the highlight animation
  card.classList.add("flash");
}

document.addEventListener("click", (e) => {
  document.querySelectorAll(".person.open").forEach((c) => { if (!c.contains(e.target)) c.classList.remove("open"); });
});

function linkAgendaToSpeakers() {
  const agenda = document.getElementById("agenda-list");
  agenda.addEventListener("click", (e) => {
    const chip = e.target.closest("a.chip");
    const row = e.target.closest(".slot-link");
    if (!chip && !row) return;
    e.preventDefault();
    e.stopPropagation(); // keep the document listener below from closing the card straight away
    openSpeaker(chip ? chip.hash.replace("#speaker-", "") : row.dataset.speaker);
  });
}

const logoList = (orgs) =>
  orgs.map((o) => `<a href="${esc(o.url)}" target="_blank" rel="noopener"><img src="${esc(o.logo)}" alt="${esc(o.name)}" data-scale="${Number(o.scale) || 1}" /></a>`).join("");

// Size logos by aspect ratio so wide wordmarks and compact marks look equally weighted
// (height ∝ ratio^-0.6, slightly stronger than equal area). Per-logo "scale" fine-tunes.
function balanceLogos() {
  document.querySelectorAll(".logos img").forEach((img) => {
    const fit = () => {
      const ratio = img.naturalWidth / img.naturalHeight;
      img.style.height = `${Math.round(95 * Math.pow(ratio, -0.6) * img.dataset.scale)}px`;
    };
    img.complete && img.naturalWidth ? fit() : img.addEventListener("load", fit, { once: true });
  });
}

function render(data) {
  const { event, venue, people, agenda } = data;
  const $ = (id) => document.getElementById(id);

  const dateText = new Date(`${event.date}T12:00:00`).toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" });
  const fields = {
    title: `${event.title}:`, theme: event.theme, date: dateText,
    place: `${venue.name} · ${venue.city}`, about: event.about,
    venueName: venue.name, address: venue.address, directions: venue.directions,
    registerNote: event.registerNote, galleryTitle: data.gallery?.title,
  };
  document.querySelectorAll("[data-field]").forEach((el) => { el.textContent = fields[el.dataset.field] ?? ""; });

  // Register buttons: link to Luma once the URL exists; until then the header button scrolls to the
  // register band and the others say registration is opening soon. With a lumaEventId, Luma's embed
  // script turns the links into an on-page checkout pop-up (the plain link remains the fallback).
  document.querySelectorAll("[data-register]").forEach((a) => {
    if (event.registerUrl) {
      Object.assign(a, { href: event.registerUrl, target: "_blank", rel: "noopener" });
      if (event.lumaEventId) Object.assign(a.dataset, { lumaAction: "checkout", lumaEventId: event.lumaEventId });
    } else if (!a.closest(".site-header")) {
      a.textContent = "Registration opens soon";
      a.setAttribute("aria-disabled", "true");
      a.removeAttribute("href");
    }
  });
  // Luma binds its buttons once on load, so load it only after the attributes above are set.
  if (event.registerUrl && event.lumaEventId) {
    document.head.appendChild(Object.assign(document.createElement("script"), {
      id: "luma-checkout", src: "https://embed.lu.ma/checkout-button.js",
    }));
  }

  // Speakers are everyone listed on a talk, in agenda order; unfilled talks show as "To be announced".
  const talks = agenda.items.filter((i) => i.type === "talk");
  const speakerIds = [...new Set(talks.flatMap((t) => t.speakers || []))];
  const openTalks = talks.filter((t) => !(t.speakers || []).length).length;
  $("speakers-list").innerHTML =
    speakerIds.map((id) => personCard(people[id], `speaker-${id}`)).join("") + personCard().repeat(openTalks);

  $("agenda-list").innerHTML = renderAgenda(agenda, people);
  linkAgendaToSpeakers();
  $("organizers-list").innerHTML = data.organizers.map((id) => personCard(people[id])).join("");
  $("hosts-list").innerHTML = logoList(data.hosts);
  $("sponsors-list").innerHTML = logoList(data.sponsors);
  balanceLogos();
  renderGallery(data.gallery);
  $("faq-list").innerHTML = data.faq.map((f) => `<details><summary>${esc(f.q)}</summary><p>${esc(f.a)}</p></details>`).join("");
  $("contact-btn").href = `mailto:${event.contactEmail}`;

  const query = encodeURIComponent(`${venue.name}, ${venue.address}`);
  $("map").src = `https://www.google.com/maps/embed?origin=mfe&pb=!1m3!2m1!1s${query}!6i16`;
  $("map-link").href = `https://www.google.com/maps/search/?api=1&query=${query}`;
}

// Mobile menu
const menuBtn = document.getElementById("menu-btn");
const nav = document.getElementById("nav");
const setMenu = (open) => { nav.classList.toggle("open", open); menuBtn.setAttribute("aria-expanded", String(open)); };
menuBtn.addEventListener("click", () => setMenu(!nav.classList.contains("open")));
nav.addEventListener("click", (e) => { if (e.target.closest("a")) setMenu(false); });

fetch("data/content.json")
  .then((r) => r.json())
  .then(render)
  .catch((err) => console.error("Could not load data/content.json", err));
