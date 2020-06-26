function showDetails(event){
    document.getElementById("full-info").style.display = "initial";
    event.currentTarget.innerHTML = "<span class=icon>&#x2BC5;</span>Hide details";
    event.currentTarget.removeEventListener("click", showDetails)
    event.currentTarget.addEventListener("click", function(event){
        hideDetails(event);
    });
}

function hideDetails(event){
    document.getElementById("full-info").style.display = "none";
    event.currentTarget.innerHTML = "<span class=icon>&#x2BC6;</span>More details";
    event.currentTarget.addEventListener("click", function(event){
        showDetails(event);
    });
}

document.getElementById("advanced-options").addEventListener("click", showDetails);
