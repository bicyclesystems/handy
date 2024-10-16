function preloadImages() {
  const imageUrls = [
    "https://weareunder.design/work/bounce/0.png",
    "https://weareunder.design/work/rnbw/0.png",
    "https://weareunder.design/work/spacetop/0.png",
    "https://weareunder.design/work/blockaid/0.png",
    "https://weareunder.design/work/soli/19.png",
    "https://weareunder.design/work/justripe/09.png",
    "https://weareunder.design/work/utila/0.png",
    "https://weareunder.design/work/balance/0.png",
    "https://weareunder.design/work/visioncamp/6.png",
    "https://weareunder.design/work/dymension/0.png",
    "https://weareunder.design/work/finaloop/0.png",
    "https://weareunder.design/work/groundcover/0.png",
    "https://weareunder.design/work/nilus/0.png",
    "https://weareunder.design/work/raftt/0.png",
    "https://weareunder.design/work/togetherr/0.png",
    "https://weareunder.design/work/upword/0.png",
    "https://weareunder.design/work/darna/0.png",
    "https://weareunder.design/work/everafter/0.png",
    "https://weareunder.design/work/faintlines/0.png",
    "https://weareunder.design/work/grain/0.png",
    "https://weareunder.design/work/healthquarters/0.png",
    "https://weareunder.design/work/iceberg/0.png",
    "https://weareunder.design/work/karma/0.png",
    "https://weareunder.design/work/larosh/0.png",
    "https://weareunder.design/work/le_salon/0.png",
    "https://weareunder.design/work/mesh_payments/0.svg",
    "https://weareunder.design/work/notch/0.png",
    "https://weareunder.design/work/perdiem/0.png",
    "https://weareunder.design/work/reeco/0.png",
    "https://weareunder.design/work/reflect/0.png",
    "https://weareunder.design/work/tagbox/0.png",
    "https://weareunder.design/work/revelations/0.png",
    "https://weareunder.design/work/unit/0.png",
    "https://weareunder.design/work/unleash/0.png",
    "https://weareunder.design/work/zigi/0.svg",
    "https://weareunder.design/work/zoog/0.png",
  ];

  imageUrls.forEach((url) => {
    const img = new Image();
    img.src = url;
  });
}

window.addEventListener('load', preloadImages);

