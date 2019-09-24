import socket
import sys

def create_mimetype(path):
    mimetype = 'Content-Type: '
    ext = path.split('.')[-1]

    if ext == 'txt':
        mimetype += 'text/plain'
    elif ext in ['jpg', 'jpeg']:
        mimetype += 'image/jpeg'
    elif ext == 'png':
        mimetype += 'image/png'
    elif ext == 'html':
        mimetype += 'text/html'
    else:
        return None

    mimetype += '\r\n'
    return mimetype

def run_server(server_port):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', server_port))
    server_socket.listen(1)

    print('Server is listening on port {}'.format(server_port))

    while True:
        connection, addr = server_socket.accept()
        message = connection.recv(1024).decode('utf-8')
        message_parts = message.split(' ')

        print('user {} was connected.'.format(addr))

        try:
            method = message_parts[0]
            file_path = message_parts[1]
            http_version = message_parts[2].split('\r\n')[0]

            if file_path == '/':
                file_path += 'index.html'


            file_name = file_path.split('/')[-1]
            file = open('.' + file_path, 'rb')
            response = file.read()
            file.close()

            header = '{} 200 OK\r\n'.format(http_version)

            mimetype = create_mimetype(file_path)

            if mimetype:
                header += mimetype
            # else:
                # header += 'Content-Disposition: form-data; name="files";\
                #                      filename="{}"\r\n'.format(file_name)

            print('method {} returns {}'.format(method, file_path))

        except:
            header = '{} 404 Not Found\n\n'.format(http_version)
            response = '<html><body><center><h1>Error 404</h1><h3> File "{}" not found\
                                    </h3></center></body></html>'.format(file_name).encode('utf-8')

            print('method {} file "{}" not found.'.format(method, file_name))

        final_response = header.encode('utf-8')
        final_response += '\r\n'.encode('utf-8')
        final_response += response
        final_response += '\r\n'.encode('utf-8')

        connection.send(final_response)
        connection.close()

if __name__ == '__main__':
    port = 3000

    if len(sys.argv) > 1:
        port = sys.argv[1]

    run_server(int(port))
