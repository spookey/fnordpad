var delay = 10000;
// Fade dauert min 2200 ms, delay muss >= 2500 sein

function cycle()
{
    setTimeout(function(){window.location.reload();}, delay * 20);
    if(document.getElementsByTagName('img').length > 0)
    {
        var images = document.getElementById('images').getElementsByTagName('img');
        var index = 0;

        fadeImg(images[index], 0, true);
        setInterval(function(){
            index = (index + 1) % images.length;
            fadeImg(images[index], 0, true);
        }, delay);
    }
}

function fadeImg(img, val, fadein){
    if(fadein === true)
    {
        val++;
    } else
    {
        val--;
    }

    if(val > 0)
    {
        img.style.display = 'block';

    } else {
        img.style.display = 'none';
    }

    if(val === 100)
    {
        setTimeout(function(){fadeImg(img, 100, false);}, delay-2200);
    } // delay-2200 ~> 2200 == 2 mal 100 Fade-Stufen je 10 ms plus 200 ms Pause

    if(val > 0 && val < 100)
    {
        img.style.opacity = val / 100;
        setTimeout(function(){fadeImg(img, val, fadein);}, 10);
    }
}
