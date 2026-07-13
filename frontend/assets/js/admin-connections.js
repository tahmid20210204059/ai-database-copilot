/*
AI DATABASE COPILOT
ADMIN CONNECTION MONITORING
*/

(function(){
    const EMPTY_TEXT = "No database connections available.";
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
        const table = document.getElementById("connectionsTableBody");

        if(!table){
            return;
        }

        clearTable(table);
        renderEmptyState(table, message);
    }

    function renderConnections(connections){
        const table = document.getElementById("connectionsTableBody");

        if(!table){
            return;
        }

        clearTable(table);

        if(!Array.isArray(connections) || connections.length === 0){
            renderEmptyState(table, "No database connections available.");
            setMetric("totalConnections", "0");
            setMetric("activeConnections", "0");
            setMetric("inactiveConnections", "0");
            return;
        }

        let activeCount = 0;
        let inactiveCount = 0;

        connections.forEach(function(item){
            const isActive = String(item.status || "").toLowerCase() === "active";

            if(isActive){
                activeCount += 1;
            }
            else{
                inactiveCount += 1;
            }

            const row = document.createElement("tr");

            row.appendChild(createCell(
                item.user_id ? `User #${item.user_id}` : "No data available"
            ));
            row.appendChild(createCell(item.connection_name || "No data available"));
            row.appendChild(createCell(item.database_name || "No data available"));
            row.appendChild(createCell(item.host || "No data available"));
            row.appendChild(createCell(item.status || "No data available"));

            table.appendChild(row);
        });

        setMetric("totalConnections", String(connections.length));
        setMetric("activeConnections", String(activeCount));
        setMetric("inactiveConnections", String(inactiveCount));
    }

    async function loadAdminConnections(){
        const table = document.getElementById("connectionsTableBody");

        if(table){
            clearTable(table);
            renderEmptyState(table, "Loading databases...");
        }

        try{
            const connections = await window.adminFetchJson("/api/admin/connections");

            renderConnections(connections);
        }
        catch(error){
            console.error(error);
            renderErrorState(`Failed to load databases: ${error.message}`);
        }
    }

    function initializeAdminPage(){
        if(hasLoaded || !window.__adminAccessGranted){
            return;
        }

        hasLoaded = true;
        loadAdminConnections();
    }

    window.initializeAdminPage = initializeAdminPage;

    document.addEventListener("DOMContentLoaded", initializeAdminPage);
})();
