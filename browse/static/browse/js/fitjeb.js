$(document).ready(function() {
$('.nav li a[href="' + this.location.pathname + '"]').parent().addClass('active');
});

$(".nav li a").on("click", function(){
$(".nav").find(".active").removeClass("active");
$(this).parent().addClass("active");
});
