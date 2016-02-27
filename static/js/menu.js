semantic.menu = {};

// ready event
semantic.menu.ready = function() {

  // selector cache
  var
    $menuItem = $('.ui.menu a.item'),
    $dropdown = $('.ui.menu .dropdown'),
    // alias
    handler = {

      activate: function() {
        if(!$(this).hasClass('dropdown')) {
          $(this)
            .addClass('active')
            .closest('.ui.menu')
            .find('.item')
              .not($(this))
              .removeClass('active')
          ;
        }
      }

    }
  ;

  $dropdown
    .dropdown({
      on: 'click'
    })
  ;

  $menuItem
    .on('click', handler.activate)
  ;

}
);

// attach ready event
$(document)
  .ready(semantic.menu.ready)
;
