let tweenBrandsprint, tween1, tween2, tween3, tween4, tween5;
let circle1, circle2, brandsprintElement, circle3, circle4, circle5;

var dot, container, containerBounds, xMax, xMin, yMax, yMin;

// Single animation instance for the preorder ball
let bouncingAnimation;

// Global state object
window.pingPongVars = window.pingPongVars || {
    dot: null,
    container: null,
    containerBounds: null,
    xMax: null,
    xMin: null,
    yMax: null,
    yMin: null,
    tweens: {}
};

function updatePlayground(element) {
    const vars = window.pingPongVars;
    vars.dot = element;
    if (!vars.dot) return;
    vars.container = document.querySelector(".ping-pong");
    const dotBounds = vars.dot.getBoundingClientRect();
    vars.containerBounds = vars.container.getBoundingClientRect();
    vars.xMax = vars.containerBounds.right - dotBounds.right;
    vars.xMin = vars.containerBounds.left - dotBounds.left;
    vars.yMax = vars.containerBounds.bottom - dotBounds.bottom;
    vars.yMin = vars.containerBounds.top - dotBounds.top;
}

function ensureInsideContainer(ball) {
    const container = window.pingPongVars.container || document.querySelector('.ping-pong');
    if (!container) return;
    const containerRect = container.getBoundingClientRect();
    const ballRect = ball.getBoundingClientRect();
    let deltaX = 0, deltaY = 0;
    
    if (ballRect.left < containerRect.left) {
        deltaX = containerRect.left - ballRect.left;
    } else if (ballRect.right > containerRect.right) {
        deltaX = containerRect.right - ballRect.right;
    }
    
    if (ballRect.top < containerRect.top) {
        deltaY = containerRect.top - ballRect.top;
    } else if (ballRect.bottom > containerRect.bottom) {
        deltaY = containerRect.bottom - ballRect.bottom;
    }
    
    let currentX = 0, currentY = 0;
    const transform = ball.style.transform;
    if (transform) {
        const match = transform.match(/translate\(([-\d.]+)px,\s*([-\d.]+)px\)/);
        if (match) {
            currentX = parseFloat(match[1]);
            currentY = parseFloat(match[2]);
        }
    }
    ball.style.transform = `translate(${currentX + deltaX}px, ${currentY + deltaY}px)`;
}

function animationToElement(element) {
    let tween = gsap.to(element, {
        duration: 80,
        repeat: -1,
        ease: "none",
        onUpdate: () => {
            updateBallPosition(element);
            resolveCollision(element);
        }
    });

    element.addEventListener("mouseenter", () => tween.pause());
    element.addEventListener("mouseleave", () => tween.resume());
    
    return tween;
}

function initializeCircles() {
    try {
        const circles = document.querySelectorAll('[class*="circle"]');
        circles.forEach(circle => {
            updatePlayground(circle);
            ensureInsideContainer(circle);
            // Reduced initial velocity for slower movement
            circle.velocity = { x: 1, y: 1 };
        });
        if (window.pingPongVars.containerBounds && window.pingPongVars.containerBounds.bottom > 0) {
            circles.forEach(circle => {
                const id = circle.className;
                window.pingPongVars.tweens[id] = animationToElement(circle);
            });
        }
    } catch (err) {
        console.log(err);
    }
}

function updateBallPosition(ball) {
    let currentX = 0, currentY = 0;
    const transform = ball.style.transform;
    if (transform) {
        const match = transform.match(/translate\(([-\d.]+)px,\s*([-\d.]+)px\)/);
        if (match) {
            currentX = parseFloat(match[1]);
            currentY = parseFloat(match[2]);
        }
    }

    const container = window.pingPongVars.container;
    const containerBounds = container.getBoundingClientRect();
    const ballRect = ball.getBoundingClientRect();

    // Bounce off left/right boundaries
    if ((ballRect.left + ball.velocity.x <= containerBounds.left) || 
        (ballRect.right + ball.velocity.x >= containerBounds.right)) {
        ball.velocity.x *= -1;
    }
    // Bounce off top/bottom boundaries
    if ((ballRect.top + ball.velocity.y <= containerBounds.top) || 
        (ballRect.bottom + ball.velocity.y >= containerBounds.bottom)) {
        ball.velocity.y *= -1;
    }

    currentX += ball.velocity.x;
    currentY += ball.velocity.y;
    ball.style.transform = `translate(${currentX}px, ${currentY}px)`;
}

