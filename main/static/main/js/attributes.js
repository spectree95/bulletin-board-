const subcategorySelect = document.getElementById("id_subcategory");
const attributesContainer = document.getElementById("attributes");

subcategorySelect.addEventListener("change", function () {
    const subcategoryId = this.value;

    fetch(`ajax/load-attributes/?subcategory=${subcategoryId}`)
        .then(response => response.json())
        .then(data => {
            attributesContainer.innerHTML = "";

            data.forEach(attr => {
                const div = document.createElement("div");

                const label = document.createElement("label");
                label.textContent = attr.name;

                const input = document.createElement("input");
                input.type = "text";
                input.name = `attribute_${attr.id}`;

                div.appendChild(label);
                div.appendChild(input);

                attributesContainer.appendChild(div);
            });
        });
});