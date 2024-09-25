function addSlider() {
    const TEMPLATE = `
    <div class="box-l view row product" id="body-content" style="overflow: hidden;">
        <div class="slider view">
            <div class="slides view">
                <div class="slide view"
                    style="background-image: url('./images/slide1.png');"
                    data-title="casual" data-subtitle="browse, scroll, and click without, well, clicking. it's computing, but make it comfy."></div>
                <div class="slide view"
                    style="background-image: url('./images/slide2.png');"
                    data-title="music" data-subtitle="conduct your digital orchestra. mix, loop, and create with a wave of your hand."></div>
                <div class="slide view"
                    style="background-image: url('./images/slide3.png');"
                    data-title="design" data-subtitle="sculpt your ideas in thin air. your creativity, now unbound by clunky interfaces."></div>
            </div>
            <div class="sliderbuttons padding-xl">
                <button class="arrow prev"><img src="https://weareunder.design/images/arrow_left.svg" /></button>
                <button class="arrow next"><img src="https://weareunder.design/images/arrow_right.svg" /></button>
            </div>
            <div class="slidertext box-xs white padding-xl column gap-xs" style="top:0;">
                <p style="word-wrap: break-word; overflow-wrap: break-word; white-space: normal;"></p>
                <div class="text-m box-l" style="word-wrap: break-word; overflow-wrap: break-word; white-space: normal;"></div>
            </div>
        </div>
    </div>
    `;

    class UnderSlider extends HTMLElement {
        constructor() {
            super();
            this.innerHTML = TEMPLATE;
            this.addStyles();
        }

        addStyles() {
            const style = document.createElement('style');
            style.textContent = `
                .slidertext {
                    max-width: 300px;
                }
                .slidertext p,
                .slidertext .text-m {
                    width: 100%;
                    max-width: 100%;
                    word-wrap: break-word;
                    overflow-wrap: break-word;
                    white-space: normal;
                }
            `;
            this.appendChild(style);
        }
    }
    customElements.define("handy-slider", UnderSlider);

    const slider = document.querySelector('.slider');
    const slides = document.querySelector('.slides');
    const slide = document.querySelectorAll('.slide');
    const slideTextTitle = document.querySelector('.slidertext p');
    const slideTextSubtitle = document.querySelector('.slidertext div.text-m');
    const prevButton = document.querySelector('.prev');
    const nextButton = document.querySelector('.next');
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

        const currentSlideIndex = Math.floor(currentPosition / 100);
        const currentSlide = slide[currentSlideIndex % slide.length];
        slideTextTitle.textContent = currentSlide.dataset.title;
        slideTextSubtitle.textContent = currentSlide.dataset.subtitle;
    }

    function moveToSlide(index) {
        currentPosition = index * 100;
        if (currentPosition < 0) {
            currentPosition = (slide.length - 1) * 100;
        } else if (currentPosition >= slide.length * 100) {
            currentPosition = 0;
        }
        slides.style.transition = 'transform 0.5s ease';
        updateSlider();
        setTimeout(() => {
            slides.style.transition = 'none';
        }, 500);
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

    function handleManualScroll() {
        stopAutoScroll();
    }

    updateSlider();
    startAutoScroll();

    slider.addEventListener('mouseenter', stopAutoScroll);
    slider.addEventListener('mouseleave', startAutoScroll);

    prevButton.addEventListener('click', () => {
        let index = Math.floor(currentPosition / 100);
        index = (index - 1 + slide.length) % slide.length;
        moveToSlide(index);
        handleManualScroll();
    });

    nextButton.addEventListener('click', () => {
        let index = Math.floor(currentPosition / 100);
        index = (index + 1) % slide.length;
        moveToSlide(index);
        handleManualScroll();
    });
}

addSlider();