from canvas_token import authentication
import requests
import json
import wget
if __name__ == '__main__':
    auth = authentication()

    canvas_key = auth.getcanvas_key()
    canvas_url = auth.getcanvas_url()
    download_filename = 'hello2.txt'
    upload_filename   = 'hello.txt'
    # Set up a session
    session = requests.Session()
    session.headers = {'Authorization': 'Bearer %s' % canvas_key}


    # Step 1 - tell Canvas you want to upload a file
    payload = {}
    payload['name'] = upload_filename
    payload['parent_folder_path'] = '/'
    r = session.post(canvas_url, data=payload)
    r.raise_for_status()
    r = r.json()
    print(' ')
    print(r)  # This successfully returns the expected response...


    # Step 2 - upload file
    payload = list(r['upload_params'].items())  # Note this is now a list of tuples
    print(' ')
    print(payload)
    with open(upload_filename, 'rb') as f:
        file_content = f.read()
    payload.append((u'file', file_content))  # Append file at the end of list of tuples
    r = requests.post(r['upload_url'], files=payload)
    r.raise_for_status()
    r = r.json()  # The requests now works and returns response 200 - not 301.
    print(' ')
    print(r)  # This is a dictionary containing some info about the uploaded file


    # Step 3 - download file
    params = (
        ('sort=name')
    )
    session.headers = {'Authorization': 'Bearer %s' % canvas_key}
    r = session.get(canvas_url+'?'+'only[]=names',params=params)
    r.raise_for_status()
    r = r.json()
    for x in r:
        if (x['filename']) == download_filename:
            file_id = (x['id'])
    r = session.get(canvas_url+'/'+str(file_id), stream=True)
    r = r.json()
    with open(download_filename, 'wb') as f:
        f.write(file_content)

    print(' ')
    print(r)  # This is a dictionary containing some info about the downloaded file


    # Step 4 - list the files
    params = (
        ('sort=name')
    )
    r = session.get(canvas_url+'?'+'only[]=names',params=params)
    r.raise_for_status()
    r = r.json()
    print('\nFiles within folder:')
    for x in r:
        print(x['filename'])
