const swiper = new Swiper('.swiper', {

  autoplay: {
     delay: 2000,
     disableOnInteraction: false
   },

   spaceBetween: 30,
        effect: "fade",
        navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
        },
        pagination: {
          el: false,
          clickable: false,
    },

  

});
$(".owl-carousel").owlCarousel({
  loop: true,
  autoplay: true,
  margin: 12,
  responsiveClass: true,
  responsive: {
    0: {
      items: 1,
      nav: true,
    },
    600: {
      items: 2,
      nav: false,
    },
    1000: {
      items: 3,
      nav: true,
      loop: true,
    },
  },
});

jQuery(document).ready(function ($) {
  "use strict";
  // TESTIMONIALS CAROUSEL HOOK
  $("#customers-testimonials").owlCarousel({
    loop: true,
    center: true,
    items: 3,
    margin: 0,
    autoplay: true,
    autoplayTimeout: 8500,
    smartSpeed: 450,
    responsive: {
      0: {
        items: 1, // Show 1 item on small screens
      },
      768: {
        items: 2, // Show 2 items on medium screens
      },
      1170: {
        items: 3, // Show 3 items on larger screens
      },
    },
  });
});
// feature project
$("#featureProject").owlCarousel({
  loop: true,
  center: true,
  margin: 10,
  responsive: {
    0: {
      items: 1,
    },
    600: {
      items: 3,
    },
    1000: {
      items: 5,
    },
  },
});

// feature project
$('#featureProject').owlCarousel({
  loop: true,
  center: true,
  margin: 10,
  autoplay: true,
  responsive: {
      0: {
          items: 1
      },
      600: {
          items: 2,
      },
      1000: {
          items: 3,
      }
  }
})

