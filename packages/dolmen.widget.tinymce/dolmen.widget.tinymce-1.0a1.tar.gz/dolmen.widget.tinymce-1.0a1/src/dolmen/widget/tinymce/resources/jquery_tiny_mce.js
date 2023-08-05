$('form').bind('form-pre-serialize', function(e) {
    tinyMCE.triggerSave();
});

$.fn.tinymce = function(){
    return this.each(function(){
        // I don't think the style declaration is not really used in this sense, but I left it anyway
        preString = "<div class='jqHTML_frame' style='width:"+$(this).css("width")+"px;height:" + ($(this).css("height")+20) + "px;'>";
        postString = "</div>";
        $(this).wrap(preString + postString);

        // this comes last to avoid IE7 bug
        tinyMCE.execCommand('mceAddControl', false, $(this).attr('id'));
    });
}

function initMCE()
{
    tinyMCE.init({ mode : "none",
       theme : "advanced",
       plugins : "advhr,advlink,style",
       theme_advanced_layout_manager : "SimpleLayout",
       theme_advanced_disable: "",
       theme_advanced_buttons1: "pasteword,justifyleft,justifycenter,justifyright,justifyfull,separator,removeformat,separator,charmap,advhr,separator,styleprops",
       theme_advanced_buttons2: "styleselect,bold,italic,underline,separator,link,separator,bullist,numlist,outdent,indent,",
       theme_advanced_buttons3: "",
       theme_advanced_toolbar_location : "top",
       theme_advanced_toolbar_align : "left",
       content_css : "css/content.css"});
}
// initialize tiny mce
initMCE();
