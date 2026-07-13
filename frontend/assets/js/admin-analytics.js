/*
AI DATABASE COPILOT
ADMIN ANALYTICS
*/

(function(){
    const UNAVAILABLE_TEXT = "Data not available from current API.";
    let hasLoaded = false;

    function setText(id, value){
        const element = document.getElementById(id);

        if(element){
            element.textContent = value;
        }
    }

    function setUnavailable(ids){
        ids.forEach(function(id){
            setText(id, UNAVAILABLE_TEXT);
        });
    }

    function setErrorState(message){
        [
            "totalUsers",
            "totalConnections",
            "totalQueries",
            "userStatistics",
            "databaseStatistics",
            "queryStatistics"
        ].forEach(function(id){
            setText(id, message);
        });
    }

    async function loadAdminAnalytics(){
        try{
            const data = await window.adminFetchJson("/api/admin/stats");

            setText("totalUsers", String(data.total_users ?? "N/A"));
            setText("totalConnections", String(data.total_connections ?? "N/A"));
            setText("totalQueries", String(data.total_queries ?? "N/A"));

            setUnavailable([
                "userStatistics",
                "databaseStatistics",
                "queryStatistics"
            ]);
        }
        catch(error){
            console.error("Admin analytics error:", error);
            setErrorState(`Failed to load analytics: ${error.message}`);
        }
    }

    function initializeAdminPage(){
        if(hasLoaded || !window.__adminAccessGranted){
            return;
        }

        hasLoaded = true;
        loadAdminAnalytics();
    }

    window.initializeAdminPage = initializeAdminPage;

    document.addEventListener("DOMContentLoaded", initializeAdminPage);
})();
