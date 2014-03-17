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
    };
}

function setclock()
{
    var clock = document.getElementById('clock');
    var date = document.getElementById('date');
    months = new Array('Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez');
    var interval = setInterval(function()
    {
        var time = new Date();

        var day = time.getDate();
        var month = time.getMonth();
        var year = time.getFullYear();

        var hours = time.getHours();
        var minutes = time.getMinutes();
        var seconds = time.getSeconds();

        if(day < 10)
        {
            day = '0' + day;
        }
        if(hours < 10)
        {
            hours = '0' + hours;
        }
        if(minutes < 10)
        {
            minutes = '0' + minutes;
        }
        if(seconds < 10)
        {
            seconds = '0' + seconds;
        }

        if(typeof(date) != 'undefined' && date !== null)
        {
            date.innerHTML = day + '. ' + months[month] + ' ' + year;
        }
        if(typeof(clock) != 'undefined' && clock !== null)
        {
            clock.innerHTML = hours + ':' + minutes + ':' + seconds;
        }
    }, 100);

}

function imagecycle(image)
{

    var imagesource = new EventSource('/index/stream');
    var xmlhttp = new XMLHttpRequest();

    imagesource.onmessage = function(event)
    {

        var currentimage = document.getElementById('currentimage');
        if(typeof(currentimage) != 'undefined' && currentimage !== null)
        {
            if(currentimage.complete)
            {
                var nextimage = new Image();
                nextimage.src = '/image/' + event.data;
                nextimage.alt = event.data;
                nextimage.id = 'currentimage';
                currentimage.parentNode.insertBefore(nextimage, currentimage);
                currentimage.parentNode.removeChild(currentimage);
            }
        }
    };

    var interval = setInterval(function()
    {
        xmlhttp.open("GET", "/index/next", true);
        xmlhttp.send(null);
    }, delay);

}

function shoutbox(shout)
{
    var shoutsource = new EventSource('/shout/stream');
    shoutsource.onmessage = function(event)
    {
        shout.innerHTML = event.data;
        shout.style.display = 'block';

        var timeout = setTimeout(function()
        {
            shout.style.display = 'none';
        }, delay);

    };
}

function start()
{

    var sortc = document.getElementById('sort');
    var error = document.getElementById('error');
    var clock = document.getElementById('clock');
    var image = document.getElementById('currentimage');
    var datet = document.getElementById('date');
    var shout = document.getElementById('shout');


    if(typeof(sortc) != 'undefined' && sortc !== null)
    {
        shortcuts();
    }

    if(typeof(error) != 'undefined' && error !== null)
    {
        setTimeout(function()
        {
            window.location.href = '/';
        }, delay / 2);
    }

    if(typeof(clock) != 'undefined' && clock !== null || typeof(datet) != 'undefined' && datet !== null)
    {
        setclock();
    }

    if(typeof(image) != 'undefined' && image !== null)
    {
        imagecycle(image);
    }



    if(typeof(shout) != 'undefined' && shout !== null)
    {
        shoutbox(shout);
    }
}

window.onload = start;
