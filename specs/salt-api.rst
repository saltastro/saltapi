************
Introduction
************

The communication from the client-side to the server-side and vice versa is a common ground in establishing the interaction with the data stored in the database.
This common ground may become complex as the data stored increases. The database is loaded with multiple tables that contain information used from one table to another.
The forever growing complexity needed to be overcame, hence, the rise of the REST API. REST API are the middle man between the client and the server.
They bring the flexibility and the ease the communication between the client and server.
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
|                           | Returns the list of the URI of proposals in a json format.                 |
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
| **Success Response**      | 1. **Code**: 200 OK                                                        |
|                           |                                                                            |
|                           | 2. **Content**: {proposal1_uri, proposal2_uri, ...}                        |
+---------------------------+----------------------------------------------------------------------------+
| **Error Response**        | 1. **Code**: 404 NOT FOUND                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'proposals doesn't exist'}                         |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 403 FORBIDDEN                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'You do not have permission to make this request'} |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 401 UNAUTHORIZED                                              |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'Incorrect credentials, please try again'}         |
+---------------------------+----------------------------------------------------------------------------+
| **HTTP Request/Response** | GET /proposals HTTP/1.1                                                    |
|                           |                                                                            |
|                           | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _                |
|                           |                                                                            |
|                           | HTTP/1.x 200 OK                                                            |
|                           |                                                                            |
|                           | Content-Type: application/json                                             |
+---------------------------+----------------------------------------------------------------------------+
| **Notes**                 | To view the proposal, must redirect to the proposal's URI.                 |
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
| **URL Params**            | 1. **Required**: None                                                      |
|                           |                                                                            |
|                           | 2. **Optional**: None                                                      |
+---------------------------+----------------------------------------------------------------------------+
| **Data Params**           | None                                                                       |
+---------------------------+----------------------------------------------------------------------------+
| **Success Response**      | 1. **Code**: 200 OK                                                        |
|                           |                                                                            |
|                           | 2. **Content**: ?                                                          |
+---------------------------+----------------------------------------------------------------------------+
| **Error Response**        | 1. **Code**: 404 NOT FOUND                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'proposal with [proposal_code] doesn't exist'}     |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 403 FORBIDDEN                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'You do not have permission to make this request'} |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 401 UNAUTHORIZED                                              |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'Incorrect credentials, please try again'}         |
+---------------------------+----------------------------------------------------------------------------+
| **HTTP Request/Response** | GET /proposals/[proposal_code] HTTP/1.1                                    |
|                           |                                                                            |
|                           | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _                |
|                           |                                                                            |
|                           | HTTP/1.x 200 OK                                                            |
|                           |                                                                            |
|                           | Content-Type: application/zip                                              |
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
|                           | Replaces the content of the existing proposal.                             |
+---------------------------+----------------------------------------------------------------------------+
| **URL**                   | **/proposals/[proposal_code]**                                             |
+---------------------------+----------------------------------------------------------------------------+
| **Method**                | **PUT**                                                                    |
+---------------------------+----------------------------------------------------------------------------+
| **URL Params**            | 1. **Required**: None                                                      |
|                           |                                                                            |
|                           | 2. **Optional**: None                                                      |
+---------------------------+----------------------------------------------------------------------------+
| **Data Params**           | Zip file                                                                   |
+---------------------------+----------------------------------------------------------------------------+
| **Success Response**      | 1. **Code**: 200 OK                                                        |
|                           |                                                                            |
|                           | 2. **Content**: Zip file                                                   |
+---------------------------+----------------------------------------------------------------------------+
| **Error Response**        | 1. **Code**: 404 NOT FOUND                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'proposal with [proposal_code] doesn't exist'}     |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 403 FORBIDDEN                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'You do not have permission to make this request'} |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 401 UNAUTHORIZED                                              |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'Incorrect credentials, please try again'}         |
+---------------------------+----------------------------------------------------------------------------+
| **HTTP Request/Response** | PUT /proposals/[proposal_code] HTTP/1.1                                    |
|                           |                                                                            |
|                           | Content-type: application/zip                                              |
|                           |                                                                            |
|                           | Content-length: 128                                                        |
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
| **URL**                   | **/proposals**                                                             |
+---------------------------+----------------------------------------------------------------------------+
| **Method**                | **POST**                                                                   |
+---------------------------+----------------------------------------------------------------------------+
| **URL Params**            | 1. **Required**: None                                                      |
|                           |                                                                            |
|                           | 2. **Optional**: None                                                      |
+---------------------------+----------------------------------------------------------------------------+
| **Data Params**           | Zip file                                                                   |
+---------------------------+----------------------------------------------------------------------------+
| **Success Response**      | 1. **Code**: 201 CREATED                                                   |
|                           |                                                                            |
|                           | 2. **Content**: {proposal_code}                                            |
+---------------------------+----------------------------------------------------------------------------+
| **Error Response**        | 1. **Code**: 403 FORBIDDEN                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'You do not have permission to make this request'} |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 401 UNAUTHORIZED                                              |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'Incorrect credentials, please try again'}         |
+---------------------------+----------------------------------------------------------------------------+
| **HTTP Request/Response** | POST /proposals/[proposal_code] HTTP/1.1                                   |
|                           |                                                                            |
|                           | Content-type: application/zip                                              |
|                           |                                                                            |
|                           | Content-length: 128                                                        |
|                           |                                                                            |
|                           | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _                |
|                           |                                                                            |
|                           | HTTP/1.x 200 OK                                                            |
|                           |                                                                            |
|                           | Location: /proposal/[proposal_code]                                        |
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
|                           | Downloads the summaries of the proposal as the pdf file                    |
+---------------------------+----------------------------------------------------------------------------+
| **URL**                   | **/proposal-summaries/[semester]**                                         |
+---------------------------+----------------------------------------------------------------------------+
| **Method**                | **GET**                                                                    |
+---------------------------+----------------------------------------------------------------------------+
| **URL Params**            | 1. **Required**: None                                                      |
|                           |                                                                            |
|                           | 2. **Optional**: None                                                      |
+---------------------------+----------------------------------------------------------------------------+
| **Data Params**           | None                                                                       |
+---------------------------+----------------------------------------------------------------------------+
| **Success Response**      | 1. **Code**: 200 OK                                                        |
|                           |                                                                            |
|                           | 2. **Content**: PDF                                                        |
+---------------------------+----------------------------------------------------------------------------+
| **Error Response**        | 1. **Code**: 404 NOT FOUND                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'proposals summaries doesn't exist'}               |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 403 FORBIDDEN                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'You do not have permission to make this request'} |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 401 UNAUTHORIZED                                              |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'Incorrect credentials, please try again'}         |
+---------------------------+----------------------------------------------------------------------------+
| **HTTP Request/Response** | GET /proposal-summaries/[semester] HTTP/1.1                                |
|                           |                                                                            |
|                           | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _                |
|                           |                                                                            |
|                           | HTTP/1.x 200 OK                                                            |
|                           |                                                                            |
|                           | Content-Type: application/pdf                                              |
+---------------------------+----------------------------------------------------------------------------+
| **Notes**                 | File downloaded is the pdf file, must have pdf enabled software to view.   |
+---------------------------+----------------------------------------------------------------------------+

