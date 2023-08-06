
function getCheckedTab() {
    var tab_lockedItems = new Array();        
	var chkbox = document.getElementsByName('itemId:list');
	for (var i = 0; i < chkbox.length; i++){
		if (chkbox[i].checked) {
		       tab_lockedItems.push(chkbox[i].value);	                                 
		}
	}
	return tab_lockedItems
}


// Permet de selectionner - deselectionner toutes les boites a cocher
function toggleCheck(check){
    var l_elements = document.getElementsByName('itemId:list');
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
function items2unlock() {
 var items = getCheckedTab();
 unlockItemsQuery.getJSON('./unlockItems?items_ids='+items,
	                               function(data) {
	                                    document.forms['findlockeditems_form'].submit();
	                               })
}