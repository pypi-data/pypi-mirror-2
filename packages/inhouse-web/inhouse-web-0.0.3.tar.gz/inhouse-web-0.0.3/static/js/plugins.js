// remap jQuery to $
(function($){
  $(".default-table tr").mouseover(function() {
      if ( !$(this).hasClass("sum") ) {
        $(this).addClass("over");
      }
    }).mouseout(function() {
      $(this).removeClass("over");
    });
  $(".default-table tr:even").addClass("alt");
  $(".timer-table tr").mouseover(function() {$(this).addClass("over");}).mouseout(function() {$(this).removeClass("over");});
  $(".timeline-list li").mouseover(function() {$(this).addClass("over");}).mouseout(function() {$(this).removeClass("over");});
})(window.jQuery);



// usage: log('inside coolFunc',this,arguments);
// paulirish.com/2009/log-a-lightweight-wrapper-for-consolelog/
window.log = function(){
  log.history = log.history || [];   // store logs to an array for reference
  log.history.push(arguments);
  if(this.console){
    console.log( Array.prototype.slice.call(arguments) );
  }
};

// catch all document.write() calls
(function(){
  var docwrite = document.write;
  document.write = function(q){
    log('document.write(): ',q);
    if (/docwriteregexwhitelist/.test(q)) docwrite(q);
  }
})();

// background image cache bug for ie6. www.mister-pixel.com/#Content__state=
/*@cc_on   @if (@_win32) { document.execCommand("BackgroundImageCache",false,true) }   @end @*/