*************************
Download Proposal Summary
*************************
+---------------------------+----------------------------------------------------------------------------+
| API Item                  | Description                                                                |
+===========================+============================================================================+
| **Title**                 | **Download Proposal Summary**                                              |
|                           |                                                                            |
|                           | Downloads the summary of the proposal as the pdf file                      |
+---------------------------+----------------------------------------------------------------------------+
| **URL**                   | **/proposal-summaries/[proposal_code]/[semester]**                         |
+---------------------------+----------------------------------------------------------------------------+
| **Method**                | **GET**                                                                    |
+---------------------------+----------------------------------------------------------------------------+
| **URL Params**            | 1. **Required**: None                                                      |
|                           |                                                                            |
|                           | 2. **Optional**: None                                                      |
+---------------------------+----------------------------------------------------------------------------+
| **Data Params**           | None                                                                       |
+---------------------------+----------------------------------------------------------------------------+
| **Success Response**      | 1. **Code**: 200 OK                                                        |
|                           |                                                                            |
|                           | 2. **Content**: PDF                                                        |
+---------------------------+----------------------------------------------------------------------------+
| **Error Response**        | 1. **Code**: 404 NOT FOUND                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'proposal with [proposal_code] doesn't exist'}     |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 403 FORBIDDEN                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'You do not have permission to make this request'} |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 401 UNAUTHORIZED                                              |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'Incorrect credentials, please try again'}         |
+---------------------------+----------------------------------------------------------------------------+
| **HTTP Request/Response** | GET /proposal-summaries/[proposal_code]/[semester] HTTP/1.1                |
|                           |                                                                            |
|                           | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _                |
|                           |                                                                            |
|                           | HTTP/1.x 200 OK                                                            |
|                           |                                                                            |
|                           | Content-Type: application/pdf                                              |
+---------------------------+----------------------------------------------------------------------------+
| **Notes**                 | File downloaded is the pdf file, must have pdf enabled software to view.   |
+---------------------------+----------------------------------------------------------------------------+

