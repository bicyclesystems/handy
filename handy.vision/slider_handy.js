function addSlider() {
    const TEMPLATE = `
    <div class="box-l view row product" id="body-content">
        <div class="slider view">
            <div class="slides view">
                <div class="slide view" id="bounce"
                    style="background-image: url('./images/slide1.png');"></div>
                <div class="slide view" id="nilus"
                    style="background-image: url('./images/slide2.png');"></div>
                <div class="slide view" id="spacetop"
                    style="background-image: url('./images/slide3.png');"></div>
            </div>
        </div>
    </div>
    `;

    class UnderSlider extends HTMLElement {
        constructor() {
            super();
            this.innerHTML = TEMPLATE;
        }
    }
    customElements.define("handy-slider", UnderSlider);
    
    const slider = document.querySelector('.slider');
    const slides = document.querySelector('.slides');
    const slide = document.querySelectorAll('.slide');
    let currentPosition = 0;
    
    let isAutoScrolling = true;
    let scrollDirection = 0.045;
    let animationFrameId;
    
    slides.style.transition = 'none'; 
    slides.style.willChange = 'transform'; 
    
    function updateSlider() {
        const totalWidth = slide.length * 100;
        currentPosition = (currentPosition + totalWidth) % totalWidth;
        slides.style.transform = `translateX(${-currentPosition}%)`;
    }
    
    function autoScroll() {
        if (!isAutoScrolling) return;
    
        currentPosition += scrollDirection;
        if (currentPosition <= 0 || currentPosition >= (slide.length - 1) * 100) {
            scrollDirection *= -1; 
        }
        updateSlider();
        animationFrameId = requestAnimationFrame(autoScroll);
    }
    
    function startAutoScroll() {
        isAutoScrolling = true;
        cancelAnimationFrame(animationFrameId);
        animationFrameId = requestAnimationFrame(autoScroll);
    }
    
    function stopAutoScroll() {
        isAutoScrolling = false;
        cancelAnimationFrame(animationFrameId);
    }
    
    updateSlider();
    startAutoScroll();
    
    slider.addEventListener('mouseenter', stopAutoScroll);
    slider.addEventListener('mouseleave', startAutoScroll);
}

addSlider();