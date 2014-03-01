var delay = 15000;

function shortcuts()
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

function setclock()
{
    var clock = document.getElementById('clock');
    var interval = setInterval(function ()
    {
        var time = new Date();
        var hours = time.getHours();
        var minutes = time.getMinutes();
        var seconds = time.getSeconds();
        if (hours < 10)
        {
            hours = '0' + hours;
        }
        if (minutes < 10)
        {
            minutes = '0' + minutes;
        }
        if (seconds < 10)
        {
            seconds = '0' + seconds;
        }
        if(typeof(clock) != 'undefined' && clock != null)
        {
            clock.innerHTML = hours + ':' + minutes + ':' + seconds;
        }
    }, 100);

}

function shifting()
{
    var img_total = document.getElementsByTagName('img').length;
    document.getElementsByTagName('img')[0].style.marginLeft = (window.innerWidth + 'px')/2;
    document.getElementsByTagName('img')[img_total - 1].style.marginRight = (window.innerWidth + 'px')/2;
    var img_pos = img_total;
    var step = 1;
    setInterval(function(){
        document.getElementById('img' + img_pos).scrollIntoView();
        img_pos -= step;
        if(img_pos <= 1 || img_pos >= img_total)
        {
            step *= -1;
        }
    }, delay / 2);
}

function start()
{
    var start_images = document.getElementById('images');
    var start_sort = document.getElementById('sort');
    var start_error = document.getElementById('error');
    var clock = document.getElementById('clock');
    var shout = document.getElementById('shout');

    if(typeof(start_images) != 'undefined' && start_images != null)
    {

        setTimeout(function()
        {
            window.location.reload();
        }, delay * 25);

        shifting();

    }
    if(typeof(start_sort) != 'undefined' && start_sort != null)
    {
        shortcuts();
    }

    if(typeof(start_error) != 'undefined' && start_error != null)
    {
        setTimeout(function()
        {
            window.location.href = '/';
        }, 5000);
    }

    if(typeof(clock) != 'undefined' && clock != null)
    {
        setclock();
    }

    if(typeof(shout) != 'undefined' && shout != null)
    {

        var source = new EventSource('/shout/stream/');
        source.onmessage = function(event)
        {
            shout.innerHTML = event.data;
            shout.style.display = 'block';

            var timeout = setTimeout(function()
            {
                shout.style.display = 'none';
            }, delay);

        };

    }
}

window.onload = start;
