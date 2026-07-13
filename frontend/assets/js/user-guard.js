/*
AI DATABASE COPILOT
USER ROLE ACCESS GUARD
*/

const USER_ALLOWED_PAGES = [
    "dashboard.html",
    "connections.html",
    "query.html",
    "history.html",
    "profile.html"
];

async function protectUserPage(){
    const user = await window.getCurrentUser();

    if(!user){
        window.location.href = "login.html";
        return;
    }

    if(user.role !== "user"){
        if(user.role === "owner"){
            window.location.href = "admin-dashboard.html";
            return;
        }

        window.location.href = "login.html";
        return;
    }

    const currentPage = window.location.pathname.split("/").pop();

    if(!USER_ALLOWED_PAGES.includes(currentPage)){
        window.location.href = "dashboard.html";
    }
}

document.addEventListener("DOMContentLoaded", function(){
    protectUserPage();
});
