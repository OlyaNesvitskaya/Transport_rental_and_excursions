var current_address = window.location.href;
$(document).ready(function(){
    $('div.topnav').find('a').each(function() {
        if (this.href == current_address){
            this.classList.add("active");
        }
    });
});