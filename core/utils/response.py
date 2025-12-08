from rest_framework import response

def api_response(data=None, message=None, status_code=200, success=True):
    return response.Response(
        {
            "success": success,
            "message": message,
            "data": data,
            "status_code": status_code,
        },
        status=status_code
    )
