function inout_selectAllWords(theList) {
  myList = document.getElementById(theList);
  for (var x=0; x < myList.length; x++) {
    myList[x].selected="selected";
  }
}

function inout_addNewKeyword(toList, newText, newValue) {
  theToList=document.getElementById(toList);
  for (var x=0; x < theToList.length; x++) {
    if (theToList[x].text == newText) {
      return false;
    }
  }
  theLength = theToList.length;
  theToList[theLength] = new Option(newText);
  theToList[theLength].value = newValue;
}

function inout_moveKeywords(fromList,toList,selectThese) {
  theFromList=document.getElementById(fromList);
  for (var x=0; x < theFromList.length; x++) {
    if (theFromList[x].selected) {
      inout_addNewKeyword(toList, theFromList[x].text, theFromList[x].value);
    }
  }
  theToList=document.getElementById(fromList);
  for (var x=theToList.length-1; x >= 0 ; x--) {
    if (theToList[x].selected) {
      theToList[x] = null;
    }
  }
  inout_selectAllWords(selectThese);
}

function inout_moveUp(id) {
    var select_box = document.getElementById(id)
    var index = select_box.selectedIndex;

    if (index == 0)
      return;

    value = select_box[index].value;
    text = select_box[index].text;
    select_box[index].value = select_box[index - 1].value;
    select_box[index].text = select_box[index - 1].text;
    select_box[index - 1].value = value;
    select_box[index - 1].text = text;

    select_box.selectedIndex--;
    inout_selectAllWords(id);
}

function inout_moveDown(id) {
    var select_box =document.getElementById(id)
    var index = select_box.selectedIndex;
    if (index == select_box.length - 1)
      return;
    value = select_box[index].value;
    text = select_box[index].text;
    select_box[index].value = select_box[index + 1].value;
    select_box[index].text = select_box[index + 1].text;
    select_box[index + 1].value = value;
    select_box[index + 1].text = text;
    select_box.selectedIndex++;
    inout_selectAllWords(id);
}
