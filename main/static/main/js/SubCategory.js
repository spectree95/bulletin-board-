document.getElementById("id_category").addEventListener("change", function () {

    let categoryId = this.value;

    fetch(`/ajax/load-subcategories/?category=${categoryId}`)
        .then(response => response.json())
        .then(data => {

            let subSelect = document.getElementById("id_subcategory");
            subSelect.innerHTML = "";

            let placeholder = document.createElement("option");
            placeholder.value = "";
            placeholder.textContent = "Выберите подкатегорию";
            placeholder.selected = true;
            placeholder.hidden = true;
            subSelect.appendChild(placeholder);


            data.forEach(function(sub) {
                let option = document.createElement("option");
                option.value = sub.id;
                option.textContent = sub.name;
                subSelect.appendChild(option);
            });

        });
});