*************
Get SALT User
*************
+---------------------------+----------------------------------------------------------------------------+
| API Item                  | Description                                                                |
+===========================+============================================================================+
| **Title**                 | **Get SALT User**                                                          |
|                           |                                                                            |
|                           | Returns the SALT user in a json format                                     |
+---------------------------+----------------------------------------------------------------------------+
| **URL**                   | **/users/[username]**                                                      |
+---------------------------+----------------------------------------------------------------------------+
| **Method**                | **GET**                                                                    |
+---------------------------+----------------------------------------------------------------------------+
| **URL Params**            | 1. **Required**: username=[String], password=[String]                      |
|                           |                                                                            |
|                           | 2. **Optional**: None                                                      |
+---------------------------+----------------------------------------------------------------------------+
| **Data Params**           | None                                                                       |
+---------------------------+----------------------------------------------------------------------------+
| **Success Response**      | 1. **Code**: 200 OK                                                        |
|                           |                                                                            |
|                           | 2. **Content**:                                                            |
|                           |                                                                            |
|                           |  {                                                                         |
|                           |                                                                            |
|                           |    user:                                                                   |
|                           |                                                                            |
|                           |      {                                                                     |
|                           |                                                                            |
|                           |        name: "name",                                                       |
|                           |                                                                            |
|                           |        email: "email",                                                     |
|                           |                                                                            |
|                           |        username: "username", ...                                           |
|                           |                                                                            |
|                           |      }                                                                     |
|                           |                                                                            |
|                           |  }                                                                         |
+---------------------------+----------------------------------------------------------------------------+
| **Error Response**        | 1. **Code**: 404 NOT FOUND                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'user with the [username] doesn't exist'}          |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 403 FORBIDDEN                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'You do not have permission to make this request'} |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 401 UNAUTHORIZED                                              |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'Incorrect credentials, please try again'}         |
+---------------------------+----------------------------------------------------------------------------+
| **HTTP Request/Response** | GET /users/[username] HTTP/1.1                                             |
|                           |                                                                            |
|                           | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _                |
|                           |                                                                            |
|                           | HTTP/1.x 200 OK                                                            |
|                           |                                                                            |
|                           | Content-Type: application/json                                             |
+---------------------------+----------------------------------------------------------------------------+
| **Notes**                 | None                                                                       |
+---------------------------+----------------------------------------------------------------------------+

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
| **Method**                | **PATCH**                                                                  |
+---------------------------+----------------------------------------------------------------------------+
| **URL Params**            | 1. **Required**: None                                                      |
|                           |                                                                            |
|                           | 2. **Optional**: None                                                      |
+---------------------------+----------------------------------------------------------------------------+
| **Data Params**           | {                                                                          |
|                           |                                                                            |
|                           |   user:                                                                    |
|                           |                                                                            |
|                           |     {                                                                      |
|                           |                                                                            |
|                           |       name: "name",                                                        |
|                           |                                                                            |
|                           |       email: "email",                                                      |
|                           |                                                                            |
|                           |       username: "username", ...                                            |
|                           |                                                                            |
|                           |     }                                                                      |
|                           |                                                                            |
|                           | }                                                                          |
+---------------------------+----------------------------------------------------------------------------+
| **Success Response**      | 1. **Code**: 200 OK                                                        |
|                           |                                                                            |
|                           | 2. **Content**:                                                            |
|                           |                                                                            |
|                           |  {                                                                         |
|                           |                                                                            |
|                           |    user:                                                                   |
|                           |                                                                            |
|                           |      {                                                                     |
|                           |                                                                            |
|                           |        name: "name",                                                       |
|                           |                                                                            |
|                           |        email: "email",                                                     |
|                           |                                                                            |
|                           |        username: "username", ...                                           |
|                           |                                                                            |
|                           |      }                                                                     |
|                           |                                                                            |
|                           |  }                                                                         |
+---------------------------+----------------------------------------------------------------------------+
| **Error Response**        | 1. **Code**: 404 NOT FOUND                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'user with [username] doesn't exist'}              |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 403 FORBIDDEN                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'You do not have permission to make this request'} |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 401 UNAUTHORIZED                                              |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'Incorrect credentials, please try again'}         |
+---------------------------+----------------------------------------------------------------------------+
| **HTTP Request/Response** | PATCH /users/[username] HTTP/1.1                                           |
|                           |                                                                            |
|                           | Content-type: application/json                                             |
|                           |                                                                            |
|                           | Content-length: 8                                                          |
|                           |                                                                            |
|                           | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _                |
|                           |                                                                            |
|                           | HTTP/1.x 200 OK                                                            |
|                           |                                                                            |
|                           | Location: /users/[username]                                                |
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
| **URL**                   | **/users**                                                                 |
+---------------------------+----------------------------------------------------------------------------+
| **Method**                | **POST**                                                                   |
+---------------------------+----------------------------------------------------------------------------+
| **URL Params**            | 1. **Required**: None                                                      |
|                           |                                                                            |
|                           | 2. **Optional**: None                                                      |
+---------------------------+----------------------------------------------------------------------------+
| **Data Params**           | {                                                                          |
|                           |                                                                            |
|                           |   user:                                                                    |
|                           |                                                                            |
|                           |     {                                                                      |
|                           |                                                                            |
|                           |       name: "name",                                                        |
|                           |                                                                            |
|                           |       email: "email",                                                      |
|                           |                                                                            |
|                           |       username: "username", ...                                            |
|                           |                                                                            |
|                           |     }                                                                      |
|                           |                                                                            |
|                           | }                                                                          |
+---------------------------+----------------------------------------------------------------------------+
| **Success Response**      | 1. **Code**: 201 CREATED                                                   |
|                           |                                                                            |
|                           | 2. **Content**:                                                            |
|                           |                                                                            |
|                           |  {                                                                         |
|                           |                                                                            |
|                           |    user:                                                                   |
|                           |                                                                            |
|                           |      {                                                                     |
|                           |                                                                            |
|                           |        name: "name",                                                       |
|                           |                                                                            |
|                           |        email: "email",                                                     |
|                           |                                                                            |
|                           |        username: "username", ...                                           |
|                           |                                                                            |
|                           |      }                                                                     |
|                           |                                                                            |
|                           |  }                                                                         |
+---------------------------+----------------------------------------------------------------------------+
| **Error Response**        | 1. **Code**: 403 FORBIDDEN                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'You do not have permission to make this request'} |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 401 UNAUTHORIZED                                              |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'Incorrect credentials, please try again'}         |
+---------------------------+----------------------------------------------------------------------------+
| **HTTP Request/Response** | POST /users HTTP/1.1                                                       |
|                           |                                                                            |
|                           | Content-type: application/json                                             |
|                           |                                                                            |
|                           | Content-length: 5                                                          |
|                           |                                                                            |
|                           | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _                |
|                           |                                                                            |
|                           | HTTP/1.x 200 OK                                                            |
|                           |                                                                            |
|                           | Location: /users/[username]                                                |
+---------------------------+----------------------------------------------------------------------------+
| **Notes**                 | None                                                                       |
+---------------------------+----------------------------------------------------------------------------+

