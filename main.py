from flask import abort, Flask
from git import Git
from git import Repo
from docker import Client
from subprocess import call

import os

app = Flask(__name__)

@app.route("/<token>/<commit>")
def main(token, commit):

  if token != os.getenv("TOKEN"):
    abort(401)  

  working_copy = "/repository/checkout"
  if not os.path.isdir(working_copy):
    os.mkdir(working_copy)
    Git().clone(os.getenv("GIT_REPOSITORY_URL"), working_copy)

  print "Refreshing git repository"
  repo = Repo(working_copy)
  origin = repo.remotes.origin
  origin.pull();
  repo.git.reset(commit, hard=True)  
  
  print "Building docker image"
  docker = Client(base_url='unix://mount/run/docker.sock')
  docker.login(username=os.getenv("DOCKER_REGISTRY_USERNAME"), password=os.getenv("DOCKER_REGISTRY_PASSWORD"), email=os.getenv("DOCKER_REGISTRY_EMAIL", "foo@bar.fr"))
  docker.build(path=working_copy)  

  print "Pushing docker image"
  res = docker.push('artquid/artquid')

  print "Listing docker image"
  check_call(["maestro", "-f", "/repository/checkout/demo.yaml", "restart", os.getenv("CONTAINER"), "-f"])

  return "OK"

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
