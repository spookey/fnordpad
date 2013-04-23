function vertical()
{
    if(document.getElementsByTagName('img').length > 0)
    {
        var pictures = document.getElementsByTagName('img');
        var i = pictures.length;

        if(document.getElementById('image'))
        {
            var height = (window.innerHeight/2);
        } else {
            var height = 100;
        }

        while (i--)
        {
            pictures[i].style.paddingTop = Math.round(height - pictures[i].height/2) + 'px';
        }
    }


}

window.onload=vertical;
