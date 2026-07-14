/*
AI DATABASE COPILOT
AI QUERY WORKSPACE
*/


(function(){


    let selectedConnectionId = null;

    let generatedSQL = "";





    function setText(
        id,
        value
    ){

        const element =
        document.getElementById(id);


        if(element){

            element.textContent =
            value ?? "";

        }

    }








    async function loadConnections(){


        const select =
        document.getElementById(
            "databaseSelect"
        );


        try{


            const connections =
            await window.apiGet(
                "/api/connections"
            );



            select.innerHTML =
            "";



            if(
                !connections ||
                connections.length === 0
            ){

                select.innerHTML =
                "<option>No database connected</option>";

                return;

            }





            connections.forEach(
                connection=>{


                    const option =
                    document.createElement(
                        "option"
                    );


                    option.value =
                    connection.id;


                    option.textContent =
                    `${connection.connection_name} (${connection.database_name})`;



                    select.appendChild(
                        option
                    );


                }
            );



            selectedConnectionId =
            connections[0].id;



        }


        catch(error){


            console.error(
                "Connection loading failed:",
                error
            );


            select.innerHTML =
            "<option>Failed to load databases</option>";

        }


    }









    async function generateSQL(){


        const prompt =
        document.getElementById(
            "queryPrompt"
        ).value.trim();



        const select =
        document.getElementById(
            "databaseSelect"
        );



        selectedConnectionId =
        Number(
            select.value
        );





        if(
            !selectedConnectionId ||
            !prompt
        ){

            setText(
                "generateStatus",
                "Select database and enter question."
            );

            return;

        }





        const button =
        document.getElementById(
            "generateSqlBtn"
        );


        button.disabled =
        true;


        button.textContent =
        "Generating...";





        try{


            const response =
            await window.apiPost(

                "/api/ai/generate",

                {

                    connection_id:
                    selectedConnectionId,


                    prompt:
                    prompt

                }

            );





            generatedSQL =
            response.sql;





            setText(
                "generatedSql",
                response.sql
            );



            setText(
                "sqlSummary",
                `Summary: ${response.summary || "-"}`
            );



            setText(
                "sqlConfidence",
                `Confidence: ${response.confidence ?? "-"}`
            );





            document
            .getElementById(
                "sqlSection"
            )
            .classList
            .remove(
                "hidden"
            );



            setText(
                "generateStatus",
                "SQL generated successfully."
            );



        }


        catch(error){


            setText(
                "generateStatus",
                error.message
            );


        }



        finally{


            button.disabled =
            false;


            button.textContent =
            "Generate SQL";


        }


    }









    async function executeQuery(){


        if(
            !generatedSQL ||
            !selectedConnectionId
        ){

            return;

        }





        const button =
        document.getElementById(
            "executeQueryBtn"
        );


        button.disabled =
        true;


        button.textContent =
        "Executing...";





        try{


            const result =
            await window.apiPost(

                "/api/query/execute",

                {

                    connection_id:
                    selectedConnectionId,


                    sql:
                    generatedSQL

                }

            );





            renderResult(
                result
            );



        }


        catch(error){


            setText(
                "executionStatus",
                error.message
            );


        }



        finally{


            button.disabled =
            false;


            button.textContent =
            "Execute Query";


        }


    }









    function renderResult(
        result
    ){



        document
        .getElementById(
            "resultSection"
        )
        .classList
        .remove(
            "hidden"
        );




        setText(
            "executionStatus",
            result.success
            ?
            "Success"
            :
            "Failed"
        );



        setText(
            "executionTime",
            `${result.execution_time_ms} ms`
        );



        setText(
            "rowsReturned",
            result.row_count
        );





        const head =
        document.getElementById(
            "resultHead"
        );


        const body =
        document.getElementById(
            "resultBody"
        );



        head.innerHTML =
        "";

        body.innerHTML =
        "";






        const headerRow =
        document.createElement(
            "tr"
        );



        result.columns.forEach(
            column=>{


                const th =
                document.createElement(
                    "th"
                );


                th.textContent =
                column;


                headerRow.appendChild(
                    th
                );


            }
        );



        head.appendChild(
            headerRow
        );






        result.rows.forEach(
            row=>{


                const tr =
                document.createElement(
                    "tr"
                );



                result.columns.forEach(
                    column=>{


                        const td =
                        document.createElement(
                            "td"
                        );


                        td.textContent =
                        row[column] ?? "-";


                        tr.appendChild(
                            td
                        );


                    }
                );



                body.appendChild(
                    tr
                );


            }
        );


    }









    document.addEventListener(
        "DOMContentLoaded",
        function(){


            loadConnections();



            document
            .getElementById(
                "generateSqlBtn"
            )
            .addEventListener(
                "click",
                generateSQL
            );



            document
            .getElementById(
                "executeQueryBtn"
            )
            .addEventListener(
                "click",
                executeQuery
            );


        }
    );



})();