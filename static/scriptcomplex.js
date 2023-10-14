

// const flow_url ="simple/simpleflow.json";
// const matrix_url ="simple/simplematrix.json";
// const complexflow_url ="complex/flowtree.json";
// const complexmatrix_url ="complex/matrix.json";

// const inquireflow_url ="inquire/flowtree.json";
// const inquirematrix_url ="inquire/matrix.json";


const flow =  getData(flow_url);
const matrix = getData(matrix_url);
const complexflow =  getData(complexflow_url);
const complexmatrix = getData(complexmatrix_url);

const inquireflow =  getData(inquireflow_url);
const inquirematrix = getData(inquirematrix_url);
const usersystem = getData(systemrequest_url);

const matrixInput=[]
const matrixOutput=[]
const matrixMiddle=[];
const line=[];
const lineLibrary=[];
const matrixGroup=[]

const matrixInquire=[];
var newelement=[]

const lock=[]

// create a promise variable to wait for all data to be loaded
Promise.all([flow,matrix,complexflow,complexmatrix,inquireflow,inquirematrix,usersystem]).then(data => {
const flow = data[0]
const matrix = data[1]
const complexflow = data[2]
const complexmatrix = data[3]
const inquireflow = data[4]
const inquirematrix = data[5] 
const usersystem = data[6] 

logSimple(flow,matrix,matrixInput,matrixOutput,line,lineLibrary)
logComplex(complexflow,complexmatrix,matrixGroup,matrixMiddle,line,lineLibrary)
logInspiration(inquireflow,inquirematrix,matrixInquire,line,lineLibrary)
enableDropdownItems(line,lineLibrary)

// default setting
showsimpleflow(lineLibrary)

})// End of Promise.all !!!!!!!!!!!!!!!!!!!
// // // // // // // // // // // // // // // // // // // // // // 
// // // // // // // // // // // // // // // // // // // // // // 
// // // // // // // // // // // // // // // // // // // // // // 


function logSimple(flow,matrix,matrixInput,matrixOutput,line,lineLibrary){ 

  for (var key in matrix) {
    if (key === "TOTAL"){
      continue;}else{
    let keyObject = {key: key, color: matrix[key][0], loc: [matrix[key][1], matrix[key][2]]};
    if (matrix[key][1] ===0 ){
      matrixInput.push(keyObject);}
    else if(matrix[key][1] ===1){matrixOutput.push(keyObject)}
    else{console.log("error")}}}
    matrixInput.forEach(keyObject => {
    setTag(keyObject,document.getElementById("tabRight"))
    let tag = document.getElementById('tag' + keyObject.key)
    tag.style.left=tagX*(-4.5)+"px";
    tag.style.border ="5px solid black"//
  })
  matrixOutput.forEach(keyObject => {
    setTag(keyObject,document.getElementById("tabRight"))
    let tag = document.getElementById('tag' + keyObject.key)
    tag.style.left="0px";
    tag.style.border ="5px solid black"//
  })
  
  flow.forEach(flow => {
    for(var index=0; index<flow.length-1; index++) {
      let keyStart= flow[index];
      let tagStart = document.getElementById('tag' + keyStart)
      let keyEnd = flow[index+1];
      let tagEnd = document.getElementById('tag' + keyEnd)
      drawline(tagStart,tagEnd,line,lineLibrary)}})
  lineLibrary.forEach(lineObject => {lineObject.line.position()})
    return [matrixInput,matrixOutput,line,lineLibrary]
  }

function logComplex(complexflow,complexmatrix,matrixGroup,matrixMiddle,line,lineLibrary){
  for (var group in complexmatrix) {
    groupIndex = Object.keys(complexmatrix).indexOf(group)
    for (var key in complexmatrix[group]) {if (key === "TOTAL"){continue}
      else{let keyObject = {key: key, color: complexmatrix[group][key][0],loc: [complexmatrix[group][key][1], complexmatrix[group][key][2]],group:groupIndex};
        matrixMiddle.push(keyObject)}}

    let groupObject = {group:groupIndex, total:[complexmatrix[group]["TOTAL"][1],complexmatrix[group]["TOTAL"][2]],height:(complexmatrix[group]["TOTAL"][2]+1)*tagY*coefficient,width:(complexmatrix[group]["TOTAL"][1]+1)*tagX*coefficient}
    if (groupIndex>0){groupObject.top = matrixGroup[groupIndex-1].top+matrixGroup[groupIndex-1].height}else{groupObject.top = 30}
    matrixGroup.push(groupObject)}
    console.log(matrixMiddle)

    matrixGroup.forEach(groupObject => setTagGroup(groupObject,"tabMiddle"))
    matrixMiddle.forEach(keyObject =>{
      setTag(keyObject,document.getElementById('group' + keyObject.group))
      updatePaddling(keyObject,tabpad)})

    complexflow.forEach(flow => {  
      for(var index=0; index<flow.length-1; index++) {
      let keyStart= flow[index];
      let tagStart = document.getElementById('tag' + keyStart)
      let keyEnd = flow[index+1];
      let tagEnd = document.getElementById('tag' + keyEnd)

        // complexflow sauce
    //   if (matrixMiddle.every(keyObject => keyObject.key != keyStart)) {
    //     if(tagEnd.closest('.group')!=null){ 
    //       let group=tagEnd.closest('.group')
    //       tagStart.style.top = ((parseInt(group.style.height)/2+parseInt(group.style.top)-tagY/2))+"px"
    //       console.log()
    //     }
    // }
    //   if (matrixMiddle.every(keyObject => keyObject.key != keyEnd)) {
    //     if(tagStart.closest('.group')!=null){ 
    //       let group=tagStart.closest('.group')
    //       tagEnd.style.top =((parseInt(group.style.height)/2+parseInt(group.style.top)-tagY/2))+"px"
    //     }
    // }   



      drawline(tagStart,tagEnd,line,lineLibrary)}})
      lineLibrary.forEach(lineObject => {lineObject.line.position()})
return [matrixGroup,matrixMiddle,line,lineLibrary]
}

