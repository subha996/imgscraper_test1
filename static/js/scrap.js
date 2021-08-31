$(function(){
    $('#nEmail, .Shedul').css('display','none');
    $('#shld').click(function(){
        $('#nEmail, .Shedul').css('display','inline-block');
        setTimeout(function(){$('#shld').attr('type','Submit');},1000);
        $('#shld').attr('value','Submit');
    });
    $('#dwnlN').click(function(){
        $('form').attr('action','download_now')
    });
});