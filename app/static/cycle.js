var delay = 10000;

function cycle()
{
    setTimeout(function(){window.location.reload();}, delay * 20);
    if(document.getElementsByTagName('img').length > 0)
    {
        var images = document.getElementById('images').getElementsByTagName('img');
        var index = 0;

        images[index].style.display = 'block';
        var current = parseInt(document.getElementById('served').innerHTML, 10);
        setInterval(function(){
            images[index].style.display = 'none';
            document.getElementById('served').innerHTML = current + index + 1;
            index = (index + 1) % images.length;
            images[index].style.display = 'block';
        }, delay);
    }
}
