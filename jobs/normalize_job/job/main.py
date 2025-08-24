from normalize_db import normalize_new_stores
import argparse

def main():

    parser = argparse.ArgumentParser(description='Normalize store names in the database.')
    parser.add_argument('--chunk-size', type=int, required=False, default=5000, help='Size of chunks to process at a time')

    args = parser.parse_args()

    normalize_new_stores(chunk_size=args.chunk_size)

if __name__ == "__main__":
    main()