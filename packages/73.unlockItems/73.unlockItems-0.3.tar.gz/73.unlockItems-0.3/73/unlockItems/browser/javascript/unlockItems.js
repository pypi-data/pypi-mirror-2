
// Permet de selectionner - deselectionner toutes les boites a cocher
function toggleCheck(check){
    var l_elements = document.getElementsByName('itemsObj:list');
    if (check==1) {
        for (var i=0;i<l_elements.length;i++){  
            l_elements[i].checked=true;
        }
    }
    else{
        for (var i=0;i<=l_elements.length;i++){  
            l_elements[i].checked=false;
        }
    }
}