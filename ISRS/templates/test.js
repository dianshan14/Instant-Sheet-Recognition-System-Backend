function send_request()
{
    sheetData = {
        'asd': 10,
        'asdasd': [
            'a','b' 
        ]
    }
    $.ajax({
        type: "POST",
		url: "http://18.191.142.38/test",
        data: sheetData,
        success: showResult,
        error: onError
    });
}