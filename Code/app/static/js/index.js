function changeLabel(){
	
	document.getElementById("uploadButtonName").style.display = 'none';
	document.getElementById("manualISBNinput").style.display = 'none';
	
	document.getElementById("cauta").style.display = 'inline-block';
	document.getElementById("fileToUpload").style.display = 'inline-block';
	document.getElementById("labelUpload").style.background = 'gray';
	document.getElementById("labelUpload").style.background = '#232323';
}



function showSearchBtnIfText(){
	document.getElementById("uploadButtonName").style.display = 'none';
	document.getElementById("labelUpload").style.display = 'none';
	document.getElementById("cauta").style.display = 'inline-block';
}

