var current_address = window.location.href;
$(document).ready(function(){
    // cannot use .children() because the <dt> are not direct children
    $('div.topnav').find('a').each(function() {
        if (this.href == current_address){
            console.log(current_address)
            this.classList.add("active");
        }
    });
});