from pinecone import Pinecone, ServerlessSpec
import time
import os


def VectorDBConfigurations(pinecone_api_key,index_name):
    pc = Pinecone(api_key=pinecone_api_key)

    existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        while not pc.describe_index(index_name).status["ready"]:
            time.sleep(1)

    index = pc.Index(index_name)
    return index