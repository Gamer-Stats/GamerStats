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

const showNotice = () => {
    document.getElementsByClassName("copied")[0].classList.remove("hidden");
}

const hideNotice = () => {
    document.getElementsByClassName("copied")[0].classList.add("hidden");
}

const noticeClose = () => {
    document.getElementsByClassName("copied")[0].classList.add("hidden");
}

function copy() {
    let pageLink = document.querySelector("#pageLink");
    pageLink.select();
    document.execCommand("copy");
    showNotice();
    setTimeout(hideNotice, 2000)
}

document.querySelector("#copyLink").addEventListener("click", copy);


function shareMe() {
    window.open('https://google.com', 'popup', 'width=600,height=600');
    return false;
}

const scrollLeftBtn = document.getElementById('scrollLeft');
const scrollRightBtn = document.getElementById('scrollRight');

scrollRightBtn.onclick = function () {
    document.getElementById('scrollBtns').scrollLeft += 20;
};
scrollLeftBtn.onclick = function () {
    document.getElementById('scrollBtns').scrollLeft -= 20;
};