**********
Get Blocks
**********
+---------------------------+----------------------------------------------------------------------------+
| API Item                  | Description                                                                |
+===========================+============================================================================+
| **Title**                 | **Get Blocks**                                                             |
|                           |                                                                            |
|                           | Returns blocks in a json format                                            |
+---------------------------+----------------------------------------------------------------------------+
| **URL**                   | **/proposals/[proposal_code]/blocks**                                      |
+---------------------------+----------------------------------------------------------------------------+
| **Method**                | **GET**                                                                    |
+---------------------------+----------------------------------------------------------------------------+
| **URL Params**            | 1. **Required**: None                                                      |
|                           |                                                                            |
|                           | 2. **Optional**: None                                                      |
+---------------------------+----------------------------------------------------------------------------+
| **Data Params**           | None                                                                       |
+---------------------------+----------------------------------------------------------------------------+
| **Success Response**      | 1. **Code**: 200 OK                                                        |
|                           |                                                                            |
|                           | 2. **Content**:                                                            |
|                           |                                                                            |
|                           |  {                                                                         |
|                           |                                                                            |
|                           |    blocks                                                                  |
|                           |                                                                            |
|                           |      {                                                                     |
|                           |        block_id:                                                           |
|                           |                                                                            |
|                           |        {                                                                   |
|                           |                                                                            |
|                           |          Observing conditions: {Transparency: "Any", ...},                 |
|                           |                                                                            |
|                           |          Iterations: {Wait: "11 days", ..},                                |
|                           |                                                                            |
|                           |          Total-Obs-times: {Overhead: 5184, ...}, ...                       |
|                           |                                                                            |
|                           |        }, ...                                                              |
|                           |                                                                            |
|                           |      }                                                                     |
|                           |                                                                            |
|                           |  }                                                                         |
+---------------------------+----------------------------------------------------------------------------+
| **Error Response**        | 1. **Code**: 403 FORBIDDEN                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'You do not have permission to make this request'} |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 401 UNAUTHORIZED                                              |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'Incorrect credentials, please try again'}         |
+---------------------------+----------------------------------------------------------------------------+
| **HTTP Request/Response** | GET /proposals/[proposal_code]/blocks HTTP/1.1                             |
|                           |                                                                            |
|                           | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _                |
|                           |                                                                            |
|                           | HTTP/1.x 200 OK                                                            |
|                           |                                                                            |
|                           | Content-Type: application/json                                             |
+---------------------------+----------------------------------------------------------------------------+
| **Notes**                 | None                                                                       |
+---------------------------+----------------------------------------------------------------------------+

