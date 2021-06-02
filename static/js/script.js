$(document).ready(function(){
    $('.sidenav').sidenav();
    $('.carousel').carousel();
    $('select').formSelect();
    $('.modal').modal();
  });

  // function to add a back button at the bottom of the display book page
  // inspiration from https://stackoverflow.com/questions/31347882/back-button-with-javascript-jquery
$( "#back-btn" ).click(function() {
  window.history.back();
});
