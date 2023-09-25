function message_center(message, type="success")
{
    // Clear any previous message first
    $("#message_center").removeClass();
    $("#message_content").text("");
    $("#message_content").text(message);
    $("#message_center").addClass(type).show(300);
}

function set_token(token, remember_me)
{
    if(remember_me)
        localStorage.setItem("token", token)
    else
        sessionStorage.setItem("token", token)
}
function get_token()
{
    if(localStorage.getItem("token"))
        return localStorage.getItem("token");
    else if(sessionStorage.getItem("token"))
        return sessionStorage.getItem("token");
    else
        return "";
}


$(document).ready( function()
{
    // Login
    $("#body_login form").on("submit", function(event){
        event.preventDefault();
        data = {
            "email_address": $("#field_email_address").val(),
            "password": $("#field_password").val(),
            "remember_me": $("#field_remember_me").is(":checked")
        }
        process_request("auth/login", data, "POST").then((response) => {
            // Store in session or local storage (depending on remember_me)
            set_token(response.token, data.remember_me);
            // Load homepage
            window.location.href = server_url;
        },
        (error) => {
            message_center("Error logging in, please check your credentials and try again.", "error");
        })
    });
});