function logInspiration(inquireflow,inquirematrix,matrixInquire,line,lineLibrary){

  for (var key in inquirematrix) {
    if (key === "TOTAL"){
        continue;}
    else{
        let keyObject = {key: key, color: inquirematrix[key][0], loc: [inquirematrix[key][1], inquirematrix[key][2]]};
        matrixInquire.push(keyObject)
        newelement.push(keyObject.key)
  }}
  console.log(matrixInquire);
  

  matrixInquire.forEach(keyObject => {
    setTag(keyObject,document.getElementById("tabInspire"))
    updatePaddling(keyObject,tabpad)

    })
  

  
  inquireflow.forEach(flow => {
  for(var index=0; index<flow.length-1; index++) {
    let keyStart= flow[index];
    let tagStart = document.getElementById('tag' + keyStart)
    tagStart.setAttribute("data-inspiration", "true");
    let keyEnd = flow[index+1];
    let tagEnd = document.getElementById('tag' + keyEnd)
    tagEnd.setAttribute("data-inspiration", "true");
    drawline(tagStart,tagEnd,line,lineLibrary)}})

  lineLibrary.forEach(lineObject => {lineObject.line.position()})
return [matrixInquire,line,lineLibrary]
  
}

function logClassification(keytext,usersystem){
  console.log(usersystem)
  if(usersystem[keytext]){
  let tempcolor=findColor(keytext,usersystem)
  console.log(tempcolor)
  let tag = document.getElementById('tag' + keytext)
  tag.style.backgroundColor = colorToRGBA(tempcolor, 0.8);}
}
    
function showsimpleflow(lineLibrary){
  var buttons=document.querySelectorAll('button.tag');
  buttons.forEach(button => {hidetag(button)})
  lineLibrary.forEach(lineObject => {
    if(lineObject.line!=undefined && lineObject.line!=null){
      try {
        lineObject.line.hide("none")
    } catch (e) {
        return;
    }
   }})
  lineSimple=findSimpleLine(lineLibrary)
  lineSimple.forEach(lineObject => {
    try {
      lineObject.line.show("none")
  } catch (e) {
      return;
  }
    showtag(lineObject.line.start)
    showtag(lineObject.line.end)})
    tabs=["tabRight","tabLeft","tabMiddle"]
    tabs.forEach(tab => {
      let tabElement = document.getElementById(tab)
      tabElement.style.zIndex = "2"
    })
  let tabInspire = document.getElementById("tabInspire")
  tabInspire.style.zIndex = "1"

}


function showcomplexflow(lineLibrary){
  openModal(modal)
  var buttons=document.querySelectorAll('button.tag');
  buttons.forEach(button => {hidetag(button)})
  lineLibrary.forEach(lineObject => {
    if (lineObject.line!=undefined){
      try {
        lineObject.line.hide("none")
    } catch (e) {
        return;
    }
  
  
  }})

  lineComplex=findComplexLine(lineLibrary)
  lineComplex.forEach(lineObject => {
    try {
      lineObject.line.show("none")
  } catch (e) {
      return;
  }




    let tagStart = document.getElementById('tag' + lineObject.tagStart)
    let tagEnd = document.getElementById('tag' +lineObject.tagEnd)
    showtag(tagStart)
    showtag(tagEnd)




  }
    )




    tabs=["tabRight","tabLeft","tabMiddle"]
    tabs.forEach(tab => {
      let tabElement = document.getElementById(tab)
      tabElement.style.zIndex = "2"
    })
    let tabInspire = document.getElementById("tabInspire")
    tabInspire.style.zIndex = "1"
}

function showSeleced(lineLibrary){
  let selected=[]
  buttons=document.querySelectorAll('button.tag');
  buttons.forEach(button => {hidetag(button)})
  lineLibrary.forEach(lineObject => {
    if (lineObject.line!=undefined && lineObject.line!=null){
      try {
        lineObject.line.hide("none")
    } catch (e) {
        return;
    }
  
    
    
    }})

  buttons.forEach(button => {
    if(button.style.borderColor === "black"){
      showtag(button)
      selected.push(button.id.substring(3))
    }
  })
  lineLibrary.forEach(lineObject => {
    if (selected.includes(lineObject.tagStart) && selected.includes(lineObject.tagEnd)){
      try {
        lineObject.line.show("none")
        unselFlow(lineObject.line)
    } catch (e) {
        return;
    }
    showtag(lineObject.line.start)
    showtag(lineObject.line.end)
    unselElement(lineObject.line.start)
    unselElement(lineObject.line.end)
    }
  })
}

function returnlock(lock,lockflow,lineLibrary){
  buttons=document.querySelectorAll('button.tag');
  buttons.forEach(button => {
    if(button.style.borderColor === "black"){
      let taglock={key:button.id.substring(3),color:button.style.backgroundColor,loc:[parseInt(button.style.left)/tagX/coefficient,parseInt(button.style.top)/tagY/coefficient]}
      lock.push(taglock)
    }
  })
  lineLibrary.forEach(lineObject => {
    if (lock.includes(lineObject.tagStart) && lock.includes(lineObject.tagEnd)){
      let tagLockStart={key:lineObject.tagStart,color:lineObject.line.start.style.backgroundColor,loc:[parseInt(lineObject.line.start.style.left)/tagX/coefficient,parseInt(lineObject.line.start.style.top)/tagY/coefficient]}
      let tagLockEnd={key:lineObject.tagEnd,color:lineObject.line.end.style.backgroundColor,loc:[parseInt(lineObject.line.end.style.left)/tagX/coefficient,parseInt(lineObject.line.end.style.top)/tagY/coefficient]}
      lockflow.push([tagLockStart,tagLockEnd])
    }
  })
  console.log("This is new lock and lockflow.")
  console.log(lock,lockflow)
  return lock,lockflow
}