function addSidebar() {
  const TEMPLATE = `
  <div class="row padding-xl gap-m" style="
  position: fixed;
  right: 0;
  z-index: 999;
" id="under-nav">
<a class="header-link" href="https://weareunder.design/brandsprint/" data-page="brandsprint">
<div class="column align-center gap-xs">
<img src="https://rnbw.design/images/under/brandsprint.svg">
<span class="text-m" style="text-decoration: none;">brandsprint</span>
</div>
</a>
<a class="header-link" target="_blank" href="https://rnbw.design/" data-page="rnbw">
<div class="column align-center gap-xs">
<img src="https://rnbw.design/images/under/rnbw.svg">
<span class="text-m" style="text-decoration: none;">rnbw</span>
</div>
</a>
<a class="header-link" style="cursor: pointer" target="_blank" href="" data-page="handy">
<div class="column align-center gap-xs">
<img src="https://rnbw.design/images/under/handy.svg">
<span class="text-m" style="text-decoration: none;">handy</span>
</div>
</a>
<a class="header-link" style="cursor: pointer" href="https://store.weareunder.design" data-page="store">
<div class="column align-center gap-xs">
<img src="https://rnbw.design/images/under/store.svg">
<span class="text-m" style="text-decoration: none;">store</span>
</div>
</a>
<div class="column align-center header-link gap-xs" style="cursor: pointer" id="nav-work" data-page="design">
<img src="https://rnbw.design/images/under/design.svg">
<span class="text-m" style="text-decoration: none;">design</span>
</div>
</div>

<div id="works-wrapper" class="hidden">
<div class="view row show-project" style="position: relative; z-index: 100;" id="brand-sprints-section">
<a href="https://weareunder.design/" class="logo padding-xl mix-diff" href="/" style="">
        <img src="https://weareunder.design/images/under-header-logo.svg" class="desktop-logo-navigation"/>
        <img src="https://weareunder.design/images/under-header-logo-small.svg" class="mobile-logo-navigation"/>
</a>
<div class="sidebar column" data-ix="sidebar" id="sidebar-work">
  <a href="https://weareunder.design/work/pointfive/" class="sidebar-project-link" id="pointfive-0216C9">pointfive</a>
  <a href="https://weareunder.design/work/rnbw/" class="sidebar-project-link" id="rnbw-000000">rnbw</a>
  <a href="https://weareunder.design/work/bounce/" class="sidebar-project-link" id="bounce-03542C">bounce</a>
  <a href="https://weareunder.design/work/spacetop/" class="sidebar-project-link" id="spacetop-1E1E1E">spacetop</a>
  <a href="https://weareunder.design/work/blockaid/" class="sidebar-project-link" id="blockaid-FF4500">blockaid</a>
  <a href="https://weareunder.design/work/soli/" class="sidebar-project-link" id="soli-FF8A00">soli</a>
  <a href="https://weareunder.design/work/justripe/" class="sidebar-project-link" id="justripe-221C35">justripe</a>
  <a href="https://weareunder.design/work/utila/" class="sidebar-project-link" id="utila-00794E">utila</a>
  <a href="https://weareunder.design/work/visioncamp/" class="sidebar-project-link" id="visioncamp-0700FD">visioncamp</a>
  <a href="https://weareunder.design/work/balance/" class="sidebar-project-link" id="balance-1d1d1d">balance</a>
  <a href="https://weareunder.design/work/finaloop/" class="sidebar-project-link" id="finaloop-FF0000">finaloop</a>
  <a href="https://weareunder.design/work/dymension/" class="sidebar-project-link" id="dymension-24201F">dymension</a>
  <a href="https://weareunder.design/work/groundcover/" class="sidebar-project-link" id="groundcover-1BB485">groundcover</a>
  <a href="https://weareunder.design/work/nilus/" class="sidebar-project-link" id="nilus-db160d">nilus</a>
  <a href="https://weareunder.design/work/raftt/" class="sidebar-project-link" id="raftt-0C6BEA">raftt</a>
  <a href="https://weareunder.design/work/togetherr/" class="sidebar-project-link" id="togetherr-000000">togetherr</a>
  <a href="https://weareunder.design/work/upword/" class="sidebar-project-link" id="upword-B8A4FD">upword</a>
  <a href="https://weareunder.design/work/darna/" class="sidebar-project-link" id="darna-2a52cf">darna</a>
  <a href="https://weareunder.design/work/everafter/" class="sidebar-project-link" id="everafter-FF7051">everafter</a>
  <a href="https://weareunder.design/work/faintlines/" class="sidebar-project-link" id="faintlines-FF0DBD">faintlines</a>
  <a href="https://weareunder.design/work/grain/" class="sidebar-project-link" id="grain-FED164">grain</a>
  <a href="https://weareunder.design/work/healthquarters/" class="sidebar-project-link" id="healthquarters-0E305A">healthquarters</a>
  <a href="https://weareunder.design/work/iceberg/" class="sidebar-project-link" id="iceberg-EC7926">iceberg</a>
  <a href="https://weareunder.design/work/karma/" class="sidebar-project-link" id="karma-FCAC8B">karma</a>
  <a href="https://weareunder.design/work/larosh/" class="sidebar-project-link" id="larosh-C0815F">larosh</a>
  <a href="https://weareunder.design/work/le_salon/" class="sidebar-project-link" id="le_salon-000000">le salon</a>
  <a href="https://weareunder.design/work/mesh_payments/" class="sidebar-project-link" id="mesh_payments-19F08B">mesh payments</a>
  <a href="https://weareunder.design/work/notch/" class="sidebar-project-link" id="notch-CF6AFF">notch</a>
  <a href="https://weareunder.design/work/perdiem/" class="sidebar-project-link" id="perdiem-0171EA">perdiem</a>
  <a href="https://weareunder.design/work/reeco/" class="sidebar-project-link" id="reeco-0FCB71">reeco</a>
  <a href="https://weareunder.design/work/reflect/" class="sidebar-project-link" id="reflect-D1A8FD">reflect</a>
  <a href="https://weareunder.design/work/tagbox/" class="sidebar-project-link" id="tagbox-C2A78D">tagbox</a>
  <a href="https://weareunder.design/work/revelations/" class="sidebar-project-link" id="revelations-000000">Revelations</a>
  <a href="https://weareunder.design/work/unit/" class="sidebar-project-link" id="unit-000000">unit</a>
  <a href="https://weareunder.design/work/unleash/" class="sidebar-project-link" id="unleash-BE8DF6">unleash</a>
  <a href="https://weareunder.design/work/zigi/" class="sidebar-project-link" id="zigi-22D285">zigi</a>
  <a href="https://weareunder.design/work/zoog/" class="sidebar-project-link" id="zoog-FF7051">zoog</a>
</div>
</div>
</div>

<div id="main-content">
<div class="projects">
<img src="https://weareunder.design/work/pointfive/0.png" class="sidebar-project-image" id="pointfive" loading="lazy"></img>
<img src="https://weareunder.design/work/bounce/0.png" class="sidebar-project-image" id="bounce" loading="lazy"></img>
<img src="https://weareunder.design/work/rnbw/0.png" class="sidebar-project-image" id="rnbw" loading="lazy"></img>
<img src="https://weareunder.design/work/spacetop/0.png" class="sidebar-project-image" id="spacetop" loading="lazy"></img>
<img src="https://weareunder.design/work/blockaid/0.png" class="sidebar-project-image" id="blockaid" loading="lazy"></img>
<img src="https://weareunder.design/work/soli/19.png" class="sidebar-project-image box-l" id="soli" loading="lazy"></img>
<img src="https://weareunder.design/work/justripe/09.png" class="sidebar-project-image box-l" id="justripe" loading="lazy"></img>
<img src="https://weareunder.design/work/utila/0.png" class="sidebar-project-image box-l" id="utila" loading="lazy"></img>
<img src="https://weareunder.design/work/balance/0.png" class="sidebar-project-image box-l" id="balance" loading="lazy"></img>
<img src="https://weareunder.design/work/visioncamp/6.png" class="sidebar-project-image box-l" id="visioncamp" loading="lazy"></img>
<img src="https://weareunder.design/work/dymension/0.png" class="sidebar-project-image" id="dymension" loading="lazy"></img>
<img src="https://weareunder.design/work/finaloop/0.png" class="sidebar-project-image" id="finaloop" loading="lazy"></img>
<img src="https://weareunder.design/work/groundcover/0.png" class="sidebar-project-image" id="groundcover" loading="lazy"></img>
<img src="https://weareunder.design/work/nilus/0.png" class="sidebar-project-image" id="nilus" loading="lazy"></img>
<img src="https://weareunder.design/work/raftt/0.png" class="sidebar-project-image" id="raftt" loading="lazy"></img>
<img src="https://weareunder.design/work/togetherr/0.png" class="sidebar-project-image" id="togetherr" loading="lazy"></img>
<img src="https://weareunder.design/work/upword/0.png" class="sidebar-project-image" id="upword" loading="lazy"></img>
<img src="https://weareunder.design/work/darna/0.png" class="sidebar-project-image" id="darna" loading="lazy"></img>
<img src="https://weareunder.design/work/everafter/0.png" class="sidebar-project-image" id="everafter" loading="lazy"></img>
<img src="https://weareunder.design/work/faintlines/0.png" class="sidebar-project-image" id="faintlines" loading="lazy"></img>
<img src="https://weareunder.design/work/grain/0.png" class="sidebar-project-image" id="grain" loading="lazy"></img>
<img src="https://weareunder.design/work/healthquarters/0.png" class="sidebar-project-image" id="healthquarters" loading="lazy"></img>
<img src="https://weareunder.design/work/iceberg/0.png" class="sidebar-project-image" id="iceberg" loading="lazy"></img>
<img src="https://weareunder.design/work/karma/0.png" class="sidebar-project-image" id="karma" loading="lazy"></img>
<img src="https://weareunder.design/work/larosh/0.png" class="sidebar-project-image" id="larosh" loading="lazy"></img>
<img src="https://weareunder.design/work/le_salon/0.png" class="sidebar-project-image" id="le_salon" loading="lazy"></img>
<img src="https://weareunder.design/work/mesh_payments/0.svg" class="sidebar-project-image" id="mesh_payments" loading="lazy"></img>
<img src="https://weareunder.design/work/notch/0.png" class="sidebar-project-image" id="notch" loading="lazy"></img>
<img src="https://weareunder.design/work/perdiem/0.png" class="sidebar-project-image" id="perdiem" loading="lazy"></img>
<img src="https://weareunder.design/work/reeco/0.png" class="sidebar-project-image" id="reeco" loading="lazy"></img>
<img src="https://weareunder.design/work/reflect/0.png" class="sidebar-project-image" id="reflect" loading="lazy"></img>
<img src="https://weareunder.design/work/tagbox/0.png" class="sidebar-project-image" id="tagbox" loading="lazy"></img>
<img src="https://weareunder.design/work/revelations/0.png" class="sidebar-project-image" id="revelations" loading="lazy"></img>
<img src="https://weareunder.design/work/unit/0.png" class="sidebar-project-image" id="unit" loading="lazy"></img>
<img src="https://weareunder.design/work/unleash/0.png" class="sidebar-project-image" id="unleash" loading="lazy"></img>
<img src="https://weareunder.design/work/zigi/0.svg" class="sidebar-project-image" id="zigi" loading="lazy"></img>
<img src="https://weareunder.design/work/zoog/0.png" class="sidebar-project-image" id="zoog" loading="lazy"></img>
</div>
    `;

  class UnderNavigation extends HTMLElement {
    constructor() {
      super();
      this.innerHTML = TEMPLATE;
    }
  }
  customElements.define("under-navigation", UnderNavigation);

  var count = 0;

  const resizerInterval = setInterval(function () {
    if (count < 50) {
      window.dispatchEvent(new Event("resize"));
      count++;
    } else clearInterval(resizerInterval);
  }, 100);

  window.addEventListener("resize", () => {
    setInterval(function () {
      if (count < 50) {
        window.dispatchEvent(new Event("resize"));
        count++;
      } else clearInterval(resizerInterval);
    }, 100);
  });

  const animations = $(".lottie-animation");

  function getRandomInt(max) {
    return Math.floor(Math.random() * max);
  }

  $(".sidebar").on("mouseover", function () {
    // document.body.style.overflow = "hidden";
  });

  $(".sidebar").on("mouseout", function () {
    document.body.style.overflow = "auto";
  });

  $("#nav-work").on("click", function () {
    window.scrollTo({ top: 0 });
    $(".hero-section").css("display", "none");
    $("#under-nav").css("display", "none");
    $("#works-wrapper").css("display", "block");
    $("#body-content").css("display", "none");
  });

  $("#sidebar-work").on("mouseleave", function () {
    $(".hero-section").css("display", "block");
    $("#under-nav").css({
      "display": "flex",
      "flex-direction": "row"
    });
    $("#works-wrapper").css("display", "none");
    $("#body-content").css("display", "block");
  });

  function setActiveNavItem() {
    const pageIdentifier = document.body.dataset.page;
    if (pageIdentifier) {
      const navItem = $(`.header-link[data-page="${pageIdentifier}"]`);
      if (navItem.length) {
        const img = navItem.find("img");
        const originalSrc = img.attr("src");
        img.attr("src", originalSrc.replace(".svg", "a.svg"));
        navItem.addClass('active');
      }
    }
  }

  $(".header-link").on("mouseover", function () {
    if (!$(this).hasClass('active')) {
      const img = $(this).find("img");
      const originalSrc = img.attr("src");
      img.attr("src", originalSrc.replace(".svg", "h.svg"));
    }
  }).on("mouseout", function () {
    if (!$(this).hasClass('active')) {
      const img = $(this).find("img");
      const originalSrc = img.attr("src");
      img.attr("src", originalSrc.replace("h.svg", ".svg"));
    }
  });

  setActiveNavItem();
}

