(function($) {
  
  $.fn.pfgTabs = function(settings) {
    var defaults = {
      content: 'fieldset',
      label: 'legend',
      error: '.field.error',
      buttons: '.formControls input[type="submit"]',
      active: 0,
      nextLabel: 'continue',
      prevLabel: 'back',
      infoLabel: 'step {current} of {total}',
      rightLabel: '&rsaquo;',
      leftLabel: '&lsaquo;'
    };
    
    var pfgTabs = function(el, settings) {
      var tabs = this;
      
      tabs.settings = $.extend(defaults, settings);
      tabs.el = el;
      
      var contents = tabs.el.find(tabs.settings.content);
      if(contents.size() < 2)
        return;
      tabs.footer = $('<div class="pfg-tabs-footer" />');
      tabs.buttons = $('<div class="pfg-tabs-buttons" />').append(tabs.el.find(tabs.settings.buttons).hide().clone(true).show()).hide().appendTo(tabs.footer);
      tabs.header = $('<div class="pfg-tabs-header" />');
      tabs.tabs = $('<ul class="pfg-tabs-tabs" />').appendTo(tabs.header);
      tabs.prev = $('<input type="submit" class="pfg-tabs-prev" value="'+tabs.settings.prevLabel+'" />').hide().appendTo(tabs.footer).click(function(e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        tabs.activate(tabs.current-1);
      });
      tabs.next = $('<input type="submit" class="pfg-tabs-next" value="'+tabs.settings.nextLabel+'" />').hide().appendTo(tabs.footer).click(function(e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        tabs.activate(tabs.current+1);
      });
      tabs.info = $('<span class="pfg-tabs-info">'+tabs.settings.infoLabel+'</span>').appendTo(tabs.footer);
      
      var i = 0;
      contents.each(function() {
        $(this).data('pfg-tabs-index', i);
        var label = $(this).find(tabs.settings.label).hide().html();
        var li = $('<li />').appendTo(tabs.tabs);
        var tab = $('<a href="javascript://">'+label+'</a>').data('pfg-tabs-index', i);
        var required = $(this).find('.required:first');
        if(required.size())
          tab.append(required.clone());
        tab.click(function(e) {
          e.preventDefault();
          tabs.activate($(this).data('pfg-tabs-index'));
        }).appendTo(li);
        i++;
      }).wrap('<div class="pfg-tabs-content" />');
      tabs.contents = tabs.el.find('.pfg-tabs-content').hide();
      
      tabs.el.prepend(tabs.header);
      tabs.el.append(tabs.footer);
      tabs.el.addClass('pfg-tabs');
      
      var error = tabs.el.find(tabs.settings.error);
      if(error.size())
        error.each(function() {
          var content = $(this).closest(tabs.settings.content).addClass('pfg-tabs-error');
          tabs.tabs.find('li').eq(content.data('pfg-tabs-index')).addClass('pfg-tabs-error');
        });
      if(!tabs.tabs.find('li.pfg-tabs-selected').size())
        tabs.tabs.find('li:first').addClass('pfg-tabs-selected');
      tabs.scrollInit();
      if(error.size())
        tabs.activate(error.first().closest(tabs.settings.content).data('pfg-tabs-index'));
      else
        tabs.activate(tabs.settings.active);
      $(window).resize(function(e) {
        if(tabs.resizeTimer)
          window.clearTimeout(tabs.resizeTimer);
        tabs.resizeTimer = window.setTimeout(function() {
          tabs.scrollInit();
          tabs.toggleArrows();
        }, 100);
      });
      return this;
    }
    pfgTabs.prototype.activate = function(index) {
      index = Math.min(this.contents.size() - 1, Math.max(0, index));
      this.current = index;
      if(index == 0)
        this.prev.hide();
      else
        this.prev.show();
      if(index == this.contents.size() - 1) {
        this.next.hide();
        this.buttons.show();
      } else {
        this.next.show();
        this.buttons.hide();
      }
      this.contents.hide();
      this.contents.eq(index).append(this.footer).show();
      this.tabs.find('li').removeClass('pfg-tabs-selected');
      this.tabs.find('li').eq(index).addClass('pfg-tabs-selected');
      this.info.html(this.settings.infoLabel.replace('{current}', this.current + 1).replace('{total}', this.contents.size()));
      if(this.rightPos < 0)
        this.scrollTo(index);
      var top = $(document).scrollTop();
      var pos = this.tabs.offset().top;
      if(top > pos)
        $(document).scrollTop(pos);
    }
    pfgTabs.prototype.scrollTo = function(index) {
      index = Math.min(this.contents.size() - 1, Math.max(0, index));
      var pos = index > 0 ? -this.tabs.find('li').eq(index).position().left+this.left.outerWidth() : 0;
      pos = Math.min(0, Math.max(this.rightPos, pos));
      this.tabs.css('left', pos);
      this.toggleArrows();
    }
    pfgTabs.prototype.scrollInit = function() {
      var tabs = this;
      var left = tabs.tabs.css('left');
      tabs.tabs.css({
        'left': 'auto',
        'right': 0
      });
      tabs.rightPos = tabs.tabs.position().left;
      tabs.tabs.css({
        'left': left,
        'right': 'auto'
      });
      if(tabs.rightPos < 0) {
        if(!tabs.right) {
          tabs.right = $('<div class="pfg-tabs-right"><a href="javascript://">'+tabs.settings.rightLabel+'</a></div>').appendTo(tabs.header);
          tabs.right.find('a').click(function(e) {
            e.preventDefault();
            tabs.scrollRight();
          });
        }
        if(!tabs.left) {
          tabs.left = $('<div class="pfg-tabs-left"><a href="javascript://">'+tabs.settings.leftLabel+'</a></div>').hide().appendTo(tabs.header);
          tabs.left.find('a').click(function(e) {
            e.preventDefault();
            tabs.scrollLeft();
          });
        }
        tabs.tabs.css('left', Math.min(0, Math.max(tabs.rightPos, tabs.tabs.position().left)));
      } else {
        if(tabs.right)
          tabs.right.hide();
        if(tabs.left)
          tabs.left.hide();
        tabs.tabs.css('left', 0);
      }
    }
    pfgTabs.prototype.toggleArrows = function() {
      var pos = this.tabs.position().left;
      if(Math.ceil(pos) < 0)
        this.left.fadeIn('fast');
      else
        this.left.fadeOut('fast');
      if(Math.floor(pos) > this.rightPos)
        this.right.fadeIn('fast');
      else
        this.right.fadeOut('fast');
    }
    pfgTabs.prototype.scrollLeft = function() {
      this.scrollTo(this.currentScroll() - 1);
    }
    pfgTabs.prototype.scrollRight = function() {
      this.scrollTo(this.currentScroll() + 1);
    }
    pfgTabs.prototype.currentScroll = function() {
      var x = this.tabs.position().left;
      var tabs = this.tabs.find('li');
      var size = tabs.size();
      for(var index=0; index < size; index++) {
        var pos = index > 0 ? -tabs.eq(index).position().left+this.left.outerWidth() : 0;
        if(pos <= x)
          return index;
      }
      return index;
    }
    pfgTabs.prototype.destroy = function() {
      this.buttons.remove();
      this.footer.remove();
      this.header.remove();
      this.contents.show().removeClass('pfg-tabs-error').data('pfg-tabs-index', null).find(this.settings.legend).show();
      this.el.data('pfgTabs', null);
      this.el.find(this.settings.buttons).show();
    }
    
    this.each(function() {
      if(!$(this).data('pfgTabs'))
        $(this).data('pfgTabs', new pfgTabs($(this), settings));
    });
    
    return this;
  }
})(jQuery);
