let tweenBrandsprint, tween1, tween2, tween3, tween4, tween5;
let circle1, circle2, brandsprintElement, circle3, circle4, circle5;

var dot, container, containerBounds, xMax, xMin, yMax, yMin;

function updatePlayground(class_target) {
  dot = document.querySelector(class_target);
  if (!dot) return;
  container = document.querySelector(".ping-pong");
  dotBounds = dot.getBoundingClientRect();
  containerBounds = container.getBoundingClientRect();
  xMax = containerBounds.right - dotBounds.right;
  xMin = containerBounds.left - dotBounds.left;
  yMax = containerBounds.bottom - dotBounds.bottom;
  yMin = containerBounds.top - dotBounds.top;
}

function animationToClass(class_target) {
  let gsapTween = gsap.to(class_target, {
    x: "+=3000",
    y: "+=2000",
    duration: 50,
    repeat: -1,
    repeatRefresh: true,
    ease: "none",
    modifiers: {
      x: bounceModifier(xMin, xMax),
      y: bounceModifier(yMin, yMax),
    },
  });

  let targetElement = document.querySelector(class_target);
  if (!!targetElement) {
    targetElement.addEventListener("mouseenter", () => {
      gsapTween.pause();
    });
    targetElement.addEventListener("mouseleave", () => {
      gsapTween.resume();
    });
  }
  return gsapTween;
}
function ping(class_target) {
  try {
    updatePlayground(class_target);
    if (containerBounds && containerBounds.bottom > 0) {
      if (class_target === ".circle-brandsprint") {
        tweenBrandsprint = animationToClass(class_target);
        clearInterval(intervalId3);
      }
      if (class_target === ".circle1") {
        tween1 = animationToClass(class_target);
        clearInterval(interval1);
      }
      if (class_target === ".circle2") {
        tween2 = animationToClass(class_target);
        clearInterval(interval2);
      }
      if (class_target === ".circle3") {
        tween3 = animationToClass(class_target);
        clearInterval(interval3);
      }
      if (class_target === ".circle4") {
        tween4 = animationToClass(class_target);
        clearInterval(interval4);
      }
      if (class_target === ".circle5") {
        tween5 = animationToClass(class_target);
        clearInterval(interval5);
      }
    }

    //make x and y go as high (or low) as you want, and the modifier will always keep it within the xMin/xMax and yMin/yMax ranges.
  } catch (err) {
    console.log(err);
  }
}
//this function spits back a modifier function that'll keep the value within a range, bouncing off the min/max boundaries.
function bounceModifier(min, max) {
  var range = max - min;
  return function (value) {
    value = parseFloat(value); // comes in as px, like "10px"
    var cycle, clippedValue;
    if (value > max) {
      cycle = (value - max) / range;
      clippedValue = (cycle % 1) * range;
      value = (cycle | 0) & (1 !== 0) ? min + clippedValue : max - clippedValue; //on even cycles, go backwards.
    } else if (value < min) {
      cycle = (min - value) / range;
      clippedValue = (cycle % 1) * range;
      value = (cycle | 0) & (1 !== 0) ? max - clippedValue : min + clippedValue; //on even cycles, go backwards.
    }
    return value + "px";
  };
}
var intervalId3 = setInterval(() => ping(".circle-brandsprint"), 1000);
var interval1 = setInterval(() => ping(".circle1"), 1000);
var interval2 = setInterval(() => ping(".circle2"), 1000);
var interval3 = setInterval(() => ping(".circle3"), 1000);
var interval4 = setInterval(() => ping(".circle4"), 1000);
var interval5 = setInterval(() => ping(".circle5"), 1000);

//Setting the circles to their initial position
function bringCircleToInitialPosition() {
  let circle1 = document.querySelector(".circle1");
  let circle2 = document.querySelector(".circle2");
  let circle3 = document.querySelector(".circle3");
  let circle4 = document.querySelector(".circle4");
  let circle5 = document.querySelector(".circle5");
  let brandsprintElement = document.querySelector(".circle-brandsprint");

  if (circle1) circle1.style.transform = "none";
  if (circle2) circle2.style.transform = "none";
  if (circle3) circle3.style.transform = "none";
  if (circle4) circle4.style.transform = "none";
  if (circle5) circle5.style.transform = "none";

  if (brandsprintElement) brandsprintElement.style.transform = "none";
}

//Pause Bouncing Animation
function pauseBouncingAnimation() {
  try {
    tweenBrandsprint?.pause();
    tween1?.pause();
    tween2?.pause();
    tween3?.pause();
    tween4?.pause();
    tween5?.pause();
  } catch (err) {
    console.log(err);
  }
}

//Restart Bouncing Animation
function restartBouncingAnimation() {
  try {
    tweenBrandsprint?.restart();
    tween1?.restart();
    tween2?.restart();
    tween3?.restart();
    tween4?.restart();
    tween5?.restart();
  } catch (err) {
    console.log(err);
  }
}

const pingPongMediaQuery = window.matchMedia("(max-width: 992px)");
pingPongMediaQuery.addEventListener("change", handlePingPongMediaQueryChange);
handlePingPongMediaQueryChange(pingPongMediaQuery);

function handlePingPongMediaQueryChange(mediaQuery) {
  const cta = document.getElementById("cta-animation");
  const brandsprintCircles = document.querySelectorAll(".brand-sprint-circle");
  let circlesArray = Array.from(brandsprintCircles);
  if (mediaQuery.matches) {
    bringCircleToInitialPosition();
    pauseBouncingAnimation();

    if (!!cta) {
      cta.style.display = "none";
    }
    if (!!brandsprintCircles) {
      circlesArray.forEach((circle) => {
        circle.style.display = "none";
      });
    }
  } else {
    bringCircleToInitialPosition();
    restartBouncingAnimation();

    if (!!cta) {
      cta.style.display = "flex";
    }
    if (!!brandsprintCircles) {
      circlesArray.forEach((circle) => {
        circle.style.display = "flex";
      });
    }
  }
}