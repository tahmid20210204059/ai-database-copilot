/*
AI DATABASE COPILOT
AUTHENTICATION MANAGEMENT
*/

(function(){

    function setButtonState(
        button,
        disabled,
        label
    ){

        if(!button){
            return;
        }

        button.disabled =
        disabled;

        button.innerText =
        label;

    }





    async function handleLoginSubmit(
        event
    ){

        event.preventDefault();



        const emailInput =
        document.getElementById(
            "email"
        );


        const passwordInput =
        document.getElementById(
            "password"
        );


        const loginButton =
        document.getElementById(
            "loginButton"
        );



        const email =
        emailInput
        ?
        emailInput.value.trim()
        :
        "";



        const password =
        passwordInput
        ?
        passwordInput.value
        :
        "";



        const selectedRoleInput =
        document.getElementById(
            "selectedRole"
        );



        const selectedRole =
        selectedRoleInput
        ?
        selectedRoleInput.value
        :
        "user";





        setButtonState(
            loginButton,
            true,
            "Logging in..."
        );





        try{


            const data =
            await window.apiPost(
                "/api/login",
                {

                    email: email,

                    password: password,

                },
                {

                    auth:false,

                }
            );





            if(
                data.user &&
                data.user.role !== selectedRole
            ){

                throw new Error(
                    `Please select ${data.user.role} workspace for this account`
                );

            }






            window.setUserSession(
                data.access_token,
                data.user
            );





            if(
                typeof showToast === "function"
            ){

                showToast(
                    "Login successful",
                    "success"
                );

            }






            setTimeout(
                function(){


                    if(
                        data.user &&
                        data.user.role === "owner"
                    ){

                        window.location.href =
                        "admin-dashboard.html";

                        return;

                    }



                    window.location.href =
                    "dashboard.html";



                },
                1000
            );



        }


        catch(error){


            if(
                typeof showToast === "function"
            ){

                showToast(
                    error.message,
                    "error"
                );

            }


        }



        finally{


            setButtonState(
                loginButton,
                false,
                "Login"
            );


        }

    }








    async function loadUserProfile(){

        const user =
        await window.getCurrentUser();



        if(!user){

            return;

        }




        const welcomeName =
        document.getElementById(
            "welcomeName"
        );


        const avatar =
        document.querySelector(
            ".avatar"
        );


        const username =
        document.querySelector(
            ".user-name"
        );





        if(welcomeName){

            welcomeName.innerText =
            user.name || "User";

        }





        if(avatar){

            avatar.innerText =
            window.getInitials(
                user.name
            );

        }





        if(username){

            username.innerText =
            user.name || "User";

        }


    }








    document.addEventListener(
        "DOMContentLoaded",
        function(){


            const loginForm =
            document.getElementById(
                "loginForm"
            );



            if(loginForm){

                loginForm.addEventListener(
                    "submit",
                    handleLoginSubmit
                );

            }



            loadUserProfile();


        }
    );




    window.loadUserProfile =
    loadUserProfile;


})();