function showinspirationflow(lineLibrary){
  openModal(modal)
  tabs=["tabRight","tabLeft","tabInspire","tabMiddle"]
  tabs.forEach(tab => {
    let tabElement = document.getElementById(tab)
    tabElement.style.zIndex = "1"
  })
  var buttons=document.querySelectorAll('button.tag');
  buttons.forEach(button => {hidetag(button)})
  lineLibrary.forEach(lineObject => {
    if (lineObject.line!=undefined  && lineObject.line!=null){
      try {
        lineObject.line.hide("none")
    } catch (e) {
        return;
    }

}})
  inspirationLine=findInspirationLine(lineLibrary)
  inspirationLine.forEach(lineObject => {
    lineObject.line.show("none")
    let tagStart = document.getElementById('tag' + lineObject.tagStart)
    let tagEnd = document.getElementById('tag' + lineObject.tagEnd)
    showtag(tagStart)
    showtag(tagEnd)
    tagStart.zIndex = "2"
    tagEnd.zIndex = "2"
  }
    )

}
    

function setTag(keyObject,parent){
  if(document.getElementById('tag' + keyObject.key)){
    return;}  
  else{
    var tag = document.createElement("button");
    tag.className = 'tag';
    tag.id = 'tag' + keyObject.key;
    tag.style.width = tagX+"px";
    tag.style.height = tagY+"px";
    tagL =  keyObject.loc[0]*tagX*coefficient;
    tagT =  keyObject.loc[1]*(tagY)*coefficient;
    tag.style.left = tagL+"px";
    tag.style.top = tagT+"px";
    tag.style.borderStyle = "solid";
    tag.style.borderWidth = "1px";
    tag.style.borderColor = "white";
    tag.style.color = "white";
    tag.style.fontWeight = "bold";
    tag.style.backgroundColor = colorToRGBA(keyObject.color, 0.8);
    tag.innerHTML = keyObject.key;
    tag.style.borderRadius = "5px";
    tag.style.position="absolute";
    parent.appendChild(tag)

  }
}


function updatePaddling(keyObject,paddling){
  let tag = document.getElementById('tag' + keyObject.key)
  let tagL =  parseInt(tag.style.left)+(keyObject.loc[0]*paddling)
  tag.style.left= tagL+"px";
}

function setTagGroup(groupObject,parent){
  var div = document.createElement("div");
  div.className = 'group';
  div.id = 'group' + groupObject.group;
  div.style.position = "absolute";
  div.style.top = groupObject.top+"px";
  div.style.width = groupObject.width+"px";
  div.style.height = groupObject.height+"px";
  let tabMiddle = document.getElementById(parent);
  tabMiddle.appendChild(div);
}

function drawline(tagStart,tagEnd,line,lineLibrary){
  
  let startColor = tagStart.style.backgroundColor;
  let endColor = tagEnd.style.backgroundColor;
  // LeaderLine.pointAnchor(tagStart, {x: '100%', y: "50%"}),LeaderLine.pointAnchor(tagEnd, {x: '0%', y: "50%"}),
  var linetemp =new LeaderLine(tagStart,tagEnd,{
          startSocket: 'Right', endSocket: 'Left',
          startPlug: "hidden",
          startPlugSize: 4,
          endPlug: "arrow1",
          endPlugSize: 2,size: 1.5,
          startPlugColor:startColor,
          endPlugColor: endColor,
          gradient: true
          , path:'fluid',dropShadow: {color: 'white', dx: 0, dy: 0},
          startPlugOutline: true,
          startPlugOutlineColor:  startColor,
          startSocketGravity: [50,0],
          endSocketGravity: [-50,0],hide: false,})
  
  
  // create a JSON object to store the line and the tag
  let lineObject = {line:linetemp,tagStart:tagStart.id.substring(3),tagEnd:tagEnd.id.substring(3)}
  lineLibrary.push(lineObject);
  line.push(linetemp)
  let alllineSvg=document.querySelectorAll('.leader-line');
  let lastlineSvg=alllineSvg[alllineSvg.length-1]
  lastlineSvg.setAttribute("data-start",tagStart.id.substring(3));
  lastlineSvg.setAttribute("data-end",tagEnd.id.substring(3));

  draggable1=new PlainDraggable(tagStart,{onMove:fixLine,containment:
    {left: parseInt(field.style.left), top: parseInt(field.style.top)+30, width: parseInt(field.style.width), height: parseInt(field.style.height)}});
  draggable2=new PlainDraggable(tagEnd,{onMove:fixLine,containment:
    {left: parseInt(field.style.left), top: parseInt(field.style.top)+30, width: parseInt(field.style.width), height: parseInt(field.style.height)}});
  
  function fixLine() {

    lineLibrary.forEach(lineObject=> {

      let singleLine=lineObject.line

        // Check if the current line object is defined and has required properties
        if (singleLine) {
            try {
                singleLine.position();
            } catch (e) {
                return;
            }


            let startRect = singleLine.start.getBoundingClientRect();
            let endRect = singleLine.end.getBoundingClientRect();

            if (startRect.left > endRect.left) {
                singleLine.setOptions({
                    startSocket: 'left',
                    endSocket: 'right',
                    path: "fluid",
                    startSocketGravity: [-50, 0],
                    endSocketGravity: [50, 0],
                });
            } else if (startRect.left < endRect.left) {
                singleLine.setOptions({
                    startSocket: 'right',
                    endSocket: 'left',
                    startSocketGravity: [50, 0],
                    endSocketGravity: [-50, 0],
                });
            }
        }
    });
  }
  


}








