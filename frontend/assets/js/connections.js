/*
AI DATABASE COPILOT
DATABASE CONNECTION MANAGEMENT
*/

let selectedConnection = null;
let editingConnectionId = null;
let cachedConnections = [];

function getConnectionFormValue(id){
    const element = document.getElementById(id);
    return element ? element.value : "";
}

function getConnectionFormData(){
    return {
        connection_name: getConnectionFormValue("connection_name").trim(),
        database_name: getConnectionFormValue("database_name").trim(),
        host: getConnectionFormValue("host").trim(),
        port: Number(getConnectionFormValue("port")),
        username: getConnectionFormValue("username").trim(),
        password: getConnectionFormValue("password"),
    };
}

function setMetricValue(id, value){
    const element = document.getElementById(id);

    if(element){
        element.innerText = value;
    }
}

function updateConnectionStats(connections){
    setMetricValue("totalConnections", String(connections.length));
}

function setContainerMessage(message){
    const container = document.getElementById("connectionsContainer");

    if(!container){
        return;
    }

    container.replaceChildren();

    const card = document.createElement("div");
    card.className = "ui-card";

    const heading = document.createElement("h3");
    heading.textContent = message;

    card.appendChild(heading);
    container.appendChild(card);
}

function createDetailLine(label, value){
    const line = document.createElement("p");
    const labelNode = document.createTextNode(`${label}: `);
    const valueNode = document.createElement("span");

    valueNode.textContent = value;
    line.appendChild(labelNode);
    line.appendChild(valueNode);

    return line;
}

function createActionButton(label, className, handler){
    const button = document.createElement("button");

    button.type = "button";
    button.className = className;
    button.textContent = label;
    button.addEventListener("click", handler);

    return button;
}

function renderConnectionCard(connection){
    const card = document.createElement("div");
    const title = document.createElement("h3");
    const statusLine = document.createElement("p");
    const statusLabel = document.createElement("span");
    const buttons = document.createElement("div");

    const lastTested = connection.last_tested_at
        ? new Date(connection.last_tested_at).toLocaleString()
        : "Not tested yet";

    card.className = "ui-card premium-hover";

    title.className = "connection-name";
    title.textContent = connection.connection_name || "Unnamed connection";

    statusLine.textContent = "Status: ";
    statusLabel.className = connection.is_active ? "badge badge-success" : "badge badge-danger";
    statusLabel.textContent = connection.is_active ? "Connected" : "Inactive";
    statusLine.appendChild(statusLabel);

    buttons.className = "connection-actions";
    buttons.style.marginTop = "16px";
    buttons.style.display = "flex";
    buttons.style.flexWrap = "wrap";
    buttons.style.gap = "10px";

    buttons.appendChild(createActionButton("Test", "ui-btn ui-btn-success test-btn", function(){
        testExistingConnection(connection.id);
    }));
    buttons.appendChild(createActionButton("Edit", "ui-btn ui-btn-primary edit-btn", function(){
        editConnection(connection.id);
    }));
    buttons.appendChild(createActionButton("Delete", "ui-btn ui-btn-danger delete-btn", function(){
        deleteConnection(connection.id);
    }));

    card.appendChild(title);
    card.appendChild(createDetailLine("Host", connection.host || "No data available"));
    card.appendChild(createDetailLine("Port", String(connection.port ?? "No data available")));
    card.appendChild(createDetailLine("Username", connection.username || "No data available"));
    card.appendChild(createDetailLine("Last Tested", lastTested));
    card.appendChild(statusLine);
    card.appendChild(buttons);

    return card;
}

function renderConnections(connections){
    const container = document.getElementById("connectionsContainer");

    if(!container){
        return;
    }

    cachedConnections = Array.isArray(connections) ? connections : [];
    container.replaceChildren();

    if(cachedConnections.length === 0){
        const card = document.createElement("div");
        const heading = document.createElement("h3");
        const paragraph = document.createElement("p");

        card.className = "ui-card";
        heading.textContent = "No Connections";
        paragraph.textContent = "Add your first database connection to get started.";

        card.appendChild(heading);
        card.appendChild(paragraph);
        container.appendChild(card);
        return;
    }

    cachedConnections.forEach(function(connection){
        container.appendChild(renderConnectionCard(connection));
    });
}

function getErrorMessage(error){
    if(!error){
        return "Request failed";
    }

    return error.message || "Request failed";
}

