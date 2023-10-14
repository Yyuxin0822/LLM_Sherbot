async function getData(url) {
  const response = await fetch(url);
  return response.json();}

function addGlobalEventListener(type,selector,callback){
  document.addEventListener(type,e=>{
      if(e.target.matches(selector)) callback(e);
  })
}

function downloadJSON(data, filename) {
  var fileData = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data, null, 4));
  var downloader = document.createElement('a');
  downloader.setAttribute('href', fileData);
  downloader.setAttribute('download', filename);
  downloader.click();
}

function hidetag(element){element.style.visibility = "hidden"}

function showtag(element){element.style.visibility = "visible"} 
menuButton=[];
// create buttons under "tabFunction"
function funcBtn(text,pane){
  // get rid of space in text
  var button = document.createElement('button')
  button.className = 'button';
  button.id = 'button'+text.replace(/\s/g, '');
  let tabFunction = document.getElementById("tab"+pane);
  tabFunction.appendChild(button);
  if (pane==="Function"||pane==="Env"){button.innerHTML = text;}
  else if (pane==="FuncMenu"){
    button.innerHTML = "&#9656  "+text
    // add underline stylye to button
    button.style.textDecoration = "underline";
    menuButton.push(button);
}
}


// funcBtn("Show Simple Flow","Function");
// funcBtn("Show Complex Flow","Function");
funcBtn("Explore","Function");
// funcBtn("Save Board","Function");
funcBtn("Show Note","Function");
funcBtn("ASK SHERBOT","Env");

function clearMenu(){
  menuButton.forEach(button => button.remove())}

// addGlobalEventListener('click','#buttonShowSimpleFlow,#buttonShowComplexFlow',e=>{
//   clearMenu();
//   funcBtn("Show Creative Image","FuncMenu");
//   funcBtn("Hide Creative Image","FuncMenu");
// })


addGlobalEventListener('click','#buttonShowNote',e=>{
  console.log(e.target.id);
  openModal(document.getElementById('modal'))
})


addGlobalEventListener('click','#buttonExplore',e=>{
  console.log(e.target.id);
  clearMenu();

  funcBtn("Lookup Simple Flow","FuncMenu");
  funcBtn("Lookup Complex Flow","FuncMenu");


  funcBtn("Lookup Element Co-optimization","FuncMenu");
  funcBtn("Display Selected Only","FuncMenu");
  // funcBtn("Save Selected","FuncMenu");

  funcBtn("Edit Image","FuncMenu");
  funcBtn("Exit Edit Image","FuncMenu");
  funcBtn("Show Creative Image","FuncMenu");
  funcBtn("Hide Creative Image","FuncMenu");
  
  funcBtn("Enable Draw","FuncMenu");
  funcBtn("Disable Draw","FuncMenu");
  funcBtn("Show Draw","FuncMenu");
  funcBtn("Hide Draw","FuncMenu");

  // funcBtn("Hide All Flow","FuncMenu");
})






















   





// build double click event listener for "field"
//////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////
const fullsystemlist=["HYDRO",'ENERGY','ECOSYSTEM','OTHERS','UNKNOWN']
const fullcolorlist=[colorToRGBA("#00aeef",0.8),colorToRGBA("#ffc60b",0.8),colorToRGBA("#39b54a",0.8),colorToRGBA("lightgrey",0.8),colorToRGBA("lightgrey",0.8)]
const systeminfo =  getData(systemDataUrl);
function findColor(text,system){
  let keytext = text.toUpperCase();
  let foundSystem;
  if (system[text])  {
      foundSystem = system[keytext];
      let index = fullsystemlist.indexOf(foundSystem);
      colortemp= fullcolorlist[index];
  }else {colortemp= fullcolorlist[3];}
  // console.log(colortemp);
  return colortemp;
}

