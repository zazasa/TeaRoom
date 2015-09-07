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


  $('[data-toggle="tooltip"]').tooltip()

//Student selector panel
  $('.list-group.checked-list-box .list-group-item').each(function () {
      
      // Settings
      var $widget = $(this),
          $checkbox = $('<input type="checkbox" class="hidden" />'),
          color = ($widget.data('color') ? $widget.data('color') : "primary"),
          style = ($widget.data('style') == "button" ? "btn-" : "list-group-item-"),
          settings = {
              on: {
                  icon: 'glyphicon glyphicon-check'
              },
              off: {
                  icon: 'glyphicon glyphicon-unchecked'
              }
          };
          
      $widget.css('cursor', 'pointer')
      $widget.append($checkbox);

      // Event Handlers
      $widget.on('click', function () {
          $checkbox.prop('checked', !$checkbox.is(':checked'));
          $checkbox.triggerHandler('change');
          updateDisplay();
      });
      $checkbox.on('change', function () {
          updateDisplay();
      });
        

      // Actions
      function updateDisplay() {
          var isChecked = $checkbox.is(':checked');

          // Set the button's state
          $widget.data('state', (isChecked) ? "on" : "off");

          // Set the button's icon
          $widget.find('.state-icon')
              .removeClass()
              .addClass('state-icon ' + settings[$widget.data('state')].icon);

          // Update the button's color
          if (isChecked) {
              $widget.addClass(style + color + ' active');
          } else {
              $widget.removeClass(style + color + ' active');
          }
      }

      // Initialization
      function init() {
          
          if ($widget.data('checked') == true) {
              $checkbox.prop('checked', !$checkbox.is(':checked'));
          }
          
          updateDisplay();

          // Inject the icon if applicable
          if ($widget.find('.state-icon').length == 0) {
              $widget.prepend('<span class="state-icon ' + settings[$widget.data('state')].icon + '"></span>');
          }
      }
      init();
  });

  $('#student-select-all').on('click', function(event) {
      var is_checked = $(this).find('input:checkbox').prop('checked');
      $("#students-selector li input").each(function(idx, cb) {
        $(cb).prop('checked', is_checked);
        $(cb).triggerHandler('change');
      });
  });    

  // $('#get-checked-data').on('click', function(event) {
  //     event.preventDefault(); 
  //     var checkedItems = {}, counter = 0;
  //     $("#check-list-box li.active").each(function(idx, li) {
  //         checkedItems[counter] = $(li).text();
  //         counter++;
  //     });
  //     $('#display-json').html(JSON.stringify(checkedItems, null, '\t'));
  // });


$('.button-checkbox').each(function () {
  // Settings
  var $widget = $(this),
      $button = $widget.find('button'),
      $checkbox = $widget.find('input:checkbox'),
      color = $button.data('color'),
      settings = {
          on: {
              icon: 'glyphicon glyphicon-check'
          },
          off: {
              icon: 'glyphicon glyphicon-unchecked'
          }
      };

  // Event Handlers
  $button.on('click', function () {
      $checkbox.prop('checked', !$checkbox.is(':checked'));
      $checkbox.triggerHandler('change');
      updateDisplay();
  });
  $checkbox.on('change', function () {
      updateDisplay();
  });

  // Actions
  function updateDisplay() {
      var isChecked = $checkbox.is(':checked');

      // Set the button's state
      $button.data('state', (isChecked) ? "on" : "off");

      // Set the button's icon
      $button.find('.state-icon')
          .removeClass()
          .addClass('state-icon ' + settings[$button.data('state')].icon);

      // Update the button's color
      if (isChecked) {
          $button
              .removeClass('btn-default')
              .addClass('btn-' + color + ' active');
      }
      else {
          $button
              .removeClass('btn-' + color + ' active')
              .addClass('btn-default');
      }
  }

  // Initialization
  function init() {

      updateDisplay();

      // Inject the icon if applicable
      if ($button.find('.state-icon').length == 0) {
          $button.prepend('<i class="state-icon ' + settings[$button.data('state')].icon + '"></i> ');
      }
  }
  init();
  });


// AJAX POST SETUP
var csrftoken = $.cookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


// exercise table filter
    $('.btn-filter').click(function(){

        var $panel = $(this).parents('.ex-header').next('.ex-content.filterable'),
        $filters = $panel.find('.filters input'),
        $tbody = $panel.find('.table tbody');

        console.log($panel);

        if ($filters.prop('disabled') == true) {
            $filters.prop('disabled', false);
            $filters.first().focus();
        } else {
            $filters.val('').prop('disabled', true);
            $tbody.find('.no-result').remove();
            $tbody.find('tr').show();
        }
    });

    $('.filterable .filters input').keyup(function(e){
        /* Ignore tab key */
        var code = e.keyCode || e.which;
        if (code == '9') return;
        /* Useful DOM data and selectors */
        var $input = $(this),
        inputContent = $input.val().toLowerCase(),
        $panel = $input.parents('.filterable'),
        column = $panel.find('.filters th').index($input.parents('th')),
        $table = $panel.find('.table'),
        $rows = $table.find('tbody tr');
        /* Dirtiest filter function ever ;) */
        var $filteredRows = $rows.filter(function(){
            var value = $(this).find('td').eq(column).text().toLowerCase();
            return value.indexOf(inputContent) === -1;
        });
        /* Clean previous no-result if exist */
        $table.find('tbody .no-result').remove();
        /* Show all rows, hide filtered ones (never do that outside of a demo ! xD) */
        $rows.show();
        $filteredRows.hide();
        /* Prepend no-result row if all rows are filtered */
        if ($filteredRows.length === $rows.length) {
            $table.find('tbody').prepend($('<tr class="no-result text-center"><td colspan="'+ $table.find('.filters th').length +'">No result found</td></tr>'));
        }
    });




})();
