const header = document.querySelector(".site-header");
const toggle = document.querySelector(".menu-toggle");
const nav = document.querySelector(".nav");

const calmMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
const canHover = window.matchMedia("(hover: hover)");

window.addEventListener("scroll", () => {
  header.classList.toggle("scrolled", window.scrollY > 12);
}, { passive: true });

toggle?.addEventListener("click", () => {
  const open = nav.classList.toggle("open");
  toggle.classList.toggle("is-open", open);
  toggle.setAttribute("aria-expanded", String(open));
});

document.querySelectorAll(".service, .offer-card").forEach((card) => {
  card.addEventListener("toggle", () => {
    queueScroll();
    if (!card.open) return;
    document.querySelectorAll(".service, .offer-card").forEach((other) => {
      if (other !== card) other.open = false;
    });
  });
});

/* ---------------------------------------------------------------- reveals */

const REVEAL_RULES = [
  [".page-hero .eyebrow", "up"],
  [".page-hero h1", "mask"],
  [".page-hero .lead", "up"],
  [".section > .wrap > .eyebrow", "up"],
  [".section > .wrap > h2", "mask"],
  [".section > .wrap > p", "up"],
  [".frame", "wipe"],
  [".fleet-show", "zoom"],
  [".prose", "up"],
  [".service", "up"],
  [".offer-card", "up"],
  [".service-board-intro", "left"],
  [".stat", "up"],
  [".reason", "up"],
  [".quote", "up"],
  [".faq details", "up"],
  [".contact-card", "left"],
  [".form", "up"],
  [".legal", "up"],
  [".map", "zoom"],
  [".two-col > *", "up"],
  [".split > *", "up"],
  [".foot-grid > div", "up"],
  [".legal-row", "up"],
  [".inview", "up"],
];

const tagged = [];
REVEAL_RULES.forEach(([selector, mode]) => {
  document.querySelectorAll(selector).forEach((el) => {
    if (el.hasAttribute("data-anim") || el.closest(".hero") || el.classList.contains("reveal")) return;
    el.setAttribute("data-anim", mode);
    tagged.push(el);
  });
});

/* pairs inside a two-column split slide in from their own side */
document.querySelectorAll(".split").forEach((split) => {
  [...split.children].forEach((child, i) => {
    if (child.getAttribute("data-anim") !== "up") return;
    child.setAttribute("data-anim", i % 2 ? "right" : "left");
  });
});

/* siblings revealed together cascade instead of popping at once */
const seats = new Map();
document.querySelectorAll("[data-anim]").forEach((el) => {
  const parent = el.parentElement;
  const seat = seats.get(parent) || 0;
  seats.set(parent, seat + 1);
  if (seat) el.style.setProperty("--d", `${Math.min(seat, 6) * 85}ms`);
});

const land = (el) => {
  el.removeAttribute("data-anim");
  el.style.removeProperty("will-change");
};

/* a geometry sweep rather than IntersectionObserver: clip-path reveals report
   an empty intersection rect, so the observer would never fire for them */
let pending = tagged.slice();
const sweepReveals = (relaxed) => {
  if (!pending.length) return;
  const gate = window.innerHeight * (relaxed ? 1 : 0.92);
  pending = pending.filter((el) => {
    const box = el.getBoundingClientRect();
    if (box.bottom < 0) {
      el.classList.add("is-in", "show");
      land(el);
      return false;
    }
    if (box.top > gate) return true;
    el.classList.add("is-in", "show");
    setTimeout(() => land(el), (parseFloat(el.style.getPropertyValue("--d")) || 0) + 1500);
    return false;
  });
};

/* safety net: once scrolling settles, anything with pixels on screen shows,
   so the last rows of the page can never stay stuck below the 92% gate */
let settleTimer;
const sweepOnSettle = () => {
  clearTimeout(settleTimer);
  settleTimer = setTimeout(() => sweepReveals(true), 420);
};

sweepReveals();
sweepOnSettle();

/* hero list items and buttons carry their own cascade index */
document.querySelectorAll(".checks, .hero-actions").forEach((group) => {
  [...group.children].forEach((child, i) => child.style.setProperty("--i", String(i)));
});

document.querySelectorAll("[data-since]").forEach((el) => {
  const [year, month] = el.dataset.since.split("-").map(Number);
  const now = new Date();
  let years = now.getFullYear() - year;
  if (now.getMonth() + 1 < month) years -= 1;
  el.dataset.count = String(Math.max(years, 0));
});

