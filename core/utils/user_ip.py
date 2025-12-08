def user_ip(request):
    x_forwared_for = request.META.get("X_FORWARED_FOR")
    remote_addr = request.META.get("REMOTE_ADDR")

    if x_forwared_for:
        ip = x_forwared_for.split(",")[0].strip()
    if remote_addr:
        ip = remote_addr

    return ip

