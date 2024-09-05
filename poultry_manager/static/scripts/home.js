document.addEventListener('DOMContentLoaded', () => {
    // Animated Scroll Effects
    const faders = document.querySelectorAll('.fade-in');
    const appearOptions = {
        threshold: 0,
        rootMargin: '0px 0px -200px 0px'
    };

    const appearOnScroll = new IntersectionObserver(function(entries, appearOnScroll) {
        entries.forEach(entry => {
            if (!entry.isIntersecting) {
                return;
            } else {
                entry.target.classList.add('visible');
                appearOnScroll.unobserve(entry.target);
            }
        });
    }, appearOptions);

    faders.forEach(fader => {
        appearOnScroll.observe(fader);
    });

    // Interactive Hero Section
    const heroText = document.querySelector('.hero-content h1');
    const heroButton1 = document.querySelector('.hero-content .btn');
    const heroButton2 = document.querySelector('.hero-content .btn-outline-info');

    setTimeout(() => {
        heroText.classList.add('visible');
    }, 500);

    setTimeout(() => {
        heroButton1.classList.add('visible');
        heroButton2.classList.add('visible');
    }, 1000);
});
