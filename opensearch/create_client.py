import os
from dotenv import load_dotenv
import certifi
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth

def create_client():
    '''
    This function creates an OpenSearch client. If the environment variables OPENSEARCH_HOST and OPENSEARCH_PORT are not
    set, an error is raised. If ENVIRONMENT is set to 'local', it connects using basic auth. Otherwise,
    it uses AWS request signing. This abstracts away local vs cloud setup.
    @return: OpenSearch client
    '''
    load_dotenv()

    env = os.getenv("ENVIRONMENT", "local").lower()
    host = os.getenv('OPENSEARCH_HOST')
    port = os.getenv('OPENSEARCH_PORT')
    region = 'us-east-1'
    # Makes sure your environment variables are set
    if not host or not port:
        raise ValueError('Please set the environment variables OPENSEARCH_HOST and OPENSEARCH_PORT')
    # If the environment is local, we use basic auth and returns the client immediately
    if env == "local":
        auth = ('admin', os.getenv('OPENSEARCH_INITIAL_ADMIN_PASSWORD'))

        ca_certs_path = certifi.where()
        client = OpenSearch(
            hosts=[{'host': host, 'port': int(port)}],
            http_compress=True,
            http_auth=auth,
            use_ssl=False,
            verify_certs=False,
            ssl_show_warn=False,
            connection_class=RequestsHttpConnection
        )
        return client

    service = 'aoss'
    credentials = boto3.Session().get_credentials()
    auth = AWSV4SignerAuth(credentials, region, service)
    # creates the opensearch aws client (for production)
    client = OpenSearch(
        hosts=[{'host': host, 'port': int(port)}],
        http_compress=True,
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        pool_maxsize=20,
        timeout=60
    )

    return client
