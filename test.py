from serpapi import GoogleSearch

params = {
  "engine": "google",
  "q": "Coffee",
  "api_key": "fb7fb71e75da87583254d23587e12b645a70ebcd1f839ac0321c051537709723"
}

search = GoogleSearch(params)
results = search.get_dict()
print(results)
#organic_results = results["organic_results"]