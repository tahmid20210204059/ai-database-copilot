/*
AI DATABASE COPILOT
SHARED API HELPERS
*/

(function(){
    const API_BASE_URL = window.API_BASE_URL || "http://127.0.0.1:8000";
    const TOKEN_KEY = "access_token";
    const USER_KEY = "user";

    let cachedUser = null;
    let cachedUserToken = null;

    function getToken(){
        return localStorage.getItem(TOKEN_KEY);
    }

    function getStoredUser(){
        const raw = localStorage.getItem(USER_KEY);

        if(!raw){
            return null;
        }

        try{
            return JSON.parse(raw);
        }
        catch(error){
            console.error("Stored user parse error:", error);
            return null;
        }
    }

    function setStoredUser(user){
        if(!user){
            localStorage.removeItem(USER_KEY);
            return;
        }

        localStorage.setItem(USER_KEY, JSON.stringify(user));
    }

    function clearSession(){
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(USER_KEY);
        cachedUser = null;
        cachedUserToken = null;
    }

    function setUserSession(token, user){
        if(token){
            localStorage.setItem(TOKEN_KEY, token);
        }

        setStoredUser(user);
        cachedUser = user || null;
        cachedUserToken = token || null;
    }

    function getInitials(name){
        const trimmed = String(name || "").trim();

        if(!trimmed){
            return "AD";
        }

        const parts = trimmed.split(/\s+/).filter(Boolean);
        const first = parts[0]?.[0] || "A";
        const second = parts.length > 1 ? parts[1][0] : (parts[0]?.[1] || "D");

        return `${first}${second}`.toUpperCase();
    }

    function logout(){
        clearSession();
        window.location.href = "login.html";
    }

    function serializeBody(body, headers){
        if(
            body == null ||
            body instanceof FormData ||
            body instanceof URLSearchParams ||
            body instanceof Blob ||
            typeof body === "string"
        ){
            return body;
        }

        if(!headers.has("Content-Type")){
            headers.set("Content-Type", "application/json");
        }

        return JSON.stringify(body);
    }

    async function readResponseBody(response){
        if(response.status === 204){
            return null;
        }

        const text = await response.text();

        if(!text){
            return null;
        }

        try{
            return JSON.parse(text);
        }
        catch(error){
            return text;
        }
    }

    function buildErrorMessage(payload, response){
        if(payload && typeof payload === "object"){
            if(typeof payload.detail === "string"){
                return payload.detail;
            }

            if(Array.isArray(payload.detail)){
                return payload.detail
                    .map(function(item){
                        return item.msg || item.detail || "Validation error";
                    })
                    .join(", ");
            }

            if(typeof payload.message === "string"){
                return payload.message;
            }

            if(typeof payload.error === "string"){
                return payload.error;
            }
        }

        if(typeof payload === "string" && payload.trim()){
            return payload.trim();
        }

        return `${response.status} ${response.statusText || "Request failed"}`.trim();
    }

    async function apiRequest(path, options = {}){
        const {
            method = "GET",
            auth = true,
            headers = {},
            body = null,
        } = options;

        const requestHeaders = new Headers(headers);
        const token = getToken();

        if(auth){
            if(!token){
                throw new Error("Authentication required");
            }

            requestHeaders.set("Authorization", `Bearer ${token}`);
        }

        const response = await fetch(`${API_BASE_URL}${path}`, {
            method,
            headers: requestHeaders,
            body: serializeBody(body, requestHeaders),
        });

        const payload = await readResponseBody(response);

        if(!response.ok){
            throw new Error(buildErrorMessage(payload, response));
        }

        return payload;
    }

    function apiGet(path, options = {}){
        return apiRequest(path, {
            ...options,
            method: "GET",
        });
    }

    function apiPost(path, body, options = {}){
        return apiRequest(path, {
            ...options,
            method: "POST",
            body,
        });
    }

    function apiPut(path, body, options = {}){
        return apiRequest(path, {
            ...options,
            method: "PUT",
            body,
        });
    }

    function apiDelete(path, options = {}){
        return apiRequest(path, {
            ...options,
            method: "DELETE",
        });
    }

    async function getCurrentUser(forceRefresh = false){
        const token = getToken();

        if(!token){
            return null;
        }

        if(!forceRefresh && cachedUser && cachedUserToken === token){
            return cachedUser;
        }

        try{
            const user = await apiGet("/api/profile");
            cachedUser = user;
            cachedUserToken = token;
            setStoredUser(user);
            return user;
        }
        catch(error){
            cachedUser = null;
            cachedUserToken = null;
            console.error("Profile load failed:", error);
            return null;
        }
    }

    window.API_BASE_URL = API_BASE_URL;
    window.getToken = getToken;
    window.getCurrentUser = getCurrentUser;
    window.getInitials = getInitials;
    window.logout = logout;
    window.clearSession = clearSession;
    window.setUserSession = setUserSession;
    window.apiRequest = apiRequest;
    window.apiGet = apiGet;
    window.apiPost = apiPost;
    window.apiPut = apiPut;
    window.apiDelete = apiDelete;
    window.adminFetchJson = function(path, options = {}){
        return apiRequest(path, {
            ...options,
            method: "GET",
        });
    };
})();
