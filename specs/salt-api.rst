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

*************
Get proposals
*************
+---------------------------+----------------------------------------------------------------------------+
| API Item                  | Description                                                                |
+===========================+============================================================================+
| **Title**                 | **Get proposals**                                                          |
|                           |                                                                            |
|                           | Returns the list of the links of proposals.                                |
+---------------------------+----------------------------------------------------------------------------+
| **URL**                   | **/proposals**                                                             |
+---------------------------+----------------------------------------------------------------------------+
| **Method**                | **GET**                                                                    |
+---------------------------+----------------------------------------------------------------------------+
| **URL Params**            | 1. **Required**: None                                                      |
|                           |                                                                            |
|                           | 2. **Optional**: None                                                      |
+---------------------------+----------------------------------------------------------------------------+
| **Data Params**           | None                                                                       |
+---------------------------+----------------------------------------------------------------------------+
| **Success Response**      | 1. **Code**: 200                                                           |
|                           |                                                                            |
|                           | 2. **Content**: [proposal1_link, proposal2_link, ...]                      |
+---------------------------+----------------------------------------------------------------------------+
| **Error Response**        | 1. **Code**: 404 NOT FOUND                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'proposals doesn't exist'}                         |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 403 UNAUTHORIZED                                              |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'You do not have permission to make this request'} |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 401 UNAUTHENTICATED                                           |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'Incorrect credentials, please try again'}         |
+---------------------------+----------------------------------------------------------------------------+
| **HTTP Request/Response** | GET /proposals HTTP/1.1                                                    |
|                           |                                                                            |
|                           | User-Agent: Mozilla/5.0 (compatible; MSIE5.01; Windows NT)                 |
|                           |                                                                            |
|                           | Host: www.salt-api.ac.za                                                   |
|                           |                                                                            |
|                           | Accept-Language: en-us                                                     |
|                           |                                                                            |
|                           | Accept-Encoding: gzip                                                      |
|                           |                                                                            |
|                           | Connection: Keep-Alive                                                     |
|                           |                                                                            |
|                           | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _                |
|                           |                                                                            |
|                           | HTTP/1.x 200 OK                                                            |
|                           |                                                                            |
|                           | Date: Sat, 28 Nov 2009 04:36:25 GMT                                        |
|                           |                                                                            |
|                           | Server: salt-api sever                                                     |
|                           |                                                                            |
|                           | Connection: close                                                          |
|                           |                                                                            |
|                           | Expires: Sat, 28 Nov 2009 05:36:25 GMT                                     |
|                           |                                                                            |
|                           | Content-Type: zip                                                          |
|                           |                                                                            |
|                           | Last-Modified: Sat, 28 Nov 2009 03:50:37 GMT                               |
|                           |                                                                            |
|                           | Content-Encoding: gzip                                                     |
+---------------------------+----------------------------------------------------------------------------+
| **Notes**                 | To view the proposal, must click on the proposal's link.                   |
+---------------------------+----------------------------------------------------------------------------+

