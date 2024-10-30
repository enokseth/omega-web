// Exemples de fonctions d'animation
export function fadeIn(element, duration = 1000) {
    element.style.opacity = 0;
    element.style.transition = `opacity ${duration}ms ease-in-out`;
    requestAnimationFrame(() => {
        element.style.opacity = 1;
    });
}

export function slideInFromLeft(element, duration = 1000) {
    element.style.transform = "translateX(-100%)";
    element.style.transition = `transform ${duration}ms ease-in-out`;
    requestAnimationFrame(() => {
        element.style.transform = "translateX(0)";
    });
}

export function bounce(element, duration = 1000) {
    element.classList.add('bounce-animation');
    setTimeout(() => {
        element.classList.remove('bounce-animation');
    }, duration);
}
