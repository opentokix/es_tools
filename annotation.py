#!/usr/bin/env python3
"""
annoations
GF5KFCTY1RXP
api_key: d1RLaGc0WUJiSHBOX1plQVROcUQ6VDJEZ1Zzd3hSRU9jdVBnMldqT1JVdw==
{"id":"wTKhg4YBbHpN_ZeATNqD","name":"annotations","api_key":"T2DgVswxREOcuPg2WjORUw","encoded":"d1RLaGc0WUJiSHBOX1plQVROcUQ6VDJEZ1Zzd3hSRU9jdVBnMldqT1JVdw=="}

"""
import sys
import elasticsearch
import click
from base64 import b64decode
from datetime import datetime

@click.command()
@click.option('--port', '-P', type=str, required=False, default='9200', help="port of elasticsearch server")
@click.option('--host', '-H', type=str, required=True, default='localhost', help="Host of elasticsearch server")
@click.option('--index', '-i', type=str, required=True, help="Index for annotations")
@click.option('--invoker', type=str, required=True, help="Who triggered this command")
@click.option('--tags', type=str, required=False, default=None, help="List of tags for the annotation")
@click.option('--message', type=str, required=True, help="The message for the annotation")
@click.option('--token', '-u', type=str, required=False, help="User for elastic search")
@click.option('--secret', '-p', type=str, required=False, help="User for elasticsearch")
@click.option('--scheme', default='https', type=click.Choice(['http', 'https']), help="Use http or https")
@click.option('--enctoken', default=None, type=str, help="Base64 encoded token from Kibana")
def main(host, port, index, invoker, tags, message, token, secret, scheme, enctoken):
  if enctoken:
    decoded_token = b64decode(enctoken).decode('ascii')
    token_parts = decoded_token.split(':', 1)
    token = token_parts[0]
    secret = token_parts[1]
  if tags:
    split_tags = tags.split(',')

  es = elasticsearch.Elasticsearch(
    f"{scheme}://{host}:{port}",
    api_key=(token, secret),
  )
  doc = {
    'text': message,
    'invoker': invoker,
    'tags': split_tags,
    'timestamp': datetime.utcnow()
  }
  try:
    result = es.index(index=index, body=doc)
  except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

if __name__ == "__main__":
  main()