/*
AI DATABASE COPILOT
USER PROFILE
*/


(function(){


    function formatDate(
        value,
        includeTime = false
    ){

        if(!value){

            return "-";

        }



        let formattedValue =
        value;


        if(
            !formattedValue.endsWith("Z")
        ){

            formattedValue += "Z";

        }



        const date =
        new Date(
            formattedValue
        );



        if(
            isNaN(
                date.getTime()
            )
        ){

            return "-";

        }




        return new Intl.DateTimeFormat(
            "en-GB",
            includeTime
            ?
            {

                timeZone:
                "Asia/Dhaka",

                day:
                "2-digit",

                month:
                "2-digit",

                year:
                "numeric",

                hour:
                "2-digit",

                minute:
                "2-digit",

                second:
                "2-digit",

                hour12:
                true

            }
            :
            {

                timeZone:
                "Asia/Dhaka",

                day:
                "2-digit",

                month:
                "2-digit",

                year:
                "numeric"

            }
        )
        .format(date);


    }








    function renderDatabases(
        databases
    ){


        const container =
        document.getElementById(
            "connectedDatabases"
        );



        const count =
        document.getElementById(
            "databaseCount"
        );



        if(!container){

            return;

        }




        container.innerHTML =
        "";





        if(
            !Array.isArray(databases)
            ||
            databases.length === 0
        ){

            container.textContent =
            "No connected databases.";

            if(count){

                count.textContent =
                "0";

            }

            return;

        }






        if(count){

            count.textContent =
            databases.length;

        }






        databases.forEach(
            database=>{


                const card =
                document.createElement(
                    "div"
                );


                card.className =
                "ui-card profile-database-card";



                const title =
                document.createElement(
                    "h3"
                );


                title.textContent =
                database.connection_name ||
                "Database";



                const name =
                document.createElement(
                    "p"
                );


                name.textContent =
                `Database: ${
                    database.database_name || "-"
                }`;



                const host =
                document.createElement(
                    "p"
                );


                host.textContent =
                `Host: ${
                    database.host || "-"
                }`;



                const status =
                document.createElement(
                    "p"
                );


                status.textContent =
                `Status: ${
                    database.status || "-"
                }`;



                card.appendChild(
                    title
                );

                card.appendChild(
                    name
                );

                card.appendChild(
                    host
                );

                card.appendChild(
                    status
                );



                container.appendChild(
                    card
                );


            }
        );


    }









    async function loadProfile(){


        const loading =
        document.getElementById(
            "profileLoading"
        );


        const content =
        document.getElementById(
            "profileContent"
        );



        try{


            const user =
            await window.apiGet(
                "/api/profile"
            );



            const databases =
            await window.apiGet(
                "/api/connections"
            );







            document.getElementById(
                "profileName"
            ).textContent =
            user.name || "User";





            document.getElementById(
                "profileEmail"
            ).textContent =
            user.email || "-";





            document.getElementById(
                "profileRole"
            ).textContent =
            user.role || "user";





            document.getElementById(
                "profileStatus"
            ).textContent =
            user.is_active
            ?
            "Active"
            :
            "Inactive";





            document.getElementById(
                "profileCreated"
            ).textContent =
            formatDate(
                user.created_at
            );





            document.getElementById(
                "profileLastLogin"
            ).textContent =
            formatDate(
                user.last_login_at,
                true
            );







            const avatar =
            document.getElementById(
                "profileAvatar"
            );



            if(avatar){

                avatar.textContent =
                window.getInitials
                ?
                window.getInitials(
                    user.name
                )
                :
                "U";

            }







            renderDatabases(
                databases
            );







            if(loading){

                loading.style.display =
                "none";

            }



            if(content){

                content.style.display =
                "block";

            }




        }


        catch(error){


            console.error(
                "Profile loading failed:",
                error
            );



            if(loading){

                loading.textContent =
                "Failed to load profile.";

            }


        }


    }








    document.addEventListener(
        "DOMContentLoaded",
        loadProfile
    );


})();