$(function() {
    $('.action').click(function(e) {
        var self = $(this);
        var tr = $(this).parents('tr')
        e.preventDefault();
        var url = $(this).attr('href');
        $.get(url, function(data) {
            if(data.status != 'SUCCESS') {
                alert('FAILED');
            } else {
                alert('SUCCESS');
                $('.status', tr).text(data.app.status);
            }
        }, 'json');
    });
    $('.unstoppable .action.stop').remove();
})