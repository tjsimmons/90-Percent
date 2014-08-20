/***************************/
//@Author: Adrian "yEnS" Mato Gondelle
//@website: www.yensdesign.com
//@email: yensamg@gmail.com
//@license: Feel free to use it, but keep this credits please!					
/***************************/

//SETTING UP OUR POPUP
//0 means disabled; 1 means enabled;
var popupStatus = 0;

//loading popup with jQuery magic!
function loadPopup(a){
	centerPopup();
	//loads popup only if it is disabled
	if(popupStatus==0){
		$("#backgroundPopup").css({
			"opacity": "0.7"
		});
		$("#backgroundPopup").fadeIn("slow");
		$("#popupContact").fadeIn("slow");
		popupStatus = 1;
	}
	//alert(a.substring(4));
	//var v=document.getElementById('hproductdesc_EPWHROV0').value;
	//alert(v);
	var productCodeId = a.substring(4);
	var hcategory 		= document.getElementById('hcategory_'+productCodeId).value;
	var hproductcode 	= document.getElementById('hproductcode_'+productCodeId).value;
	var hproductdesc 	= document.getElementById('hproductdesc_'+productCodeId).value;
	var henddate 		= document.getElementById('henddate_'+productCodeId).value;
	var htype 			= document.getElementById('htype_'+productCodeId).value;
	var hbrand 			= document.getElementById('hbrand_'+productCodeId).value;
	var htdu 			= document.getElementById('htdu_'+productCodeId).value;
	var hrank 			= document.getElementById('hrank_'+productCodeId).value;
	var hverbiage 		= document.getElementById('hverbiage_'+productCodeId).value;
	var hstatus 		= document.getElementById('hstatus_'+productCodeId).value;
	
	//alert(hcategory +".."+hproductcode+".."+hproductdesc+".."+henddate+".."+htype+".."+hbrand+".."+htdu+".."+hrank+".."+hverbiage);
	
	document.getElementById('inputCategory').value=hcategory;
	document.getElementById('inputProductId').value=productCodeId;
	document.getElementById('inputProductCode').value=hproductcode;
	document.getElementById('inputProductDesc').value=hproductdesc;
	document.getElementById('inputProducteddate').value=henddate;
	document.getElementById('inputProductType').value=htype;
	document.getElementById('inputProductBrand').value=hbrand;
	document.getElementById('inputProductTDU').value=htdu;

	document.getElementById('inputCallCenter').value=hverbiage;
	document.getElementById('inputStatus').value=hstatus;
	
	if(hstatus == 'Y'){
		document.getElementById('inputStatus').className="on";
		document.getElementById('inputStatus').value = "Active";
	}else{
		document.getElementById('inputStatus').className="off";
		document.getElementById('inputStatus').value = "Inactive";
	}
	
	//Get select object
	var objSelect = document.getElementById('inputProductRank');

	//Set selected
	setSelectedValue(objSelect, hrank);
	
	
}

function setSelectedValue(selectObj, valueToSet) {
    for (var i = 0; i < selectObj.options.length; i++) {
        if (selectObj.options[i].text== valueToSet) {
            selectObj.options[i].selected = true;
            return;
        }
    }
}

//disabling popup with jQuery magic!
function disablePopup(){
	//disables popup only if it is enabled
	if(popupStatus==1){
		$("#backgroundPopup").fadeOut("slow");
		$("#popupContact").fadeOut("slow");
		popupStatus = 0;
	}
}

//centering popup
function centerPopup(){
	//request data for centering
	var windowWidth = document.documentElement.clientWidth;
	var windowHeight = document.documentElement.clientHeight;
	//alert($("#popupContact").height());alert($("#popupContact").width());
	var popupHeight = $("#popupContact").height();
	var popupWidth = $("#popupContact").width();
	//centering
	$("#popupContact").css({
		"position": "absolute",
		"top": windowHeight/2-popupHeight/2-300,
		"left": windowWidth/2-popupWidth/2,
		"height": "650px"
	});
	//only need force for IE6
	
	$("#backgroundPopup").css({
		"height": windowHeight
	});
	
}

/*
//CONTROLLING EVENTS IN jQuery
$(document).ready(function(){
	
	//LOADING POPUP
	//Click the button event!
	$("#popId").click(function(){
		//centering with css
		centerPopup();
		//load popup
		loadPopup();
	});
				
	//CLOSING POPUP
	//Click the x event!
	$("#popupContactClose").click(function(){
		disablePopup();
	});
	//Click out event!
	$("#backgroundPopup").click(function(){
		disablePopup();
	});
	//Press Escape event!
	$(document).keypress(function(e){
		if(e.keyCode==27 && popupStatus==1){
			disablePopup();
		}
	});

});*/