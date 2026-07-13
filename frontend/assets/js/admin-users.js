/*
AI DATABASE COPILOT
ADMIN USERS MANAGEMENT
*/

(function(){
    let hasLoaded = false;

    function setMetric(id, value){
        const element = document.getElementById(id);

        if(element){
            element.textContent = value;
        }
    }

    function clearTable(table){
        while(table.firstChild){
            table.removeChild(table.firstChild);
        }
    }

    function createCell(text){
        const cell = document.createElement("td");
        cell.textContent = text;
        return cell;
    }

    function renderEmptyState(table, message){
        const row = document.createElement("tr");
        const cell = document.createElement("td");

        cell.colSpan = 5;
        cell.textContent = message;
        row.appendChild(cell);
        table.appendChild(row);
    }

    function renderErrorState(message){
        const table = document.getElementById("usersTableBody");

        if(!table){
            return;
        }

        clearTable(table);
        renderEmptyState(table, message);
    }

    function renderUsers(users){
        const table = document.getElementById("usersTableBody");

        if(!table){
            return;
        }

        clearTable(table);

        if(!Array.isArray(users) || users.length === 0){
            renderEmptyState(table, "No users available.");
            setMetric("totalUsers", "0");
            setMetric("activeUsers", "0");
            setMetric("ownerAccounts", "0");
            setMetric("normalUsers", "0");
            return;
        }

        let activeCount = 0;
        let ownerCount = 0;
        let normalCount = 0;

        users.forEach(function(user){
            if(user.is_active){
                activeCount += 1;
            }

            if(user.role === "owner"){
                ownerCount += 1;
            }
            else{
                normalCount += 1;
            }

            const row = document.createElement("tr");

            row.appendChild(createCell(user.name || "No data available"));
            row.appendChild(createCell(user.email || "No data available"));
            row.appendChild(createCell(user.role || "No data available"));
            row.appendChild(createCell(user.is_active ? "Active" : "Inactive"));
            row.appendChild(createCell(
                user.created_at
                    ? new Date(user.created_at).toLocaleDateString()
                    : "No data available"
            ));

            table.appendChild(row);
        });

        setMetric("totalUsers", String(users.length));
        setMetric("activeUsers", String(activeCount));
        setMetric("ownerAccounts", String(ownerCount));
        setMetric("normalUsers", String(normalCount));
    }

    async function loadAdminUsers(){
        const table = document.getElementById("usersTableBody");

        if(table){
            clearTable(table);
            renderEmptyState(table, "Loading users...");
        }

        try{
            const users = await window.adminFetchJson("/api/admin/users");

            renderUsers(users);
        }
        catch(error){
            console.error(error);
            renderErrorState(`Failed to load users: ${error.message}`);
        }
    }

    function initializeAdminPage(){
        if(hasLoaded || !window.__adminAccessGranted){
            return;
        }

        hasLoaded = true;
        loadAdminUsers();
    }

    window.initializeAdminPage = initializeAdminPage;

    document.addEventListener("DOMContentLoaded", initializeAdminPage);
})();
