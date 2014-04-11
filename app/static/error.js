/* displays shoutID for errormessage and redirects to frontpage */

window.onload = function()
{
    var shoutID = document.getElementById('shoutID');
    if(typeof(shoutID) != 'undefined' && shoutID !== null)
    {
        shoutID.style.display = 'block';
        console.log('fnordpad error. redirecting to index in ' + delay/1000 + ' seconds');
        var timeout = setTimeout(function()
        {
            window.location.href = '/';
        }, delay);
    }
};