const MAX_DOUBLE_CLICK_TIME = 500;
systeminfo.then(system => {
// Double-click custom event listener
field.addEventListener('custom:doubleClick', e => {
    //... rest of your code for the double-click event

    const inputBox = document.createElement('input');
    inputBox.type = 'text';
    inputBox.placeholder = 'Input Element Here...';
    inputBox.style.position = 'fixed';  // Example styling, adjust as needed
    inputBox.style.top = e.detail.clientY+ 'px';
    inputBox.style.left =  e.detail.clientX + 'px';
    document.body.appendChild(inputBox);
    inputBox.addEventListener('blur', () => {
        console.log('Input value:', inputBox.value);
        if (inputBox.parentNode) {  document.body.removeChild(inputBox); } // Remove the input from the DOM
      });
    inputBox.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
          if(document.getElementById("tag"+inputBox.value.toUpperCase())===null){
            let keytext = inputBox.value.toUpperCase();
            let inputObject ={key:keytext,color: findColor(keytext,system)};
            var tag = document.createElement("button");
            tag.className = 'tag';
            tag.id = 'tag' + inputObject.key;
            tag.style.width = tagX+"px";
            tag.style.height = tagY+"px";
            console.log(window.scrollX,window.scrollY)
            tag.style.left = (e.detail.clientX + window.scrollX-435) + 'px';
            tag.style.top = (e.detail.clientY + window.scrollY-270) + 'px';
            tag.style.borderStyle = "solid";
            tag.style.borderWidth = "1px";
            tag.style.borderColor = "white";
            tag.style.color = "white";
            tag.style.fontWeight = "bold";
            tag.style.backgroundColor = inputObject.color;
            tag.innerHTML = inputObject.key
            tag.style.borderRadius = "5px";
            tag.style.position="absolute";
            let parent = document.getElementById("tabMiddle");
            parent.appendChild(tag)
            if (inputObject.color===fullcolorlist[3]){
            tag.setAttribute("data-unknown-class", "true");}
            createDropdown(tag);

            draggable=new PlainDraggable(tag,{containment:{left: fieldRect.x, top: fieldRect.y, width: fieldRect.width, height: fieldRect.height}})}

          if (inputBox.parentNode) {  inputBox.parentNode.removeChild(inputBox); }
        }
    },{capture: true,
      bubbles: false,
      cancelable: true});
  

    inputBox.focus();
});

let lastClick = 0;
field.addEventListener('click', e => {
    // e.stopPropagation();

    const clientX = e.clientX;
    const clientY = e.clientY;

    const timeBetweenClicks = e.timeStamp - lastClick;
    if (timeBetweenClicks > MAX_DOUBLE_CLICK_TIME) {
        lastClick = e.timeStamp;
        return;
    }

    const doubleClickEvent = new CustomEvent('custom:doubleClick', {
        detail: {timeBetweenClicks, clientX, clientY},
        capture: true,
        bubbles: false,
        cancelable: true
    });

    field.dispatchEvent(doubleClickEvent);
    lastClick = 0;
}, {capture: false, bubbles: false});// end of field.addEventListener
})// end of systemInfo.then




// End of double click event listener for canvas
////////////////////////////////////////////////////




// selet all buttons under tabFunction
addGlobalEventListener('auxclick', 'button.tag', e => {
  if (e.button === 1) {
      console.log(e.target.id);
      let button = document.getElementById(e.target.id);
      hidetag(button);

      lineLibrary.forEach(lineObject => {
        if (lineObject.tagStart === e.target.id.substring(3) || lineObject.tagEnd === e.target.id.substring(3)){
          lineObject.line.hide('none');
        }
      })
      e.preventDefault();  // To prevent default behavior of middle-click
  }
});



// End of double click event listener for canvas
////////////////////////////////////////////////////
function colorToRGBA(inputColor, alpha) {
  // Create an off-screen canvas
  var canvas = document.createElement('canvas');
  canvas.width = canvas.height = 1;
  var ctx = canvas.getContext('2d');

  // Render the named color to the canvas
  ctx.fillStyle = inputColor;
  ctx.fillRect(0, 0, 1, 1);

  // Retrieve the rgb values
  var data = ctx.getImageData(0, 0, 1, 1).data;

  // Return in RGBA format
  return `rgba(${data[0]}, ${data[1]}, ${data[2]}, ${alpha})`;
}