*********
Get Block
*********
+---------------------------+----------------------------------------------------------------------------+
| API Item                  | Description                                                                |
+===========================+============================================================================+
| **Title**                 | **Get Block**                                                              |
|                           |                                                                            |
|                           | Returns the block in a json format                                         |
+---------------------------+----------------------------------------------------------------------------+
| **URL**                   | **/proposals/[proposal_code]/blocks/[block_id]**                           |
+---------------------------+----------------------------------------------------------------------------+
| **Method**                | **GET**                                                                    |
+---------------------------+----------------------------------------------------------------------------+
| **URL Params**            | 1. **Required**: None                                                      |
|                           |                                                                            |
|                           | 2. **Optional**: None                                                      |
+---------------------------+----------------------------------------------------------------------------+
| **Data Params**           | None                                                                       |
+---------------------------+----------------------------------------------------------------------------+
| **Success Response**      | 1. **Code**: 200 OK                                                        |
|                           |                                                                            |
|                           | 2. **Content**:                                                            |
|                           |                                                                            |
|                           |  {                                                                         |
|                           |                                                                            |
|                           |    block_id:                                                               |
|                           |                                                                            |
|                           |      {                                                                     |
|                           |                                                                            |
|                           |        Observing conditions: {Transparency: "Any", ...},                   |
|                           |                                                                            |
|                           |        Iterations: {Wait: "11 days", ..},                                  |
|                           |                                                                            |
|                           |        Total-Obs-times: {Overhead: 5184, ...}, ...                         |
|                           |                                                                            |
|                           |      }                                                                     |
|                           |                                                                            |
|                           |  }                                                                         |
+---------------------------+----------------------------------------------------------------------------+
| **Error Response**        | 1. **Code**: 404 NOT FOUND                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'block with the [block_id] doesn't exist'}         |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 403 FORBIDDEN                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'You do not have permission to make this request'} |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 401 UNAUTHORIZED                                              |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'Incorrect credentials, please try again'}         |
+---------------------------+----------------------------------------------------------------------------+
| **HTTP Request/Response** | GET /proposals/[proposal_code]/blocks/[block_id] HTTP/1.1                  |
|                           |                                                                            |
|                           | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _                |
|                           |                                                                            |
|                           | HTTP/1.x 200 OK                                                            |
|                           |                                                                            |
|                           | Content-Type: application/json                                             |
+---------------------------+----------------------------------------------------------------------------+
| **Notes**                 | None                                                                       |
+---------------------------+----------------------------------------------------------------------------+

