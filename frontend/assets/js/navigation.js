/*
AI DATABASE COPILOT
NAVIGATION SYSTEM
*/

(function(){
    const USER_MENU_ITEMS = [
        { label: "Dashboard", href: "dashboard.html" },
        { label: "Database Connections", href: "connections.html" },
        { label: "AI Query", href: "query.html" },
        { label: "History", href: "history.html" },
        { label: "Profile", href: "profile.html" },
        { label: "Logout", href: "#logout", action: "logout" },
    ];

    const OWNER_MENU_ITEMS = [
        { label: "Admin Dashboard", href: "admin-dashboard.html" },
        { label: "Users", href: "admin-users.html" },
        { label: "Databases", href: "admin-connections.html" },
        { label: "Analytics", href: "admin-analytics.html" },
        { label: "Logout", href: "#logout", action: "logout" },
    ];

    function getCurrentPage(){
        return window.location.pathname.split("/").pop();
    }

    function getRoleLabel(role){
        return role === "owner" ? "Owner" : "User";
    }

    function getInitials(name){
        return typeof window.getInitials === "function"
            ? window.getInitials(name)
            : "AD";
    }

    function getMenuRoot(role){
        if(role === "owner"){
            return document.querySelector("#adminSidebar .menu");
        }

        const userSidebar = document.querySelector('[data-navigation-shell="user"] .menu');

        if(userSidebar){
            return userSidebar;
        }

        return document.querySelector(".sidebar .menu");
    }

    function getNavbarRoot(role){
        if(role === "owner"){
            return document.getElementById("adminNavbar") || document.querySelector(".navbar");
        }

        return document.querySelector('[data-navigation-shell="user"]') || document.querySelector(".navbar");
    }

    function createMenuItem(item, currentPage){
        const link = document.createElement("a");

        link.href = item.href;
        link.className = "menu-item";
        link.textContent = item.label;

        if(item.action){
            link.dataset.action = item.action;
        }

        const itemPage = item.href.split("/").pop();

        if(itemPage === currentPage && !item.action){
            link.classList.add("active");
        }

        return link;
    }

    function setActiveNavigationLink(root = document){
        const currentPage = getCurrentPage();

        root.querySelectorAll(".menu-item").forEach(function(link){
            if(link.dataset.action === "logout"){
                link.classList.remove("active");
                return;
            }

            const href = link.getAttribute("href") || "";
            const page = href.split("/").pop();
            link.classList.toggle("active", page === currentPage);
        });
    }

    function bindLogoutControls(root = document){
        root.querySelectorAll("[data-action='logout'], [data-logout-button], #adminLogoutBtn").forEach(function(button){
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

    function renderMenu(role){
        const menuRoot = getMenuRoot(role);

        if(!menuRoot){
            return;
        }

        const currentPage = getCurrentPage();
        const items = role === "owner" ? OWNER_MENU_ITEMS : USER_MENU_ITEMS;

        menuRoot.replaceChildren(...items.map(function(item){
            return createMenuItem(item, currentPage);
        }));
    }

    function renderNavbar(user){
        const navbarRoot = getNavbarRoot(user.role);

        if(!navbarRoot){
            return;
        }

        const roleLabel = getRoleLabel(user.role);
        const initials = getInitials(user.name);
        const userNameElements = navbarRoot.querySelectorAll("[data-user-name], #navbarUserName, #adminName, .user-name");
        const userRoleElements = navbarRoot.querySelectorAll("[data-user-role], #navbarUserRole, #adminRole, .user-role");
        const avatarElements = navbarRoot.querySelectorAll("[data-user-avatar], #navbarAvatar, #adminAvatar, .avatar");

        userNameElements.forEach(function(element){
            element.textContent = user.name || roleLabel;
        });

        userRoleElements.forEach(function(element){
            element.textContent = roleLabel;
        });

        avatarElements.forEach(function(element){
            element.textContent = initials;
        });
    }

    function renderUserNavigation(user){
        if(!user){
            return;
        }

        renderMenu(user.role);
        renderNavbar(user);
        bindLogoutControls(document);
        setActiveNavigationLink(document);
    }

    function renderAdminNavigation(user){
        if(!user){
            return;
        }

        bindLogoutControls(document);
        setActiveNavigationLink(document);
        renderNavbar(user);
    }

    function initializeNavigation(user){
        if(!user){
            return;
        }

        if(user.role === "owner" && document.getElementById("adminSidebar")){
            renderAdminNavigation(user);
            return;
        }

        renderUserNavigation(user);
    }

    async function bootNavigation(){
        const user = await window.getCurrentUser();

        if(!user){
            return;
        }

        initializeNavigation(user);
    }

    function scheduleBoot(){
        const run = function(){
            bootNavigation().catch(function(error){
                console.error("Navigation bootstrap failed:", error);
            });
        };

        if(window.__componentsReady && typeof window.__componentsReady.then === "function"){
            window.__componentsReady.then(run);
            return;
        }

        if(document.readyState === "loading"){
            document.addEventListener("DOMContentLoaded", run, { once: true });
            return;
        }

        run();
    }

    window.setActiveNavigationLink = function(root = document){
        setActiveNavigationLink(root);
    };
    window.initializeNavigation = initializeNavigation;
    window.initializeUserNavigation = renderUserNavigation;
    window.initializeAdminNavigation = renderAdminNavigation;
    window.bindLogoutControls = bindLogoutControls;

    scheduleBoot();
})();
