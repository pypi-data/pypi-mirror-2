jq(document).ready(function() {	
	jq("input[name='paths:list']").change(function(e) {
		
		var checked_status = this.checked;
		var childUl = jq(this).parent().parent().children('ul');
		
		var childInput = childUl.find('input[@name=paths:list]');
		//alert(childInput.attr('value'));
		childInput.attr('checked', checked_status);
		childInput.attr('disabled', checked_status);
	});
	jq("#migration-confirm-form input[@name=form.button.Save]").click(function(e){jq("#kss-spinner").show());
});