// //////////////////////////////////////////////////////////////
// //////////////////////////////////////////////////////////////
// //////////////////////////////////////////////////////////////
// //////////////////////////////////////////////////////////////
// //////////////////////////////////////////////////////////////
function enableDropdownItems(line, lineLibrary,newelement) {
   console.log("Here is the line")
  console.log(line)
  console.log("Here is the lineLibrary")
  console.log(lineLibrary)

// // Everything in the funcMenu // // // // // // // // // // 
// // // // // // // // // // // // // // // // // // // // // // 
addGlobalEventListener('click','#buttonSaveSelected',e=>{
  returnlock(lock,lockflow,lineLibrary)
})

addGlobalEventListener('click','#buttonLookupSimpleFlow',e=>{
  console.log(e.target.id);
  showsimpleflow(lineLibrary)
  })

addGlobalEventListener('click','#buttonLookupComplexFlow',e=>{
  e.stopPropagation();
  console.log(e.target.id);
  showcomplexflow(lineLibrary)
  })

addGlobalEventListener('click','#buttonLookupElementCo-optimization',e=>{
  e.stopPropagation();
  console.log(e.target.id);
  showinspirationflow(lineLibrary)
  })

addGlobalEventListener('click','#buttonDisplaySelectedOnly',e=>{
  e.stopPropagation();
  console.log(e.target.id);
  showSeleced(lineLibrary)
  })
addGlobalEventListener('click','#buttonHideAllFlow',e=>{
  e.stopPropagation();
  console.log(e.target.id);
  lineSimple=findSimpleLine(lineLibrary)
  lineComplex=findComplexLine(lineLibrary)
  lineComplex.forEach(lineObject => lineObject.line.hide('none'))
  lineSimple.forEach(lineObject => lineObject.line.hide('none'))
  })
    
addGlobalEventListener('click', '#buttonASKSHERBOT', e => {
  console.log(e.target.id);
  openModal(modal)
  logInquire(lineLibrary);
})

// addGlobalEventListener('click', '#buttonConfirmSelect', e => {
//   // logSelected();
// })


  function getfulltaglist(){  
    var buttons=document.querySelectorAll('button.tag');
    var fulltaglist=[]
    buttons.forEach(button => {fulltaglist.push(button.id.substring(3))})
    return fulltaglist}



  clearDropdownItems()
  var tag = document.querySelectorAll('button.tag');
  tag.forEach(tag => createDropdown(tag))

  addGlobalEventListener('click', '#dropdownSelectElement', e => {
    clearSubDropdownItems()
    console.log(e.target.innerHTML);
    let tag = e.target.closest('.tag');
    selElement(tag, {color: "black"})
  })
  
  addGlobalEventListener('click', '#dropdownSelectInputFlow', e => {
    clearSubDropdownItems()
    console.log(e.target.innerHTML);
    let tag = e.target.closest('.tag');
    let inputline = findinputline(tag,lineLibrary)
    inputline.forEach(singleline => {
      appendSubDropdownItem(singleline.start.id.substring(3),e.target).addEventListener('click', e => {
      selFlow(singleline)
      })
    })
  })
  
  addGlobalEventListener('click', '#dropdownSelectOutputFlow', e => {
    clearSubDropdownItems()
    console.log(e.target.innerHTML);
    let tag = e.target.closest('.tag');
    let outputline = findoutputline(tag,lineLibrary,lineLibrary)//tag is an DOM element
    outputline.forEach(singleline => {
      if(singleline.end.style.visibility != "hidden"){
      appendSubDropdownItem(singleline.end.id.substring(3),e.target).addEventListener('click', e => {
      selFlow(singleline)
      })
    }
    })
  })
  
  addGlobalEventListener('click', '#dropdownUnselectElement', e => {
    clearSubDropdownItems()
    console.log(e.target.innerHTML);
    let tag = e.target.closest('.tag');
    unselElement(tag)
    lineLibrary.forEach(lineObject => {
      if (lineObject.tagStart === tag.id.substring(3) || lineObject.tagEnd === tag.id.substring(3)){
        unselFlow(lineObject.line)
        }
      })//End of lineLibrary.forEach
  })
  
  addGlobalEventListener('click', '#dropdownUnselectInputFlow', e => {
    clearSubDropdownItems()
    console.log(e.target.innerHTML);
    let tag = e.target.closest('.tag');
    let inputline = findinputline(tag,lineLibrary)
    inputline.forEach(line => {
      appendSubDropdownItem(line.start.id.substring(3),e.target).addEventListener('click', e => {
      unselFlow(line)
      })
    })
  })
  
  addGlobalEventListener('click', '#dropdownUnselectOutputFlow', e => {
    clearSubDropdownItems()
    console.log(e.target.innerHTML);
    let tag = e.target.closest('.tag');
    let outputline = findoutputline(tag,lineLibrary,lineLibrary)
    outputline.forEach(line => {
      appendSubDropdownItem(line.end.id.substring(3),e.target).addEventListener('click', e => {
      unselFlow(line)
      })
    })
  })
  
  ////////////////////////////////////////
  addGlobalEventListener('click', '#dropdownResetSystem', e => {
    clearSubDropdownItems()
    console.log(e.target.innerHTML);
    let tag = e.target.closest('.tag');
  
    systemlist=["HYDRO",'ENERGY','ECOSYSTEM','OTHERS']
    colorlist=["rgba(0, 174, 239, 0.8)","rgba(255, 198, 11, 0.8)","rgba(57, 181, 74, 0.8)","rgba(211, 211, 211, 0.8)"]
    
  
    for(let i = 0; i < systemlist.length; i++) {
      let item = appendSubDropdownItem(systemlist[i], e.target);
      item.addEventListener('click', e => {
          tag.style.backgroundColor = colorlist[i];
          console.log("clicked" + systemlist[i]);
  
          lineLibrary.forEach(lineObject => {
            if (lineObject.tagEnd === tag.id.substring(3)){
              lineObject.line.setOptions({endPlugColor: colorlist[i]})
              }
            if (lineObject.tagStart === tag.id.substring(3)){
              lineObject.line.setOptions({startPlugColor: colorlist[i]})
              }
            })//End of lineLibrary.forEach
  
      });
    }//End of for loop
  })
  
  addGlobalEventListener('click', '#dropdownAddNewInputFlow', e => {
    clearSubDropdownItems()
    console.log(e.target.innerHTML);
    let tag = e.target.closest('.tag');
    let inputtaglist=findinputtag(tag.id.substring(3),lineLibrary)
    let fulltaglist=getfulltaglist()
    let newtaglist=fulltaglist.filter(x => !inputtaglist.includes(x)).sort()
    // remove the tag itself from the list
    newtaglist=newtaglist.filter(x => x != tag.id.substring(3))
    newtaglist.forEach(tagtext => {
    appendSubDropdownItem(tagtext, e.target).addEventListener('click', e => {
      let tagStart = document.getElementById('tag' + tagtext)
      drawline(tagStart,tag,line,lineLibrary)
      console.log("clicked" + tagtext);
    })
  })
  })
  
  addGlobalEventListener('click', '#dropdownAddNewOutputFlow', e => {
    clearSubDropdownItems()
    console.log(e.target.innerHTML);
    let tag = e.target.closest('.tag');
    let outputtaglist=findoutputtag(tag.id.substring(3),lineLibrary)
    let fulltaglist=getfulltaglist()
    let newtaglist=fulltaglist.filter(x => !outputtaglist.includes(x)).sort()
    newtaglist=newtaglist.filter(x => x != tag.id.substring(3))
    newtaglist.forEach(tagtext => {
    appendSubDropdownItem(tagtext, e.target).addEventListener('click', e => {
      let tagEnd = document.getElementById('tag' + tagtext)
      drawline(tag,tagEnd,line,lineLibrary)
      console.log("clicked" + tagtext);
    })
    })
  })
  
  addGlobalEventListener('click', '#dropdownDeleteInputFlow', e => {
    clearSubDropdownItems()
    console.log(e.target.innerHTML);
    let tag = e.target.closest('.tag');
    let inputline=findinputline(tag,lineLibrary)
    inputline.forEach(singleline => {
      appendSubDropdownItem(singleline.start.id.substring(3),e.target).addEventListener('click', e => {
        removeLine(singleline,line,lineLibrary) })
    })   
  
  })
  
  addGlobalEventListener('click', '#dropdownDeleteOutputFlow', e => {
    clearSubDropdownItems()
    console.log(e.target.innerHTML);
    let tag = e.target.closest('.tag');
    let outputline=findoutputline(tag,lineLibrary)
    outputline.forEach(singleline => {
      appendSubDropdownItem(singleline.end.id.substring(3),e.target).addEventListener('click', e => {
        removeLine(singleline,line,lineLibrary)})
    })   
  })
  
  addGlobalEventListener('click', '#dropdownDeleteElement', e => {
    clearSubDropdownItems()
    console.log(e.target.innerHTML);
    let tag = e.target.closest('.tag');
    tag.remove()
    let inputline=findinputline(tag,lineLibrary)
    let outputline=findoutputline(tag,lineLibrary)
    inputline.forEach(singleline => {removeLine(singleline,line,lineLibrary)})
    outputline.forEach(singleline => {removeLine(singleline,line,lineLibrary)})
  })
    
  addGlobalEventListener('click', '#dropdownChangeFlowStyle', e => {
    clearSubDropdownItems()
    let tag = e.target.closest('.tag');
    console.log(e.target.innerHTML);
    let inputline=findinputline(tag,lineLibrary)
    let outputline=findoutputline(tag,lineLibrary)
    inputline.forEach(singleline => {
      appendSubDropdownItem(singleline.start.id.substring(3),e.target).addEventListener('click', e => {
        fixstyle(singleline)})})
    outputline.forEach(singleline => {
      appendSubDropdownItem(singleline.end.id.substring(3),e.target).addEventListener('click', e => {
        fixstyle(singleline)})})
        
  })
}//End of dropdown