async function SideBarFunctionality() {
  "use strict";

  const sidebar = document.getElementsByClassName("sidebar")[0];
  if (sidebar) {
    sidebar.setAttribute("data-ix", "sidebar");
  }
  const rotateMenu = document.getElementsByClassName("work")[0];
  if (rotateMenu) {
    rotateMenu.setAttribute("data-ix", "show-sidebar");
  }

  var Main = function () { };
  Main.main = function () {
    var initTimer = new haxe_Timer(50);
    initTimer.run = function () {
      if (
        window.document.readyState == "interactive" ||
        window.document.readyState == "complete"
      ) {
        Main.init();
        initTimer.stop();
      }
    };
  };
  Main.init = function () {
    Main.heroElement = window.document.getElementById("brand-sprints-section");
    Main.projectsElement =
      window.document.getElementsByClassName("projects")[0];
    Main.sidebarElement = window.document.getElementsByClassName("sidebar")[0];
    if (!Main.projectsElement) return;
    var img_len = Main.projectsElement.children.length;

    var _g21 = 0;
    while (_g21 < img_len) {
      var child1 = Main.projectsElement.children.item(_g21++);
      if (child1.tagName == "IMG") {
        var img = child1;
        var key9 = img.id;
        var _this9 = Main.navLinks.images;
        if (__map_reserved[key9] != null) {
          _this9.setReserved(key9, img);
        } else {
          _this9.h[key9] = img;
        }
      }
    }
    var nav_len = Main.sidebarElement.children.length;
    var _g4 = 0;
    while (_g4 < nav_len) {
      var child2 = Main.sidebarElement.children.item(_g4++);
      if (child2.tagName == "A") {
        var anchor = child2;
        var anID = [anchor.id.split("-")];
        if (anID[0].length == 2) {
          var _this10 = Main.navLinks.anchors;
          var key10 = anID[0][0];
          if (__map_reserved[key10] != null) {
            _this10.setReserved(key10, anchor);
          } else {
            _this10.h[key10] = anchor;
          }
          var this1 = Main.navLinks.colors;
          var value = "#" + anID[0][1].toUpperCase();
          var _this11 = this1;
          var key11 = anID[0][0];
          if (__map_reserved[key11] != null) {
            _this11.setReserved(key11, value);
          } else {
            _this11.h[key11] = value;
          }
          anchor.addEventListener(
            "mouseover",
            (function (anID1) {
              return function () {
                Main.previewProject(anID1[0][0]);
              };
            })(anID)
          );
        }
      }
    }

    new haxe_Timer(24).run = function () {
      if (Main.latestScrollY != window.scrollY) {
        Main.latestScrollY = window.scrollY;
      }
      if (Main.sidebarElement.style.display == "none") {
        if (Main.stopMotionMode == false) {
          Main.stopMotionMode = true;
        }
      } else {
        Main.stopMotionMode = false;
      }
    };
  };

  Main.previewProject = function (id) {
    var _this = Main.navLinks.colors;
    if (
      (__map_reserved[id] != null
        ? _this.existsReserved(id)
        : _this.h.hasOwnProperty(id)) == true
    ) {
      var _this1 = Main.navLinks.colors;
      $(".hero-section svg").hide();
      Main.sidebarElement.style.backgroundColor =
        __map_reserved[id] != null ? _this1.getReserved(id) : _this1.h[id];
    }

    var _this2 = Main.navLinks.images;
    if (
      (__map_reserved[id] != null
        ? _this2.existsReserved(id)
        : _this2.h.hasOwnProperty(id)) == true
    ) {
      var _this3 = Main.navLinks.images;
      var newImage =
        __map_reserved[id] != null ? _this3.getReserved(id) : _this3.h[id];

      Main.heroElement.style.backgroundImage = "url(" + newImage.src + ")";
    }
  };

  Main.setStopMotionFrame = function (position, sequence) {
    if (sequence.images.length > 0) {
      var framePos = Math.floor((sequence.images.length - 1) * position);
      Main.heroElement.style.backgroundImage =
        "url(" + sequence.images[framePos].src + ")";
    }
  };
  var Std = function () { };
  Std.parseInt = function (x) {
    var v = parseInt(
      x,
      x && x[0] == "0" && (x[1] == "x" || x[1] == "X") ? 16 : 10
    );
    if (isNaN(v)) {
      return null;
    }
    return v;
  };
  var haxe_IMap = function () { };
  var haxe_Timer = function (time_ms) {
    var me = this;
    this.id = setInterval(function () {
      me?.run();
    }, time_ms);
  };
  haxe_Timer.prototype = {
    stop: function () {
      if (this.id == null) {
        return;
      }
      clearInterval(this.id);
      this.id = null;
    },
    run: function () { },
  };
  var haxe_ds_StringMap = function () {
    this.h = {};
  };
  haxe_ds_StringMap.__interfaces__ = [haxe_IMap];
  haxe_ds_StringMap.prototype = {
    setReserved: function (key, value) {
      if (this.rh == null) {
        this.rh = {};
      }
      this.rh["$" + key] = value;
    },
    getReserved: function (key) {
      if (this.rh == null) {
        return null;
      } else {
        return this.rh["$" + key];
      }
    },
    existsReserved: function (key) {
      if (this.rh == null) {
        return false;
      }
      return this.rh.hasOwnProperty("$" + key);
    },
  };

  var __map_reserved = {};
  Main.latestScrollY = 0;
  Main.relatedScroll = 0;
  Main.stopMotionMode = true;
  Main.animations = [];
  Main.animationMap = new haxe_ds_StringMap();
  Main.navLinks = {
    images: new haxe_ds_StringMap(),
    anchors: new haxe_ds_StringMap(),
    colors: new haxe_ds_StringMap(),
  };
  Main.main();
}

function hideTextOnMobile() {
  const navLinks = document.querySelectorAll('.header-link p');
  if (window.innerWidth <= 768) {
    navLinks.forEach(link => {
      link.style.display = 'none';
    });
  } else {
    navLinks.forEach(link => {
      link.style.display = '';
    });
  }
}

window.addEventListener('load', hideTextOnMobile);
window.addEventListener('resize', hideTextOnMobile);

SideBarFunctionality();

addSidebar();