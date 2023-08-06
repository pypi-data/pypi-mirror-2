(function($) {
  
  $(document).ready(function() {
    var settings = {};
    function setTranslation(id, string) {
      settings[id] = string;
      if(settings.nextLabel && settings.prevLabel && settings.infoLabel)
        $('.pfg-form form').pfgTabs(settings);
    }
    $.get('translate?msgid=continue&domain=raptus.pfg.tabs', function(data) {
      setTranslation('nextLabel', data);
    });
    $.get('translate?msgid=back&domain=raptus.pfg.tabs', function(data) {
      setTranslation('prevLabel', data);
    });
    $.get('translate?msgid=step {current} of {total}&domain=raptus.pfg.tabs', function(data) {
      setTranslation('infoLabel', data);
    });
  });
  
})(jQuery);