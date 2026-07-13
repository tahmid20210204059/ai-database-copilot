/*
AI DATABASE COPILOT
OWNER ACCESS GUARD
*/

(function(){
    const LOGIN_URL = "login.html";
    const USER_DASHBOARD_URL = "dashboard.html";

    window.__adminAccessGranted = false;

    function getCurrentPage(){
        return window.location.pathname.split("/").pop();
    }

    function redirectTo(target){
        if(getCurrentPage() === target){
            return;
        }

        window.location.href = target;
    }

    function populateAdminChrome(user){
        const adminName = document.getElementById("adminName");
        const adminRole = document.getElementById("adminRole");
        const adminAvatar = document.getElementById("adminAvatar");

        if(adminName){
            adminName.textContent = user.name || "Admin";
        }

        if(adminRole){
            adminRole.textContent = "Owner";
        }

        if(adminAvatar){
            adminAvatar.textContent = window.getInitials(user.name);
        }

        window.setUserSession(window.getToken(), user);
    }

    function revealAdminShell(){
        const shell = document.getElementById("adminShell");

        if(shell){
            shell.classList.remove("is-loading");
            shell.classList.add("is-ready");
        }
    }

    function bindLogout(){
        const logoutButtons = document.querySelectorAll(
            "#adminLogoutBtn, #adminSidebar [data-action='logout']"
        );

        logoutButtons.forEach(function(button){
            if(button.dataset.bound === "true"){
                return;
            }

            button.dataset.bound = "true";
            button.addEventListener("click", function(event){
                event.preventDefault();
                window.logout();
            });
        });
    }

    async function protectOwnerPage(){
        const user = await window.getCurrentUser();

        if(!user){
            redirectTo(LOGIN_URL);
            return;
        }

        if(user.role !== "owner"){
            redirectTo(USER_DASHBOARD_URL);
            return;
        }

        window.__adminAccessGranted = true;
        populateAdminChrome(user);
        bindLogout();

        if(typeof window.initializeAdminNavigation === "function"){
            window.initializeAdminNavigation(user);
        }

        if(typeof window.initializeAdminPage === "function"){
            try{
                window.initializeAdminPage(user);
            }
            catch(error){
                console.error("Admin page initialization error:", error);
            }
        }

        if(typeof window.loadAdminDashboardStats === "function"){
            const statsResult = window.loadAdminDashboardStats(window.getToken(), user);

            if(statsResult && typeof statsResult.catch === "function"){
                statsResult.catch(function(error){
                    console.error("Admin stats error:", error);
                });
            }
        }

        revealAdminShell();
    }

    document.addEventListener("DOMContentLoaded", protectOwnerPage);
})();
