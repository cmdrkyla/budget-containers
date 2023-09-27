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
    if(localStorage.getItem("token") !== null)
        return localStorage.getItem("token");
    else if(sessionStorage.getItem("token") !== null)
        return sessionStorage.getItem("token");
    else
        return "";
}
function delete_token()
{
    if(localStorage.getItem("token") !== null)
        localStorage.removeItem("token")
    else if(sessionStorage.getItem("token") !== null)
        sessionStorage.removeItem("token");
}

function logout()
{
    delete_token();
    api_request("auth/logout").then((response) => {
        window.location.href = server_url + "login"
    });
}

function format_date(date)
{
    let js_date = new Date(date);
    // Fun with js dates - using "-" seperators with no time causes the date to be one day off
    js_date.setDate(js_date.getDate() + 1 );
    return js_date.getFullYear() + "-" + (js_date.getMonth()+1).toString().padStart(2,0) + "-" + js_date.getDate().toString().padStart(2,0);
}

function format_number(number)
{
    // TODO: toLocaleString isn't working on firefox, hardcoding to US for now
    let usa_format = new Intl.NumberFormat('en-US', {minimumFractionDigits: 2});
    return usa_format.format(number);
}

function null_to_ws(value)
{
    if(value === null)
        return "&nbsp;"
    else
        return value;
}

// Handlers
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
        api_request("auth/login", data, "POST").then((response) => {
            // Store in session or local storage (depending on remember_me)
            set_token(response.token, data.remember_me);
            // Load homepage
            window.location.href = server_url;
        },
        (error) => {
            message_center("Error logging in, please check your credentials and try again.", "error");
        })
    });

    // Logout
    $("#logout").on("click", function(event){
        event.preventDefault();
        logout();
    });
});