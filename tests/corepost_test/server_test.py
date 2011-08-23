'''
Created on 2011-08-23

@author: jacekf
'''

from corepost.server import CorePost, Http

app = CorePost()

@app.route("/",Http.GET)
def test():
    return "test"

@app.route("/",(Http.POST,Http.PUT))
def test_post():
    return "test POST/PUT"

if __name__ == '__main__':
    app.run()