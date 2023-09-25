async function api_request(slug, data=null, method="GET")
{
    let url = server_url + "api/" + slug;
    return await $.ajax({
        url: url,
        type: method,
        data: (data) ? JSON.stringify(data) : null,
        dataType: "json",
        contentType: "application/json",
        headers: { 'X-Login-Token': get_token() },
        error: function(response)
        {
            // 403 => send to login page cause they are logged out
            if(response.status == 403)
                window.location.href = server_url + "login"
        }
    });
}