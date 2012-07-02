/* Author:

*/

$(document).ready(function() {
   $('ul.dropdown-menu > li.active > a > i').addClass('icon-white');
   $('ul.dropdown-menu > li').not('.active').hover(function(){
    $(this).find('a > i').addClass('icon-white');
   },function() {
    $(this).find('a > i').removeClass('icon-white');
   });
});