************
Update Block
************
+---------------------------+----------------------------------------------------------------------------+
| API Item                  | Description                                                                |
+===========================+============================================================================+
| **Title**                 | **Update Block**                                                           |
|                           |                                                                            |
|                           | Modifies the content of the existing block.                                |
+---------------------------+----------------------------------------------------------------------------+
| **URL**                   | **/proposals/[proposal_code]/blocks/[block_id]**                           |
+---------------------------+----------------------------------------------------------------------------+
| **Method**                | **PATCH**                                                                  |
+---------------------------+----------------------------------------------------------------------------+
| **URL Params**            | 1. **Required**: None                                                      |
|                           |                                                                            |
|                           | 2. **Optional**: None                                                      |
+---------------------------+----------------------------------------------------------------------------+
| **Data Params**           | {                                                                          |
|                           |                                                                            |
|                           |   block_id:                                                                |
|                           |                                                                            |
|                           |     {                                                                      |
|                           |                                                                            |
|                           |       Observing conditions: {Transparency: "Any", ...},                    |
|                           |                                                                            |
|                           |       Iterations: {Wait: "11 days", ..},                                   |
|                           |                                                                            |
|                           |       Total-Obs-times: {Overhead: 5184, ...}, ...                          |
|                           |                                                                            |
|                           |     }                                                                      |
|                           |                                                                            |
|                           | }                                                                          |
+---------------------------+----------------------------------------------------------------------------+
| **Success Response**      | 1. **Code**: 200 OK                                                        |
|                           |                                                                            |
|                           | 2. **Content**:                                                            |
|                           |                                                                            |
|                           |  {                                                                         |
|                           |                                                                            |
|                           |    block_id:                                                               |
|                           |                                                                            |
|                           |      {                                                                     |
|                           |                                                                            |
|                           |        Observing conditions: {Transparency: "Any", ...},                   |
|                           |                                                                            |
|                           |        Iterations: {Wait: "11 days", ..},                                  |
|                           |                                                                            |
|                           |        Total-Obs-times: {Overhead: 5184, ...}, ...                         |
|                           |                                                                            |
|                           |      }                                                                     |
|                           |                                                                            |
|                           |  }                                                                         |
+---------------------------+----------------------------------------------------------------------------+
| **Error Response**        | 1. **Code**: 404 NOT FOUND                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'block with [block_id] doesn't exist'}             |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 403 FORBIDDEN                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'You do not have permission to make this request'} |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 401 UNAUTHORIZED                                              |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'Incorrect credentials, please try again'}         |
+---------------------------+----------------------------------------------------------------------------+
| **HTTP Request/Response** | PATCH /proposals/[proposal_code]/blocks/[block_id] HTTP/1.1                |
|                           |                                                                            |
|                           | Content-type: application/json                                             |
|                           |                                                                            |
|                           | Content-length: 8                                                          |
|                           |                                                                            |
|                           | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _                |
|                           |                                                                            |
|                           | HTTP/1.x 200 OK                                                            |
|                           |                                                                            |
|                           | Location: /proposals/[proposal_code]/blocks/[block_id]                     |
+---------------------------+----------------------------------------------------------------------------+
| **Notes**                 | None                                                                       |
+---------------------------+----------------------------------------------------------------------------+

