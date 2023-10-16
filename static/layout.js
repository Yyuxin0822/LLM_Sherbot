
const tagX = 256;
const tagY = 30;
const coefficient = 1;
const repeatX=[1,3,1];
const tabpad=64;

let pane = document.getElementById("pane");
pane.style.top = 60+"px";
pane.style.position="absolute";
pane.style.width = tagX*coefficient*5+tabpad*2+"px";
pane.style.height = "150px";
// pane.style.borderStyle = "solid";
// pane.style.borderWidth = "1px";
// pane.style.borderColor = "black";
let paneRect = pane.getBoundingClientRect();
console.log(paneRect);


let field = document.getElementById("field");
field.style.position="absolute";
field.style.left = "0px";
field.style.top = "210px";
field.style.width = "12000px";
field.style.height = "12000px";

let fieldRect = field.getBoundingClientRect();
console.log(fieldRect);

let canvasboard = document.getElementById("canvasboard");
canvasboard.style.position="absolute";
canvasboard.style.left = "0px";
canvasboard.style.top = "210px";
canvasboard.style.width = "12000px";
canvasboard.style.height = "12000px";

let canvasRect = field.getBoundingClientRect();
console.log(fieldRect);

logtab();

function logtab(){
  // Under pane
  setTab(5.5,2,0,0,"Env"); //60px high
  setTab(5.5,1,0,60,"Function"); //30px high
  setTab(10.5,1,0,90,"FuncMenu");//30px high
  setTab(5.5,1,0,120,"Field");//30px high
  // Under field
  setTab(1,7000,0,0,"Left");
  setTab(3,7000,tagX*coefficient*1+tabpad,0,"Middle");
  setTab(1,7000,tagX*coefficient*4+tabpad*2,0,"Right");
  setTab(3,7000,tagX*coefficient*1+tabpad,0,"Inspire");

  // set the height of the field
  let field = document.getElementById("field");
  field.style.position = "absolute";
}


// function logtabCoomplex(){}



function setTab(repeat,repeatY,left,top,id){
  let tab = document.getElementById("tab"+id);
  tab.style.width = tagX*coefficient*repeat+"px";
  tab.style.height = tagY*coefficient*repeatY+"px";
  tab.style.left =left+"px";
  tab.style.top = top+"px"; 
  // tab.style.borderStyle = "solid";
  tab.style.borderWidth = "0.5px";
  tab.style.borderColor = "black";}






