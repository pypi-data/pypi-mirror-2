$(document).ready(function() {
$('#control').append('<div id="" class="button">Led 1</div>');
$('.button')
    .button()
    .click(function() {
        alert($(this).text());
    });
var reload = function() {
    $('img').attr('src', '/static/image?'+Math.random())
    setTimeout(reload, 2000);
};
reload();
});
