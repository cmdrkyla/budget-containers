async function process_request(slug, data=null, method="GET")
{
    let url = server_url + "api/" + slug;
    return await $.ajax({
        url: url,
        type: method,
        data: (data) ? JSON.stringify(data) : null,
        contentType: "application/json",
        headers: { 'X-Login-Token': get_token() }
    });
}