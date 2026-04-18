const likes = document.querySelectorAll(".like");

likes.forEach(like => {

    like.addEventListener("click", function () {
        let productID = this.dataset.productId;
        let url = this.dataset.url;
        fetch(url,{
            method: "POST",
            credentials: "same-origin",
            headers: {
                "X-CSRFToken" : getCookie("csrftoken"),
                "Content-Type": "application/x-www-form-urlencoded" 
            },
            body: "pk=" + productID 
    
        })
        .then(res => {
            if (res.status === 401) {
                window.location.href = "/users/login/";
                return null;
        }
            return res.json();
        })
        .then(data => {
            if (!data) return;
    
            this.src = data.favorited
                ? this.dataset.redHeart
                : this.dataset.blackHeart;
        });
    });
})



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