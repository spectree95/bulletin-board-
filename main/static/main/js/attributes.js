const subcategorySelect = document.getElementById("id_subcategory");
const attributesContainer = document.getElementById("attributes");
let additionalInformation = document.querySelector(".additional-information")

const attributeScript = document.getElementById("attribute-values");

const attributeValues = attributeScript
    ? JSON.parse(attributeScript.textContent)
    : {};


function loadattributes(){
    const subcategoryId = subcategorySelect.value

    if (!subcategoryId){
        additionalInformation.style.display = "none";
        attributesContainer.innerHTML = "";
        return;
    }
    additionalInformation.style.display = "flex";
    fetch(`/ajax/load-attributes/?subcategory=${subcategoryId}`)
        
        .then(response => response.json())
        .then(data => {
            attributesContainer.innerHTML = "";


            data.forEach(attr => {
                const div = document.createElement("div");

                div.style.padding = "0";

                const name = document.createElement("h5");
                name.style.fontSize = "14px"
                name.type = "text";
                name.textContent = attr.name;

                const input = document.createElement("input");
                input.type = "text";
                input.name = `attribute_${attr.id}`;
                if (attributeValues[attr.id]){
                    input.value = attributeValues[attr.id]
                }
                input.style.border = "1.5px solid gray"
                input.style.borderRadius = "3px"
                input.style.marginBottom = "10px"
                input.style.paddingLeft = "10px"
                div.appendChild(name);
                div.appendChild(input);

                attributesContainer.appendChild(div);
            });
                    
        });
}


subcategorySelect.addEventListener("change", loadattributes);

loadattributes();
    
   