jq(document).ready(function() {
  jq('table.table td.icon:not(.hidden)').each(function() {
    var format = jq(this).parents('table').hasClass('gif') ? 'gif' : 'jpg';
    if(!jq.trim(jq(this).html()))
      return;
    jq(this).wrapInner('<span class="icon-content" />');
    jq(this).prepend('<img class="trigger" src="info_icon.'+format+'" />');
    jq(this).hover(function() {
      jq(this).find('.icon-content').css(jq(this).find('.trigger').position()).fadeIn(200);
    },
    function() {
      jq(this).find('.icon-content').fadeOut(200);
    });
  });
  jq('table.table .add-row').each(function() {
    var format = jq(this).parents('table').hasClass('gif') ? 'gif' : 'jpg';
    jq(this).find('td:not(.hidden) input:not([type=submit]), td:not(.hidden) textarea').each(function() {
      jq(this).wrap('<span class="wrap" />');
      jq(this).parent().width(30).height(jq(this).height());
      jq(this).css(jq(this).position());
    }).css({
      'width': 30,
      'height': '1em',
      'position': 'absolute',
    }).focus(function() {
      jq(this).css({
        'width': 150,
        'height': 'auto',
        'z-index': 1
      });
    }).
    blur(function() {
      jq(this).css({
        'width': 30,
        'height': '1em',
        'z-index': 0
      });
    });
    jq(this).find('.context').before('<a href="javascript://" class="icon add"><img src="add_icon.'+format+'" /></a>');
    jq(this).find('.add').click(function(event) {
      event.preventDefault();
      var row = jq(this).parents('.add-row');
      var new_row = row.clone(true);
      row.after(new_row);
      row.find('.add').after('<a href="javascript://" class="icon delete"><img src="delete_icon.'+format+'" /></a>');
      row.find('.delete').click(function(event) {
        event.preventDefault();
        jq(this).parents('.add-row').remove();
      });
      row.find('.context, .add').remove();
      new_row.find('input:first').focus();
    });
  });
  jq('table.table td.hidden').each(function() {
    if(!jq.trim(jq(this).html()))
      return;
    var format = jq(this).parents('table').hasClass('gif') ? 'gif' : 'jpg';
    var hidden = jq(this).parent().find('td:first').find('.hidden-content');
    if(!hidden.size()) {
      jq(this).parent().find('td:first').prepend('<span class="hidden-content"><img class="trigger" src="search_icon.'+format+'" /><span class="content"><table></table></span></span>')
      hidden = jq(this).parent().find('td:first').find('.hidden-content');
      hidden.hover(function() {
        jq(this).find('.content').fadeIn(200).css('display', 'block');
      },
      function() {
        jq(this).find('.content').fadeOut(200);
      });
    }
    hidden.find('table').append('<tr><th>'+jq(this).parents('table').find('th.'+jq(this).attr('class').match(/column-[^\s]+/)).html()+'</th><td>'+jq(this).html()+'</td></tr>');
  }).remove();
  jq('table.table th.hidden').remove();
});