document.querySelectorAll("[data-count]").forEach((el) => {
  const target = Number(el.dataset.count);
  const io = new IntersectionObserver((entries) => {
    if (!entries[0].isIntersecting) return;
    const start = performance.now();
    const tick = (now) => {
      const p = Math.min(1, (now - start) / 1100);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))).toString();
      if (p < 1) requestAnimationFrame(tick);
      else el.closest(".stat")?.classList.add("counted");
    };
    requestAnimationFrame(tick);
    io.disconnect();
  }, { threshold: 0.6 });
  io.observe(el);
});

function glideTo(target, hash) {
  if (!target) return false;
  if (target.tagName === "DETAILS") target.open = true;
  document.documentElement.style.scrollBehavior = "auto";
  const start = window.scrollY;
  const destination = () => {
    let y = 0;
    let node = target;
    while (node) {
      y += node.offsetTop;
      node = node.offsetParent;
    }
    return Math.max(0, y - 88);
  };
  const finish = () => {
    const settle = () => {
      const live = destination();
      if (Math.abs(live - window.scrollY) > 4) window.scrollTo(0, live);
    };
    settle();
    document.documentElement.style.scrollBehavior = "";
    if (hash) history.replaceState(null, "", hash);
    if (target.id === "oferta") target.classList.add("arrive");
    window.addEventListener("load", settle, { once: true });
    setTimeout(settle, 500);
  };
  if (calmMotion.matches) {
    window.scrollTo(0, destination());
    finish();
    return true;
  }
  target.classList.remove("arrive");
  const duration = Math.min(1500, Math.max(750, Math.abs(destination() - start) * 0.5));
  const t0 = performance.now();
  const ease = (t) => 1 - Math.pow(1 - t, 3);
  const step = (now) => {
    const p = Math.min(1, (now - t0) / duration);
    const end = destination();
    window.scrollTo(0, start + (end - start) * ease(p));
    if (p < 1) requestAnimationFrame(step);
    else finish();
  };
  requestAnimationFrame(step);
  return true;
}

function glideToOffer(service) {
  const target = document.getElementById("oferta");
  if (!target) return false;
  const select = target.querySelector("[name=serviciu]");
  if (select && service) {
    select.value = service;
    select.dispatchEvent(new Event("change"));
  }
  return glideTo(target, "#oferta");
}

function closeNav() {
  nav?.classList.remove("open");
  toggle?.classList.remove("is-open");
  toggle?.setAttribute("aria-expanded", "false");
}

document.addEventListener("click", (event) => {
  const link = event.target.closest("a[href]");
  if (!link || link.target === "_blank") return;
  const url = new URL(link.getAttribute("href"), location.href);
  if (url.origin !== location.origin) return;
  const here = location.pathname.replace(/\/+$/, "") || "/";
  const there = url.pathname.replace(/\/+$/, "") || "/";
  if (here !== there) return;
  const id = url.hash.slice(1);
  if (!id) return;
  const target = document.getElementById(id);
  if (!target) return;
  event.preventDefault();
  closeNav();
  if (id === "oferta") glideToOffer(link.dataset.serviciu || "");
  else glideTo(target, "#" + id);
});

const bootHash = () => {
  const id = location.hash.slice(1);
  const target = id && document.getElementById(id);
  if (!target) return;
  if (id === "oferta") glideToOffer("");
  else glideTo(target, "#" + id);
};
if (location.hash) {
  if (document.readyState === "complete") bootHash();
  else window.addEventListener("load", bootHash, { once: true });
}

