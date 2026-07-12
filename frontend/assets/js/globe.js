/*
==================================================
AI DATABASE COPILOT
3D NEURAL GLOBE ENGINE
Pure Canvas 2D
==================================================
*/


class NeuralGlobe {


    constructor(canvas){


        this.canvas = canvas;

        this.ctx =
        canvas.getContext("2d");


        this.points = [];

        this.rotation = 0;


        this.speed = 0.01;


        this.radius = 200;

        this.blobs = [];


        this.resize();


        window.addEventListener(
            "resize",
            ()=>this.resize()
        );


        this.createGlobePoints();
        this.createBlobs();

        requestAnimationFrame(
            ()=>this.animate()
        );

    }


    createBlobs(){

        const count = 16;

        this.blobs.length = 0;

        for(
            let i=0;
            i<count;
            i++
        ){

            const theta = (Math.PI*2/count) * i;
            const phi = (Math.random()*0.2 - 0.1) * Math.PI;

            this.blobs.push({
                theta: theta,
                phi: phi,
                radius: this.radius * (1.08 + Math.random()*0.07),
                speed: 0.009 + Math.random()*0.006,
                size: 2 + Math.random()*2,
                drift: (Math.random()*0.004 - 0.002)
            });

        }

    }


    /*
    Fibonacci Sphere Distribution
    */

    createGlobePoints(){

        const count = 220;

        const golden =
        Math.PI *
        (3 - Math.sqrt(5));

        this.points.length = 0;

        for(
            let i=0;
            i<count;
            i++
        ){

            const y =
            1 -
            (i/(count-1))*2;

            const ringRadius =
            Math.sqrt(
                1-y*y
            ) * this.radius;

            const theta =
            golden*i;

            this.points.push({

                x:
                Math.cos(theta)
                *
                ringRadius,

                y:
                y * this.radius,

                z:
                Math.sin(theta)
                *
                ringRadius

            });

        }

    }




    resize(){

        const dpr =
        window.devicePixelRatio || 1;

        this.width = this.canvas.clientWidth;
        this.height = this.canvas.clientHeight;

        this.canvas.width = this.width * dpr;
        this.canvas.height = this.height * dpr;

        // Reset transform to avoid cumulative scaling when resize is called
        this.ctx.setTransform(1,0,0,1,0,0);
        this.ctx.scale(dpr, dpr);

        this.centerX = this.width/2;
        this.centerY = this.height/2;

    }


    updateBlobs(){

        this.blobs.forEach(blob=>{

            blob.theta += blob.speed;
            blob.phi += blob.drift;

            const x =
            Math.cos(blob.phi)
            * Math.cos(blob.theta)
            * blob.radius;

            const y =
            Math.sin(blob.phi)
            * blob.radius * 0.7;

            const z =
            Math.cos(blob.phi)
            * Math.sin(blob.theta)
            * blob.radius;

            blob.screen =
            this.project(
                this.rotatePoint({x,y,z})
            );

        });

    }


    drawBlobs(){

        const ctx =
        this.ctx;

        ctx.save();
        ctx.globalCompositeOperation =
        "lighter";

        this.blobs.forEach(blob=>{
            if(!blob.screen) return;

            const p = blob.screen;
            const alpha =
            0.28 +
            ((p.z + this.radius) /
             (this.radius*2)) * 0.5;

            ctx.fillStyle =
            `rgba(56, 212, 255, ${Math.min(0.75, alpha)})`;
            ctx.shadowBlur =
            10;
            ctx.shadowColor =
            "#38bdf8";

            ctx.beginPath();
            ctx.arc(
                p.x,
                p.y,
                blob.size,
                0,
                Math.PI*2
            );
            ctx.fill();

        });

        ctx.restore();

    }


    rotatePoint(point){


        const cos =
        Math.cos(
            this.rotation
        );


        const sin =
        Math.sin(
            this.rotation
        );



        /*
        Y axis rotation matrix

        x' = xcosθ + zsinθ

        z' = -xsinθ + zcosθ

        */


        return {


            x:
            point.x*cos
            +
            point.z*sin,


            y:
            point.y,


            z:
            -point.x*sin
            +
            point.z*cos


        };


    }







    project(point){


        const distance =
        800;


        const scale =
        800 /
        (
            distance-point.z
        );



        return {


            x:
            this.centerX
            +
            point.x*scale,


            y:
            this.centerY
            +
            point.y*scale,


            z:
            point.z,


            scale:
            scale


        };


    }









    drawConnections(points){


        const ctx =
        this.ctx;



        for(
            let i=0;
            i<points.length;
            i++
        ){



            for(
                let j=i+1;
                j<points.length;
                j++
            ){


                const a =
                points[i];


                const b =
                points[j];



                const dx =
                a.x-b.x;


                const dy =
                a.y-b.y;



                const dist =
                Math.sqrt(
                    dx*dx+
                    dy*dy
                );



                if(
                    dist < 55
                    &&
                    a.z > -0.2
                    &&
                    b.z > -0.2
                ){



                   const opacity =
                   ((a.z+b.z+2)
                   /
                   8)
                   *
                   0.45;



                    ctx.strokeStyle =
                    `rgba(
                    77,
                    166,
                    255,
                    ${opacity}
                    )`;



                    ctx.lineWidth =
                    0.5;



                    ctx.beginPath();


                    ctx.moveTo(
                        a.x,
                        a.y
                    );


                    ctx.lineTo(
                        b.x,
                        b.y
                    );


                    ctx.stroke();


                }



            }


        }


    }









    drawPoints(points){


        const ctx =
        this.ctx;



        points
        .sort(
            (a,b)=>
            a.z-b.z
        );




        points.forEach(
            p=>{


                const brightness =
                Math.max(
                    0,
                    Math.min(
                        1,
                        (p.z+1)/2
                    )
                );



                const size =
                Math.max(
                    0.8,
                    1.5+
                    brightness*2
                );



                ctx.beginPath();



                ctx.fillStyle =
                `rgba(
                77,
                166,
                255,
                ${0.35+
                brightness*0.65}
                )`;



                ctx.shadowBlur =
                8;



                ctx.shadowColor =
                "#00d4ff";



                ctx.arc(
                    p.x,
                    p.y,
                    size,
                    0,
                    Math.PI*2
                );


                ctx.fill();



            }
        );



        ctx.shadowBlur=0;


    }









    render(){


        const ctx =
        this.ctx;



        ctx.clearRect(
            0,
            0,
            this.width,
            this.height
        );






        const projected =
        this.points.map(
            p=>
            this.project(
                this.rotatePoint(p)
            )
        );



        this.updateBlobs();


        this.drawConnections(
            projected
        );


        this.drawPoints(
            projected
        );


        this.drawBlobs();



    }








    animate(){


        this.rotation +=
        this.speed;



        this.render();



        requestAnimationFrame(
            ()=>this.animate()
        );


    }



}







window.addEventListener(
"DOMContentLoaded",
()=>{


const canvas =
document.getElementById(
"aiGlobe"
);



if(canvas){

    new NeuralGlobe(
        canvas
    );

}


});
