
function start()
{
    var start_images = document.getElementById('images');
    var start_sort = document.getElementById('sort');

    if(typeof(start_images) != 'undefined' && start_images != null)
    {
        cycle();
        justify();
        console.info('start: images');
    }
    if(typeof(start_sort) != 'undefined' && start_sort != null)
    {
        justify();
        console.info('start: sort');
    }
}

window.onload = start;