const highway = document.createElement("div");
highway.className = "highway";
highway.setAttribute("aria-hidden", "true");
highway.innerHTML = `<div class="highway-lane"></div><div class="highway-truck"><svg viewBox="0 0 24 96">
  <rect x="4" y="1" width="16" height="64" rx="2.5" fill="#89CFF0"/>
  <path d="M12 6v54" stroke="#6eb8dc" stroke-width="1.2"/>
  <rect x="10" y="65" width="4" height="3" rx="1" fill="#7ec4e4"/>
  <rect x="3.5" y="68" width="17" height="24" rx="3" fill="#A7D8F0"/>
  <rect x="6" y="83" width="12" height="7" rx="1.4" fill="#f4fbfe"/>
</svg></div>`;
document.body.appendChild(highway);
const lane = highway.querySelector(".highway-lane");
const truck = highway.querySelector(".highway-truck");
const services = document.getElementById("servicii");
const footer = document.querySelector(".site-footer");
const roadRange = () => {
  const max = document.documentElement.scrollHeight - window.innerHeight;
  const start = services ? Math.max(0, services.offsetTop - 80) : 0;
  const end = footer ? Math.max(start, footer.offsetTop - window.innerHeight) : max;
  return { start, end };
};
const placeTruck = () => {
  const { start, end } = roadRange();
  highway.classList.toggle("is-on", window.scrollY >= start && window.scrollY < end);
  const span = Math.max(1, end - start);
  const progress = Math.min(1, Math.max(0, (window.scrollY - start) / span));
  const travel = highway.clientHeight - truck.offsetHeight;
  truck.style.transform = `translateY(${progress * travel}px)`;
  lane.style.setProperty("--dash", `${-progress * 120}px`);
};
placeTruck();
window.addEventListener("scroll", placeTruck, { passive: true });
window.addEventListener("resize", placeTruck);
highway.addEventListener("click", (event) => {
  const rect = highway.getBoundingClientRect();
  const progress = Math.min(1, Math.max(0, (event.clientY - rect.top) / rect.height));
  const { start, end } = roadRange();
  window.scrollTo({ top: start + progress * (end - start), behavior: "smooth" });
});

const captchaFont = {
  A: ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
  B: ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
  C: ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
  D: ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
  E: ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
  F: ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
  G: ["01111", "10000", "10000", "10111", "10001", "10001", "01111"],
  H: ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
  J: ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
  K: ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
  L: ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
  M: ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
  N: ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
  P: ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
  Q: ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
  R: ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
  S: ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
  T: ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
  U: ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
  V: ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
  W: ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
  X: ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
  Y: ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
  Z: ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
  2: ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
  3: ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
  4: ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
  5: ["11111", "10000", "10000", "11110", "00001", "00001", "11110"],
  6: ["01110", "10000", "10000", "11110", "10001", "10001", "01110"],
  7: ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
  8: ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
  9: ["01110", "10001", "10001", "01111", "00001", "00001", "01110"]
};

function attachCaptcha(form) {
  const alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  const box = document.createElement("div");
  box.className = "captcha";
  box.innerHTML = '<div class="captcha-code"><canvas width="180" height="56" aria-hidden="true"></canvas><img alt="" hidden><button type="button" class="captcha-refresh" aria-label="Alt cod">↻</button></div><label>Scrie codul din imagine<input name="captcha" autocomplete="off" autocapitalize="characters" spellcheck="false" required></label><p class="captcha-error" hidden>Codul nu corespunde. Încearcă din nou.</p>';
  form.querySelector("button[type=submit]").before(box);
  const canvas = box.querySelector("canvas");
  const image = box.querySelector("img");
  const input = box.querySelector("input");
  const error = box.querySelector(".captcha-error");
  let code = "";
  let server = false;
  let imageUrl = "";

  const drawLocal = () => {
    code = Array.from({ length: 5 }, () => alphabet[Math.floor(Math.random() * alphabet.length)]).join("");
    const context = canvas.getContext("2d");
    context.clearRect(0, 0, 180, 56);
    context.fillStyle = "#f4f7fb";
    context.fillRect(0, 0, 180, 56);
    context.strokeStyle = "rgba(0, 159, 227, 0.45)";
    context.lineWidth = 2;
    context.beginPath();
    context.moveTo(8, 18 + Math.random() * 20);
    context.bezierCurveTo(50, 4, 120, 52, 172, 14 + Math.random() * 24);
    context.stroke();
    code.split("").forEach((char, index) => {
      const glyph = captchaFont[char];
      const originX = 16 + index * 32 + Math.round(Math.random() * 3);
      const originY = 10 + Math.round(Math.random() * 6);
      context.fillStyle = index % 2 ? "#4c2460" : "#0678b0";
      glyph.forEach((row, y) => {
        row.split("").forEach((bit, x) => {
          if (bit === "1") context.fillRect(originX + x * 3, originY + y * 3, 3, 3);
        });
      });
    });
    for (let dot = 0; dot < 28; dot += 1) {
      context.fillStyle = Math.random() > 0.5 ? "rgba(112, 61, 130, 0.35)" : "rgba(0, 159, 227, 0.4)";
      context.fillRect(Math.random() * 180, Math.random() * 56, 2, 2);
    }
  };

  const refresh = async () => {
    input.value = "";
    error.hidden = true;
    try {
      const response = await fetch("/captcha.php?t=" + Date.now(), { cache: "no-store", credentials: "same-origin" });
      const type = response.headers.get("content-type") || "";
      if (response.ok && type.includes("image")) {
        server = true;
        if (imageUrl) URL.revokeObjectURL(imageUrl);
        imageUrl = URL.createObjectURL(await response.blob());
        image.src = imageUrl;
        image.hidden = false;
        canvas.hidden = true;
        return;
      }
    } catch (err) {
      server = false;
    }
    server = false;
    image.hidden = true;
    canvas.hidden = false;
    drawLocal();
  };

  box.querySelector(".captcha-refresh").addEventListener("click", refresh);
  refresh();

  return {
    refresh,
    valid() {
      if (server) return true;
      const ok = input.value.trim().toUpperCase() === code;
      error.hidden = ok;
      if (!ok) {
        input.focus();
        drawLocal();
        input.value = "";
      }
      return ok;
    }
  };
}

