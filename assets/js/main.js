const header = document.querySelector(".site-header");
const toggle = document.querySelector(".menu-toggle");
const nav = document.querySelector(".nav");

window.addEventListener("scroll", () => {
  header.classList.toggle("scrolled", window.scrollY > 12);
}, { passive: true });

toggle?.addEventListener("click", () => {
  const open = nav.classList.toggle("open");
  toggle.setAttribute("aria-expanded", String(open));
});

document.querySelectorAll(".service").forEach((card) => {
  card.addEventListener("toggle", () => {
    if (!card.open) return;
    document.querySelectorAll(".service").forEach((other) => {
      if (other !== card) other.open = false;
    });
  });
});

document.querySelectorAll(".inview").forEach((el) => {
  const io = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("show");
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.18 });
  io.observe(el);
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
    };
    requestAnimationFrame(tick);
    io.disconnect();
  }, { threshold: 0.6 });
  io.observe(el);
});

function glideToOffer(service) {
  const target = document.getElementById("oferta");
  if (!target) return false;
  const select = target.querySelector("[name=serviciu]");
  if (select && service) {
    select.value = service;
    select.dispatchEvent(new Event("change"));
  }
  target.classList.remove("arrive");
  document.documentElement.style.scrollBehavior = "auto";
  const start = window.scrollY;
  const end = target.getBoundingClientRect().top + start - 88;
  const change = end - start;
  const duration = Math.min(1500, Math.max(750, Math.abs(change) * 0.5));
  const t0 = performance.now();
  const ease = (t) => 1 - Math.pow(1 - t, 3);
  const step = (now) => {
    const p = Math.min(1, (now - t0) / duration);
    window.scrollTo(0, start + change * ease(p));
    if (p < 1) requestAnimationFrame(step);
    else {
      document.documentElement.style.scrollBehavior = "";
      target.classList.add("arrive");
      history.replaceState(null, "", "#oferta");
    }
  };
  requestAnimationFrame(step);
  return true;
}

document.addEventListener("click", (event) => {
  const link = event.target.closest("a[href='#oferta']");
  if (!link || !document.getElementById("oferta")) return;
  event.preventDefault();
  glideToOffer(link.dataset.serviciu || "");
});

document.querySelectorAll("[data-service-form]").forEach((form) => {
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
    const button = form.querySelector("button[type=submit]");
    const ok = form.querySelector(".form-ok");
    button.disabled = true;
    const body = new FormData(form);
    try {
      const response = await fetch("/send.php", { method: "POST", body });
      if (!response.ok) throw new Error("mail");
      form.reset();
      sync();
      ok.classList.add("show");
    } catch {
      const params = new URLSearchParams();
      body.forEach((value, key) => {
        if (key !== "company" && value) params.append(key, value);
      });
      window.location.href = `mailto:office@gistransporturi.ro?subject=${encodeURIComponent("Cerere ofertă GIS Transporturi")}&body=${encodeURIComponent(params.toString().replace(/&/g, "\n").replace(/=/g, ": "))}`;
    } finally {
      button.disabled = false;
    }
  });
});
