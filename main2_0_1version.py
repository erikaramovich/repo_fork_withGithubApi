import requests
import json
import os
import base64


def get_user_repositories(username):
  url = f'https://api.github.com/users/{username}/repos'
  response = requests.get(url)
  if response.status_code == 200:
    repositories = response.json()
    return repositories
  else:
    print(f'Error: {response.status_code}')
    return None



def get_repository_content(username, repo_name):
  base_url = "https://api.github.com"

  # Construct the endpoint for the contents
  endpoint = f"/repos/{username}/{repo_name}/contents"

  response = requests.get(base_url + endpoint)

  if response.status_code == 200:
    contents = response.json()
    file_contents = {}
    dir_contents = {}
    
    with open(f"{repo_name}_content.json", "w") as file:
      json.dump(contents, file, indent=3)
    os.mkdir(repo_name)
    for content in contents:
      print(f"CONTENT TYPE of {content['path']} ---> {content['type']}")
      
      if content["type"] == "file":
        file_path = content["path"]
        
        print(f"file path: {file_path}")

        file_content = get_file_content(username, repo_name, file_path)
        with open(f'{repo_name}/{content["name"]}', "w") as file:
          file.write(file_content)
        file_contents[file_path] = file_content
        
      if content["type"] == "dir":
        os.mkdir(f'{repo_name}/{content["path"]}')
        dir_path = content["path"]

        print(f"dir: {dir_path}")

        get_dir_content(username, repo_name, dir_path)
      

      

    return None
  else:
    return f"Request failed with status code {response.status_code}"



def get_file_content(username, repo_name, file_path):
  base_url = "https://api.github.com"

  # Construct the endpoint for the file
  endpoint = f"/repos/{username}/{repo_name}/contents/{file_path}"

  response = requests.get(base_url + endpoint)

  if response.status_code == 200:
    file_data = response.json()
    content = file_data["content"]
    
    if content:
      # Decode the base64-encoded content
      file_contents = base64.b64decode(content).decode("utf-8")
      return file_contents
    else:
      return "File content not found."
  else:
    return f"Request failed with status code {response.status_code}"




def get_dir_content(username, repo_name, dir_path):
    
    base_url = "https://api.github.com"
    endpoint = f"/repos/{username}/{repo_name}/contents/{dir_path}"
  
    response = requests.get(base_url + endpoint)

    if response.status_code == 200:
      dir_data = response.json()
      
  
      for element in dir_data:
        if element["type"] == "dir":
          dir_path = element["path"]
          
          print(f"dir: {dir_path}")

          os.mkdir(f"{repo_name}/{dir_path}")
          get_dir_content(username, repo_name, dir_path)
 
        if element["type"] == "file":
          file_content = get_file_content(username, repo_name, element["path"])
          with open(f'{repo_name}/{dir_path}/{element["name"]}', "w") as file:
            file.write(file_content)

        

    else:
      return f"Request failed with status code {response.status_code}"
      




username = "davidks13"
user_repositories = get_user_repositories(username)
user_repos_list = list()

i = 1
for repo in user_repositories:
  user_repos_list.append(repo["name"])
  print(f'{i}: {repo["name"]} -> {repo["language"]}')
  i += 1

while True:
  input_repo = int(input("Enter repo number: "))
  if 1 <= input_repo <= len(user_repos_list):
    print(user_repos_list[input_repo - 1])
    repo_content = get_repository_content(username, user_repos_list[input_repo - 1])
    break
  elif input_repo == 0:
    break
  else:
    print("Invalid index, Try again or enter '0'")




""" 
KONKRET CASE A, erb repoyum menak filer a

os.mkdir(user_repos_list[input_repo - 1])
for key, value in repo_content[0].items():
  with open(f"{user_repos_list[input_repo - 1]}/{key}", "w") as file:
    file.write(value)

"""