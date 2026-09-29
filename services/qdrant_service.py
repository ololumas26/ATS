from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


CV_COLLECTION_NAME = 'first_collection'


qclient : QdrantClient = QdrantClient(path='./qdrant_files')

if not qclient.collection_exists(collection_name=CV_COLLECTION_NAME):
    qclient.create_collection(
        collection_name=CV_COLLECTION_NAME,
        vectors_config=(VectorParams(size=1536, distance=Distance.COSINE))
    )
