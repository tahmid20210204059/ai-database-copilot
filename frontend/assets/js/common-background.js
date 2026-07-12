function loadCommonBackground(){

    const target =
    document.getElementById(
        "common-background"
    );


    if(!target)
    return;


    fetch(
        "../components/common-background.html"
    )
    .then(response=>{

        if(!response.ok){

            throw new Error(
                "Background component load failed"
            );

        }

        return response.text();

    })
    .then(data=>{

        target.innerHTML=data;

    })
    .catch(error=>{

        console.error(
            "Common background error:",
            error
        );

    });

}



document.addEventListener(
"DOMContentLoaded",
loadCommonBackground
);
