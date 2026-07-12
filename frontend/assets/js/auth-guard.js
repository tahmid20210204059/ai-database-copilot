/*
AI DATABASE COPILOT
AUTH GUARD SYSTEM
*/


(function(){


const token =
localStorage.getItem(
    "access_token"
);



const currentPage =
window.location.pathname;



const isLoginPage =
currentPage.includes(
    "login.html"
);



if(
    !token &&
    !isLoginPage
){

    window.location.href =
    "login.html";

}



})();