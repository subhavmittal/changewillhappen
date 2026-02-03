// Mobile Menu Toggle
const mobileMenuToggle = document.querySelector(".mobile-menu-toggle");
const navMenu = document.querySelector(".nav-menu");

if (mobileMenuToggle) {
  mobileMenuToggle.addEventListener("click", () => {
    navMenu.classList.toggle("active");
    mobileMenuToggle.classList.toggle("active");
  });
}

// Close mobile menu when clicking on a link
document.querySelectorAll(".nav-menu a").forEach((link) => {
  link.addEventListener("click", () => {
    navMenu.classList.remove("active");
    mobileMenuToggle.classList.remove("active");
  });
});

// Hero Carousel Functionality
const carouselSlides = document.querySelectorAll(".carousel-slide");
const carouselDots = document.querySelectorAll(".carousel-dots .dot");
const prevCarouselBtn = document.querySelector(".carousel-prev");
const nextCarouselBtn = document.querySelector(".carousel-next");

let currentSlide = 0;
let carouselInterval;
const slideInterval = 5000; // 5 seconds

function showSlide(index) {
  // Handle wraparound
  if (index >= carouselSlides.length) {
    currentSlide = 0;
  } else if (index < 0) {
    currentSlide = carouselSlides.length - 1;
  } else {
    currentSlide = index;
  }

  // Update slides
  carouselSlides.forEach((slide, i) => {
    slide.classList.toggle("active", i === currentSlide);
  });

  // Update dots
  carouselDots.forEach((dot, i) => {
    dot.classList.toggle("active", i === currentSlide);
  });
}

function nextSlide() {
  showSlide(currentSlide + 1);
}

function prevSlide() {
  showSlide(currentSlide - 1);
}

function startCarousel() {
  clearInterval(carouselInterval);
  carouselInterval = setInterval(nextSlide, slideInterval);
}

function stopCarousel() {
  clearInterval(carouselInterval);
}

function resetCarousel() {
  stopCarousel();
  startCarousel();
}

// Initialize carousel if elements exist
if (carouselSlides.length > 0) {
  // Start auto-play
  startCarousel();

  // Navigation buttons
  if (prevCarouselBtn) {
    prevCarouselBtn.addEventListener("click", () => {
      prevSlide();
      resetCarousel();
    });
  }

  if (nextCarouselBtn) {
    nextCarouselBtn.addEventListener("click", () => {
      nextSlide();
      resetCarousel();
    });
  }

  // Dot navigation
  carouselDots.forEach((dot, index) => {
    dot.addEventListener("click", () => {
      showSlide(index);
      resetCarousel();
    });
  });

  // Pause on hover
  const carouselContainer = document.querySelector(".carousel-container");
  if (carouselContainer) {
    carouselContainer.addEventListener("mouseenter", stopCarousel);
    carouselContainer.addEventListener("mouseleave", startCarousel);
  }

  // Keyboard navigation for carousel
  document.addEventListener("keydown", (e) => {
    if (document.querySelector(".lightbox.active")) return; // Don't interfere with lightbox

    if (e.key === "ArrowLeft") {
      prevSlide();
      resetCarousel();
    }
    if (e.key === "ArrowRight") {
      nextSlide();
      resetCarousel();
    }
  });
}

// Newsletter Form
const newsletterForm = document.querySelector(".newsletter-form");
if (newsletterForm) {
  newsletterForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const email = newsletterForm.querySelector('input[type="email"]').value;
    alert(
      `Thank you for subscribing with ${email}! You'll receive our updates soon.`,
    );
    newsletterForm.reset();
  });
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    const href = this.getAttribute("href");
    if (href === "#") return;

    const target = document.querySelector(href);
    if (target) {
      e.preventDefault();
      target.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  });
});

// Navbar scroll effect
const navbar = document.querySelector(".navbar");
let lastScroll = 0;

window.addEventListener("scroll", () => {
  const currentScroll = window.pageYOffset;

  if (currentScroll > 100) {
    navbar.style.boxShadow = "0 2px 10px rgba(0, 0, 0, 0.1)";
  } else {
    navbar.style.boxShadow = "none";
  }

  lastScroll = currentScroll;
});

// Intersection Observer for scroll animations
const observerOptions = {
  threshold: 0.1,
  rootMargin: "0px 0px -50px 0px",
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("visible");
    }
  });
}, observerOptions);

// Observe elements for animation
document
  .querySelectorAll(
    ".impact-item, .gallery-item, .project-card, .footer-section",
  )
  .forEach((el) => {
    el.style.opacity = "0";
    el.style.transform = "translateY(20px)";
    el.style.transition = "opacity 0.6s ease, transform 0.6s ease";
    observer.observe(el);
  });

// Add visible state styles
const style = document.createElement("style");
style.textContent = `
    .visible {
        opacity: 1 !important;
        transform: translateY(0) !important;
    }
`;
document.head.appendChild(style);

