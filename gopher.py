def to_gopher_payload(port, data):
    if type(data) == str:
        data = data.encode()

    a = [data[i : i + 2] for i in range(0, len(data), 2)]
    return b"gopher://127.0.0.1:" + port + b"/_%" + b"%".join(a)
