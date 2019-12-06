from github import Github, GithubException
import getpass
import base64
import os
import shutil
import logging
import argparse

"""
METHODS
"""

def get_sha_for_tag(repository, tag):
    """
    Returns a commit PyGithub object for the specified repository and tag.
    """
    branches = repository.get_branches()
    matched_branches = [match for match in branches if match.name == tag]
    if matched_branches:
        return matched_branches[0].commit.sha

    tags = repository.get_tags()
    matched_tags = [match for match in tags if match.name == tag]
    if not matched_tags:
        raise ValueError('No Tag or Branch exists with that name')
    return matched_tags[0].commit.sha


def download_directory(repository, sha, server_path):
    """
    Download all contents at server_path with commit tag sha in
    the repository.
    """
    contents = repository.get_dir_contents(server_path, ref=sha)

    for content in contents:
        print("Processing %s" % content.path)
        if content.type == 'dir':
            os.makedirs(DL_DIR + content.path)
            download_directory(repository, sha, content.path)
        else:
            try:
                path = content.path
                file_content = repository.get_contents(path, ref=sha)
                file_data = base64.b64decode(file_content.content).decode('latin-1')
                file_out = open(DL_DIR + path, "w", encoding="latin-1")
                file_out.write(file_data)
                file_out.close()
            except (GithubException, IOError) as exc:
                logging.error('Error processing %s: %s', path, exc)

"""
CODE
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", required=True)
    parser.add_argument("-p", "--password", required=True)
    parser.add_argument("-o", "--organization_name", required=True)
    parser.add_argument("-r", "--repository_name", required=True)
    parser.add_argument("-b", "--branch_or_tag_to_download", required=True)
    parser.add_argument("-d", "--directory_to_download", required=True)
    args = parser.parse_args()
    # Assign Variables #
    username = args.username
    password = args.password
    organization_name = args.organization_name
    repository_name = args.repository_name
    branch_or_tag_to_download = args.branch_or_tag_to_download
    directory_to_download = args.directory_to_download
    # Preassign Variables
    github = Github(username, password)
    DL_DIR = organization_name + "/" + repository_name + "/"
    INIT_DIR = organization_name + "/" + repository_name + "/" + directory_to_download
    # Get Files #
    # Login credentials
    user = github.get_user()
    # Get organization (UiPath)
    # organization = github.get_user().get_orgs()[0] # assuming that user only has one organization
    organizations = github.get_user().get_orgs()
    for sample_organization in organizations:
        if sample_organization.name == organization_name:
            organization = sample_organization
            break
    # Choose repo
    repository = organization.get_repo(repository_name)
    # Choose branch
    sha = get_sha_for_tag(repository, branch_or_tag_to_download)
    # Choose directory
    # Download all files in directory
    if os.path.exists(INIT_DIR):
        # if directory already exists on local, delete
        shutil.rmtree(INIT_DIR)
    os.makedirs(INIT_DIR)
    download_directory(repository, sha, directory_to_download)