// //////////////////////////////////////////////////////////////
// //////////////////////////////////////////////////////////////
// //////////////////////////////////////////////////////////////
// //////////////////////////////////////////////////////////////
// //////////////////////////////////////////////////////////////

// Dropdown DOM Objects /////////////////////////////////////////
// //////////////////////////////////////////////////////////////
const dropdownState = new Map();
addGlobalEventListener('contextmenu', 'button.tag', e => {
  e.stopPropagation(); 
  // Hide all dropdowns except for the target
  let allDropdowns = document.querySelectorAll('.dropdown-menu');
  allDropdowns.forEach(dropdown => {
      dropdown.style.opacity = 0;
      dropdown.style.transform = 'translateY(-10px)';
      dropdown.style.pointerEvents = 'none';
  });

  // Now, show or hide the target dropdown
  let dropdowns = e.target.querySelectorAll('.dropdown-menu');
  dropdowns.forEach(dropdown => {
    const currentState = dropdownState.get(dropdown) || false;

    if (currentState) {
        // If the dropdown is currently shown, hide it.
        e.target.style.zIndex = "1";
        dropdown.style.opacity = 0;
        dropdown.style.transform = 'translateY(-10px)';
        dropdown.style.pointerEvents = 'none';
        // remove all sub-dropdowns
        let subdropdowns = document.querySelectorAll('.dropdown-item-sub');
        subdropdowns.forEach(subdropdown => {
          subdropdown.remove();
        });
    } else {
        // If the dropdown is currently hidden, show it.
        e.target.style.zIndex = "3";
        dropdown.style.opacity = 1;
        dropdown.style.transform = 'translateY(0)';
        dropdown.style.pointerEvents = 'auto';
    }

    // Update the state in our Map.
    dropdownState.set(dropdown, !currentState);
});
  e.preventDefault();
 // To prevent the default context menu from appearing
});


