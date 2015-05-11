(function(){
  $(window).scroll(function () {
    var top = $(document).scrollTop();
    $('.corporate-jumbo').css({
      'background-position': '0px -'+(top/3).toFixed(2)+'px'
    });
    if(top > 50)
      $('.navbar').removeClass('navbar-transparent');
    else
      $('.navbar').addClass('navbar-transparent');
  }).trigger('scroll');



  // bootstrap course-list template
  $('[id^=detail-]').hide();
  $('.toggle').click(function() {
    $input = $( this );
    $target = $('#'+$input.attr('data-toggle'));
    $target.slideToggle();
  });
})();
