/*
AI DATABASE COPILOT
COMPONENT ENGINE
*/


const componentBaseUrl =
    document.currentScript?.src
        ? new URL(
            "../../components/",
            document.currentScript.src
        )
        : new URL(
            "../components/",
            window.location.href
        );


function escapeHtml(
    value
){

    return String(
        value ?? ""
    )
    .replace(
        /&/g,
        "&amp;"
    )
    .replace(
        /</g,
        "&lt;"
    )
    .replace(
        />/g,
        "&gt;"
    )
    .replace(
        /"/g,
        "&quot;"
    )
    .replace(
        /'/g,
        "&#039;"
    );

}




function showToast(
    message,
    type="success"
){


    const toast =
    document.createElement(
        "div"
    );


    toast.className =
    `toast toast-${type}`;


    toast.innerText =
    message;


    document.body.appendChild(
        toast
    );


    setTimeout(()=>{


        toast.style.opacity="0";


        setTimeout(()=>{

            toast.remove();

        },200);


    },3000);


}






function showLoader(
    element
){

    if(!element)
    return;


    element.innerHTML =
    `
    <div class="ui-loader"></div>
    `;

}





function hideLoader(
    element
){

    if(!element)
    return;


    element.innerHTML="";

}









async function loadComponent(
    element
){

    const name =
    element.dataset.component;


    if(
        !name ||
        element.dataset.componentLoaded === "true"
    )
    return;



    element.dataset.componentLoaded =
    "true";



    try{


        const response =
        await fetch(
            new URL(
                `${name}.html`,
                componentBaseUrl
            )
        );



        if(!response.ok){

            throw new Error(
                `Failed to load component "${name}" (${response.status})`
            );

        }




        let html =
        await response.text();




        html =
        html.replace(
            /{{(.*?)}}/g,
            (_,key)=>{

                return escapeHtml(
                    element.dataset[key.trim()]
                );

            }
        );





        if(
            element.dataset.replace === "true"
        ){

            element.outerHTML =
            html;

        }
        else
        {

            element.innerHTML =
            html;

        }



    }


    catch(error){


        element.dataset.componentLoaded =
        "false";


        console.error(
            "Component load failed:",
            error
        );


    }


}









function hydrateComponents(
    root=document
){


    const components =
    root.querySelectorAll(
        "[data-component]"
    );



    components.forEach(
        component=>{


            loadComponent(
                component
            );


        }
    );


}








function initComponents(){

    hydrateComponents();

}







if(
    document.readyState === "loading"
)
{

    document.addEventListener(
        "DOMContentLoaded",
        initComponents,
        {
            once:true
        }
    );


}
else
{

    initComponents();

}
