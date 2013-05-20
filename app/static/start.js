
function start()
{
    var start_images = document.getElementById('images');
    var start_sort = document.getElementById('sort');

    if(typeof(start_images) != 'undefined' && start_images != null)
    {
        cycle();
        justify();
    }
    if(typeof(start_sort) != 'undefined' && start_sort != null)
    {
        justify();
        shortcut();
    }
}

window.onload = start;
