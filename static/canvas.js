// Image Image Image Image Image Image Image
function loadimage(newWidth){

  var img = document.createElement("img");
  img.src = imageUrl;
  img.id = "canvasImage";
  img.style.position = "absolute";
  img.style.width = newWidth+"px";
  img.style.height = newWidth+"px";
  // img.style.border = "1px solid #ccc";
  img.style.borderRadius = "5px";
  canvasboard.appendChild(img);
  let imgRect=img.getBoundingClientRect();
  console.log(imgRect);}

function firstLoad(){
  var imageWidth=tagX * coefficient * 3
  loadimage(imageWidth);
  let img=document.getElementById("canvasImage");
  img.style.top = "30px";
  img.style.left = tagX * coefficient+tabpad+"px";
  img.style.zIndex = -3;

  img.style.boxSizing = "border-box";}

firstLoad();

function updateimage(delta){
  let img = document.getElementById("canvasImage");
  let startWidth=parseInt(img.style.width);
  let startTop=parseInt(img.style.top);
  let startLeft=parseInt(img.style.left);
  let imgRect=img.getBoundingClientRect();

  console.log(startTop);
  console.log(startLeft);
  // remove the old image
  canvasboard.removeChild(img);
  loadimage(startWidth+delta);
  let newimg = document.getElementById("canvasImage");
  newimg.style.zIndex = 2;
  newimg.style.top = (imgRect.y+window.scrollY-240)+"px";
  newimg.style.left = (imgRect.x+window.scrollX-120)+"px";
  newimg.style.border = "1px solid #ccc";
  newimg.style.boxSizing = "border-box";

  draggable=new PlainDraggable(newimg)

}


// // // // // // // // // // // // // // // // // // // // // // // // // // // // 
// // // // // // // // // // // // // // // // // // // // // // // // // // // // 
// Brush colour and size
const colour = "rgb(30, 30, 30)";
var strokeWidth = 4;
// function updateBrushSize() {
//   return strokeWidth;
// }
// Drawing state
let latestPoint;
let drawing = false;

// Set up our drawing context
const canvas = document.getElementById("canvasDraw");
const context = canvas.getContext("2d");

// Event helpers
const BUTTON = 0b01;
const MIDDLE_BUTTON = 0b10;
const mouseButtonIsDown = buttons => (BUTTON & buttons) === BUTTON;
const middleButtonIsDown = buttons => (MIDDLE_BUTTON & buttons) === MIDDLE_BUTTON;

// Drawing functions
const continueStroke = newPoint => {
  context.beginPath();
  context.moveTo(latestPoint[0], latestPoint[1]);
  context.strokeStyle = colour;
  context.lineWidth = strokeWidth;
  context.lineCap = "round";
  context.lineJoin = "round";
  context.lineTo(newPoint[0], newPoint[1]);
  context.stroke();

  latestPoint = newPoint;
};

const startStroke = point => {
  drawing = true;
  latestPoint = point;
};

const getTouchPoint = evt => {
  const rect = evt.currentTarget.getBoundingClientRect();
  const touch = evt.targetTouches[0];
  return [touch.clientX - rect.left, touch.clientY - rect.top];
};

// Event handlers
const mouseMove = evt => {
  if (!drawing) return;
  continueStroke([evt.offsetX, evt.offsetY]);
};

const mouseDown = evt => {
  if (drawing) return;

  evt.preventDefault();

  if (evt.button === 1) {
    context.globalCompositeOperation = 'destination-out';
  } else {
    context.globalCompositeOperation = 'source-over';
  }

  canvas.addEventListener("mousemove", mouseMove, false);
  startStroke([evt.offsetX, evt.offsetY]);
};

const mouseEnter = evt => {
  if (middleButtonIsDown(evt.buttons)) {
    context.globalCompositeOperation = 'destination-out';
  } else {
    context.globalCompositeOperation = 'source-over';
  }

  if ((!mouseButtonIsDown(evt.buttons) && !middleButtonIsDown(evt.buttons)) || drawing) {
    return;
  }
  mouseDown(evt);
};

const endStroke = evt => {
  if (!drawing) return;

  drawing = false;
  context.globalCompositeOperation = 'source-over';
  evt.currentTarget.removeEventListener("mousemove", mouseMove, false);
};

const touchStart = evt => {
  if (drawing) return;
  evt.preventDefault();
  startStroke(getTouchPoint(evt));
};

const touchMove = evt => {
  if (!drawing) return;
  continueStroke(getTouchPoint(evt));
};

const touchEnd = evt => {
  drawing = false;
};

// Register event handlers
canvas.addEventListener("touchstart", touchStart, false);
canvas.addEventListener("touchend", touchEnd, false);
canvas.addEventListener("touchcancel", touchEnd, false);
canvas.addEventListener("touchmove", touchMove, false);

canvas.addEventListener("mousedown", mouseDown, false);
canvas.addEventListener("mouseup", endStroke, false);
canvas.addEventListener("mouseout", endStroke, false);
canvas.addEventListener("mouseenter", mouseEnter, false);


hidetag(canvas);
// // // // // // // // // // // // // // // // // // // // // // // // // // // // 
// // // // // // // // // // // // // // // // // // // // // // // // // // // // 
///////////////////addEventListener
////////////////////////////////////////////////////////// 




