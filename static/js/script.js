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

// function to replace cover image with the default logo if link is broken
// code got from 

$("img").on("error", function () {
    $(this).attr("src", "static/images/our-lockdown-reads-logo-reworked.png");
});

