
function shortcut()
{

    var click_event = document.createEvent('MouseEvent');
    click_event.initMouseEvent ('click', true, true, window);

    document.onkeydown=function(e)
    {
        if(e.which == 80) //p
        {
            // Plus
            document.getElementById('plus').dispatchEvent(click_event);
        }

        if(e.which == 77) //m
        {
            // Minus
            document.getElementById('minus').dispatchEvent(click_event);
        }

        if(e.which == 65) //a
        {
            // Again
            window.location.reload();
            return false;
        }

        if(e.which == 72) //h
        {
            // Home
            document.location.href = '/index';
            return false;
        }

    }

}
