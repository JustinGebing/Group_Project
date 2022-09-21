$(function(){
	$('submit','image-form').click(function(){
		
		$.ajax({
			url: '/new/bill',
			data:$('#inputImage').val(),
			type: 'POST',
			success: function(){
				alert('saved');
			},
			error: function(){
				alert('error');
			}
		});
	});
});