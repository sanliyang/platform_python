function allowDrop(event) {
    event.preventDefault();
}

function drag(event, algorithmName) {
    let div_name = document.getElementById(algorithmName);
    event.dataTransfer.setData("text", div_name.innerText);
}

function toggleSubMenu(element) {
    const submenu = element.nextElementSibling;
    submenu.style.display = (submenu.style.display === 'block') ? 'none' : 'block';
}

function drop(event) {
    event.preventDefault();
    var algorithmName = event.dataTransfer.getData("text");
    var algorithmBlock = document.createElement("div");
    algorithmBlock.className = "algorithm-block-bak";
    algorithmBlock.innerText = algorithmName;

    let icon1 = document.createElement("img");
    icon1.src = "/static/icon/icon-add.svg";
    icon1.className = "icon-center";

    let icon2 = document.createElement("img");
    icon2.src = "/static/icon/icon-delete.svg";
    icon2.className = "icon-right";

    let icon3 = document.createElement("img");
    icon3.src = "/static/icon/icon-vip.svg";
    icon3.className = "icon-left";

    algorithmBlock.appendChild(icon1);
    algorithmBlock.appendChild(icon2);
    algorithmBlock.appendChild(icon3);


    algorithmBlock.style.left = (event.clientX - event.target.getBoundingClientRect().left - event.target.clientLeft - algorithmBlock.offsetWidth / 2) + "px";
    algorithmBlock.style.top = (event.clientY - event.target.getBoundingClientRect().top - event.target.clientTop - algorithmBlock.offsetHeight / 2) + "px";

    event.target.appendChild(algorithmBlock);

    algorithmBlock.addEventListener("mousedown", startDrag);
    algorithmBlock.addEventListener("mouseup", stopDrag);
}

var selectedAlgorithm = null;
var offset = {x: 0, y: 0};

function startDrag(event) {
    selectedAlgorithm = event.target;
    offset.x = event.clientX - selectedAlgorithm.getBoundingClientRect().left;
    offset.y = event.clientY - selectedAlgorithm.getBoundingClientRect().top;

    document.addEventListener("mousemove", dragAlgorithm);
}

function stopDrag() {
    selectedAlgorithm = null;
    document.removeEventListener("mousemove", dragAlgorithm);
}

function dragAlgorithm(event) {
    if (selectedAlgorithm) {
        selectedAlgorithm.style.left = (event.clientX - offset.x - canvas.getBoundingClientRect().left) + "px";
        selectedAlgorithm.style.top = (event.clientY - offset.y - canvas.getBoundingClientRect().top) + "px";
    }
}

window.addEventListener("load", function () {
    var sidebar = document.getElementById("sidebar");
    var algorithmBlocks = sidebar.getElementsByClassName("algorithm-block-bak");
    var totalHeight = 0;

    for (var i = 0; i < algorithmBlocks.length; i++) {
        algorithmBlocks[i].style.top = i * (algorithmBlocks[i].offsetHeight + 10) + "px";
        totalHeight += algorithmBlocks[i].offsetHeight + 10;
    }

    sidebar.style.minHeight = totalHeight + "px";
});
