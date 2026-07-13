/*
AI DATABASE COPILOT
COMPONENT ENGINE
*/

const componentBaseUrl = document.currentScript?.src
    ? new URL("../../components/", document.currentScript.src)
    : new URL("../components/", window.location.href);

function escapeHtml(value){
    return String(value ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function showToast(message, type = "success"){
    const toast = document.createElement("div");

    toast.className = `toast toast-${type}`;
    toast.innerText = message;

    document.body.appendChild(toast);

    setTimeout(function(){
        toast.style.opacity = "0";

        setTimeout(function(){
            toast.remove();
        }, 200);
    }, 3000);
}

function showLoader(element){
    if(!element){
        return;
    }

    element.innerHTML = "<div class=\"ui-loader\"></div>";
}

function hideLoader(element){
    if(!element){
        return;
    }

    element.innerHTML = "";
}

async function getComponentHTML(name){
    const response = await fetch(new URL(`${name}.html`, componentBaseUrl));

    if(!response.ok){
        throw new Error(`Failed to load component ${name}`);
    }

    return await response.text();
}

function replaceVariables(html, data){
    return html.replace(/{{(.*?)}}/g, function(_, key){
        return escapeHtml(data[key.trim()]);
    });
}

async function loadComponent(element){
    const name = element.dataset.component;

    if(!name || element.dataset.componentLoaded === "true"){
        return;
    }

    element.dataset.componentLoaded = "true";

    try{
        let html = await getComponentHTML(name);
        html = replaceVariables(html, element.dataset);

        if(element.dataset.replace === "true"){
            element.outerHTML = html;
        }
        else{
            element.innerHTML = html;
        }
    }
    catch(error){
        element.dataset.componentLoaded = "false";
        console.error("Component load failed:", error);
    }
}

async function hydrateComponents(root = document){
    const components = Array.from(root.querySelectorAll("[data-component]"));
    await Promise.allSettled(components.map(loadComponent));
}

function notifyComponentsLoaded(){
    window.dispatchEvent(new Event("componentsLoaded"));
}

async function initComponents(){
    await hydrateComponents();

    if(typeof window.setActiveNavigationLink === "function"){
        try{
            window.setActiveNavigationLink();
        }
        catch(error){
            console.error("Active navigation update failed:", error);
        }
    }

    notifyComponentsLoaded();
}

function startComponents(){
    if(document.readyState === "loading"){
        return new Promise(function(resolve){
            document.addEventListener("DOMContentLoaded", function(){
                resolve(initComponents());
            }, { once: true });
        });
    }

    return initComponents();
}

window.__componentsReady = startComponents();
window.componentsReady = window.__componentsReady;
