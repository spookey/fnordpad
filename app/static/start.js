/* window load launch */

function setclock()
{
    var clockID = document.getElementById('clockID');
    var dateID = document.getElementById('dateID');
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

        if(typeof(dateID) != 'undefined' && dateID !== null)
        {
            dateID.innerHTML = day + '. ' + months[month] + ' ' + year;
        }
        if(typeof(clockID) != 'undefined' && clockID !== null)
        {
            clockID.innerHTML = hours + ':' + minutes + ':' + seconds;
        }
    }, 250);

}

function imagechannel()
{
    console.log('listening to images');
    var imagestream = new EventSource('/stream/image/');
    imagestream.onmessage = function(event)
    {
        var currentimage = document.getElementById('imageID');
        if(typeof(currentimage) != 'undefined' && currentimage !== null)
        {
            var nextimage = new Image();
            nextimage.src = '/static/' + event.data;
            nextimage.alt = event.data;
            nextimage.id = 'imageID';
            currentimage.parentNode.insertBefore(nextimage, currentimage);
            currentimage.parentNode.removeChild(currentimage);
            console.log('new image: ' + event.data);
        }

    };
}

function shoutchannel()
{
    console.log('listening to shouts');
    var shoutstream = new EventSource('/stream/shout/');
    shoutstream.onmessage = function(event)
    {
        var shoutID = document.getElementById('shoutID');
        if(typeof(shoutID) != 'undefined' && shoutID !== null)
        {
            shoutID.innerHTML = event.data;
            shoutID.style.display = 'block';
            console.log('shout: ' + event.data);
            var timeout = setTimeout(function()
            {
                shoutID.style.display = 'none';
            }, delay);
        }

    };
}

window.onload = function()
{
    imagechannel();
    shoutchannel();
    setclock();
};
