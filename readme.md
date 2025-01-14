
<pre>
Table Creation: Initializes the database and ensures the image table exists.
Create: Inserts a new record into the image table.
Read: Retrieves an image record by its name.
Update: Updates an existing image record by its name.
Delete: Removes an image record by its name.
</pre>

sql to create, read, write, update, delete as a simple registry.
There is also a function to export sql to csv.

![change_in_status](change_in_status.png)

`status_signature` field represents a signature created by hashing all the fields in the record.
`status_url field` for notes on the status, such as a CVE URL when the status is "suspended."

```
image.name:
image.contents (base64):
sha256: 
hmac: 
team:
team.owner:
```