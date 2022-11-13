// Change navbar depending on scroll
var scrollSpy = new bootstrap.ScrollSpy(document.body, {
    target: '#navbar'
});

// Section animations depending on scroll
// https://alvarotrigo.com/blog/css-animations-scroll/
let allHeaders = document.querySelectorAll("h2");

function animateScroll() {
    for (let i = 0; i < allHeaders.length; i++) {
        var windowHeight = window.innerHeight;
        var elementTop = allHeaders[i].getBoundingClientRect().top;
        var elementVisible = 150;
        if (elementTop < windowHeight - elementVisible) {
          allHeaders[i].classList.add("scrolled");
        } else {
          allHeaders[i].classList.remove("scrolled");
        }
    }
}

window.addEventListener("scroll", animateScroll);