*********
Add Block
*********
+---------------------------+----------------------------------------------------------------------------+
| API Item                  | Description                                                                |
+===========================+============================================================================+
| **Title**                 | **Add Block**                                                              |
|                           |                                                                            |
|                           | Inserts the new record of the block.                                       |
+---------------------------+----------------------------------------------------------------------------+
| **URL**                   | **/proposals/[proposal_code]/blocks**                                      |
+---------------------------+----------------------------------------------------------------------------+
| **Method**                | **POST**                                                                   |
+---------------------------+----------------------------------------------------------------------------+
| **URL Params**            | 1. **Required**: None                                                      |
|                           |                                                                            |
|                           | 2. **Optional**: None                                                      |
+---------------------------+----------------------------------------------------------------------------+
| **Data Params**           | {                                                                          |
|                           |                                                                            |
|                           |   block_id:                                                                |
|                           |                                                                            |
|                           |     {                                                                      |
|                           |                                                                            |
|                           |       Observing conditions: {Transparency: "Any", ...},                    |
|                           |                                                                            |
|                           |       Iterations: {Wait: "11 days", ..},                                   |
|                           |                                                                            |
|                           |       Total-Obs-times: {Overhead: 5184, ...}, ...                          |
|                           |                                                                            |
|                           |     }                                                                      |
|                           |                                                                            |
|                           | }                                                                          |
+---------------------------+----------------------------------------------------------------------------+
| **Success Response**      | 1. **Code**: 201 CREATED                                                   |
|                           |                                                                            |
|                           | 2. **Content**: { block_id }                                               |
+---------------------------+----------------------------------------------------------------------------+
| **Error Response**        | 1. **Code**: 403 FORBIDDEN                                                 |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'You do not have permission to make this request'} |
|                           |                                                                            |
|                           | OR                                                                         |
|                           |                                                                            |
|                           | 1. **Code**: 401 UNAUTHORIZED                                              |
|                           |                                                                            |
|                           | 2. **Content**: {error: 'Incorrect credentials, please try again'}         |
+---------------------------+----------------------------------------------------------------------------+
| **HTTP Request/Response** | POST /proposals/[proposal_code]/blocks HTTP/1.1                            |
|                           |                                                                            |
|                           | Content-type: application/json                                             |
|                           |                                                                            |
|                           | Content-length: 8                                                          |
|                           |                                                                            |
|                           | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _                |
|                           |                                                                            |
|                           | HTTP/1.x 200 OK                                                            |
|                           |                                                                            |
|                           | Location: /proposals/[proposal_code]/blocks/[block_id]                     |
+---------------------------+----------------------------------------------------------------------------+
| **Notes**                 | None                                                                       |
+---------------------------+----------------------------------------------------------------------------+