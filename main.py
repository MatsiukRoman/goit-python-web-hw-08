from typing import List, Any
import redis
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)

@cache
def find_by_tag(tag: str) -> list[str | None]:
    print(f"Find by {tag}")
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result

@cache
def find_by_author(author: str) -> list[list[Any]]:
    print(f"Find by {author}")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result

def parse_input(user_input):
    if not user_input.strip():
        return None, []
    
    parts = user_input.strip().split(maxsplit=1)
    cmd = parts[0].lower().rstrip(':')
    
    if len(parts) > 1:
        args = [arg.strip() for arg in parts[1].split(',')]
    else:
        args = parts[1:] if len(parts) > 1 else []
    return cmd, args

def main():

    while True:
        user_input = input("Enter a command: ")
        
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "name":
            print(find_by_author(str(args[0])))

        elif command == "tag":
            print(find_by_tag(str(args[0])))

        elif command == "tags":
            for item in args:
               print(find_by_tag(str(item)))

        else:
            print("Invalid command.")

if __name__ == '__main__':
    main()
