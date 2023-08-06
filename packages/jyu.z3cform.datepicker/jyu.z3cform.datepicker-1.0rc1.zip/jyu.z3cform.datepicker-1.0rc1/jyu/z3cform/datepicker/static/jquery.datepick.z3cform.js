/*globals document,$,jQuery*/
(function($){
  $.datepick.setDefaults($.datepick.regional['']);
  $.fn.datepick_z3cform = function(options) {
    return $(this).each(function() {
      var day = $(this).children(".date-widget[id$=day], .datetime-widget[id$=day]"),
          month = $(this).children(".date-widget[id$=month], .datetime-widget[id$=month]"),
          year = $(this).children(".date-widget[id$=year], .datetime-widget[id$=year]"),
          anchor = $('<input type="hidden" />')
            .insertAfter($(this).children(".date-widget:eq(2), .datetime-widget:eq(2)")),
      getFormDate = function() {
        if (day.val() && month.val() && year.val()) {
          return new Date(year.val(), month.val() - 1, day.val(), 12);
        } else {
          return undefined;
        }
      },
      setFormDate = function(date) {
        day.val(date.getDate());
        month.val(date.getMonth() + 1);
        year.val(date.getFullYear()).trigger('focus').trigger('blur');
      };
      $(anchor).datepick($.extend({
        showOnFocus: false, showAnim: '',
        showTrigger: '<button type="button" class="datepick"><img src="popup_calendar.png" alt="" /></button>',
        defaultDate: getFormDate(),
        onShow: function(picker, inst) {
          picker.css("width", '');
          $(getFormDate()).each(function() {
            picker.find(".dp" + Number(this).toString()).addClass("selected");
          });
        },
        onSelect: function(dates) {
          $(anchor).datepick("option", "defaultDate", dates[0]);
          return setFormDate(dates[0]);
        }
      }, options));
      $(day.toArray().concat(month.toArray()).concat(year.toArray())).bind("change", function() {
        $(getFormDate()).each(function() {
          $(anchor).datepick("option", "defaultDate", this);
        });
      });
    });
  };
})(jQuery);
