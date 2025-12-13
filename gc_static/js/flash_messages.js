// Auto-dismiss flash messages with a slight stagger.
window.addEventListener("DOMContentLoaded", () => {
  const messages = document.querySelectorAll("[data-flash-message]");
  let delay = 0;

  messages.forEach((msg) => {
    // Ensure we have a transition even if none is set in CSS.
    msg.style.transition = msg.style.transition || "opacity 300ms ease, transform 300ms ease";

    setTimeout(() => {
      msg.style.opacity = "0";
      msg.style.transform = "translateY(-4px)";
      setTimeout(() => msg.remove(), 350);
    }, 5000 + delay);

    delay += 200; // Stagger fade-outs
  });
});
