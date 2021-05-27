# github-py-webhook
Github -> ngrok -> Flask -> Github

A project to listen to incoming **Github** _Repositories_ webhooks and specifically target at repository creation events to:

* Create an open issue with
    * Issue title and body
    * Tag `good first issue` 
    * @mention `pandaedward`
* Automatically enable protected-branch on default branch

## Core packages used

1. ngrok
    * Allows a web server running in local machine to be exposed to the internet without needing a public URL. More information about `ngrok` [HERE](https://ngrok.com/docs)
    * An `ngrok` account and some set up are required. I will discuss more later
    * In a high level we start up `ngrok` before everything else and configure GitHub to invoke `ngrok` provided URL back up by our `Flask` web server
2. Github (obviously)
    * A GitHub account (free to create), a GitHub organization (free to create) 
    * [Protected branches](https://docs.github.com/en/rest/reference/repos#get-branch-protection) are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server
    * If the organization is **NOT** in one of the paid-for plan, create the repository as **Public** in the testing step
3. Flask - Python
    * `flask` version 1.1.2 is in use. Please check `requirements.txt` file
    * In a high level Flask sets up a Python web server to listen to incoming `POST` requests forwarded by `ngrok`
4. Pygithub - Python
    * `pygithub` version 1.54.1 is in use. Please check `requirements.txt` file
    * The official GitHub python library enables interaction with GitHub API v3
    
## Step by step set up guide
1. Create a `ngrok` account, download the executable command and set up auth token like below
    * `$ ./ngrok authtoken YOUR_NGROK_AUTH_TOKEN`
    * Start `ngrok` by `$ ./ngrok http 5000` and leave the terminal window **running**
    * Make note and copy the command output http url, it looks something like `http://23e5ab11586f.ngrok.io/` 
    * Port 5000 is python `flask` default listening port. `ngrok` needs to forward traffic to `flask` listening port
    * For detail please find official [ngrok setup guide](https://dashboard.ngrok.com/get-started/setup)  
    * Strictly development only as we are using http. For production please configure https for secure access
2. Log on to GitHub and create an organization. Go to the organization's Settings - Webhooks - Add webhook
    * I won't go in details about how to do this step. Please find office GitHub documentation [Creating webhooks](https://docs.github.com/en/developers/webhooks-and-events/webhooks/creating-webhooks)
    * Paste the `ngrok` http url to **Payload URL** field during creating a webhook. Add suffix `/payload` to the url. Make it looks something like `http://23e5ab11586f.ngrok.io/payload`
    * Set Content type to `application/json`
    * Choose individual events to trigger the Github webhook. I pick `Repositories` event to limit the webhook call.
    * Your configuration except **Payload URL** should look like ![image](https://user-images.githubusercontent.com/17075586/119789787-7a373400-bf27-11eb-831e-88a23d2c9afa.png)
    * GitHub will now make webhook call to the Payload URL everytime an repository event occurred in the organization.
3. Continue on GitHub, generate a `Personal Access Token`. Official GitHub documentation [HERE](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token)
    * The scope must have read/write access to repository to add issue to, as well as `write discussion`
    * Ensure `repo` and `write:discussion` scopes are checked:
    * ![image](https://user-images.githubusercontent.com/17075586/119794106-57a71a00-bf2b-11eb-9f84-9def5b348ee5.png)
    * Copy the `Personal Access Token` once it is generated. We will use it later to set an environment variable
4. Clone this repository and `$ cd` to the directory
    * The stack is tested with Python version `3.6` 
    * Ensure all Python dependencies are installed with command `$ pip3 install requirements.txt`
    * Use the `Personal Access Token` generated above to set an OS or project level environment variable key: `GITHUB_PAT` value: `_PERSONAL_ACCESS_TOKEN_`
    * Start the server with command `$ python3 server.py`. Leave the terminal window **running**
    * If `Flask` web server is started successfully it will be reachable via `http://127.0.0.1:5000`. Test the URL to ensure a `200` success code is observed.
    * Also test browsing to your `ngrok` public url `http://NGROK_UUID.ngrok.io/` to make sure a `200` success code is there. We know `ngrok` tunnel forwarding to our local `flask` server on port 5000 is working smoothly.
## Run the test
1. On GitHub, navigate to the organization and click on `New` to create an repository
2. Give the repository a name and choose `Public` to create it as a public repository, _protected branch_ is supported only with one of the paid-for plans for the GitHub organization. Also check one of `Add a README file` or `Add .gitignore` boxes to set a default branch in which our `Python` script will automatically enable protection upon.
3. Hit `Create repository` button and GitHub will fire a webhook to `ngrok` url which will be forwarded to our `flask` web server. Check back on `Python` terminal window for console logs.
4. Navigate to the newly created repository and make sure issue is created and default branch is protected

## 

    
    

    

    
    