************
Get proposal
************
+---------------------------+----------------------------------------------------------------------------+
| API Item                  | Description                                                                |
+===========================+============================================================================+
| **Title**                 | **Get proposal**                                                           |
|                           |                                                                            |
|                           | Returns a proposal as a zip file containing the proposal's details.        |
+---------------------------+----------------------------------------------------------------------------+
| **URL**                   | **/proposals/[proposal_code]**                                             |
+---------------------------+----------------------------------------------------------------------------+
| **Method**                | **GET**                                                                    |
+---------------------------+----------------------------------------------------------------------------+
| **URL Params**            | 1. **Required**: proposal_code=[String]                                    |
|                           |                                                                            |
|                           | 2. **Optional**: None                                                      |
+---------------------------+----------------------------------------------------------------------------+
| **Data Params**           | None                                                                       |
+---------------------------+----------------------------------------------------------------------------+
| **Success Response**      | 1. **Code**: 200                                                           |
|                           |                                                                            |
|                           | 2. **Content**: zipped_proposal                                            |
+---------------------------+----------------------------------------------------------------------------+
| **Error Response**        | 1. **Code**: 404 NOT FOUND                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'proposal with [proposal_code] doesn't exist'}     |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 403 UNAUTHORIZED                                              |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'You do not have permission to make this request'} |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 401 UNAUTHENTICATED                                           |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'Incorrect credentials, please try again'}         |
+---------------------------+----------------------------------------------------------------------------+
| **HTTP Request/Response** | GET /proposals/[proposal_code] HTTP/1.1                                    |
|                           |                                                                            |
|                           | User-Agent: Mozilla/5.0 (compatible; MSIE5.01; Windows NT)                 |
|                           |                                                                            |
|                           | Host: www.salt-api.ac.za                                                   |
|                           |                                                                            |
|                           | Accept-Language: en-us                                                     |
|                           |                                                                            |
|                           | Accept-Encoding: gzip                                                      |
|                           |                                                                            |
|                           | Connection: Keep-Alive                                                     |
|                           |                                                                            |
|                           | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _                |
|                           |                                                                            |
|                           | HTTP/1.x 200 OK                                                            |
|                           |                                                                            |
|                           | Date: Sat, 28 Nov 2009 04:36:25 GMT                                        |
|                           |                                                                            |
|                           | Server: salt-api sever                                                     |
|                           |                                                                            |
|                           | Connection: close                                                          |
|                           |                                                                            |
|                           | Expires: Sat, 28 Nov 2009 05:36:25 GMT                                     |
|                           |                                                                            |
|                           | Content-Type: zip                                                          |
|                           |                                                                            |
|                           | Last-Modified: Sat, 28 Nov 2009 03:50:37 GMT                               |
|                           |                                                                            |
|                           | Content-Encoding: gzip                                                     |
+---------------------------+----------------------------------------------------------------------------+
| **Notes**                 | Currently only support the zip file                                        |
+---------------------------+----------------------------------------------------------------------------+

***************
Update proposal
***************
+---------------------------+----------------------------------------------------------------------------+
| API Item                  | Description                                                                |
+===========================+============================================================================+
| **Title**                 | **Update proposal**                                                        |
|                           |                                                                            |
|                           | Modifies the content of the existing proposal.                             |
+---------------------------+----------------------------------------------------------------------------+
| **URL**                   | **/proposals/[proposal_code]**                                             |
+---------------------------+----------------------------------------------------------------------------+
| **Method**                | **PUT**                                                                    |
+---------------------------+----------------------------------------------------------------------------+
| **URL Params**            | 1. **Required**: proposal_code=[String]                                    |
|                           |                                                                            |
|                           | 2. **Optional**: None                                                      |
+---------------------------+----------------------------------------------------------------------------+
| **Data Params**           | Zip file                                                                   |
+---------------------------+----------------------------------------------------------------------------+
| **Success Response**      | 1. **Code**: 200                                                           |
|                           |                                                                            |
|                           | 2. **Content**: zipped_proposal                                            |
+---------------------------+----------------------------------------------------------------------------+
| **Error Response**        | 1. **Code**: 404 NOT FOUND                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'proposal with [proposal_code] doesn't exist'}     |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 403 UNAUTHORIZED                                              |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'You do not have permission to make this request'} |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 401 UNAUTHENTICATED                                           |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'Incorrect credentials, please try again'}         |
+---------------------------+----------------------------------------------------------------------------+
| **HTTP Request/Response** | PUT /proposals/[proposal_code] HTTP/1.1                                    |
|                           |                                                                            |
|                           | User-Agent: Mozilla/5.0 (compatible; MSIE5.01; Windows NT)                 |
|                           |                                                                            |
|                           | Host: www.salt-api.ac.za                                                   |
|                           |                                                                            |
|                           | Content-type: zip file                                                     |
|                           |                                                                            |
|                           | Content-length: 16                                                         |
|                           |                                                                            |
|                           | Accept-Language: en-us                                                     |
|                           |                                                                            |
|                           | Accept-Encoding: gzip                                                      |
|                           |                                                                            |
|                           | Connection: Keep-Alive                                                     |
|                           |                                                                            |
|                           | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _                |
|                           |                                                                            |
|                           | HTTP/1.x 200 OK                                                            |
|                           |                                                                            |
|                           | Content-Location: /proposal/proposal_code                                  |
+---------------------------+----------------------------------------------------------------------------+
| **Notes**                 | Currently only support the zip file                                        |
+---------------------------+----------------------------------------------------------------------------+

