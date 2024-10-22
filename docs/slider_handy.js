function addSlider() {
    const TEMPLATE = `
    <div class="box-l view row product" id="body-content">
        <div class="slider view">
            <div class="slides view">
                <a href="#" class="slide view"
                    style="background-image: url('./images/slide1.png');"
                    data-title="casual" data-subtitle="browse, scroll, and click <br> without, well, clicking. it's <br> computing, but make it comfy."></a>
                <a href="#" class="slide view"
                    style="background-image: url('./images/slide2.png');"
                    data-title="music" data-subtitle="conduct your digital orchestra. <br> mix, loop, and create with <br> a wave of your hand."></a>
                <a href="#" class="slide view"
                    style="background-image: url('./images/slide3.png');"
                    data-title="design" data-subtitle="sculpt your ideas in thin air. <br> your creativity, now unbound <br> by clunky interfaces."></a>
            </div>
            <div class="sliderbuttons padding-xl">
                <button class="arrow prev"><img src="https://weareunder.design/images/arrow_left.svg" /></button>
                <button class="arrow next"><img src="https://weareunder.design/images/arrow_right.svg" /></button>
            </div>
            <div class="slidertext box-xs white padding-xl column gap-xs">
                <p></p>
                <div class="text-m"></div>
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
                .slider {
                    position: relative;
                    overflow: hidden;
                    width: 100%;
                    height: 100vh;
                }
                .slides {
                    display: flex;
                    transition: transform 0.5s ease;
                    will-change: transform;
                }
                .slide {
                    flex: 0 0 100%;
                    height: 100vh;
                    background-size: cover;
                    background-position: center;
                }
                .slidertext {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    background: linear-gradient(to bottom, rgba(90, 45, 20, 0.4) 0%, rgba(90, 45, 20, 0.1) 100%);
                }
                .sliderbuttons {
                    position: absolute;
                    bottom: 20px;
                    right: 20px;
                    z-index: 99;
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
    
    let currentPosition = 0;
    let isScrolling = false;
    let lastScrollTime = 0;
    let scrollDirection = null;
    const scrollCooldown = 1000; 

    function updateSlider() {
        slides.style.transform = `translateX(${-currentPosition}%)`;

        const currentSlideIndex = Math.round(currentPosition / 100) % slide.length;
        const currentSlide = slide[currentSlideIndex];
        slideTextTitle.innerHTML = currentSlide.dataset.title;
        slideTextSubtitle.innerHTML = currentSlide.dataset.subtitle;
    }

    function moveToSlide(index) {
        currentPosition = index * 100;
        updateSlider();
    }

    slider.addEventListener('wheel', (e) => {
        const isHorizontal = Math.abs(e.deltaX) > Math.abs(e.deltaY);
        
        if (isHorizontal) {
            e.preventDefault();
            
            const currentTime = Date.now();
            const deltaX = Math.abs(e.deltaX);

            if (currentTime - lastScrollTime < scrollCooldown) {
                return;
            }

            if (!isScrolling && deltaX > 25) {
                isScrolling = true;
                scrollDirection = e.deltaX > 0 ? 1 : -1;

                let index = Math.round(currentPosition / 100);
                let newIndex = index + scrollDirection;

                if (newIndex >= slide.length) {
                    newIndex = 0;
                } else if (newIndex < 0) {
                    newIndex = slide.length - 1;
                }

                moveToSlide(newIndex);
                lastScrollTime = currentTime;

                setTimeout(() => {
                    isScrolling = false;
                    scrollDirection = null;
                }, scrollCooldown);
            }
        }
    }, { passive: false });

    updateSlider();
}

addSlider();

let removedBrTags = [];

function handleBrTags() {
    const isMobile = window.innerWidth <= 768;

    if (isMobile && removedBrTags.length === 0) {
        const allBrTags = document.getElementsByTagName('br');
        
        Array.from(allBrTags).forEach(brTag => {
            if (!brTag.closest('[data-subtitle]')) {
                removedBrTags.push({
                    element: brTag,
                    parent: brTag.parentNode,
                    nextSibling: brTag.nextSibling
                });
                brTag.parentNode.removeChild(brTag);
            }
        });
    } else if (!isMobile && removedBrTags.length > 0) {
        removedBrTags.forEach(({ element, parent, nextSibling }) => {
            parent.insertBefore(element, nextSibling);
        });
        removedBrTags = [];
    }
}

document.addEventListener('DOMContentLoaded', handleBrTags);
window.addEventListener('resize', handleBrTags);