addGlobalEventListener('click', '.dropdown-item, .dropdown-item-sub', e => {
  let tag = e.target.closest('.tag');
  tag.style.zIndex = "3";

})


function createDropdown(tagElement){
  // add dropdown menu
  var dropdown = document.createElement('div');
  dropdown.className = 'dropdown-menu';
  tagElement.appendChild(dropdown);

  appendDropdownItem('Select Element',dropdown)
  appendDropdownItem('Select Input Flow',dropdown)
  appendDropdownItem('Select Output Flow',dropdown)
  appendDropdownItem('Unselect Element',dropdown)
  appendDropdownItem('Unselect Input Flow',dropdown)
  appendDropdownItem('Unselect Output Flow',dropdown)
  appendDropdownItem('',dropdown)//This group are about selection and send further for focused display and inquire
  
  // add new tag is double-click
  appendDropdownItem('Reset System',dropdown)//Please do not hide, but only delete
  appendDropdownItem('Add New Input Flow',dropdown)
  appendDropdownItem('Add New Output Flow',dropdown)
  appendDropdownItem('Delete Input Flow',dropdown)//Please do not hide, but only delete
  appendDropdownItem('Delete Output Flow',dropdown)//Please do not hide, but only delete
  appendDropdownItem('Delete Element',dropdown)//Please do not hide, but only delete
  // appendDropdownItem('',dropdown)//This group are about add and delete

  appendDropdownItem('Change Flow Style',dropdown)//Please do not hide, but only delete
  // appendDropdownItem('Generate Complex Process',dropdown)
  // appendDropdownItem('Cooptimization Element',dropdown)
  let emptyItems=document.querySelectorAll("#dropdown")
  emptyItems.forEach(emptyItem => emptyItem.style.visibility = "hidden")

}

function appendDropdownItem(itemName,dropdown){
  let item = document.createElement('div');
  item.className = 'dropdown-item';
  item.id = "dropdown" + itemName.replace(/\s+/g, '');
  item.innerHTML = "&#9656  "+itemName;
  dropdown.appendChild(item);
}

function appendSubDropdownItem(itemName,dropdown){
  if (document.getElementById('dropdownsub' + itemName.replace(/\s+/g, ''))){
    let item = document.getElementById('dropdownsub' + itemName.replace(/\s+/g, ''));
    return item}else{
  let item = document.createElement('div');
  item.className = 'dropdown-item-sub';
  item.style.transform="translateX(20px)";
  item.style.color="grey"
  item.id = "dropdownsub" + itemName.replace(/\s+/g, '');
  item.innerHTML = "&#9656  "+itemName;
  dropdown.appendChild(item)
  return item}
}

function clearSubDropdownItems() {
  var subItems = document.querySelectorAll('.dropdown-item-sub');
  subItems.forEach(item => {
          item.remove();
  });
}

function clearDropdownItems(){
  var dropdowns = document.querySelectorAll('.dropdown-item');
  dropdowns.forEach(item => {
          item.remove();
  });
}
// //////////////////////////////////////////////////////////////
// //////////////////////////////////////////////////////////////


// Dropdown DOM Objects /////////////////////////////////////////
// //////////////////////////////////////////////////////////////

function removeLine(singleline,line,lineLibrary){
  line.forEach(l => {if (l === singleline){
    try {
      l.remove()
  } catch (e) {
      return;
  } }})
  lineLibrary.filter(lineObject => lineObject.line != singleline)
}

function findSimpleLine(lineLibrary){
  let simpleLine=[];

  var simplebuttons=findElement("tabRight").concat(findElement("tabLeft"))
  var simplebuttontags=simplebuttons.map(button => button.id.substring(3))

  lineLibrary.forEach(lineObject => {
    if(simplebuttontags.includes(lineObject.tagStart) && simplebuttontags.includes(lineObject.tagEnd)){
      simpleLine.push(lineObject);
    }
  })
  return simpleLine;
}


function findInspirationLine(lineLibrary) {
  let inspirationLine = [];
  console.log(lineLibrary)
  var buttons=document.querySelectorAll('button.tag');
  buttons.forEach(button => {console.log(button.dataset.inspiration)})
  var inspirationbuttons = Array.from(buttons).filter(button => button.dataset.inspiration === "true");
  var inspirationbuttontags = inspirationbuttons.map(button => button.id.substring(3))
  console.log(inspirationbuttontags)
  lineLibrary.forEach(lineObject => {
    if(inspirationbuttontags.includes(lineObject.tagStart) && inspirationbuttontags.includes(lineObject.tagEnd)){
      inspirationLine.push(lineObject)
    }
  })
  return inspirationLine;
}

function findComplexLine(lineLibrary){
  let complexLine=[];

  var complexbuttons=findElement("tabMiddle")
  var complexbuttontags=complexbuttons.map(button => button.id.substring(3))
  lineLibrary.forEach(lineObject => {
    if(complexbuttontags.includes(lineObject.tagStart) || complexbuttontags.includes(lineObject.tagEnd)){
      complexLine.push(lineObject)
    }
  })
  return complexLine;
}

