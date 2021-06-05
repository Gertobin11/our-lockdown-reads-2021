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
// code got from https://css-tricks.com/snippets/jquery/better-broken-image-handling/

$("img").on("error", function () {
    $(this).attr("src", "https://media.istockphoto.com/vectors/old-book-cover-vector-id1094620944?k=6&m=1094620944&s=612x612&w=0&h=fEqo1TbdxYj3aGqpC0aMqsYx8DPGN7RzZAn6pdO08QM=");
});

