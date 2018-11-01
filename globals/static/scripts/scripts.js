

    let sidebar = document.getElementById("snailXSidebar");
    let popup = document.getElementById("popup");

function displaySnailXUserInfo() {
    sidebar.style.display = "none";
    if (popup.style.display === "none") {
        popup.style.display = "block";
    } else {
        popup.style.display = "none";
    }
}

function displaySnailXSidebar() {
    popup.style.display = "none";
    if (sidebar.style.display === "none") {
        sidebar.style.display = "block";
    } else {
        sidebar.style.display = "none";
    }
}