function findElement(tabname){
  let Element=[];
  // find all child element under tabname
  let tab = document.getElementById(tabname);
  // get all button elements under tab
  let buttons = tab.getElementsByTagName("button");
  // iterate through all buttons
  for (var i = 0; i < buttons.length; i++) {
    Element.push(buttons[i])}
  return Element
}
function findinputtag(tagtext,lineLibrary){
  let inputtaglist=[]
  lineLibrary.forEach(lineObject => {
    if (lineObject.tagEnd === tagtext){
      let tagStart = document.getElementById('tag' + lineObject.tagStart)
      inputtaglist.push(tagStart)
      }
    })//End of lineLibrary.forEach
  return inputtaglist
}
function findoutputtag(tagtext,lineLibrary){
  let outputtaglist=[]
  lineLibrary.forEach(lineObject => {
    if (lineObject.tagStart === tagtext){
      let tagEnd = document.getElementById('tag' + lineObject.tagEnd)
      outputtaglist.push(tagEnd)
      }
    })//End of lineLibrary.forEach
  return outputtaglist
}
function findinputline(tag,lineLibrary){ 
  //tag is an DOM element
  let inputline=[]
  lineLibrary.forEach(lineObject => {
    try{
      if (lineObject.line.end.id === tag.id){
        inputline.push(lineObject.line)
        }}
      catch(err){
        return
      }
    })//End of lineLibrary.forEach
  return inputline//inputline is a collection of lineObjects
}
function findoutputline(tag,lineLibrary){
  //tag is an DOM element
  let outputline=[]
  lineLibrary.forEach(lineObject => {
    try{
      if (lineObject.line.start.id=== tag.id){
        outputline.push(lineObject.line)
        }}
      catch(err){
        return
      }
    })//End of lineLibrary.forEach
  return outputline//inputline is a collection of lineObject
}



function clearTag(butthese=[]){
  var buttons=document.querySelectorAll('button.tag');
  buttons.forEach(button => {
    if (!butthese.includes(button.id.substring(3))){button.remove()}
  })
}

// Helper Function for Dropdown Menu


function clearLine(){
  // var line=document.querySelectorAll('.leader-line');
  // line.forEach(line => {line.remove()})
  lineLibrary.forEach(lineObject => {
    removeLine(lineObject.line,line,lineLibrary)})
}


function selElement(tag, options = {}) { 
  // Set default values for the options
  const { flowtoggle = false, color = "black" } = options;

  tag.setAttribute("data-selected", "true");
  
  // If flowtoggle is true, set the attribute
  if (flowtoggle) {tag.setAttribute("data-selected-flow", "true");}
  
  tag.style.borderColor = color;
  tag.style.borderWidth = "5px";
}

function unselElement(tag, options = {}) { 
  // Set default values for the options
  const { flowtoggle = true, color = "white" } = options;

  tag.setAttribute("data-selected", "false");
  
  // If flowtoggle is true, set the attribute
  if (flowtoggle) {tag.setAttribute("data-selected-flow", "false");}
  
  tag.style.borderColor = color;
  tag.style.borderWidth = "1px";
}

function selFlow(line){
  line.setOptions({          
      outline: true,
      endPlugOutline: true,
      outlineColor: "black",
      outlineSize: 5,
      size: 15,  
      endPlugSize: 0.5})
    selElement(line.start,{color: "black",flowtoggle: "true"})
    selElement(line.end,{color: "black",flowtoggle: "true"})
}

function unselFlow(line){
  line.setOptions({          
      outline: false,
      endPlugOutline: false,
      endPlugSize: 2,size: 1.5
    })
  unselElement(line.start)
  unselElement(line.end)
}

function clearSelection(){
  var buttons=document.querySelectorAll('button.tag');
  buttons.forEach(button => {
    unselElement(button,{flowtoggle: "true"})
  })
  lineLibrary.forEach(lineObject => {
    if(lineObject.line!=undefined && lineObject.line!=null){
    unselFlow(lineObject.line)}
  })
}