async function loadConnections(){
    setContainerMessage("Loading connections...");

    try{
        const connections = await window.apiGet("/api/connections");
        updateConnectionStats(connections);
        renderConnections(connections);
    }
    catch(error){
        console.error(error);
        setMetricValue("totalConnections", "0");
        setContainerMessage(`Failed to load connections: ${getErrorMessage(error)}`);
        if(typeof showToast === "function"){
            showToast(getErrorMessage(error), "error");
        }
    }
}

async function testConnection(){
    const data = getConnectionFormData();

    try{
        await window.apiPost("/api/connections/test", data);
        if(typeof showToast === "function"){
            showToast("Connection successful", "success");
        }
    }
    catch(error){
        if(typeof showToast === "function"){
            showToast(getErrorMessage(error), "error");
        }
    }
}

async function saveConnection(event){
    event.preventDefault();

    const data = getConnectionFormData();
    const isEditing = Boolean(editingConnectionId);
    const url = isEditing
        ? `/api/connections/${editingConnectionId}`
        : "/api/connections";

    try{
        if(isEditing){
            await window.apiPut(url, data);
        }
        else{
            await window.apiPost(url, data);
        }

        if(typeof showToast === "function"){
            showToast(isEditing ? "Connection updated" : "Connection saved", "success");
        }

        editingConnectionId = null;

        const form = document.getElementById("connectionForm");
        if(form){
            form.reset();
        }

        const saveButton = document.getElementById("saveConnectionBtn");
        if(saveButton){
            saveButton.innerText = "Save Connection";
        }

        await loadConnections();
    }
    catch(error){
        if(typeof showToast === "function"){
            showToast(getErrorMessage(error), "error");
        }
    }
}

async function editConnection(id){
    let connection = cachedConnections.find(function(item){
        return item.id === id;
    });

    if(!connection){
        await loadConnections();
        connection = cachedConnections.find(function(item){
            return item.id === id;
        });

        if(!connection){
            if(typeof showToast === "function"){
                showToast("Connection not found", "error");
            }
            return;
        }
    }

    editingConnectionId = id;

    const fields = {
        connection_name: connection.connection_name,
        database_name: connection.database_name,
        host: connection.host,
        port: connection.port,
        username: connection.username,
    };

    Object.keys(fields).forEach(function(key){
        const element = document.getElementById(key);

        if(element){
            element.value = fields[key] ?? "";
        }
    });

    const saveButton = document.getElementById("saveConnectionBtn");
    if(saveButton){
        saveButton.innerText = "Update Connection";
    }

    window.scrollTo({
        top: 0,
        behavior: "smooth",
    });
}

async function deleteConnection(id){
    if(!confirm("Delete this connection?")){
        return;
    }

    try{
        await window.apiDelete(`/api/connections/${id}`);

        if(typeof showToast === "function"){
            showToast("Connection deleted", "success");
        }

        await loadConnections();
    }
    catch(error){
        if(typeof showToast === "function"){
            showToast(getErrorMessage(error), "error");
        }
    }
}

function testExistingConnection(id){
    selectedConnection = id;

    const modal = document.getElementById("testModal");
    if(modal){
        modal.classList.remove("hidden");
    }
}

function closeTestModal(){
    const modal = document.getElementById("testModal");
    const password = document.getElementById("testPassword");

    if(modal){
        modal.classList.add("hidden");
    }

    if(password){
        password.value = "";
    }
}

async function testSavedConnection(){
    const connection = cachedConnections.find(function(item){
        return item.id === selectedConnection;
    });

    if(!connection){
        if(typeof showToast === "function"){
            showToast("No connection selected", "error");
        }
        return;
    }

    const passwordField = document.getElementById("testPassword");
    const password = passwordField ? passwordField.value : "";

    try{
        await window.apiPost("/api/connections/test", {
            connection_name: connection.connection_name,
            host: connection.host,
            port: connection.port,
            database_name: connection.database_name,
            username: connection.username,
            password: password,
        });

        if(typeof showToast === "function"){
            showToast("Connection successful", "success");
        }

        closeTestModal();
        await loadConnections();
    }
    catch(error){
        if(typeof showToast === "function"){
            showToast(getErrorMessage(error), "error");
        }
    }
}

document.addEventListener("DOMContentLoaded", function(){
    loadConnections();

    const form = document.getElementById("connectionForm");
    if(form){
        form.addEventListener("submit", saveConnection);
    }

    const testButton = document.getElementById("testConnectionBtn");
    if(testButton){
        testButton.addEventListener("click", testConnection);
    }

    const confirmTestBtn = document.getElementById("confirmTestBtn");
    if(confirmTestBtn){
        confirmTestBtn.addEventListener("click", testSavedConnection);
    }
});
