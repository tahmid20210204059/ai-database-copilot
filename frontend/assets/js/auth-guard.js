/*
AI DATABASE COPILOT
AUTH GUARD SYSTEM
*/

(function(){
    const currentPage = window.location.pathname.split("/").pop();

    if(currentPage === "login.html"){
        return;
    }

    if(!window.getToken || !window.getToken()){
        window.location.href = "login.html";
    }
})();
