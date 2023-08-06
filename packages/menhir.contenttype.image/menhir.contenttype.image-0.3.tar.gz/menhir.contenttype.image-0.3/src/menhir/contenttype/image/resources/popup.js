$(document).ready(function() {
   $("a.image-link").slimbox({
	overlayOpacity: 0,
        overlayFadeDuration: 1,
	imageFadeDuration: 1,
        resizeDuration: 300,
	easing: "easeOutElastic",
	captionAnimationDuration: 1,
	counterText: "{x}/{y}",
	closeKeys: [27, 70],
	nextKeys: [39, 83]
   });
});
