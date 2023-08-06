/*
 * toggle_sections.js
 * ~~~~~~~~~~~~~~
 *
 * Sphinx JavaScript helper for collapsible sections.
 * looks for sections with css class "html-toggle", with optional addtional classes "expanded" or "collapsed" (defaults to "collapsed")
 *
 * :copyright: Copyright 2011 by Assurance Technologies
 * :license: BSD
 *
 * NOTE: while this provides full javascript instrumentation, css styling should be applied to .html-toggle > .html-toggle-button
 */

$(document).ready(function (){
  function init(){
    var jobj = $(this);
    var parent = jobj.parent();
    if(!parent.hasClass("expanded")){
      parent.addClass("collapsed").children().hide();
      jobj.show();
    }
    jobj.addClass("html-toggle-button");
  }

  function toggle(){
    var jobj = $(this);
    var parent = jobj.parent();
    if(parent.hasClass("collapsed")){
      parent.addClass("expanded").removeClass("collapsed");
      parent.children().show();
    }else{
      parent.children().hide();
      jobj.show();
      parent.addClass("collapsed").removeClass("expanded");
    }
  }

  $(".html-toggle.section > h2, .html-toggle.section > h3, .html-toggle.section > h4, .html-toggle.section > h5, .html-toggle.section > h6").click(toggle).each(init);

});
