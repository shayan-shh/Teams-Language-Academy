
  (function ($) {
  
  "use strict";

    // PRE LOADER
    $(window).load(function(){
      $('.preloader').delay(500).slideUp('slow'); // set duration in brackets    
    });

    // NAVBAR
    $(".navbar").headroom();

    $('.navbar-collapse a').click(function(){
        $(".navbar-collapse").collapse('hide');
    });

    $('.slick-slideshow').slick({
      autoplay: true,          // فعال کردن تغییر خودکار
      autoplaySpeed: 10000,     // زمان نمایش هر اسلاید (5000 میلی‌ثانیه = 5 ثانیه)
      infinite: true,          // حلقه بی‌پایان
      arrows: false,           // حذف فلش‌ها
      fade: true,              // افکت
    

    $('.slick-testimonial').slick({
      arrows: false,
      dots: true,
    });
    
  })(window.jQuery);
