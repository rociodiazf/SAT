#!/usr/bin/python3


import webapp

formulario = """
  <form action="" method="POST">
	  Contenido: <input type="text" name="content" value=" ">
	  <input type="submit" value="Enviar">
  </form>
"""



class contentApp (webapp.webApp):


    # Declare and initialize content
    content = {'/': 'Root page',
               '/page': 'you asked /page'
               }

    def parse(self, request):
        method = request.split(' ',1)[0]
        resource = request.split(' ',2)[1]
        body = request.split('\r\n\r\n', 1)[-1]

        return (method, resource, body)

    def process(self, parsedRequest):

        method, resource, body = parsedRequest

        if method == "GET":

            if resource in self.content.keys():
                httpCode = "200 OK"
                htmlBody = "<html><body><h1>" + self.content[resource] +"</h1></body></html>"
            else:   #-- La pagina no esta en el diccionario
                httpCode = "404 Not Found"
                htmlBody = "Page Not Found"

        else:   #-- PUT o POST



            httpCode = "200 OK"
            htmlBody = "<html><body> Added " + body + ": "+ self.content[body] + "</body></html>"

        return(httpCode, htmlBody)


if __name__ == "__main__":
    testWebApp = contentApp("localhost", 1234)