function fixstyle(line){
  let start=line.start
  let end=line.end
  let startRect = start.getBoundingClientRect();
  let endRect = end.getBoundingClientRect();


  if (startRect.left > endRect.left) {
    line.setOptions({          
      path:'arc',
      startSocketGravity: [0,-50],
      endSocketGravity: [0,50]
    })
} else if (startRect.left < endRect.left) {
  line.setOptions({          
    path:'arc',
    startSocketGravity: [0,-50],
    endSocketGravity: [0,-50]
  })

}



}
function logInquire(lineLibrary){
  let toinquireElement = [];
  let toinquireFlow = [];
  let toinquireSystem = [];

  var buttons = document.querySelectorAll('button.tag');
  buttons.forEach(button => {
      if (button.dataset.selected === "true") {
          toinquireElement.push(button.id.substring(3));
      }
      if (button.dataset.unknownClass === "true") {
        toinquireSystem.push(button.id.substring(3));
      }
  }); // End of buttons.forEach

  lineLibrary.forEach(lineObject => {
      // if lineObject is not undefined
      if (lineObject.line!=undefined && lineObject.line!=null){
        if(document.getElementById("tag"+lineObject.tagStart)&&document.getElementById("tag"+lineObject.tagEnd)){
        tag1=document.getElementById("tag"+lineObject.tagStart)
        tag2=document.getElementById("tag"+lineObject.tagEnd)
        if (tag1.style.borderColor==="black"&&tag2.style.borderColor==="black") {
            toinquireFlow.push([tag1.id.substring(3), tag2.id.substring(3)]);
        }}
      }else{return}

  });


  // clear the dataattribute
  buttons.forEach(button => {
      button.setAttribute("data-selected", "false");
      button.setAttribute("data-selected-flow", "false");
      button.setAttribute("data-unknown-class", "false");
      button.setAttribute("data-inspiration", "false");
  });



  ////////////////////////////////////////////
  ////////////////////////////////////////////

  let info = {
      "toinquireElement": toinquireElement,
      "toinquireFlow": toinquireFlow,
      "toinquireSystem": toinquireSystem
  }

  fetch('/inquire_data', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(info)
  })
  .then(response => {
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      return response.json();
  })
  .then(newdata => {
      console.log(newdata);
      console.log(newdata.toinquireFlow);
      console.log(newdata.toinquireElement);
      console.log(newdata.toinquireSystem);

      newflow=newdata.toinquireFlow;
      newelement=newdata.toinquireElement;
      newsystem=newdata.toinquireSystem;

      // clearSelection();
      butelement=[];
      newflow.forEach(flow => flow.forEach(key => {butelement.push(key)}))
      newelement.forEach(key => butelement.push(key))
      newsystem.forEach(key => butelement.push(key))
      clearTag(butelement);
      clearLine()
      const flow =  getData(flow_url);
      const matrix = getData(matrix_url);
      const complexflow =  getData(complexflow_url);
      const complexmatrix = getData(complexmatrix_url);
      const inquireflow =  getData(inquireflow_url);
      const inquirematrix = getData(inquirematrix_url);
      const usersystem = getData(systemrequest_url);
      // clean the data

      const matrixInput=[]
      const matrixOutput=[]
      const matrixMiddle=[];
      const line=[];
      const lineLibrary=[];
      const matrixGroup=[]
      const matrixInquire=[];

      Promise.all([flow,matrix,complexflow,complexmatrix,inquireflow,inquirematrix,usersystem]).then(data => {

        const flow = data[0]
        const matrix = data[1]
        const complexflow = data[2]
        const complexmatrix = data[3]
        const inquireflow =  data[4]
        const inquirematrix =  data[5]
        const usersystem = data[6]


        logSimple(flow,matrix,matrixInput,matrixOutput,line,lineLibrary)
        logComplex(complexflow,complexmatrix,matrixGroup,matrixMiddle,line,lineLibrary)
        logInspiration(inquireflow,inquirematrix,matrixInquire,line,lineLibrary)
        newsystem.forEach(keytext => {
          logClassification(keytext,usersystem)
        })
        console.log("Here is the new data")
        console.log([matrixInput,matrixOutput,line,lineLibrary])
        enableDropdownItems(line,lineLibrary,newelement)

        // showsimpleflow(lineLibrary)
        // showinspirationflow(lineLibrary)
        // showcomplexflow(lineLibrary)

        if(newflow.length>0){showcomplexflow(lineLibrary)} else if (newelement.length>0){showinspirationflow(lineLibrary)}else{showsimpleflow(lineLibrary)}
      })
        fetchRepeatedly();
  })
  .catch(error => {
      console.error('Error:', error);
  });

  return info;
};




// function logSelected(){
//   let selectedElement=[];
//   let selectedFlow=[];
//   // let toclassifyElement=[];

//   var buttons=document.querySelectorAll('button.tag');

//   buttons.forEach(button => {
//     if (button.dataset.selected === "true"){
//       selectedElement.push(...matrixMiddle.filter(keyObject => keyObject.key === button.id.substring(3)));
//       selectedElement.push(...matrixInput.filter(keyObject => keyObject.key === button.id.substring(3))); 
//       selectedElement.push(...matrixOutput.filter(keyObject => keyObject.key === button.id.substring(3))); 
//     }
//     if (button.dataset.selectedFlow === "true"){
//       // find all flow and complexflow that contains the tag
//       selectedFlow.push(...complexflow.filter(flow => flow.includes(button.id.substring(3))));
//       selectedFlow.push(...flow.filter(flow => flow.includes(button.id.substring(3))));
  
//     }
//     // if (button.dataset.unknownClass === "true"){
//     //   toclassifyElement.push(button.id.substring(3));
//     // }
//   })// End of buttons.forEach

//   // get rid of the duplicates in selectedElement, selectedFlow, toclassifyElement
//   selectedElement = [...new Set(selectedElement)];
//   selectedFlow = [...new Set(selectedFlow)];
//   // toclassifyElement = [...new Set(toclassifyElement)];

//   let info= {selectedElement:selectedElement,selectedFlow:selectedFlow}

//   downloadJSON(info, 'info.json');  // Call the function to trigger download
//   return info
// }//End of function



function captureAndCombine() {
  // get the body of the document
  let divs = ['field', 'canvasboard'];  // Replace with your div IDs


  Promise.all(divs.map(divId => {
      let element = document.getElementById(divId);
      return html2canvas(element, { backgroundColor: null });  // Ensure background is transparent
  })).then(results => {
      // Determine the combined canvas dimensions
      let maxWidth = Math.max(...results.map(canvas => canvas.width));
      let maxHeight = Math.max(...results.map(canvas => canvas.height));
      
      let combinedCanvas = document.createElement('canvas');
      combinedCanvas.width = maxWidth;
      combinedCanvas.height = maxHeight;
  
      let ctx = combinedCanvas.getContext('2d');
  
      results.forEach(canvas => {
          ctx.drawImage(canvas, 0, 0);
      });
  
      let link = document.createElement('a');
      link.href = combinedCanvas.toDataURL("image/png");
      link.download = 'overlay_screenshot.png';
      link.click();
  });

}



addGlobalEventListener('click','#buttonSaveBoard',e=>{
  console.log(e.target.id);
  captureAndCombine();
    }
  )
