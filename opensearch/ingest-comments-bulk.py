import argparse
import os
import json
from create_client import create_client
import time 


def get_data_from_file(file_path):
    with open(file_path) as file:
        try:
            data = json.load(file)
            document = {
                'commentText': data['data']['attributes']['comment'],
                'docketId': data['data']['attributes']['docketId'],
                'commentId': data['data']['id']
            }
            return document
        except Exception as e:
            print(f"Error reading file: {file_path}")
            print(e)
            return None

def  bulk_ingest_all(client, directory_name, index_name, max_mb_per_bulk):
    # the ingest_string will be used to store the bulk ingest request
    ingest_string = ""

    # total_count will keep track of the total number of documents ingested
    total_count = 0
    # current_chars will keep track of the current number of characters in the ingest_string
    current_chars = 0


    for dirpath, dirnames, filenames in os.walk(directory_name):
        for filename in filenames:
            if dirpath.endswith("comments") and filename.endswith(".json"):
                document = get_data_from_file(os.path.join(dirpath, filename))
                if not document:
                    continue
                comment_id = document['commentId']
            
                # the action line is used to specify the index name
                action = f'{{"index": {{"_index": "{index_name}", "_id": "{comment_id}"}}}}\n'
                # the data_string is the document to be ingested
                data_string = json.dumps(document) + '\n'

                # if the current_chars + the length of the action line + the length of the data_string is greater than 50MB, we send the bulk ingest request
                if current_chars + len(action) + len(data_string) > max_mb_per_bulk * 1024 * 1024:
                    try:
                        response = client.bulk(body = ingest_string)
                        print(f"Total documents ingested: {total_count}")
                        # reset the ingest_string and current_chars
                        ingest_string = ""
                        current_chars = 0
                    except Exception as e:
                        print(f"Error sending bulk request: {e}")
                        print()
                
                # if the current action line + the length of the data_string is greater than 50MB, we print the commentID and continue
                if len(action) + len(data_string) > max_mb_per_bulk * 1024 * 1024:
                    print(f"CommentID: {comment_id} is too large to ingest")
                    continue

                # add the length of the action line + the length of the data_string to the current_chars
                current_chars += len(action) + len(data_string)

                ingest_string += action
                ingest_string += data_string

                # increment the total_count
                total_count += 1

    # if there are any documents left in the ingest_string, we send the bulk ingest request
    if ingest_string:
        try:
            response = client.bulk(body = ingest_string)
            print(f"Total documents ingested: {total_count}")
        except Exception as e:
            print(f"Error sending bulk request: {e}")
            print(ingest_string)
            print()

if __name__ == '__main__':
    client = create_client()

    index_name = 'comments'

    # specify the directory name where the JSON files are stored
    
    parser = argparse.ArgumentParser(description='Ingest local comments into Elasticsearch.')
    parser.add_argument('--n_comments', type=int, help='Number of comments to ingest', default=-1)
    parser.add_argument('--time', type=bool, help='Time the ingest', default=False)
    parser.add_argument('--local_directory', type=str, help='Local directory containing JSON files', default='docket-samples')

    directory_name = parser.parse_args().local_directory
    args = parser.parse_args() 
    total_to_ingest = args.n_comments


    if args.time:
        start = time.time()
        
    max_mb_per_bulk = 50
    bulk_ingest_all(client, directory_name, index_name, max_mb_per_bulk)
    
    if args.time:
        end = time.time()
        print(f"Total time taken: {end - start} seconds")
