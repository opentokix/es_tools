#!/usr/bin/env python3

import sys
import elasticsearch
import argparse 
from datetime import datetime

parser = argparse.ArgumentParser(prog='Annotation poster', description="Get some arguments", usage='annotation.py [options]')
parser.add_argument('--port', '-p', type=int, help="port of elasticsearch server")
parser.add_argument('--host', '-H', type=str, help="Host of elasticsearch server")
parser.add_argument('--index', '-i', type=str, help="Index for annotations")
parser.add_argument('message')
parser.add_argument('tags')
parser.add_argument('invoker')
options = parser.parse_args()

def main():
  tags = options.tags.split(',')
  es = elasticsearch.Elasticsearch()
  doc = {
    'text': options.message,
    'invoker': options.invoker,
    'tags': tags,
    'timestamp': datetime.utcnow()
  }
  result = es.index(index=options.index, body=doc)
  print(result['result'])

if __name__ == "__main__":
  main()