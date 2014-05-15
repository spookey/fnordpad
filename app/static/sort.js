/* window load launch */

function zeroimagereload()
{
    if(document.getElementsByTagName('img').length === 0)
    {
        console.log('out of images, reloading');
        var timeout = setTimeout(function()
        {
            window.location.reload();
        }, delay/8);
    }
}

function imagerequest(image, action)
{
    var xmlhttp = new XMLHttpRequest();
    if(xmlhttp.overrideMimetype)
    {
        xmlhttp.overrideMimetype('text/xml');
    }

    if(xmlhttp)
    {
        xmlhttp.onreadystatechange = function()
        {
            var shoutID = document.getElementById('shoutID');
            var imageID = document.getElementById(image);
            if(xmlhttp.readyState == 4 && xmlhttp.status == 200)
            {
                shoutID.innerHTML = xmlhttp.responseText;
                imageID.parentNode.removeChild(imageID);
            } else
            {
                shoutID.innerHTML = 'Error [ ' + xmlhttp.statusText + ' ]';

            }
            shoutID.style.display = 'block';
            var timeout = setTimeout(function()
            {
                shoutID.style.display = 'none';
            }, delay/2);
            zeroimagereload();
        };

        var senddata = {
            'image': image,
            'action': action
        };

        xmlhttp.open('POST', '/sort/action/', true);
        xmlhttp.setRequestHeader('Content-type', 'application/json');
        xmlhttp.send(JSON.stringify(senddata));
    }
}

window.onload = function()
{
    zeroimagereload();
};
