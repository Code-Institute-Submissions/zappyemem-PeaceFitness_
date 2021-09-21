$('.datepicker').datepicker();


function disableActions(bDisable = "none") {
	let cardActions = document.getElementsByClassName("card-action");
	for(let i = 0; i < cardActions.length; i++) {
		cardActions[i].style.pointerEvents = bDisable
	}
}

function openModal() {
	let url = $('#confirm_modal_button').data('url');
	$('#yes_confirm').attr('href', url);
	$("#confirm_modal").show();
	disableActions();
}

function hideModal() {
	$('#confirm_modal').hide();
	disableActions("auto");
}