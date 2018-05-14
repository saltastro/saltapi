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

Get proposals
#############
Returns the list of the links of proposals.

* **URL**

  /proposals

* **Method**

  GET

* **URL Params**

  1. **Required**: None

* **Data Params**

  None

* **Success Response**

  1. **Code**: 200

  2. **Content**: [proposal1_link, proposal2_link, ...]

* **Error Response**

  1. **Code**: 404 NOT FOUND

  2. **Content**: {error: 'proposals links doesn't exist'}

  OR

  1. **Code**: 403 UNAUTHORIZED

  2. **Content**: {error: 'You do not have permission to make this request'}

  OR

  1. **Code**: 401 UNAUTHENTICATED

  2. **Content**: {error: 'Incorrect credentials, please try again'}

* **HTTP GET Request/Response Example**

  GET /proposals HTTP/1.1

  User-Agent: Mozilla/5.0 (compatible; MSIE5.01; Windows NT)

  Host: www.salt-api.ac.za

  Accept-Language: en-us

  Accept-Encoding: gzip

  Connection: Keep-Alive

  _ _ _ _ _ _ _ _ _ _ _ _

  HTTP/1.x 200 OK

  Date: Sat, 28 Nov 2009 04:36:25 GMT

  Server: salt-api sever

  Connection: close

  Expires: Sat, 28 Nov 2009 05:36:25 GMT

  Content-Type: zip

  Last-Modified: Sat, 28 Nov 2009 03:50:37 GMT

  Content-Encoding: gzip

* **Note**

  To view the proposal, must click on the proposal's link.

Get proposal
############
Returns a proposal as a zip file containing the proposal's details.

* **URL**

  /proposals/[proposal_code]

* **Method**

  GET

* **URL Params**

  1. **Required**: proposal_code=[String]

* **Data Params**

  None

* **Success Response**

  1. **Code**: 200

  2. **Content**: zipped_proposal

* **Error Response**

  1. **Code**: 404 NOT FOUND

  2. **Content**: {error: 'proposal_code requested doesn't exist'}

  OR

  1. **Code**: 403 UNAUTHORIZED

  2. **Content**: {error: 'You do not have permission to make this request'}

  OR

  1. **Code**: 401 UNAUTHENTICATED

  2. **Content**: {error: 'Incorrect credentials, please try again'}

* **HTTP GET Request/Response Example**

  GET /proposals/[proposal_code] HTTP/1.1

  User-Agent: Mozilla/5.0 (compatible; MSIE5.01; Windows NT)

  Host: www.salt-api.ac.za

  Accept-Language: en-us

  Accept-Encoding: gzip

  Connection: Keep-Alive

  _ _ _ _ _ _ _ _ _ _ _ _

  HTTP/1.x 200 OK

  Date: Sat, 28 Nov 2009 04:36:25 GMT

  Server: salt-api sever

  Connection: close

  Expires: Sat, 28 Nov 2009 05:36:25 GMT

  Content-Type: zip

  Last-Modified: Sat, 28 Nov 2009 03:50:37 GMT

  Content-Encoding: gzip

* **Note**

  Currently only support the zip file

Update proposal
###############
Modifies the content of the existing proposal.

* **URL**

  /proposals/[proposal_code]

* **Method**

  PUT

* **URL Params**

  1. **Required**: proposal_code=[String]

* **Data Params**
  Zip file

* **Success Response**

  1. **Code**: 200

  2. **Content**: zipped_proposal

* **Error Response**

  1. **Code**: 404 NOT FOUND

  2. **Content**: {error: 'proposal_code requested doesn't exist'}

  OR

  1. **Code**: 403 UNAUTHORIZED

  2. **Content**: {error: 'You do not have permission to make this request'}

  OR

  1. **Code**: 401 UNAUTHENTICATED

  2. **Content**: {error: 'Incorrect credentials, please try again'}

* **HTTP PUT Request/Response Example**

  PUT /proposals/[proposal_code] HTTP/1.1

  User-Agent: Mozilla/5.0 (compatible; MSIE5.01; Windows NT)

  Host: www.salt-api.ac.za

  Content-type: zip file

  Content-length: 16

  Accept-Language: en-us

  Accept-Encoding: gzip

  Connection: Keep-Alive

  _ _ _ _ _ _ _ _ _ _ _ _ _

  HTTP/1.1 200 OK

  Content-Location: /proposal/proposal_code

* **Note**

  Currently only support the zip file

Add proposal
############
Inserts the new proposal.

* **URL**

  /proposals/[proposal_code]

* **Method**

  POST

* **URL Params**

  1. **Required**: proposal_code=[String]

* **Data Params**

  Zip file

* **Success Response**

  1. **Code**: 200

  2. **Content**: zipped_proposal

* **Error Response**

  1. **Code**: 404 NOT FOUND

  2. **Content**: {error: 'proposal_code requested doesn't exist'}

  OR

  1. **Code**: 403 UNAUTHORIZED

  2. **Content**: {error: 'You do not have permission to make this request'}

  OR

  1. **Code**: 401 UNAUTHENTICATED

  2. **Content**: {error: 'Incorrect credentials, please try again'}

* **HTTP POST Request/Response Example**

  POST /proposals/[proposal_code] HTTP/1.1

  User-Agent: Mozilla/5.0 (compatible; MSIE5.01; Windows NT)

  Host: www.salt-api.ac.za

  Content-type: zip file

  Content-length: 16

  Accept-Language: en-us

  Accept-Encoding: gzip

  Connection: Keep-Alive

  _ _ _ _ _ _ _ _ _ _ _ _ _

  HTTP/1.1 200 OK

  Content-Location: /proposal/proposal_code

* **Note**

  Currently, only support the zip file

Download Proposal Summaries
###########################
Downloads the summaries of the proposal

* **URL**

  /proposal-summaries/RSA/2018-1/

* **Method**

  GET

* **URL Params**

  1. **Required**: partner=[String], semester=[String]

* **Data Params**
  None

* **Success Response**

  1. **Code**: 200

  2. **Content**: zipped_proposal_summer

* **Error Response**

  1. **Code**: 404 NOT FOUND

  2. **Content**: {error: 'proposal_code requested doesn't exist'}

  OR

  1. **Code**: 403 UNAUTHORIZED

  2. **Content**: {error: 'You do not have permission to make this request'}

  OR

  1. **Code**: 401 UNAUTHENTICATED

  2. **Content**: {error: 'Incorrect credentials, please try again'}

* **HTTP GET Request/Response Example**

  GET /proposal-summaries/[RSA]/[2018-1]/ HTTP/1.1

  User-Agent: Mozilla/5.0 (compatible; MSIE5.01; Windows NT)

  Host: www.salt-api.ac.za

  Accept-Language: en-us

  Accept-Encoding: gzip

  Connection: Keep-Alive

  _ _ _ _ _ _ _ _ _ _ _ _

  HTTP/1.x 200 OK

  Date: Sat, 28 Nov 2009 04:36:25 GMT

  Server: salt-api sever

  Connection: close

  Expires: Sat, 28 Nov 2009 05:36:25 GMT

  Content-Type: zip

  Last-Modified: Sat, 28 Nov 2009 03:50:37 GMT

  Content-Encoding: gzip

* **Note**

  Currently only support the zip file

Download Proposal Summary
#########################
Downloads the summary of the proposal

* **URL**

  /proposal-summaries/[RSA]/[2018-1]/[2018-1-SCI-009]

* **Method**

  GET

* **URL Params**

  1. **Required**: partner=[String], semester=[String], proposal_code=[String]

* **Data Params**

  None

* **Success Response**

  1. **Code**: 200

  2. **Content**: zipped_proposal_summary

* **Error Response**

  1. **Code**: 404 NOT FOUND

  2. **Content**: {error: 'proposal_code requested doesn't exist'}

  OR

  1. **Code**: 403 UNAUTHORIZED

  2. **Content**: {error: 'You do not have permission to make this request'}

  OR

  1. **Code**: 401 UNAUTHENTICATED

  2. **Content**: {error: 'Incorrect credentials, please try again'}

* **HTTP GET Request/Response Example**

  GET /proposal-summaries/[RSA]/[2018-1]/[2018-1-SCI-009] HTTP/1.1

  User-Agent: Mozilla/5.0 (compatible; MSIE5.01; Windows NT)

  Host: www.salt-api.ac.za

  Accept-Language: en-us

  Accept-Encoding: gzip

  Connection: Keep-Alive

  _ _ _ _ _ _ _ _ _ _ _ _

  HTTP/1.x 200 OK

  Date: Sat, 28 Nov 2009 04:36:25 GMT

  Server: salt-api sever

  Connection: close

  Expires: Sat, 28 Nov 2009 05:36:25 GMT

  Content-Type: zip

  Last-Modified: Sat, 28 Nov 2009 03:50:37 GMT

  Content-Encoding: gzip

* **Note**

  Currently only support the zip file


