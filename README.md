# Book-Details

Please setup Django framework-2.2.2.

List of API's:
  1. GET http://localhost:8080/api/external-books?name=:nameOfABook<br/>
  The above API display matching book details else display empty data.
  
  2. Create: POST http://localhost:8080/api/v1/books <br />
  The above API will create a new book object, please pass the data as shown below.<br />
  {<br/>
    "number_of_pages": 694,<br/>
    "authors": [<br/>
        "Abdul Kalam"<br/>
    ],<br/>
    "isbn": "978-0553103540",<br/>
    "publisher": "Bantam Books",<br/>
    "release_date": "1996-08-01",<br/>
    "status": "success",<br/>
    "status_code": 201,<br/>
    "country": "India",<br/>
    "name": "The Wings of Fire"<br/>
}<br/>
  
  3. Read: GET http://localhost:8080/api/v1/books<br/>
     The above API used to display all the existing books details from the local DB.<br /><br/>
     API is searchable by name (string), country (string), publisher (string) and release date (year, integer).<br/>
      http://127.0.0.1:8000/api/v1/books/?name=bookName<br/>
      http://127.0.0.1:8000/api/v1/books/?country=countryName <br/>
      http://127.0.0.1:8000/api/v1/books/?publisher=publisherName <br/>
      http://127.0.0.1:8000/api/v1/books/?released=releasedDate <br/>
     
     
  4. Update: POST http://localhost:8080/api/v1/books/id<br/>
    The above API used to update an object. <br />please pass the data as shown below.<br />
  {<br/>
    "number_of_pages": 700,<br/>
    "authors": [<br/>
        "Abdul Kalam"<br/>
    ],<br/>
    "isbn": "978-0553103540",<br/>
    "publisher": "Bantam Books",<br/>
    "release_date": "1996-08-01",<br/>
    "status": "success",<br/>
    "status_code": 201,<br/>
    "country": "India",<br/>
    "name": "The Wings of Fire"<br/>
}<br/>
    
  
  5. Delete: POST http://localhost:8080/api/v1/books/id/delete<br/>
  The above API used to delete an object by passing book object ID.<br/>
  6. Show: GET http://localhost:8080/api/v1/books/id<br/>
  The above API is used to display details of the book. <br/>
  
  
  
