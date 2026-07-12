/*
AI DATABASE COPILOT
DATABASE CONNECTION MANAGEMENT
*/

let selectedConnection = null;
let editingConnectionId = null;

const API_BASE_URL =
"http://127.0.0.1:8000";



function getToken(){

    return localStorage.getItem(
        "access_token"
    );

}



function authHeaders(){

    return {

        "Content-Type":
        "application/json",

        "Authorization":
        `Bearer ${getToken()}`

    };

}




function getErrorMessage(data){

    if(!data){

        return "Unknown error";

    }


    if(typeof data.detail === "string"){

        return data.detail;

    }


    if(Array.isArray(data.detail)){

        return data.detail
        .map(
            item =>
            item.msg || "Validation error"
        )
        .join(", ");

    }


    if(typeof data.detail === "object"){

        return JSON.stringify(data.detail);

    }


    return "Request failed";

}





function updateConnectionStats(
    connections
){

    const total =
    document.getElementById(
        "totalConnections"
    );


    if(total){

        total.innerText =
        connections.length;

    }

}







async function loadConnections(){

    const container =
    document.getElementById(
        "connectionsContainer"
    );


    if(!container)
    return;



    try{


        const response =
        await fetch(
            `${API_BASE_URL}/api/connections`,
            {

            method:"GET",

            headers:{

                "Authorization":
                `Bearer ${getToken()}`

            }

            }

        );



        const data =
        await response.json();



        if(!response.ok){

            throw new Error(
                getErrorMessage(data)
            );

        }



        updateConnectionStats(
            data
        );


        renderConnections(
            data
        );


    }


    catch(error){

        console.error(error);


        showToast(
            error.message,
            "error"
        );

    }


}







function renderConnections(
    connections
){


    const container =
    document.getElementById(
        "connectionsContainer"
    );


    if(!container)
    return;



    container.innerHTML = "";



    if(connections.length === 0){


        container.innerHTML = `

        <div class="ui-card">

        <h3>
        No Connections
        </h3>

        <p>
        Add your first database connection.
        </p>

        </div>

        `;

        return;

    }





    connections.forEach(
        connection => {


        const status =
        connection.is_active
        ?
        "Connected"
        :
        "Inactive";



        const statusClass =
        connection.is_active
        ?
        "badge-success"
        :
        "badge-danger";



        const lastTest =
        connection.last_tested_at
        ?
        new Date(
            connection.last_tested_at
        ).toLocaleString()
        :
        "Not tested yet";



        const card =
        document.createElement(
            "div"
        );


        card.className =
        "ui-card premium-hover";



        card.innerHTML = `

        <h3>
        ${connection.connection_name}
        </h3>


        <p>
        Database:
        ${connection.database_name}
        </p>


        <p>
        Host:
        ${connection.host}
        </p>


        <p>
        Port:
        ${connection.port}
        </p>


        <p>
        Username:
        ${connection.username}
        </p>


        <p>
        Status:

        <span class="badge ${statusClass}">
        ${status}
        </span>

        </p>


        <p>
        Last Tested:
        ${lastTest}
        </p>



        <div style="margin-top:20px;">


        <button
        class="ui-btn ui-btn-success"
        onclick="testExistingConnection(${connection.id})">

        Test

        </button>


        <button
        class="ui-btn ui-btn-primary"
        onclick="editConnection(${connection.id})">

        Edit

        </button>



        <button
        class="ui-btn ui-btn-danger"
        onclick="deleteConnection(${connection.id})">

        Delete

        </button>


        </div>

        `;


        container.appendChild(
            card
        );


        }


    );


}









async function testConnection(){

    const data =
    getConnectionFormData();



    try{


        const response =
        await fetch(
            `${API_BASE_URL}/api/connections/test`,
            {

            method:"POST",

            headers:
            authHeaders(),

            body:
            JSON.stringify(data)

            }

        );


        const result =
        await response.json();



        if(!response.ok){

            throw new Error(
                getErrorMessage(result)
            );

        }



        showToast(
            "Connection successful",
            "success"
        );


    }


    catch(error){

        showToast(
            error.message,
            "error"
        );

    }


}









async function saveConnection(e){

    e.preventDefault();


    const data =
    getConnectionFormData();



    const url =
    editingConnectionId
    ?
    `${API_BASE_URL}/api/connections/${editingConnectionId}`
    :
    `${API_BASE_URL}/api/connections`;



    const method =
    editingConnectionId
    ?
    "PUT"
    :
    "POST";



    try{


        const response =
        await fetch(
            url,
            {

            method:method,

            headers:
            authHeaders(),

            body:
            JSON.stringify(data)

            }

        );



        const result =
        await response.json();



        if(!response.ok){

            throw new Error(
                getErrorMessage(result)
            );

        }



        showToast(
            editingConnectionId
            ?
            "Connection updated"
            :
            "Connection saved",
            "success"
        );



        editingConnectionId = null;



        document
        .getElementById(
            "connectionForm"
        )
        .reset();



        document
        .getElementById(
            "saveConnectionBtn"
        )
        .innerText =
        "Save Connection";



        loadConnections();


    }


    catch(error){

        showToast(
            error.message,
            "error"
        );

    }


}








