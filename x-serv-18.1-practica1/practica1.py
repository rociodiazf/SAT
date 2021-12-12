#!/usr/bin/python3

import webapp
from urllib.parse import unquote

formulario = """
    <form action="" method="POST">
        Escribe la url: <input type="text" name="url" value=" ">
        <input type="submit" value="Enviar">
    </form>
"""
back = "<a href= http://localhost:1234/ >Back</a></h1>"


class contentApp (webapp.webApp):

    # -- Diccionario 1: nº url acrtada --> url reales
    dicc_1 = {'0': 'http://google.com'}

    # -- Diccionario 2: url real --> nº url acortada
    dicc_2 = {'http://google.com': '0'}

    def parse(self, request):
        print(request)
        method = request.split(' ', 1)[0]
        resource = request.split(' ', 2)[1]
        body = request.split('\r\n\r\n', 1)[-1]

        return (method, resource, body)

    def process(self, parsedRequest):

        # -- "/" included
        method, resource, body = parsedRequest
        print(resource)

        if method == "GET":

            if resource == "/":
                # -- Devolvemos el formulario y uno de los diccionarios
                httpCode = "HTTP/1.1 200 OK"
                htmlBody = ("<html><body><h1>" + formulario + "</h1><h1>" +
                    str(self.dicc_2) +"</h1></body></html>")

            elif resource == "/favicon.ico":
                httpCode = "HTTP/1.1 404 Not Found"
                htmlBody = ("<html><body><h1>Not found</h1>" +
                    "<h1>Esa url no esta registrada.</h1>" +
                    "<h1>" + back + "</h1></body></html>")

            else:
                num = resource[1:]      # --Quitamos la barra
                if num in self.dicc_1:
                    httpCode = "HTTP/1.1 302 Found"
                    htmlBody = ("<html><body><meta http-equiv='refresh'" +
                                  "content='1 url=" + self.dicc_1[num] + "'>" +
                                  "</body></html>")
                else:
                    httpCode = "HTTP/1.1 404 Not Found"
                    htmlBody = ("<html><body><h1>Not found</h1>" +
                        "<h1>Recurso no disponible</h1>" +
                        "<h1>" + back + "</h1></body></html>")

        elif method == "POST":
            url = unquote(body[4:])

            if (url[0] == "+"):        # -- La url viene sin contenido

                httpCode = "HTTP/1.1 204 No Content"
                htmlBody = ("<html><body><h1>Error no ha mandado ninguna URL" +
                    ".</h1><h1>" + back + "</h1></body></html>")
            else:  # -- Hay contenido

                if (url[:4] != "http"):     # -- No trae el http por delante
                    url = "http://" + url

            # -- Comprobamos si está en el Dicc_2
            if url in self.dicc_2:   # -- Sí que está
                # -- Respondemos
                httpCode = "HTTP/1.1 200 OK"
                htmlBody = ("<html><body><h1>Esta url ya estaba contempla" +
                    "da en nuestra base de datos</h1><h1> Url acortada: " +
                    "<a href=" + url + ">http://localhost:1234/" +
                    self.dicc_2[url] + "</a></h1><h1>Url entera: " +
                    "<a href=" + url + ">" + url + "</a></h1><h1>" + back +
                    "</h1></body></html>")

            else:   # -- No está
                # -- Metemos la nueva url en los diccionarios
                status = len(self.dicc_1)
                self.dicc_1[str(status)] = url
                self.dicc_2[url] = str(status)

                # -- Respondemos
                httpCode = "HTTP/1.1 200 OK"
                htmlBody = ("<html><body><h1>URL AGREGADA " +
                    "A LA BASE DE DATOS </h1>" +
                    "<h1> Url acortada: <a href=" + url + ">" +
                    "http://localhost:1234/" + self.dicc_2[url] +
                    "</a></h1><h1>Url entera: <a href=" + url + ">" + url +
                    "</a></h1><h1>" + back + "</h1></body></html>")

        return(httpCode, htmlBody)


if __name__ == "__main__":
    testWebApp = contentApp("localhost", 1234)
