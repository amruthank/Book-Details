from django.shortcuts import render
from django.http import HttpResponse

from api.models import *

import requests
import json
import dateutil.parser



#Method:GET - Method to query by book name. 
def external_books(request):

    if request.method == "GET":
        pass
    else:
        return HttpResponse("Error: INVALID METHOD", content_type='text/json')

    contents = {}

    try:
        response = requests.get("https://www.anapioficeandfire.com/api/books?name=%s"%(request.GET.get('name')))
    except Exception as e:
        contents["status"] = "failure"
        contents["Error"] = "%s"%e
        return HttpResponse(json.dumps(contents, indent = 4), content_type='text/json')

    #Formating the response.
    if response.status_code == 200:
        contents["status_code"] = response.status_code
        contents["status"] = "success"
        contents["data"] = []
        
        for item in response.json():
            data = {}
            data["name"] = item["name"]
            data["isbn"] = item["isbn"]
            data["authors"] = list(item["authors"])
            data["number_of_pages"] = item["numberOfPages"]
            data["publisher"] = item["publisher"]
            data["country"] = item["country"]
            data["release_date"] = item["released"]

            contents["data"].append(data)
        
    return HttpResponse(json.dumps(contents, indent = 4), content_type='text/json')
#End of external_books API.



#Helper function to check for a key in the POST request.
def _isKeyPresent(contents, key):

    if (key not in contents) or (contents["%s"%key] == ""):
        return False
    else:
        return True
#End of _isKeyPresent function.



#Helper function return the response.
def _return_response(book):

    details = {}
    details["id"] = book.id
    details["name"] = book.name
    details["isbn"] = book.isbn
    details["number_of_pages"] = book.numberOfPages
    #TODO: Publisher
    details["publisher"] = book.publisher
    details["country"] = book.country
    #TODO: Dateformat
    details["release_date"] = "%s"%book.released

    authors = Author.objects.filter(book_id = book.id)
    details["authors"] = []
    for author in authors:
        author_name = author.first_name+" "+author.last_name
        details["authors"].append(author_name)

    return details
#End of _return_response function.

    

#Method:GET - Method to display all the records.
#Method:POST - Method to create an object.
def create_read_method(request):    

    if request.method == 'GET':

        #The Books API should be searchable by name (string), country (string), publisher (string) and release date (year, integer).
        if request.GET.get('name'):
            books = Book.objects.filter(name = request.GET.get('name'))
        elif request.GET.get('country'):
            books = Book.objects.filter(country = request.GET.get('country'))
        elif request.GET.get('publisher'):
            books = Book.objects.filter(publisher = request.GET.get('publisher'))
        elif request.GET.get('released'):
            books = Book.objects.filter(released = request.GET.get('released'))
        else:
            #Dispay all the list of books pesent in the local DB.
            books = Book.objects.all()


        contents = {}
        contents["data"] = []

        for book in books:
            details = _return_response(book)
            contents["data"].append(details)

        contents["status_code"] = 200
        contents["stauts"] = "success"
                
        return HttpResponse(json.dumps(contents, indent = 4), content_type='text/json')
    
    else: #Create a new book object.
        try:
            contents = json.loads(request.body.decode("utf-8"))
        except Exception:
            return HttpResponse("Error parsing the response.", content_type='text/json')


        #Check for the missing key - name.
        if _isKeyPresent(contents, "name") == False:
            return HttpResponse("Error: Missing Book name tag-> name!", content_type='application/json')
        #Check for the missing key - isbn.
        elif _isKeyPresent(contents, "isbn") == False:
            return HttpResponse("Error: Missing Book ISBN tag -> isbn!", content_type='application/json')
        elif Book.objects.filter(isbn = contents["isbn"], name = contents["name"]).count()>0:
                return HttpResponse("The book %s is already exist!"%contents["name"], content_type='application/json')
        else:
            book = Book()
            book.name = contents["name"].strip()
            book.isbn = contents["isbn"]

            if _isKeyPresent(contents, "number_of_pages") == False:
                return HttpResponse("Error: Missing number of book pages tag -> number_of_pages!", content_type='application/json')
            else:
                book.numberOfPages = contents["number_of_pages"]

            if _isKeyPresent(contents, "publisher") == False:
                return HttpResponse("Error: Missing publisher tag -> publisher!", content_type='application/json')
            else:
                book.publisher = contents["publisher"].strip()

            if _isKeyPresent(contents, "country") == False:
                return HttpResponse("Error: Missing country tag -> country!", content_type='application/json')
            else:
                book.country = contents["country"].strip()

            if _isKeyPresent(contents, "release_date") == False:
                return HttpResponse("Error: Missing book release date tag -> release_date!", content_type='application/json')
            else:
                book.released = dateutil.parser.parse(contents["release_date"]).date()
                
            book.save()


            if _isKeyPresent(contents, "authors") == False:
                return HttpResponse("Error: Missing authors tag -> authors!", content_type='application/json')
            else:
                for val in contents["authors"]:
                    author = Author()
                    author.book = book
                    first_name, last_name = val.split(" ", 1)
                    author.first_name = first_name
                    author.last_name = last_name
                    author.save()

            contents["release_date"] = "%s"%(dateutil.parser.parse(contents["release_date"]).date())
            contents["status_code"] = 201
            contents["status"] = "success"
       
            return HttpResponse(json.dumps(contents, indent = 4), content_type='application/json')
