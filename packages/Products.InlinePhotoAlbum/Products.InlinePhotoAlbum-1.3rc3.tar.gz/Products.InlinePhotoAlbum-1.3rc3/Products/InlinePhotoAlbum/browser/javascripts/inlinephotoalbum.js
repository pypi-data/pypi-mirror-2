/**
 * ALL JAVASCRIPT NEEDS TO BE IN SEPARATE NAMESPACES
 * inlinephotoalbum namespace 
 */

var inlinephotoalbum = {

    setup: function() {

        jq('a.InlinePhotoAlbum').each(function() {
            var placeholder = this;
            jq.ajax({
                url : jq(this).attr("href") + "/@@inline-bare-photoalbum",
                type: 'GET',
                asynchronous: true,
                complete: function(request) {
                    if (request.status == 200) {
                        var content = jq("<div class='InlinePhotoAlbum'>" + request.responseText + "<div class='visualClear'><!-- --></div></div>");
                        jq(placeholder).replaceWith(content);
                        inlinephotoalbum.setupLightBox();
                        inlinephotoalbum.handleNavigationBar();
                    }
                }
            });
        });

    }, // end of setup

    handleNavigationBar: function() {
        jq('.inline-photo-album .listingBar a').click(function(event) {
          event.preventDefault();
          var placeholder = jq(this).parents('div.InlinePhotoAlbum')
          
          jq.ajax({
              url: this.href,
              type: 'GET',
              asynchronous: true,
              complete: function(request) {
                  if (request.status == 200) {
                      var content = jq("<div class='InlinePhotoAlbum'>" + request.responseText + "<div class='visualClear'><!-- --></div></div>");
                      placeholder.replaceWith(content);
                      inlinephotoalbum.setupLightBox();
                      inlinephotoalbum.handleNavigationBar();
                  }
              }
          })
       });
    },

    setupLightBox: function() {
        jq('.inline-photo-album a.lightbox').lightBox({
            imageLoading: '++resource++Products.InlinePhotoAlbum.images/lightbox-ico-loading.gif',
            imageBtnClose: '++resource++Products.InlinePhotoAlbum.images/lightbox-btn-close.gif',
            imageBtnPrev: '++resource++Products.InlinePhotoAlbum.images/lightbox-btn-prev.gif',
            imageBtnNext: '++resource++Products.InlinePhotoAlbum.images/lightbox-btn-next.gif',
            imageBlank: '++resource++Products.InlinePhotoAlbum.images/lightbox-blank.gif',
            txtOf: '/'
        });

    } // end of setupLightBox
}

jq(document).ready(function() {
    inlinephotoalbum.setup();
    inlinephotoalbum.setupLightBox();
    inlinephotoalbum.handleNavigationBar();
});

