$(document).ready(function () {
  console.log('script loaded');


  $("#search-form").submit(function (e) {
    e.preventDefault();
    $.ajax({
      url: "/user/search",
      method: "POST",
      data: $(this).serialize(),
      success: function (serverResponse) {
        console.log("try to pull new data");
        $("#pages-data").html(serverResponse);
        console.log("pulled data");
      },
    });
    // $(this).trigger('reset')
  });

  $("#pages-data").on('click','a', function (e) {
    console.log('start pagination')
    e.preventDefault();
    page_no = $(this).attr('no');
    $.ajax({
      url: "/user/page/" + page_no,
      method: "GET",
      data: $(this).attr("no"),
      success: function (serverResponse) {
        console.log("about to try to change page");
        $("#pages-data").html(serverResponse);
        console.log('did the page change now');
      },
    });    
  });



});
