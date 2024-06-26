// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {

    // Get the elements that we want to activate and deactivate 
    const register_button = document.getElementById('register_button');
    const anmelden_button = document.querySelector('#anmelden_button');

    // register_button.disabled = true;
    register_button.style.visibility = 'hidden';

    if(document.getElementById("email_host_var").value==="True") { 
        //register_button.disabled = true;
        register_button.style.visibility = 'visible';
    } else { 
        //register_button.disabled = false;
        register_button.style.visibility = 'hidden';
        anmelden_button.style.position = "absolute";
        anmelden_button.style.left = "50%";
        anmelden_button.style.transform = "translateX(-50%)";
    }


    

});