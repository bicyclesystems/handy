function addSlider() {
    const TEMPLATE = `
    <div class="view row box-l" id="body-content" id="slider-container" style="background: no-repeat center/cover; position: relative;">
        <div class="slider view" style="position: relative; width: 100%; height: 61.8vw; overflow: hidden;"> 
            <div class="slides view" style="width: 100%; height: 61.8vw; display: flex; transition: transform 0.5s ease-in-out;">
                <a href="#" class="slide view"
                    style="background-image: url('./images/slide1.png'); min-width: 100%; height: 100%; background-size: cover; background-position: center;"
                    data-title="casual" data-subtitle="browse, scroll, and click <rr> without, well, clicking. it's <rr> computing, but make it comfy."></a>
                <a href="#" class="slide view"
                    style="background-image: url('./images/slide2.png'); min-width: 100%; height: 100%; background-size: cover; background-position: center;"
                    data-title="design" data-subtitle="sculpt your ideas in thin air. <rr> your creativity, now unbound <rr> by clunky interfaces."></a>
                <a href="#" class="slide view"
                    style="background-image: url('./images/slide3.png'); min-width: 100%; height: 100%; background-size: cover; background-position: center;"
                    data-title="music" data-subtitle="conduct your digital orchestra. <rr> mix, loop, and create with <rr> a wave of your hand."></a>
            </div>
            <div class="sliderbuttons padding-xl">
                <button class="arrow prev" style="border: none; background: none; cursor: pointer; width: 1.75rem; height: 1.75rem;">
                <img src="https://weareunder.design/images/arrow_left.svg" /></button>
                <button class="arrow next" style="border: none; background: none; cursor: pointer; width: 1.75rem; height: 1.75rem;"><img src="https://weareunder.design/images/arrow_right.svg" /></button>
            </div>
            <div class="slidertext box-xs padding-xl column gap-xs" style="position: absolute; bottom: 0px; left: 0%; white-space: nowrap; margin: 0.5rem, 0, 0.5rem, 0 !important; line-height: 1.35 !important; color: white;">
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
                rr {
                    display: block;
                    content: '';
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

    const sliderButtons = document.querySelectorAll('.sliderbuttons .arrow');

    sliderButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const direction = e.currentTarget.classList.contains('next') ? 1 : -1;
            let index = Math.round(currentPosition / 100);
            let newIndex = index + direction;

            if (newIndex >= slide.length) {
                newIndex = 0;
            } else if (newIndex < 0) {
                newIndex = slide.length - 1;
            }

            moveToSlide(newIndex);
        });
    });

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