function resolveCollision(ball) {
    const balls = document.querySelectorAll('[class*="circle"]');
    const ballRect = ball.getBoundingClientRect();
    const ballCenter = {
        x: ballRect.left + ballRect.width / 2,
        y: ballRect.top + ballRect.height / 2
    };

    balls.forEach(otherBall => {
        if (otherBall === ball) return;
        const otherRect = otherBall.getBoundingClientRect();
        const otherCenter = {
            x: otherRect.left + otherRect.width / 2,
            y: otherRect.top + otherRect.height / 2
        };

        const dx = ballCenter.x - otherCenter.x;
        const dy = ballCenter.y - otherCenter.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        const minDist = (ballRect.width / 2) + (otherRect.width / 2);

        if (distance < minDist) {
            const tempVelocity = { ...ball.velocity };
            ball.velocity = { ...otherBall.velocity };
            otherBall.velocity = tempVelocity;
        }
    });
}

function bringCircleToInitialPosition() {
    const circles = document.querySelectorAll('[class*="circle"]');
    circles.forEach(circle => {
        // Instead of resetting to "none", ensure they are well positioned inside the container
        ensureInsideContainer(circle);
    });
}

function pauseBouncingAnimation() {
    try {
        Object.values(window.pingPongVars.tweens).forEach(tween => tween?.pause());
    } catch (err) {
        console.log(err);
    }
}

function restartBouncingAnimation() {
    try {
        Object.values(window.pingPongVars.tweens).forEach(tween => tween?.restart());
    } catch (err) {
        console.log(err);
    }
}

// Handle responsive behavior
const mediaQuery = window.matchMedia("(max-width: 992px)");

function handleResponsive(e) {
    const cta = document.getElementById("cta-animation");
    const brandsprintCircles = document.querySelectorAll(".brand-sprint-circle");
    let circlesArray = Array.from(brandsprintCircles);
    
    if (e.matches) {
        bringCircleToInitialPosition();
        pauseBouncingAnimation();
        if (cta) cta.style.display = "none";
        if (brandsprintCircles) {
            circlesArray.forEach(circle => circle.style.display = "none");
        }
    } else {
        bringCircleToInitialPosition();
        restartBouncingAnimation();
        if (cta) cta.style.display = "flex";
        if (brandsprintCircles) {
            circlesArray.forEach(circle => circle.style.display = "flex");
        }
    }
}

// Initialize
mediaQuery.addEventListener("change", handleResponsive);
handleResponsive(mediaQuery);

// Start animation on load
document.addEventListener('DOMContentLoaded', () => {
    // Ensure the ping-pong container exists and is properly positioned
    const container = document.querySelector('.ping-pong');
    if (container) {
        container.style.pointerEvents = 'none';
        container.style.overflow = 'hidden';
        container.style.position = 'fixed';
        container.style.top = '0';
        container.style.left = '0';
        container.style.width = '100%';
        container.style.height = '100%';
        container.style.zIndex = '9999';
    }
    
    // Initialize the preorder button
    const preorderBtn = document.getElementById('cta-animation');
    if (preorderBtn) {
        preorderBtn.style.cursor = 'pointer';
        preorderBtn.style.zIndex = '1000';
        preorderBtn.style.pointerEvents = 'auto';
        preorderBtn.classList.add('circle');
    }
    
    initializeCircles();
});