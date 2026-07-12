document.addEventListener(
    "DOMContentLoaded",
    () => {


        const loginForm =
        document.getElementById(
            "loginForm"
        );


        if(!loginForm)
        return;



        loginForm.addEventListener(
            "submit",
            async(e)=>{


                e.preventDefault();



                const email =
                document.getElementById(
                    "email"
                ).value;



                const password =
                document.getElementById(
                    "password"
                ).value;



                const button =
                document.getElementById(
                    "loginButton"
                );



                button.disabled = true;

                button.innerText =
                "Logging in...";



                try{


                    const response =
                    await fetch(
                        "http://127.0.0.1:8000/api/login",
                        {

                        method:"POST",

                        headers:{

                            "Content-Type":
                            "application/json"

                        },


                        body:JSON.stringify({

                            email:email,

                            password:password

                        })

                        }
                    );



                    const data =
                    await response.json();




                    if(!response.ok){

                        throw new Error(
                            data.detail ||
                            "Login failed"
                        );

                    }




                    localStorage.setItem(
                        "access_token",
                        data.access_token
                    );



                    showToast(
                        "Login successful",
                        "success"
                    );



                    setTimeout(()=>{

                        window.location.href =
                        "dashboard.html";

                    },1000);



                }


                catch(error){


                    showToast(
                        error.message,
                        "error"
                    );


                }


                finally{


                    button.disabled=false;


                    button.innerText =
                    "Login";


                }



            }

        );


    }

);







function logout(){


    localStorage.removeItem(
        "access_token"
    );


    window.location.href =
    "login.html";


}








async function getCurrentUser(){


    const token =
    localStorage.getItem(
        "access_token"
    );



    if(!token)
    return null;



    try{


        const response =
        await fetch(
            "http://127.0.0.1:8000/api/profile",
            {

            method:"GET",

            headers:{

                "Authorization":
                `Bearer ${token}`

            }

            }
        );



        if(!response.ok){

            throw new Error(
                "Failed to load profile"
            );

        }



        const user =
        await response.json();



        return user;



    }


    catch(error){


        console.error(
            "Profile error:",
            error
        );


        return null;


    }


}









async function loadUserProfile(){


    const user =
    await getCurrentUser();



    if(!user)
    return;




    const welcomeName =
    document.getElementById(
        "welcomeName"
    );



    if(welcomeName){


        welcomeName.innerText =
        user.name;


    }





    const avatar =
    document.querySelector(
        ".avatar"
    );



    if(avatar){


        avatar.innerText =
        user.name
        .substring(0,2)
        .toUpperCase();


    }





    const username =
    document.querySelector(
        ".user-name"
    );



    if(username){


        username.innerText =
        user.name;


    }



}






document.addEventListener(
    "DOMContentLoaded",
    ()=>{

        loadUserProfile();

    }
);