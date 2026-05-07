const subcategorySelect = document.getElementById("id_subcategory");
const attributesContainer = document.getElementById("attributes");
let additionalInformation = document.querySelector(".additional-information")

subcategorySelect.addEventListener("change", function () {
    const subcategoryId = this.value;

    fetch(`ajax/load-attributes/?subcategory=${subcategoryId}`)
        
        .then(response => response.json())
        .then(data => {
            attributesContainer.innerHTML = "";


            data.forEach(attr => {
                const div = document.createElement("div");

                const label = document.createElement("label");
                

                const input = document.createElement("input");
                input.type = "text";
                input.name = `attribute_${attr.id}`;
                input.placeholder = attr.name;
                input.style.border = "1.5px solid gray"
                input.style.borderRadius = "3px"
                input.style.marginBottom = "10px"
                input.style.paddingLeft = "10px"
                div.appendChild(label);
                div.appendChild(input);

                attributesContainer.appendChild(div);
            });
                    
        });
    if (subcategoryId){
        additionalInformation.style.display = "flex";
    }else{
        additionalInformation.style.display = "none";
    } 
});