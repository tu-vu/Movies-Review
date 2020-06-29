import requests

def main():
    res = requests.get("https://api.themoviedb.org/3/movie/550?api_key=2f0dbac34c4d747c83895d65efad8073")
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()
    print(data['adult'])

if __name__ == "__main__":
    main()