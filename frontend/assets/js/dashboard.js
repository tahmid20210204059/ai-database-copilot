/*
AI DATABASE COPILOT
USER DASHBOARD
*/

(function(){
    function setMetric(id, value){
        const element = document.getElementById(id);

        if(element){
            element.innerText = value;
        }
    }

    function setLoadingState(){
        setMetric("totalConnections", "Loading...");
        setMetric("totalQueries", "Loading...");
        setMetric("successRate", "Loading...");
    }

    function renderActivityMessage(message){
        const body = document.getElementById("recentActivityBody");

        if(!body){
            return;
        }

        body.replaceChildren();

        const row = document.createElement("tr");
        const cell = document.createElement("td");

        cell.colSpan = 3;
        cell.textContent = message;
        row.appendChild(cell);
        body.appendChild(row);
    }

    function renderRecentActivity(activity){
        const body = document.getElementById("recentActivityBody");

        if(!body){
            return;
        }

        body.replaceChildren();

        if(!Array.isArray(activity) || activity.length === 0){
            renderActivityMessage("No recent activity");
            return;
        }

        activity.forEach(function(item){
            const row = document.createElement("tr");
            const queryCell = document.createElement("td");
            const statusCell = document.createElement("td");
            const timeCell = document.createElement("td");

            queryCell.textContent = item.query || item.prompt || "No data available";
            statusCell.textContent = item.status || "No data available";
            timeCell.textContent = item.time || item.created_at || "No data available";

            row.appendChild(queryCell);
            row.appendChild(statusCell);
            row.appendChild(timeCell);
            body.appendChild(row);
        });
    }

    function updateDashboardCards(data){
        setMetric("totalConnections", String(data.total_connections ?? 0));
        setMetric("totalQueries", String(data.total_queries ?? 0));
        setMetric("successRate", `${data.success_rate ?? 0}%`);
    }

    async function loadUserDashboardStats(){
        setLoadingState();
        renderActivityMessage("Loading recent activity...");

        try{
            const data = await window.apiGet("/api/user/stats");

            updateDashboardCards(data);
            renderRecentActivity(data.recent_activity);
        }
        catch(error){
            console.error("Dashboard stats error:", error);

            setMetric("totalConnections", "Unavailable");
            setMetric("totalQueries", "Unavailable");
            setMetric("successRate", "Unavailable");
            renderActivityMessage(error.message || "Failed to load dashboard data");
        }
    }

    function initializeDashboard(){
        if(window.__componentsReady && typeof window.__componentsReady.then === "function"){
            window.__componentsReady.then(loadUserDashboardStats);
            return;
        }

        loadUserDashboardStats();
    }

    document.addEventListener("DOMContentLoaded", initializeDashboard);
})();
