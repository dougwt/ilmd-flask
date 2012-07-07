/* Author:

*/

$(document).ready(function() {
  $('ul.dropdown-menu > li.active > a > i').addClass('icon-white');
  $('ul.dropdown-menu > li').not('.active').hover(function(){
    $(this).find('a > i').addClass('icon-white');
  },function() {
    $(this).find('a > i').removeClass('icon-white');
  });

  //Function to preload images
  function preload_images(images_array)
  {
    $(images_array).each(function () {
      $('<img />').attr('src',this).appendTo('body').css('display','none');
    });
  }

  //Define an array of images
  var my_images = ['static/img/glyphicons-halflings.png',
                   'static/img/glyphicons-halflings-white.png'];

  //Call the function on the array of images
  preload_images(my_images);
});