document.querySelectorAll("[data-service-form]").forEach((form) => {
  const captcha = attachCaptcha(form);
  const type = form.querySelector("[name=serviciu]");
  const car = form.querySelectorAll("[data-for=auto]");
  const freight = form.querySelectorAll("[data-for=marfa]");
  const sync = () => {
    const value = type?.value || "";
    car.forEach((node) => { node.hidden = value !== "Transport autoturisme"; });
    freight.forEach((node) => { node.hidden = value !== "Transport mărfuri"; });
  };
  type?.addEventListener("change", sync);
  sync();

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!captcha.valid()) return;
    const button = form.querySelector("button[type=submit]");
    const ok = form.querySelector(".form-ok");
    button.disabled = true;
    button.classList.add("is-loading");
    ok.classList.remove("show");
    const body = new FormData(form);
    try {
      const response = await fetch("/send.php", { method: "POST", body });
      if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        if (data.error === "captcha") {
          await captcha.refresh();
          form.querySelector(".captcha-error").hidden = false;
          return;
        }
        throw new Error("mail");
      }
      form.reset();
      sync();
      captcha.refresh();
      ok.classList.add("show");
    } catch {
      const params = new URLSearchParams();
      body.forEach((value, key) => {
        if (key !== "company" && key !== "captcha" && value) params.append(key, value);
      });
      window.location.href = `mailto:office@gistransporturi.ro?subject=${encodeURIComponent("Cerere ofertă GIS Transporturi")}&body=${encodeURIComponent(params.toString().replace(/&/g, "\n").replace(/=/g, ": "))}`;
    } finally {
      button.disabled = false;
      button.classList.remove("is-loading");
    }
  });

  form.querySelectorAll("input, select, textarea").forEach((field) => {
    field.addEventListener("invalid", () => {
      field.classList.add("shake");
      setTimeout(() => field.classList.remove("shake"), 500);
    });
  });
});

document.querySelectorAll("[data-fleet-show]").forEach((root) => {
  const slides = [...root.querySelectorAll(".fleet-stage img")];
  const dots = [...root.querySelectorAll(".fleet-dots button")];
  let index = 0;
  let timer;
  const show = (n) => {
    index = (n + slides.length) % slides.length;
    slides.forEach((img, i) => img.classList.toggle("is-on", i === index));
    dots.forEach((dot, i) => {
      const on = i === index;
      dot.classList.toggle("is-on", on);
      if (on) dot.setAttribute("aria-current", "true");
      else dot.removeAttribute("aria-current");
    });
  };
  const stop = () => clearInterval(timer);
  const start = () => {
    stop();
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    timer = setInterval(() => show(index + 1), 5000);
  };
  root.querySelector(".fleet-next").addEventListener("click", () => { show(index + 1); start(); });
  root.querySelector(".fleet-prev").addEventListener("click", () => { show(index - 1); start(); });
  dots.forEach((dot, i) => dot.addEventListener("click", () => { show(i); start(); }));
  root.addEventListener("mouseenter", stop);
  root.addEventListener("mouseleave", start);

  const stage = root.querySelector(".fleet-stage");
  let swipeFrom = null;
  stage?.addEventListener("touchstart", (event) => {
    swipeFrom = event.touches[0].clientX;
    stop();
  }, { passive: true });
  stage?.addEventListener("touchend", (event) => {
    if (swipeFrom === null) return;
    const travel = event.changedTouches[0].clientX - swipeFrom;
    if (Math.abs(travel) > 44) show(index + (travel < 0 ? 1 : -1));
    swipeFrom = null;
    start();
  }, { passive: true });

  start();
});

