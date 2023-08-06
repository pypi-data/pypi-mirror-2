(function($) {
  var contentswitcher = {
    postSetInterface: function(params) {
      $(params.parent).find('.lightbox-container-image').prepend('<ul class="lightbox-contentswitcher-nav visualNoMarker '+params.settings.contentswitcher.orientation+' '+params.settings.contentswitcher.position+'"></ul>');
      var nav = $(params.parent).find('.lightbox-contentswitcher-nav');
      if(params.settings.contentswitcher.orientation == 'horizontal')
        var width = Math.min((params.settings.fixedWidth-(params.settings.matchedObjects.size()-1))/params.settings.matchedObjects.size());
      else
        var height = Math.min((params.settings.fixedHeight-(params.settings.matchedObjects.size()-1))/params.settings.matchedObjects.size());
      for(var i=0; i<params.settings.matchedObjects.size(); i++) {
        var obj = $(params.settings.matchedObjects.get(i));
        nav.append('<li class="o'+i+'"><a href="'+obj.find('h2 > a').attr('href')+'" title="'+obj.find('p').html()+'">'+obj.find('h2 > a').html()+'</a></li>');
        nav.find('li:last').fadeTo(0, params.settings.contentswitcher.baseOpacity);
        if(params.settings.contentswitcher.orientation == 'horizontal')
          nav.find('li:last').css('width', width+'px');
        else {
          nav.find('li:last').css('height', height+'px');
          nav.find('li:last').css('line-height', height+'px');
        }
        nav.find('li:last').mouseover($.proxy(function(e) {
          var target = $(e.currentTarget);
          var nav = target.parents('ul');
          var index = target.attr('class').match(/o(\d*)/)[1];
          if(this.activeImage == index)
            return;
          $(this.matchedObjects.get(index)).click();
        }, params.settings));
      }
      nav.find('li:first').addClass('first');
      nav.find('li:last').addClass('last');
      $(params.parent).find('.lightbox-container-image').hover(
        $.proxy(function(e) {
          if(this.timer) clearTimeout(this.timer);
          this._playTimeout = this.playTimeout;
          this.playTimeout = false;
          $(e.currentTarget).find('.lightbox-contentswitcher-nav').addClass('over');
          $(e.currentTarget).find('.lightbox-contentswitcher-nav > li:not(.current)').fadeTo(this.contentswitcher.fadeSpeed, this.contentswitcher.overOpacity);
          $(e.currentTarget).find('.lightbox-contentswitcher-nav > li.current').fadeTo(this.contentswitcher.fadeSpeed, this.contentswitcher.overCurrentOpacity);
        }, params.settings), 
        $.proxy(function(e) {
          this.playTimeout = this._playTimeout;
          if(this.playTimeout) {
            this.timer = setTimeout($.proxy(function() {
              $(this.settings.matchedObjects.get((this.settings.activeImage+1) % this.settings.matchedObjects.size())).click();
            }, {parent: $(e.currentTarget), settings: this}), this.playTimeout);
          }
          $(e.currentTarget).find('.lightbox-contentswitcher-nav').removeClass('over');
          $(e.currentTarget).find('.lightbox-contentswitcher-nav > li:not(.current)').fadeTo(this.contentswitcher.fadeSpeed, this.contentswitcher.baseOpacity);
          $(e.currentTarget).find('.lightbox-contentswitcher-nav > li.current').fadeTo(this.contentswitcher.fadeSpeed, this.contentswitcher.currentOpacity);
        }, params.settings)
      );
    },
    preSetImageToView: function(params) {
      var over = $(params.parent).find('.lightbox-contentswitcher-nav').hasClass('over');
      $(params.parent).find('.lightbox-contentswitcher-nav > li').removeClass('current').fadeTo(params.settings.contentswitcher.fadeSpeed, over ? params.settings.contentswitcher.overOpacity : params.settings.contentswitcher.baseOpacity);
      $(params.parent).find('.lightbox-contentswitcher-nav > li:eq('+params.settings.activeImage+')').addClass('current').fadeTo(params.settings.contentswitcher.fadeSpeed, over ? params.settings.contentswitcher.overCurrentOpacity : params.settings.contentswitcher.currentOpacity);
    }
  }
  
  $(document).ready(function() {
    $('.contentswitcher.full li').inlineLightBox($.extend(contentswitcher, inlinelightbox.settings['raptus_article_contentswitcher']));
    $('.contentswitcher.full > ul').hide();
    $('.contentswitcher.teaser li').inlineLightBox($.extend(contentswitcher, inlinelightbox.settings['raptus_article_contentswitcher_teaser']));
    $('.contentswitcher.teaser > ul').hide();
  });
})(jQuery);