// International Telephone Input Initialization
const phoneInput = document.querySelector("#phone");

if (phoneInput && window.intlTelInput) {
  const iti = window.intlTelInput(phoneInput, {
    initialCountry: "auto",
    geoIpLookup: function (callback) {
      // Using ipapi for geolocation
      fetch("https://ipapi.co/json/")
        .then((res) => res.json())
        .catch(() => {
          // Fallback to US if geolocation fails
          callback("us");
        })
        .then((data) =>
          callback(data.country_code ? data.country_code.toLowerCase() : "us"),
        )
        .catch(() => callback("us"));
    },
    preferredCountries: ["us", "ca", "gb", "au", "in"],
    separateDialCode: true,
    utilsScript:
      "https://cdn.jsdelivr.net/npm/intl-tel-input@24.4.0/build/js/utils.min.js",
  });

  // Update hidden fields on input
  phoneInput.addEventListener("change", () => {
    const phoneCountryField = document.querySelector("#phoneCountry");
    const phoneNumberOnlyField = document.querySelector("#phoneNumberOnly");

    if (phoneCountryField && phoneNumberOnlyField) {
      phoneCountryField.value = iti.getSelectedCountryData().dialCode;
      phoneNumberOnlyField.value = iti.getNumber();
    }
  });

  phoneInput.addEventListener("input", (e) => {
    const phoneCountryField = document.querySelector("#phoneCountry");
    const phoneNumberOnlyField = document.querySelector("#phoneNumberOnly");

    if (phoneCountryField && phoneNumberOnlyField) {
      phoneCountryField.value = iti.getSelectedCountryData().dialCode;
      phoneNumberOnlyField.value = iti.getNumber();
    }
  });

  // Country-specific max phone number lengths
  const countryMaxDigits = {
    us: 10, ca: 10, gb: 10, au: 9, in: 10, de: 11, fr: 9, it: 10, es: 9,
    br: 11, mx: 10, jp: 10, cn: 11, kr: 10, ru: 10, za: 9, ng: 10, ke: 9,
    ph: 10, pk: 10, bd: 10, id: 12, vn: 9, th: 9, my: 9, sg: 8, hk: 8,
    ae: 9, sa: 9, eg: 10, tr: 10, pl: 9, nl: 9, be: 9, se: 9, no: 8,
    dk: 8, fi: 10, at: 10, ch: 9, pt: 9, gr: 10, ie: 9, nz: 9, il: 9
  };

  function getMaxDigits() {
    const countryData = iti.getSelectedCountryData();
    const countryCode = countryData.iso2;
    return countryMaxDigits[countryCode] || 15;
  }

  // Use beforeinput event - fires BEFORE the input changes and can be cancelled
  phoneInput.addEventListener("beforeinput", (e) => {
    // Allow deletions
    if (e.inputType === 'deleteContentBackward' || e.inputType === 'deleteContentForward' ||
        e.inputType === 'deleteByCut' || e.inputType === 'deleteByDrag') {
      return;
    }

    // Get the data being inserted
    const insertedData = e.data || '';

    // Block any non-numeric input
    if (insertedData && !/^\d+$/.test(insertedData)) {
      e.preventDefault();
      return;
    }

    // Check if we're at max digits
    const currentDigits = phoneInput.value.replace(/\D/g, '').length;
    const maxDigits = getMaxDigits();
    const selectionStart = phoneInput.selectionStart;
    const selectionEnd = phoneInput.selectionEnd;
    const selectedDigits = phoneInput.value.substring(selectionStart, selectionEnd).replace(/\D/g, '').length;

    // Calculate digits after this input
    const newDigitsCount = insertedData.replace(/\D/g, '').length;
    const resultingDigits = currentDigits - selectedDigits + newDigitsCount;

    if (resultingDigits > maxDigits) {
      e.preventDefault();
    }
  });

  // Handle form submission
  const volunteerForm = document.querySelector(".volunteer-form");
  if (volunteerForm) {
    volunteerForm.addEventListener("submit", function (e) {
      // Validate phone number
      if (phoneInput.value.trim()) {
        if (!iti.isValidNumber()) {
          e.preventDefault();
          phoneInput.classList.add("iti__error");
          // Show error message or alert
          const errorMsg = document.createElement("div");
          errorMsg.style.color = "var(--accent-red)";
          errorMsg.style.fontSize = "0.875rem";
          errorMsg.style.marginTop = "0.25rem";
          errorMsg.textContent = "Please enter a valid phone number";

          const wrapper = phoneInput.parentElement;
          const existingError = wrapper.querySelector('[role="alert"]');
          if (existingError) existingError.remove();

          errorMsg.setAttribute("role", "alert");
          wrapper.appendChild(errorMsg);

          return false;
        } else {
          phoneInput.classList.remove("iti__error");
          const wrapper = phoneInput.parentElement;
          const existingError = wrapper.querySelector('[role="alert"]');
          if (existingError) existingError.remove();
        }
      }
    });
  }
}