async function editConnection(id){

    const response =
    await fetch(
        `${API_BASE_URL}/api/connections`,
        {

        headers:{

            "Authorization":
            `Bearer ${getToken()}`

        }

        }

    );


    const connections =
    await response.json();



    const connection =
    connections.find(
        item =>
        item.id === id
    );



    if(!connection)
    return;



    editingConnectionId = id;



    document.getElementById(
        "connection_name"
    ).value =
    connection.connection_name;



    document.getElementById(
        "database_name"
    ).value =
    connection.database_name;



    document.getElementById(
        "host"
    ).value =
    connection.host;



    document.getElementById(
        "port"
    ).value =
    connection.port;



    document.getElementById(
        "username"
    ).value =
    connection.username;



    document.getElementById(
        "saveConnectionBtn"
    ).innerText =
    "Update Connection";



    window.scrollTo({

        top:0,

        behavior:"smooth"

    });


}









async function deleteConnection(id){


    if(
        !confirm(
            "Delete this connection?"
        )
    )
    return;



    try{


        const response =
        await fetch(
            `${API_BASE_URL}/api/connections/${id}`,
            {

            method:"DELETE",

            headers:{

                "Authorization":
                `Bearer ${getToken()}`

            }

            }

        );



        const result =
        await response.json();



        if(!response.ok){

            throw new Error(
                getErrorMessage(result)
            );

        }



        showToast(
            "Connection deleted",
            "success"
        );


        loadConnections();


    }


    catch(error){

        showToast(
            error.message,
            "error"
        );

    }


}








function testExistingConnection(id){

    selectedConnection =
    id;


    document
    .getElementById(
        "testModal"
    )
    .classList
    .remove(
        "hidden"
    );

}









function closeTestModal(){

    document
    .getElementById(
        "testModal"
    )
    .classList
    .add(
        "hidden"
    );


    document
    .getElementById(
        "testPassword"
    )
    .value = "";

}









async function testSavedConnection(){

    const password =
    document
    .getElementById(
        "testPassword"
    )
    .value;



    const response =
    await fetch(
        `${API_BASE_URL}/api/connections`,
        {

        headers:{

            "Authorization":
            `Bearer ${getToken()}`

        }

        }

    );


    const connections =
    await response.json();



    const connection =
    connections.find(
        item =>
        item.id === selectedConnection
    );



    try{


        const testResponse =
        await fetch(
            `${API_BASE_URL}/api/connections/test`,
            {

            method:"POST",

            headers:
            authHeaders(),

            body:
            JSON.stringify({

                connection_name:
                connection.connection_name,

                host:
                connection.host,

                port:
                connection.port,

                database_name:
                connection.database_name,

                username:
                connection.username,

                password:
                password

            })

            }

        );



        const result =
        await testResponse.json();



        if(!testResponse.ok){

            throw new Error(
                getErrorMessage(result)
            );

        }



        showToast(
            "Connection successful",
            "success"
        );


        closeTestModal();


        loadConnections();


    }


    catch(error){

        showToast(
            error.message,
            "error"
        );

    }


}









function getConnectionFormData(){


    return {


        connection_name:
        document.getElementById(
            "connection_name"
        ).value.trim(),



        database_name:
        document.getElementById(
            "database_name"
        ).value.trim(),



        host:
        document.getElementById(
            "host"
        ).value.trim(),



        port:
        Number(
            document.getElementById(
                "port"
            ).value
        ),



        username:
        document.getElementById(
            "username"
        ).value.trim(),



        password:
        document.getElementById(
            "password"
        ).value


    };


}









document.addEventListener(
"DOMContentLoaded",
()=>{


    loadConnections();



    const form =
    document.getElementById(
        "connectionForm"
    );



    if(form){

        form.addEventListener(
            "submit",
            saveConnection
        );

    }



    const testButton =
    document.getElementById(
        "testConnectionBtn"
    );



    if(testButton){

        testButton.addEventListener(
            "click",
            testConnection
        );

    }




    const confirmTestBtn =
    document.getElementById(
        "confirmTestBtn"
    );



    if(confirmTestBtn){

        confirmTestBtn.addEventListener(
            "click",
            testSavedConnection
        );

    }


});