************
Add proposal
************
+---------------------------+----------------------------------------------------------------------------+
| API Item                  | Description                                                                |
+===========================+============================================================================+
| **Title**                 | **Add proposal**                                                           |
|                           |                                                                            |
|                           | Inserts the new proposal.                                                  |
+---------------------------+----------------------------------------------------------------------------+
| **URL**                   | **/proposals/[proposal_code]**                                             |
+---------------------------+----------------------------------------------------------------------------+
| **Method**                | **POST**                                                                   |
+---------------------------+----------------------------------------------------------------------------+
| **URL Params**            | 1. **Required**: proposal_code=[String]                                    |
|                           |                                                                            |
|                           | 2. **Optional**: None                                                      |
+---------------------------+----------------------------------------------------------------------------+
| **Data Params**           | Zip file                                                                   |
+---------------------------+----------------------------------------------------------------------------+
| **Success Response**      | 1. **Code**: 200                                                           |
|                           |                                                                            |
|                           | 2. **Content**: zipped_proposal                                            |
+---------------------------+----------------------------------------------------------------------------+
| **Error Response**        | 1. **Code**: 404 NOT FOUND                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'Proposals table doesn't exist'}     |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 403 UNAUTHORIZED                                              |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'You do not have permission to make this request'} |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 401 UNAUTHENTICATED                                           |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'Incorrect credentials, please try again'}         |
+---------------------------+----------------------------------------------------------------------------+
| **HTTP Request/Response** | POST /proposals/[proposal_code] HTTP/1.1                                   |
|                           |                                                                            |
|                           | User-Agent: Mozilla/5.0 (compatible; MSIE5.01; Windows NT)                 |
|                           |                                                                            |
|                           | Host: www.salt-api.ac.za                                                   |
|                           |                                                                            |
|                           | Content-type: zip file                                                     |
|                           |                                                                            |
|                           | Content-length: 16                                                         |
|                           |                                                                            |
|                           | Accept-Language: en-us                                                     |
|                           |                                                                            |
|                           | Accept-Encoding: gzip                                                      |
|                           |                                                                            |
|                           | Connection: Keep-Alive                                                     |
|                           |                                                                            |
|                           | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _                |
|                           |                                                                            |
|                           | HTTP/1.x 200 OK                                                            |
|                           |                                                                            |
|                           | Content-Location: /proposal/proposal_code                                  |
+---------------------------+----------------------------------------------------------------------------+
| **Notes**                 | Currently only support the zip file                                        |
+---------------------------+----------------------------------------------------------------------------+

