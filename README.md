# DLfromGitHub
A simple Python script, created with PyGitHub, to download individual directories/ files from private GitHub repos

## Purpose:

At the moment, there is no direct way for a person on GitHub to download one directory in a repository.  

Although there are tools out there to aid with this (such as GitZip), 
1. They require the user to provide their GitHub access token to a 3rd party web service, which may be a security concern for some, and
2. There was no clear option online for a script that could achieve the same purpose.

Thank you to Kevin Sookocheff for providing the functions for the script in his article here: https://sookocheff.com/post/tools/downloading-directories-of-code-from-github-using-the-github-api/

## Pre-recs:

You should have Python v.3.8.0 installed.  

## How To Use:

1. In command line, move to the directory with main_dl_github.py in it  
2. Run python main_dl_github.py + <necessary parameters> .  Enter parameters as shown below:
  
   `python main_dl_github.py -u=<username> -p=<password> -o=<organization name> -r=<repository name> -b=<branch, or tag, to download> -d=<directory to download>`
  - `username`:                       GitHub username.
  - `password`:                       GitHub password.
  - `organization name`:              Name of the organization in which the repo to download resides.  
  - `repository name`:                Name of the repo to download.
  - `branch, or tag, to download`:    The name of the branch to download (exp: master)
  - `directory to download`:          Name of the directory to download.  If it's a directory within a directory, write directories separated by forward slashes (/).  
   
3. Run command line; the final output will be a directory organized as below:
    - Organization Name
      - Repository Name
        - Directory To Download
          - Files in directory
       
## Limitations:

Due to the limitations of PyGitHub, files above 1MB will not be downloaded.  A message in the command line will notify users about files that failed to download.  

## To-Do (future upgrade ideas):
- Current script only allows for downloading directories from repos of organizations.  Should create ways for users to download other forms of private repos (exp: those shared by other users)