#End of create_read_method.





#Method:POST - Method to update an object.
def update(request, book_id):
    
    if request.method == "GET": #Create a new book.
       
        if Book.objects.filter(id = book_id).count() == 0:
            return HttpResponse("No book with the ID %s exist!"%book_id, content_type='application/json')
        else:
            book = Book.objects.get(id = book_id)
            contents = {}
            contents["data"] = []

            details = _return_response(book)
            contents["data"].append(details)

            contents["status_code"] = 200
            contents["stauts"] = "success"
                    
            return HttpResponse(json.dumps(contents, indent = 4), content_type='text/json')

    else:
        
        try:
            contents = json.loads(request.body.decode("utf-8"))
        except Exception:
            return HttpResponse("Error parsing the response.", content_type='text/json')

        if Book.objects.filter(id=book_id).count()==1:
            
            book = Book.objects.get(id=book_id)

            #Check for new updates.
            if book.name != contents["name"].strip():
                book.name = contents["name"].strip()
            if book.isbn != contents["isbn"]:
                book.isbn = contents["isbn"]
            if book.numberOfPages != contents["number_of_pages"]:
                book.numberOfPages = contents["number_of_pages"]
            if book.publisher != contents["publisher"]:
                book.publisher = contents["publisher"]
            if book.country != contents["country"]:
                book.country = contents["country"]
            if book.released != contents["release_date"]:
                book.released = contents["release_date"]
            book.save()

            for val in contents["authors"]: #Update author details.
                first_name, last_name = val.split(" ", 1)
                
                if Author.objects.filter(book = book, first_name = first_name, last_name = last_name).count() == 1:
                    continue
                else:
                    author = Author()
                    author.book = book
                    author.first_name = first_name
                    author.last_name = last_name
                    author.save()

            #Delete an author if not present in the new updates.
            authors = Author.objects.filter(book = book)
            for author in authors:
                if (author.first_name+" "+author.last_name) not in contents["authors"]:
                    author.delete()

            contents["status_code"] = 201
            contents["status"] = "success"
       
            return HttpResponse(json.dumps(contents, indent = 4), content_type='application/json')
        else:
            return HttpResponse("Error: INVALID ID!", content_type='application/json')
#End of update method.





#API to update an object.
def delete(request, book_id):
    
    if request.method == "GET": #Create a new book.
        return HttpResponse("INVALID METHOD", content_type='application/json')
    else:
        
        try:
            contents = json.loads(request.body.decode("utf-8"))
        except Exception:
            return HttpResponse("Error parsing the response.", content_type='text/json')
        else:
            if Book.objects.filter(id=book_id).count()==1:
                
                book = Book.objects.get(id=book_id)
                book_name = book.name
                book.delete()

                contents = {}
                contents["status_code"] = 201
                contents["status"] = "success"
                contents["message"] = "The book %s was deleted successfully"%book_name
                contents["data"] = []
           
                return HttpResponse(json.dumps(contents, indent = 4), content_type='application/json')
            else:
                return HttpResponse("No book with the ID %s exist!"%book_id, content_type='application/json')
#End of delete method.  


