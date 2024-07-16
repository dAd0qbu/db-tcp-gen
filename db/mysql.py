class MySQL:
    def __init__(self, user="root", password="", database="", queries=[]):
        self._user = user.encode()
        # TODO: Implement password handling
        self._password = password.encode()
        self._database = database.encode()
        self._queries = [query.encode() for query in queries]

    def _prepend_mysql_packet(self, payload, sequence_id=0):
        payload_length = len(payload).to_bytes(length=3, byteorder="little")
        sequence_id = sequence_id.to_bytes(length=1, byteorder="little")

        return payload_length + sequence_id + payload

    def _connection_phase_payload(self):
        client_flag = b"\x8d\xa2\x1a\x00"
        max_packet_size = b"\x00\x00\x00\x00"
        character_set = b"\x2d"
        filler = b"\x00" * 23
        username = self._user + b"\x00"
        auth_response = b"\x00"
        database_name = self._database + b"\x00"
        client_plugin_name = b"mysql_native_password\x00"
        attrs = b"\x00"
        handshakeResponse41_payload = (
            client_flag
            + max_packet_size
            + character_set
            + filler
            + username
            + auth_response
            + database_name
            + client_plugin_name
            + attrs
        )
        return handshakeResponse41_payload

    def _command_phase_payload(self, query):
        return b"\x03" + query

    def _generate_list_query(self):
        res = b""
        for query in self._queries:
            payload = self._command_phase_payload(query)
            res += self._prepend_mysql_packet(payload)
        return res

    def gen_tcp_payload(self):
        res = b""
        connection = self._prepend_mysql_packet(
            payload=self._connection_phase_payload(), sequence_id=1
        )
        commands = self._generate_list_query()
        quit_db = b"\x01\x00\x00\x00\x01"

        res = connection + commands + quit_db
        return res.hex()
