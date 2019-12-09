;function myAccFunc(){var x=document.getElementById("demoAcc");if(x.className.indexOf("w3-show")==-1){x.className+=" w3-show";}else{x.className=x.className.replace(" w3-show","");}}
function send(action){if(action=='all'){Notiflix.Loading.Hourglass('讀取中....');window.location.href='/softwayliving/checkreservation/'}else if(action=='sidebar_member_list'){Notiflix.Loading.Hourglass('讀取中....');window.location.href='/softwayliving/member_list/'}else if(action=='sidebar_product_list'){Notiflix.Loading.Hourglass('讀取中....');window.location.href='/softwayliving/productions/'}else if(action=='sidebar_store_list'){Notiflix.Loading.Hourglass('讀取中....');window.location.href='/softwayliving/stores/'}else if(action=='sidebar_admin_reservation'){Notiflix.Loading.Hourglass('讀取中....');window.location.href='/softwayliving/reservation/'}else if(action=='sidebar_log_out'){Notiflix.Loading.Hourglass('讀取中....');window.location.href='/softwayliving/logout/'}};/*!
 *  jQuery sidebar plugin
 *  ---------------------
 *  A stupid simple sidebar jQuery plugin.
 *
 *  Developed with <3 and JavaScript by the jillix developers.
 *  Copyright (c) 2013-15 jillix
 * */(function($){$.fn.sidebar=function(options){var self=this;if(self.length>1){return self.each(function(){$(this).sidebar(options);});}
var width=self.outerWidth();var height=self.outerHeight();var settings=$.extend({speed:200,side:"left",isClosed:false,close:true},options);/*!
         *  Opens the sidebar
         *  $([jQuery selector]).trigger("sidebar:open");
         * */self.on("sidebar:open",function(ev,data){var properties={};properties[settings.side]=0;settings.isClosed=null;self.stop().animate(properties,$.extend({},settings,data).speed,function(){settings.isClosed=false;self.trigger("sidebar:opened");});});/*!
         *  Closes the sidebar
         *  $("[jQuery selector]).trigger("sidebar:close");
         * */self.on("sidebar:close",function(ev,data){var properties={};if(settings.side==="left"||settings.side==="right"){properties[settings.side]=-self.outerWidth();}else{properties[settings.side]=-self.outerHeight();}
settings.isClosed=null;self.stop().animate(properties,$.extend({},settings,data).speed,function(){settings.isClosed=true;self.trigger("sidebar:closed");});});/*!
         *  Toggles the sidebar
         *  $("[jQuery selector]).trigger("sidebar:toggle");
         * */self.on("sidebar:toggle",function(ev,data){if(settings.isClosed){self.trigger("sidebar:open",[data]);}else{self.trigger("sidebar:close",[data]);}});function closeWithNoAnimation(){self.trigger("sidebar:close",[{speed:0}]);}
if(!settings.isClosed&&settings.close){closeWithNoAnimation();}
$(window).on("resize",function(){if(!settings.isClosed){return;}
closeWithNoAnimation();});self.data("sidebar",settings);return self;};$.fn.sidebar.version="3.3.2";})(jQuery);