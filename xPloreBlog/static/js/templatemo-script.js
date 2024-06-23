$(function () {
  $(".navbar-toggler").on("click", function (e) {
    $(".tm-header").toggleClass("show");
    e.stopPropagation();
  });

  $("html").click(function (e) {
    var header = document.getElementById("tm-header");
    console.log("HTML Clicked");
    console.log(e.target);

    if (!header.contains(e.target)) {
      console.log(e.target);
      $(".tm-header").removeClass("show");
    }
  });

  $("#tm-nav .tm-nav-link").click(function (e) {
    console.log("Click Function");
    $(".tm-header").removeClass("show");
  });
});
