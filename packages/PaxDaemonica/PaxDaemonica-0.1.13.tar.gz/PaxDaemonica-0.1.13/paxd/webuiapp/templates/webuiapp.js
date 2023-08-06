$(function() {
    $('#app-list .action').click(function(e) {
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
    
    $('#failed .action.remove').click(function(e) {
        e.preventDefault();
        var self = $(this);
        var tr = $(this).parents('tr')
        var fid = tr.data('fid');
        var log = $('.'+fid+'.log td');
        var url = $(this).attr('href');
        $.get(url, function(data){
            if(data.status == 'SUCCESS') {
                $('.'+fid).remove();
            } else {
                log.append($('<div>FAILURE</div>'));
            }
        }, 'json');
    });
    
    $('#failed .action.requeue').click(function(e) {
        e.preventDefault();
        var self = $(this);
        var tr = $(this).parents('tr')
        var fid = tr.data('fid');
        var log = $('.'+fid+'.log td');
        var url = $(this).attr('href');
        $.get(url, function(data){
            if(data.status == 'SUCCESS') {
                $('.'+fid).remove();
            } else {
                log.append($('<div>FAILURE</div>'));
            }
        }, 'json');
    });
})
