var height = (window.innerHeight/2);

function justify()
{
    if(document.getElementsByTagName('img').length > 0)
    {
        var images = document.getElementById('content').getElementsByTagName('img');
        var index = images.length;

        while (index--)
        {
            images[index].style.paddingTop = Math.round(height - images[index].height/2) + 'px';
        }
    }
}