***************************
Download Proposal Summaries
***************************
+---------------------------+----------------------------------------------------------------------------+
| API Item                  | Description                                                                |
+===========================+============================================================================+
| **Title**                 | **Download Proposal Summaries**                                            |
|                           |                                                                            |
|                           | Downloads the summaries of the proposal as the zip file                    |
+---------------------------+----------------------------------------------------------------------------+
| **URL**                   | **/proposal-summaries/RSA/2018-1/**                                        |
+---------------------------+----------------------------------------------------------------------------+
| **Method**                | **GET**                                                                    |
+---------------------------+----------------------------------------------------------------------------+
| **URL Params**            | 1. **Required**: partner=[String], semester=[String]                       |
|                           |                                                                            |
|                           | 2. **Optional**: None                                                      |
+---------------------------+----------------------------------------------------------------------------+
| **Data Params**           | None                                                                       |
+---------------------------+----------------------------------------------------------------------------+
| **Success Response**      | 1. **Code**: 200                                                           |
|                           |                                                                            |
|                           | 2. **Content**: zipped_proposal                                            |
+---------------------------+----------------------------------------------------------------------------+
| **Error Response**        | 1. **Code**: 404 NOT FOUND                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'proposals summaries doesn't exist'}               |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 403 UNAUTHORIZED                                              |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'You do not have permission to make this request'} |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 401 UNAUTHENTICATED                                           |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'Incorrect credentials, please try again'}         |
+---------------------------+----------------------------------------------------------------------------+
| **HTTP Request/Response** | GET /proposal-summaries/[RSA]/[2018-1]/ HTTP/1.1                           |
|                           |                                                                            |
|                           | User-Agent: Mozilla/5.0 (compatible; MSIE5.01; Windows NT)                 |
|                           |                                                                            |
|                           | Host: www.salt-api.ac.za                                                   |
|                           |                                                                            |
|                           | Accept-Language: en-us                                                     |
|                           |                                                                            |
|                           | Accept-Encoding: gzip                                                      |
|                           |                                                                            |
|                           | Connection: Keep-Alive                                                     |
|                           |                                                                            |
|                           | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _                |
|                           |                                                                            |
|                           | HTTP/1.x 200 OK                                                            |
|                           |                                                                            |
|                           | Date: Sat, 28 Nov 2009 04:36:25 GMT                                        |
|                           |                                                                            |
|                           | Server: salt-api sever                                                     |
|                           |                                                                            |
|                           | Connection: close                                                          |
|                           |                                                                            |
|                           | Expires: Sat, 28 Nov 2009 05:36:25 GMT                                     |
|                           |                                                                            |
|                           | Content-Type: zip                                                          |
|                           |                                                                            |
|                           | Last-Modified: Sat, 28 Nov 2009 03:50:37 GMT                               |
|                           |                                                                            |
|                           | Content-Encoding: gzip                                                     |
+---------------------------+----------------------------------------------------------------------------+
| **Notes**                 | Currently only support the zip file                                        |
+---------------------------+----------------------------------------------------------------------------+

*************************
Download Proposal Summary
*************************
+---------------------------+------------------------------------------------------------------------------+
| API Item                  | Description                                                                  |
+===========================+==============================================================================+
| **Title**                 | **Download Proposal Summary**                                                |
|                           |                                                                              |
|                           | Downloads the summary of the proposal as the zip file                        |
+---------------------------+------------------------------------------------------------------------------+
| **URL**                   | **/proposal-summaries/[RSA]/[2018-1]/[2018-1-SCI-009]**                      |
+---------------------------+------------------------------------------------------------------------------+
| **Method**                | **GET**                                                                      |
+---------------------------+------------------------------------------------------------------------------+
| **URL Params**            | 1. **Required**: partner=[String], semester=[String], proposal_code=[String] |
|                           |                                                                              |
|                           | 2. **Optional**: None                                                        |
+---------------------------+------------------------------------------------------------------------------+
| **Data Params**           | None                                                                         |
+---------------------------+------------------------------------------------------------------------------+
| **Success Response**      | 1. **Code**: 200                                                             |
|                           |                                                                              |
|                           | 2. **Content**: zipped_proposal                                              |
+---------------------------+------------------------------------------------------------------------------+
| **Error Response**        | 1. **Code**: 404 NOT FOUND                                                   |
|                           |                                                                              |
|                           | 2. **Content**: {error: 'proposal with [proposal_code] doesn't exist'}       |
|                           |                                                                              |
|                           | OR                                                                           |
|                           |                                                                              |
|                           | 1. **Code**: 403 UNAUTHORIZED                                                |
|                           |                                                                              |
|                           | 2. **Content**: {error: 'You do not have permission to make this request'}   |
|                           |                                                                              |
|                           | OR                                                                           |
|                           |                                                                              |
|                           | 1. **Code**: 401 UNAUTHENTICATED                                             |
|                           |                                                                              |
|                           | 2. **Content**: {error: 'Incorrect credentials, please try again'}           |
+---------------------------+------------------------------------------------------------------------------+
| **HTTP Request/Response** | GET /proposal-summaries/[RSA]/[2018-1]/[2018-1-SCI-009] HTTP/1.1             |
|                           |                                                                              |
|                           | User-Agent: Mozilla/5.0 (compatible; MSIE5.01; Windows NT)                   |
|                           |                                                                              |
|                           | Host: www.salt-api.ac.za                                                     |
|                           |                                                                              |
|                           | Accept-Language: en-us                                                       |
|                           |                                                                              |
|                           | Accept-Encoding: gzip                                                        |
|                           |                                                                              |
|                           | Connection: Keep-Alive                                                       |
|                           |                                                                              |
|                           | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _                  |
|                           |                                                                              |
|                           | HTTP/1.x 200 OK                                                              |
|                           |                                                                              |
|                           | Date: Sat, 28 Nov 2009 04:36:25 GMT                                          |
|                           |                                                                              |
|                           | Server: salt-api sever                                                       |
|                           |                                                                              |
|                           | Connection: close                                                            |
|                           |                                                                              |
|                           | Expires: Sat, 28 Nov 2009 05:36:25 GMT                                       |
|                           |                                                                              |
|                           | Content-Type: zip                                                            |
|                           |                                                                              |
|                           | Last-Modified: Sat, 28 Nov 2009 03:50:37 GMT                                 |
|                           |                                                                              |
|                           | Content-Encoding: gzip                                                       |
+---------------------------+------------------------------------------------------------------------------+
| **Notes**                 | Currently only support the zip file                                          |
+---------------------------+------------------------------------------------------------------------------+

*************
Get SALT User
*************
+---------------------------+------------------------------------------------------------------------------+
| API Item                  | Description                                                                  |
+===========================+==============================================================================+
| **Title**                 | **Get SALT User**                                                            |
|                           |                                                                              |
|                           | Returns the SALT user in a json format                                       |
+---------------------------+------------------------------------------------------------------------------+
| **URL**                   | **/users/[username]**                                                        |
+---------------------------+------------------------------------------------------------------------------+
| **Method**                | **GET**                                                                      |
+---------------------------+------------------------------------------------------------------------------+
| **URL Params**            | 1. **Required**: username=[String], password=[String]                        |
|                           |                                                                              |
|                           | 2. **Optional**: None                                                        |
+---------------------------+------------------------------------------------------------------------------+
| **Data Params**           | None                                                                         |
+---------------------------+------------------------------------------------------------------------------+
| **Success Response**      | 1. **Code**: 200                                                             |
|                           |                                                                              |
|                           | 2. **Content**: { user: {name: "nme", email: "email", username: "username} } |
+---------------------------+------------------------------------------------------------------------------+
| **Error Response**        | 1. **Code**: 404 NOT FOUND                                                   |
|                           |                                                                              |
|                           | 2. **Content**: {error: 'user with the [username] doesn't exist'}            |
|                           |                                                                              |
|                           | OR                                                                           |
|                           |                                                                              |
|                           | 1. **Code**: 403 UNAUTHORIZED                                                |
|                           |                                                                              |
|                           | 2. **Content**: {error: 'You do not have permission to make this request'}   |
|                           |                                                                              |
|                           | OR                                                                           |
|                           |                                                                              |
|                           | 1. **Code**: 401 UNAUTHENTICATED                                             |
|                           |                                                                              |
|                           | 2. **Content**: {error: 'Incorrect credentials, please try again'}           |
+---------------------------+------------------------------------------------------------------------------+
| **HTTP Request/Response** | GET /users/[username] HTTP/1.1                                               |
|                           |                                                                              |
|                           | User-Agent: Mozilla/5.0 (compatible; MSIE5.01; Windows NT)                   |
|                           |                                                                              |
|                           | Host: www.salt-api.ac.za                                                     |
|                           |                                                                              |
|                           | Accept-Language: en-us                                                       |
|                           |                                                                              |
|                           | Accept-Encoding: gzip                                                        |
|                           |                                                                              |
|                           | Connection: Keep-Alive                                                       |
|                           |                                                                              |
|                           | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _                  |
|                           |                                                                              |
|                           | HTTP/1.x 200 OK                                                              |
|                           |                                                                              |
|                           | Date: Sat, 28 Nov 2009 04:36:25 GMT                                          |
|                           |                                                                              |
|                           | Server: salt-api sever                                                       |
|                           |                                                                              |
|                           | Connection: close                                                            |
|                           |                                                                              |
|                           | Expires: Sat, 28 Nov 2009 05:36:25 GMT                                       |
|                           |                                                                              |
|                           | Content-Type: zip                                                            |
|                           |                                                                              |
|                           | Last-Modified: Sat, 28 Nov 2009 03:50:37 GMT                                 |
|                           |                                                                              |
|                           | Content-Encoding: gzip                                                       |
+---------------------------+------------------------------------------------------------------------------+
| **Notes**                 | None                                                                         |
+---------------------------+------------------------------------------------------------------------------+

****************
Update SALT User
****************
+---------------------------+----------------------------------------------------------------------------+
| API Item                  | Description                                                                |
+===========================+============================================================================+
| **Title**                 | **Update SALT User**                                                       |
|                           |                                                                            |
|                           | Modifies the content of the existing SALT user.                            |
+---------------------------+----------------------------------------------------------------------------+
| **URL**                   | **/users/[username]**                                                      |
+---------------------------+----------------------------------------------------------------------------+
| **Method**                | **PUT**                                                                    |
+---------------------------+----------------------------------------------------------------------------+
| **URL Params**            | 1. **Required**: username=[String], password=[String]                      |
|                           |                                                                            |
|                           | 2. **Optional**: None                                                      |
+---------------------------+----------------------------------------------------------------------------+
| **Data Params**           | Zip file                                                                   |
+---------------------------+----------------------------------------------------------------------------+
| **Success Response**      | 1. **Code**: 200                                                           |
|                           |                                                                            |
|                           | 2. **Content**: {user: {name: "nme", email: "email", username: "username}} |
+---------------------------+----------------------------------------------------------------------------+
| **Error Response**        | 1. **Code**: 404 NOT FOUND                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'user with [username] doesn't exist'}              |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 403 UNAUTHORIZED                                              |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'You do not have permission to make this request'} |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 401 UNAUTHENTICATED                                           |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'Incorrect credentials, please try again'}         |
+---------------------------+----------------------------------------------------------------------------+
| **HTTP Request/Response** | PUT /users/[username] HTTP/1.1                                             |
|                           |                                                                            |
|                           | User-Agent: Mozilla/5.0 (compatible; MSIE5.01; Windows NT)                 |
|                           |                                                                            |
|                           | Host: www.salt-api.ac.za                                                   |
|                           |                                                                            |
|                           | Content-type: json object                                                  |
|                           |                                                                            |
|                           | Content-length: 5                                                          |
|                           |                                                                            |
|                           | Accept-Language: en-us                                                     |
|                           |                                                                            |
|                           | Accept-Encoding: gzip                                                      |
|                           |                                                                            |
|                           | Connection: Keep-Alive                                                     |
|                           |                                                                            |
|                           | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _                |
|                           |                                                                            |
|                           | HTTP/1.x 200 OK                                                            |
|                           |                                                                            |
|                           | Content-Location: /users/[username]                                        |
+---------------------------+----------------------------------------------------------------------------+
| **Notes**                 | None                                                                       |
+---------------------------+----------------------------------------------------------------------------+

*************
Add SALT User
*************
+---------------------------+----------------------------------------------------------------------------+
| API Item                  | Description                                                                |
+===========================+============================================================================+
| **Title**                 | **Add SALT User**                                                          |
|                           |                                                                            |
|                           | Inserts the new record of the SALT user.                                   |
+---------------------------+----------------------------------------------------------------------------+
| **URL**                   | **/users/[username]**                                                      |
+---------------------------+----------------------------------------------------------------------------+
| **Method**                | **POST**                                                                   |
+---------------------------+----------------------------------------------------------------------------+
| **URL Params**            | 1. **Required**: name=[String], surname=[String], username=[String]        |
|                           |                                                                            |
|                           |                : password=[String]                                         |
|                           |                                                                            |
|                           | 2. **Optional**: None                                                      |
+---------------------------+----------------------------------------------------------------------------+
| **Data Params**           | {user: {username: "username", password: "password"}}                       |
+---------------------------+----------------------------------------------------------------------------+
| **Success Response**      | 1. **Code**: 200                                                           |
|                           |                                                                            |
|                           | 2. **Content**: {user: {name: "nme", email: "email", username: "username}} |
+---------------------------+----------------------------------------------------------------------------+
| **Error Response**        | 1. **Code**: 404 NOT FOUND                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'user table doesn't exist'}                        |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 403 UNAUTHORIZED                                              |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'You do not have permission to make this request'} |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 401 UNAUTHENTICATED                                           |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'Incorrect credentials, please try again'}         |
+---------------------------+----------------------------------------------------------------------------+
| **HTTP Request/Response** | POST /users/[username] HTTP/1.1                                            |
|                           |                                                                            |
|                           | User-Agent: Mozilla/5.0 (compatible; MSIE5.01; Windows NT)                 |
|                           |                                                                            |
|                           | Host: www.salt-api.ac.za                                                   |
|                           |                                                                            |
|                           | Content-type: json object                                                  |
|                           |                                                                            |
|                           | Content-length: 5                                                          |
|                           |                                                                            |
|                           | Accept-Language: en-us                                                     |
|                           |                                                                            |
|                           | Accept-Encoding: gzip                                                      |
|                           |                                                                            |
|                           | Connection: Keep-Alive                                                     |
|                           |                                                                            |
|                           | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _                |
|                           |                                                                            |
|                           | HTTP/1.x 200 OK                                                            |
|                           |                                                                            |
|                           | Content-Location: /users/[username]                                        |
+---------------------------+----------------------------------------------------------------------------+
| **Notes**                 | None                                                                       |
+---------------------------+----------------------------------------------------------------------------+