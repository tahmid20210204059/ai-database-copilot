/*
=====================================
AI DATABASE COPILOT
COMPONENT UTILITIES
=====================================
*/



function showToast(
    message,
    type="success"
){


    const toast =
    document.createElement("div");



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