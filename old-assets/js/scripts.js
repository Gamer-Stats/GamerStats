let dropdown = document.getElementsByClassName("dropdown");
let ham = document.getElementsByClassName("hamburg")[0];
let close = document.getElementsByClassName("close");
let i;

for (i = 0; i < dropdown.length; i++) {
    dropdown[i].addEventListener("click", function () {
        this.classList.toggle("active");
        if (!ham.classList.contains("active")) {
            ham.setAttribute("aria-expanded", false);
            ham.setAttribute("aria-label", "Open main menu");
        } else {
            ham.setAttribute("aria-expanded", true);
            ham.setAttribute("aria-label", "Close main menu");
        }

        let panel = this.nextElementSibling;
        if (panel.style.maxHeight) {
            panel.style.maxHeight = null;
        } else {
            panel.style.maxHeight = panel.scrollHeight + "px";
        }
    });
}

close[0].addEventListener("click", () => {
    document.getElementsByClassName("sub-menu")[0].style.maxHeight = null;
})
