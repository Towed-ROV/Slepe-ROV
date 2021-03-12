<<<<<<< Updated upstream
=======


>>>>>>> Stashed changes
class PayloadReader:

    def read_payload(self, received_data):
        """
        extracts data from message received
        :param received_data: data received from zmq
        :return: the data type and the data of the payload
        """
<<<<<<< Updated upstream
        payload_type = received_data['payload_name']
        data = received_data['payload_data']
        payload_name = data.split(':', 1)[0].replace('{', '').replace('"', "").strip()
        payload_data = data.split(':', 1)[1].replace('}', '').replace('"', "").strip()
        return payload_type, payload_name, payload_data
=======
        print('kurt')
        payload_type = received_data['payload_name']
        print(payload_type)
        data = received_data['payload_data']
        test = iter(data)
        keys= []
        values = []
        for k in data:
            size = len(k)
            print(size)
            for key, value in k.items():
                print(key,value)
                keys.append(key)
                values.append(value)
        return payload_type, keys, values

>>>>>>> Stashed changes
