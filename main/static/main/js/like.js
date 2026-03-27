const like = document.querySelector(".like");

like.addEventListener("click", function () {
    let productID = this.dataset.productId;
    let url = this.dataset.url;
    fetch(url,{
        method: "POST",
        headers: {
            "X-CSRFToken" : getCookie("csrftoken"),
            "Content-Type": "application/x-www-form-urlencoded" 
        },
        body: "pk=" + productID 

    })
    .then(res => res.json())
    .then(data => {
        this.src = data.favorited ? this.dataset.redHeart : this.dataset.blackHeart;
    });
});



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}