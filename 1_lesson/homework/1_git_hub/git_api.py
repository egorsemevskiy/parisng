import requests
import json

headers = {"Authorization": "Bearer ab4ba0c5c256c953b58f524f86f0ceb5e25825e0"}


def run_query(query):  # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


query = """
{
  viewer {
    repositories(first: 100) {
      totalCount
      nodes {
        nameWithOwner
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
}
     
"""

result = run_query(query)

all_repos = result["data"]["viewer"]["repositories"]['nodes']
has_next_page = result['data']['viewer']["repositories"]['pageInfo']['hasNextPage']

print("has next page - {} | All repositories - {}".format(has_next_page, all_repos))

with open('data.json', 'w') as outfile:
    json.dump(all_repos, outfile)
