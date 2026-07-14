/*
AI DATABASE COPILOT
USER QUERY HISTORY
*/


(function(){


    let historyLoaded = false;



    function setText(
        id,
        value
    ){

        const element =
        document.getElementById(
            id
        );


        if(element){

            element.textContent =
            value;

        }

    }







    function clearTable(){

        const table =
        document.getElementById(
            "historyTableBody"
        );


        if(table){

            table.innerHTML =
            "";

        }


        return table;

    }







    function formatDate(
        value
    ){

        if(!value){

            return "-";

        }


        const date =
        new Date(value);


        if(
            isNaN(
                date.getTime()
            )
        ){

            return "-";

        }



        return date.toLocaleString(
            "en-GB",
            {
                timeZone:
                "Asia/Dhaka"
            }
        );


    }







    function createCell(
        value
    ){

        const td =
        document.createElement(
            "td"
        );


        td.textContent =
        value ?? "-";


        return td;

    }









    function renderEmpty(){

        const table =
        document.getElementById(
            "historyTableBody"
        );


        if(!table){

            return;

        }


        clearTable();


        const row =
        document.createElement(
            "tr"
        );


        const cell =
        document.createElement(
            "td"
        );


        cell.colSpan =
        6;


        cell.textContent =
        "No query history available.";


        cell.className =
        "empty-state";


        row.appendChild(
            cell
        );


        table.appendChild(
            row
        );


    }









    function renderHistory(
        items
    ){

        const table =
        document.getElementById(
            "historyTableBody"
        );


        if(!table){

            return;

        }



        clearTable();



        if(
            !Array.isArray(items)
            ||
            items.length === 0
        ){

            renderEmpty();

            return;

        }





        let success =
        0;


        let failed =
        0;






        items.forEach(
            item=>{


                if(
                    item.status === "success"
                ){

                    success++;

                }
                else{

                    failed++;

                }





                const row =
                document.createElement(
                    "tr"
                );



                row.appendChild(
                    createCell(
                        item.prompt
                    )
                );



                row.appendChild(
                    createCell(
                        item.generated_sql
                    )
                );



                row.appendChild(
                    createCell(
                        item.status
                    )
                );



                row.appendChild(
                    createCell(
                        item.execution_time_ms
                        ?
                        `${item.execution_time_ms} ms`
                        :
                        "-"
                    )
                );



                row.appendChild(
                    createCell(
                        item.rows_returned
                    )
                );



                row.appendChild(
                    createCell(
                        formatDate(
                            item.created_at
                        )
                    )
                );



                table.appendChild(
                    row
                );


            }
        );






        setText(
            "totalQueries",
            items.length
        );


        setText(
            "successQueries",
            success
        );


        setText(
            "failedQueries",
            failed
        );


    }









    async function loadHistory(){


        try{


            const data =
            await window.apiGet(
                "/api/history"
            );



            renderHistory(
                data.items || data
            );


        }


        catch(error){


            console.error(
                "History loading failed:",
                error
            );



            const table =
            document.getElementById(
                "historyTableBody"
            );


            if(table){

                table.textContent =
                "Failed to load history.";

            }


        }


    }








    function initialize(){


        if(historyLoaded){

            return;

        }


        historyLoaded =
        true;


        loadHistory();


    }






    document.addEventListener(
        "DOMContentLoaded",
        initialize
    );



})();