/* ------------------------------------------------------- scroll choreography */

const progress = document.createElement("div");
progress.className = "scroll-progress";
progress.setAttribute("aria-hidden", "true");
document.body.appendChild(progress);

const parallax = [
  ...[...document.querySelectorAll(".hero-media")].map((el) => ({ el, pull: 0.16, cap: 130 })),
  ...[...document.querySelectorAll(".frame img")].map((el) => ({ el, pull: 0.07, cap: 14 })),
];

let prevY = window.scrollY;
let queued = false;

const paintScroll = () => {
  queued = false;
  sweepReveals();
  sweepOnSettle();
  const y = window.scrollY;
  const runway = document.documentElement.scrollHeight - window.innerHeight;

  progress.style.setProperty("--p", String(runway > 0 ? Math.min(1, y / runway) : 0));
  progress.classList.toggle("is-on", y > 40);

  if (!nav?.classList.contains("open")) {
    if (y > 620 && y > prevY + 4) header.classList.add("tuck");
    else if (y < prevY - 4 || y < 200) header.classList.remove("tuck");
  }
  prevY = y;

  if (calmMotion.matches) return;
  const middle = window.innerHeight / 2;
  parallax.forEach(({ el, pull, cap }) => {
    const box = el.getBoundingClientRect();
    if (box.bottom < -200 || box.top > window.innerHeight + 200) return;
    const offset = el.classList.contains("hero-media")
      ? y * pull
      : (middle - (box.top + box.height / 2)) * pull;
    el.style.setProperty("--py", `${Math.max(-cap, Math.min(cap, offset)).toFixed(1)}px`);
  });
};

const queueScroll = () => {
  if (queued) return;
  queued = true;
  requestAnimationFrame(paintScroll);
};

paintScroll();
window.addEventListener("scroll", queueScroll, { passive: true });
window.addEventListener("resize", queueScroll);

/* --------------------------------------------------------- pointer polish */

const spotlit = document.querySelectorAll(".offer-card, .stat, .reason, .quote, .service, .contact-card");
const tilted = document.querySelectorAll(".stat, .reason, .quote");

if (canHover.matches && !calmMotion.matches) {
  spotlit.forEach((card) => {
    card.addEventListener("pointermove", (event) => {
      const box = card.getBoundingClientRect();
      const x = ((event.clientX - box.left) / box.width) * 100;
      const y = ((event.clientY - box.top) / box.height) * 100;
      card.style.setProperty("--mx", `${x.toFixed(1)}%`);
      card.style.setProperty("--my", `${y.toFixed(1)}%`);
    });
  });

  tilted.forEach((card) => {
    card.addEventListener("pointermove", (event) => {
      const box = card.getBoundingClientRect();
      const x = (event.clientX - box.left) / box.width - 0.5;
      const y = (event.clientY - box.top) / box.height - 0.5;
      card.style.setProperty("--ry", `${(x * 7).toFixed(2)}deg`);
      card.style.setProperty("--rx", `${(-y * 7).toFixed(2)}deg`);
    });
    card.addEventListener("pointerleave", () => {
      card.style.removeProperty("--rx");
      card.style.removeProperty("--ry");
    });
  });

  document.querySelectorAll(".btn").forEach((button) => {
    button.addEventListener("pointermove", (event) => {
      const box = button.getBoundingClientRect();
      const x = (event.clientX - box.left) / box.width - 0.5;
      const y = (event.clientY - box.top) / box.height - 0.5;
      button.style.setProperty("--bx", `${(x * 7).toFixed(1)}px`);
      button.style.setProperty("--by", `${(y * 5 - 2).toFixed(1)}px`);
    });
    button.addEventListener("pointerleave", () => {
      button.style.removeProperty("--bx");
      button.style.removeProperty("--by");
    });
  });
}

document.addEventListener("pointerdown", (event) => {
  const button = event.target.closest(".btn");
  if (!button || calmMotion.matches) return;
  const box = button.getBoundingClientRect();
  const drop = document.createElement("span");
  drop.className = "ripple";
  drop.style.left = `${event.clientX - box.left}px`;
  drop.style.top = `${event.clientY - box.top}px`;
  button.appendChild(drop);
  drop.addEventListener("animationend", () => drop.remove());
});
