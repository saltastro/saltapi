************
Introduction
************

The communication from the client-side to the server-side and vice versa is a common ground to establish the interaction with the data stored in the database.
This common ground may become complex as the data stored increases. The database is loaded with multiple tables that contain information used from one table to another.
The complexity needed to be overcame, hence, the rise of the REST API. REST API are the middle man between the client and the server.
They bring the flexibility and the easy use of communication between the client and server.
REST API use the notion of endpoint to perform tasks such as (insert, retrieve, edit, and delete) data in the database accordingly.

This document, serves the purpose of explaining the endpoints used to accomplish the tasks of inserting, retrieving, editing and deleting data in an efficient manner.

It is intended for the developers (primary SALT software developers) and future developers to understand the actions performed by different endpoints simple
by referring to this document.

**************************************
Conceptual Solution & Logical Solution
**************************************
This follows a use case approach to explain the endpoints used by the salt-api.

* **Get proposals (get_proposals)**

  Returns the list of proposals containing json data about a single proposal.

* **URL**
  /proposals


* **Method**
  GET

* **URL Params**

  1. **Required**: If Required else None

  2. **Optional**: If Optional else None

* **Data Params**
  None

* **Success Response**

  1. **Code**: 200

  2. **Content**: [{proposal1}, {proposal2}, ...]

* **Error Response**

  1. **Code**: 404 NOT FOUND

  2. **Content**: {error: 'proposals doesn't exist'}

  OR

  1. **Code**: 401 UNAUTHORIZED

  2. **Content**: {error: 'You do not have permission to make this request'}

* **Sample Call**
  $.ajax(
    | url: '/proposals',
    | dataType: 'json/Object',
    | type: 'GET',
    | success: function(response){
     |  console.log(response)
    | }
  | )

* **Note**
  Any note to be made for this endpoint
