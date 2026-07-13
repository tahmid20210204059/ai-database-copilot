/*
AI DATABASE COPILOT
ADMIN ISOMETRIC DATABASE BACKGROUND
*/

(function () {


    const canvas =
    document.createElement(
        "canvas"
    );


    canvas.id =
    "adminDatabaseGrid";


    Object.assign(
        canvas.style,
        {

            position:"fixed",

            inset:"0",

            width:"100%",

            height:"100%",

            zIndex:"-1",

            pointerEvents:"none",

            opacity:"0.85"

        }
    );



    document.body.appendChild(
        canvas
    );




    const ctx =
    canvas.getContext(
        "2d"
    );



    let width;
    let height;

    let tables = [];

    let connections = [];

    let particles = [];

    let time = 0;







    function resize(){


        width =
        canvas.width =
        window.innerWidth;


        height =
        canvas.height =
        window.innerHeight;


        createTables();


    }




    window.addEventListener(
        "resize",
        resize
    );







    function randomRange(
        min,
        max
    ){

        return Math.random()
        *
        (max-min)
        +
        min;

    }









    function createTables(){


        tables = [];

        connections = [];

        particles = [];



        const count = 18;



        for(
            let i=0;
            i<count;
            i++
        ){


            tables.push({

                x:
                randomRange(
                    width*0.15,
                    width*0.8
                ),


                y:
                randomRange(
                    height*0.15,
                    height*0.8
                ),


                w:
                randomRange(
                    80,
                    130
                ),


                h:
                randomRange(
                    35,
                    65
                ),


                float:
                randomRange(
                    0,
                    Math.PI*2
                ),


                speed:
                randomRange(
                    0.3,
                    0.7
                )

            });



        }






        for(
            let i=0;
            i<tables.length;
            i++
        ){


            let target =
            Math.floor(
                Math.random()
                *
                tables.length
            );



            if(
                target !== i
            ){

                connections.push({

                    from:i,

                    to:target


                });


                particles.push({

                    progress:
                    Math.random(),


                    speed:
                    randomRange(
                        0.002,
                        0.006
                    )


                });

            }


        }


    }






    resize();









    function drawTable(
        table
    ){


        const depth = 16;



        const x =
        table.x;


        const y =
        table.y;





        ctx.save();



        ctx.translate(
            x,
            y
        );




        // top surface

        ctx.beginPath();


        ctx.moveTo(
            0,
            0
        );


        ctx.lineTo(
            table.w,
            -depth
        );


        ctx.lineTo(
            table.w,
            table.h-depth
        );


        ctx.lineTo(
            0,
            table.h
        );


        ctx.closePath();



        ctx.fillStyle =
        "rgba(40,120,220,0.18)";


        ctx.fill();



        ctx.strokeStyle =
        "rgba(80,180,255,0.65)";


        ctx.lineWidth =
        1.2;


        ctx.stroke();






        // side depth

        ctx.beginPath();


        ctx.moveTo(
            table.w,
            -depth
        );


        ctx.lineTo(
            table.w+18,
            0
        );


        ctx.lineTo(
            table.w+18,
            table.h
        );


        ctx.lineTo(
            table.w,
            table.h-depth
        );


        ctx.closePath();



        ctx.fillStyle =
        "rgba(20,80,170,0.25)";


        ctx.fill();


        ctx.stroke();







        // rows

        for(
            let i=1;
            i<4;
            i++
        ){


            ctx.beginPath();


            ctx.moveTo(
                12,
                i*12
            );


            ctx.lineTo(
                table.w-12,
                i*12-6
            );


            ctx.strokeStyle =
            "rgba(150,210,255,0.2)";


            ctx.stroke();


        }




        ctx.restore();



    }









    function drawConnections(){



        connections.forEach(
            (line,index)=>{


                const a =
                tables[line.from];


                const b =
                tables[line.to];




                const x1 =
                a.x+a.w/2;


                const y1 =
                a.y+a.h/2;



                const x2 =
                b.x+b.w/2;


                const y2 =
                b.y+b.h/2;






                ctx.beginPath();


                ctx.moveTo(
                    x1,
                    y1
                );


                ctx.lineTo(
                    x2,
                    y2
                );



                ctx.strokeStyle =
                "rgba(56,189,248,0.25)";


                ctx.lineWidth =
                1;


                ctx.stroke();








                const particle =
                particles[index];



                if(!particle)
                return;



                particle.progress +=
                particle.speed;



                if(
                    particle.progress > 1
                ){

                    particle.progress = 0;

                }





                const px =
                x1 +
                (x2-x1)
                *
                particle.progress;



                const py =
                y1 +
                (y2-y1)
                *
                particle.progress;





                ctx.beginPath();


                ctx.arc(
                    px,
                    py,
                    3,
                    0,
                    Math.PI*2
                );



                ctx.fillStyle =
                "#22d3ee";


                ctx.shadowBlur =
                12;


                ctx.shadowColor =
                "#22d3ee";


                ctx.fill();


                ctx.shadowBlur =
                0;


            }
        );


    }








    function animate(){


        ctx.clearRect(
            0,
            0,
            width,
            height
        );



        time += 0.02;





        drawConnections();






        tables.forEach(
            table=>{


                table.y +=
                Math.sin(
                    time*table.speed +
                    table.float
                )
                *
                0.15;



                drawTable(
                    table
                );


            }
        );




        requestAnimationFrame(
            animate
        );


    }






    animate();



})();