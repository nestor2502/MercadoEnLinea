$(document).ready(function() {
    let t = document.getElementById("NZoomImg"), e = t.getAttribute("data-NZoomscale") <= 0 ? 1 : t.getAttribute("data-NZoomscale"), s = t.clientWidth, o = t.clientHeight;
    $("#NZoomImg").replaceWith('<div id="NZoomContainer">' + t.outerHTML + "</div>");
    let i = $("#NZoomContainer"), n = $("#NZoomImg");
    i.css("width", s + "px"), i.css("height", o + "px"), i.mousemove(function(t) {
        let e = $(this).offset(), i = (t.pageX - e.left) / s * 100 <= 100 ? (t.pageX - e.left) / s * 100 : 100, c = (t.pageY - e.top) / o * 100 <= 100 ? (t.pageY - e.top) / o * 100 : 100;
        n.css("transform-origin", i + "% " + c + "%")
    }), i.mouseenter(function() {
        n.css("cursor", "crosshair"), n.css("width", s + "px"), n.css("height", o + "px"), n.css("transition", "0.2s"), n.css("transform", "scale(" + e + ")")
    }).mouseleave(function() {
        n.css("transition", "0.2s"), n.css("transform", "scale(1)")
    })
});