///////////////////addEventListener
////////////////////////////////////////////////////////// 
addGlobalEventListener('click','#buttonShowCreativeImage',
()=>showtag(document.getElementById("canvasImage")))
          
 
addGlobalEventListener('click','#buttonHideCreativeImage',
()=>hidetag(document.getElementById("canvasImage")))



//////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////
   

let eventDisableDraw=()=>{

  let canvasDraw = document.getElementById("canvasDraw");
  canvasDraw.style.zIndex=-2;
  canvasDraw.style.border = "none";
  if (document.getElementById("buttonBrushSizeUp")){
    tabFuncMenu.removeChild(document.getElementById("buttonBrushSizeUp"));
    tabFuncMenu.removeChild(document.getElementById("buttonBrushSizeDown"))

  }
  // hidetag();
}


let eventExitImage=()=>{
  let img=document.getElementById("canvasImage");
  img.style.zIndex=-3;
  // remove buttons
  let tabFuncMenu = document.getElementById("tabFuncMenu");

  if (document.getElementById("buttonEditImageSizeUp")){
    tabFuncMenu.removeChild(document.getElementById("buttonEditImageSizeUp"));
    tabFuncMenu.removeChild(document.getElementById("buttonEditImageSizeDown"))
    tabFuncMenu.removeChild(document.getElementById("buttonRegenerateImage"))}


}


//////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////

addGlobalEventListener('click','#buttonEditImage',e=>{
  console.log(e.target.id);
  eventDisableDraw();
  e.preventDefault();  
  let img=document.getElementById("canvasImage");
  img.style.zIndex="2";
  draggable=new PlainDraggable(img,{containment:{left: fieldRect.x, top: fieldRect.y, width: fieldRect.width, height: fieldRect.height}})
  if (document.getElementById("buttonEditImageSizeUp")===null){
    funcBtn("Edit Image Size Up","FuncMenu");
    funcBtn("Edit Image Size Down","FuncMenu");
    funcBtn("Regenerate Image","FuncMenu");
;}
  })

addGlobalEventListener('click','#buttonEditImageSizeUp',e=>{
  console.log(e.target.id);
  updateimage(12);
})
addGlobalEventListener('click','#buttonEditImageSizeDown',e=>{
  console.log(e.target.id);
  updateimage(-12);
})      

addGlobalEventListener('click','#buttonRegenerateImage',e=>{
  let env=document.getElementById("tabEnv").innerHTML;
  console.log(env);
  let info = {
    "image": env,
  }
  fetch('/regenerate_image', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(info)
  })
  .then(response => {
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(newimage => {
    let img=document.getElementById("canvasImage");
    img.src = newimage["url"]
  })
  .catch(error => {
    console.error('Error:', error);
  });

})

addGlobalEventListener('click','#buttonExitEditImage',e=>{
    e.preventDefault();  
    eventExitImage();
  })

//////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////
addGlobalEventListener('click','#buttonEnableDraw',e=>{
  eventExitImage()
  let canvasDraw = document.getElementById("canvasDraw");
  canvasDraw.style.zIndex=3;
  canvasDraw.style.border = "1px solid #ccc";
  showtag(canvasDraw);
  if (document.getElementById("buttonBrushSizeUp")===null){
    funcBtn("Brush Size Up","FuncMenu");
    funcBtn("Brush Size Down","FuncMenu");
;}
  console.log(e.target.id);
    })
        

addGlobalEventListener('click','#buttonDisableDraw',e=>{
  console.log(e.target.id);
  eventDisableDraw();
    })
          

addGlobalEventListener('click','#buttonShowDraw',e=>{
  console.log(e.target.id);
  let canvasDraw = document.getElementById("canvasDraw");
  eventDisableDraw();
  showtag(canvasDraw);

})
addGlobalEventListener('click','#buttonHideDraw',e=>{
  console.log(e.target.id);
  eventDisableDraw();
  hidetag(document.getElementById("canvasDraw"));
})






addGlobalEventListener('click','#buttonBrushSizeUp',e=>{
  console.log(e.target.id);
  strokeWidth+=2;
})
addGlobalEventListener('click','#buttonBrushSizeDown',e=>{
  console.log(e.target.id);
  strokeWidth-=2;
})      







// function loadimage(newWidth){
//   var canvas = document.createElement('canvas');
//   var ctx = canvas.getContext('2d');

//   var newWidth = tagX * coefficient * 3; // The new width for the image

//   var image = new Image();
//   image.src = 'envir.png';

//   image.onload = function() {
//     // Set the canvas dimensions
//     canvas.width = newWidth;
//     canvas.height = newWidth;
//     ctx.fillStyle = "rgba(240, 248, 255, 0)";
  
//     // Fill the canvas
//     ctx.fillRect(0, 0, newWidth, newWidth);
//     // Draw the image onto the canvas
//     ctx.drawImage(image, 0, 0, newWidth, newWidth);
    
//     var resizedImage = canvas.toDataURL('image/png'); // Convert canvas content to an image
//     var resizedImageElement = new Image();
//     resizedImageElement.src = resizedImage;
//     resizedImageElement.id = "canvasImage";
//     resizedImageElement.style.position = "absolute";
//     resizedImageElement.style.zIndex = "-20";
//     resizedImageElement.style.resize = "both";
//     resizedImageElement.style.overflow = "hidden";
//     resizedImageElement.style.border = "1px solid #ccc";
//     resizedImageElement.style.boxSizing = "border-box";
    
//     let field = document.getElementById("field");
//     field.appendChild(resizedImageElement);
//   };
  
// }

// loadimage();
// create an image element
