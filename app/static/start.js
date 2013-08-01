
function start()
{
    var start_images = document.getElementById('images');
    var start_sort = document.getElementById('sort');
    var start_error = document.getElementById('error');

    if(typeof(start_images) != 'undefined' && start_images != null)
    {
        cycle();
        justify();
    }
    if(typeof(start_sort) != 'undefined' && start_sort != null)
    {
        shortcut();
        justify();
    }

    if(typeof(start_error) != 'undefined' && start_error != null)
    {
        setTimeout(function()
        {
            window.location.href = '/';
        }, 5000);
    }
}

window.onload = start;
