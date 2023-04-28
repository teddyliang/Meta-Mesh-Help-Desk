# Meta Mesh Help Desk
*__Project Contributors:__ Ayoub Mansar, Ashwin Godura, Nicholas Clark, Sibhy Rajesh, Theodore Liang*

***
## Overviews
***

### Product Overview
Our Carnegie Mellon University student team successfully delivered a virtual help desk for our client [Meta Mesh](https://www.metamesh.org/). This is a full-fledged web application that allows end-users to ask questions, in natural English language, about technical issues that they may be facing. Our search engine will then dynamically return the best result available based on resources (links) that employees have already added to the database. Employees can add, edit, update, and delete resources at any time. Aside from these key features, our application also allows end-users to filter results by category, mark them as helpful, switch language, and more.

### Technical Overview
Our full-stack application runs on [Django](https://www.djangoproject.com/). For readability and extensibility, our search model is almost entirely decoupled from our Django implementation. It leverages the `nltk` and `sklearn` libraries. Our application is deployed on AWS EC2.

***
## User Handbook
***
### Resource management
Resources are the building blocks of what make up the search engine; each "resource" corresponds to a unique page. Similar to Google search, search results will show a URL for resource, but also other helpful metadata such as `blurb`, `title`, and `updated` (when the resource was last updated).
![Example result](https://i.imgur.com/Zuz8Zo6.png)

Employees can add new resources to the search engine by logging in to the Admin Panel and accessing the "Resources" section via the navigation bar.

Results are fetched dynamically, meaning a server reload is NOT required when adding new resources or updating/deleting existing ones.

**Filtering/sorting:** All tables in the Admin Panel include a "Filter & Sort" button to facilitate extracting information. For example, you can filter the resources table by specific categories or keywords.
![Resources filters](https://i.imgur.com/aCkzVVj.png) 

**Resource statistics:** In the "Resources" section of the Admin Panel, admins can view a list of resources in the database. One of the columns includes statistics about the resource. These include the number of times the resource has appeared in a search result, the number of times its URL was actually clicked, and the number of times a user marked it with a "thumbs-down". Resources that are marked with thumbs-down are less likely to be displayed to end-users.

### Categories
Each resource can optionally be associated with one or multiple categories. The primary benefit of categories is to give end-users more control over the results displayed to them. In the future, with potentially hundreds or thousands of resources stored in the system, it may be probable that a user's query may have a number of matching results. Users can utilize the category filter to narrow down the *number* of results or to improve the *quality* of them.

Categories can be added in a similar fashion to resources via the Admin Panel.

**Adding a new category:** Categories are dynamically fetched every time a user visits the search page, meaning a server reload is NOT necessary to update the list of category filters available. At this time, resources are not automatically tagged with a category, meaning for a newly-created category, employees will need to tag each relevant resource.

**Matching a resource to a category:** This process is the same for both new and existing resources. In the form, locate the category field box which should have a list of all categories in the system. While holding down the `CTRL` key, select or unselect the categories that you wish this resource to be associated with. It is permissible for a resource to have no categories.

**Category search:** End-users can apply a category filter when searching. This will restrict the result set to *only* results that include that category. For example:
```
Resource A belongs to category 1 & 2
Resource B belongs to only category 1
Resource C belongs to no categories
Resource D belongs to category 2
```
Assuming all resources "match" whatever the user has searched for, a search with no category filter will return all four resources. A search with a filter for category 1 will return resources `A` & `B`, and a filter for category 2 will only return resource `D`. Hence, it is advisable, if possible, to ensure that resources are always tagged to a category.

**Editing/Deleting categories:** Existing categories can be edited to reflect changes in name. Any resources tied to that category will automatically have any name changes reflected as well. While inadvisable, categories can be safely deleted in their entirety, which will automatically be reflected in any resources tied to that category. However, if a resource's only category was the deleted category, then this would lead the resource to be "category-less".

**Frequently asked questions:** The list of frequently asked questions on the homepage will dynamically change based on what category filter the user has selected.

### User management
All registered users in the system will have access to the Admin Panel and can thus manage resources, categories, etc. It is important to note, however, that each account has a `superuser` flag that determines if they have *full* administrative permissions. The default user account that we provided to you during handoff (username `bringtheweb`) has `superuser` permissions. The difference between a regular admin account and a `superuser` account is that `superuser` accounts may register new accounts, whereas regular accounts cannot. `superuser` accounts can also access the more technical Django administration backend (can be accessed by going to `http://<url>/admin`).

**Registering a new user using the admin panel:** The easiest way to create new users is through the Admin Panel. This can be done by clicking the "All Staff" button in the navigation bar.
> NOTE: You must be logged in to an account with `superuser` permissions to create new users. If you do not see the "All Staff" button in the navigation bar, then you cannot create new users.

From this page, you may then click the blue button labeled `Add new system user` which will allow you to go through the sign-up flow. You may provide any password as a default, and the user can then update that password for themselves later on.

**Elevating a user's account to `superuser` permissions:** As aforementioned, newly created accounts using the Admin Panel do NOT have `superuser` permissions. However, if you would like this account to have such permissions, navigate to `http://<url>/admin/auth/user/` and click on the corresponding user. Under the "Permissions" header, check the box that says "Superuser status".

**Adding a new superuser using the command line:** In some cases, it may be necessary to create a new account (with `superuser` permissions) from the command line, like when first deploying the app with a fresh database (no users in the system) or if access to the existing `superuser` account is lost. In this case, you may run the command: `python3 manage.py createsuperuser` from the `src` project directory and follow the relevant prompts. This assumes you are properly connected via SSH.

**Self-updating account data:** Users can update their account (email or password) by themselves using the Admin Panel. They may do this by clicking the "Account" tab in the navigation bar. Users can also update their account data, which for now is just a description. We anticipate that this field can be leveraged to store information about who this account belongs to or their role at Meta Mesh.

**Updating a user's password for them:** In some cases, a user may forget their password and may be unable to login. All passwords are always encrypted in the database, meaning a `superuser` cannot see what their password is, but a `superuser` can update their password for them. Navigate to `http://<url>/admin/auth/user/` and under the "Password:" header click the small text that says "this form".
![Password update](https://i.imgur.com/9vTd9ZN.png)

### Internationalization
End-users can elect to change the language of UI elements from English to Spanish. As discussed during our client meetings, searches using Spanish language is not currently supported and will still return resources in English language.

Admins can update translation strings in real-time through the Admin Panel. We are leveraging a library called [Rosetta](https://django-rosetta.readthedocs.io/) which allows translation strings to be easily updated using a UI. This eliminates the process of needing to SSH into the instance, run commands using the console, or recompile any of the translation strings.

By clicking on the "Rosetta" tab, two tables are listed for both English and Spanish with `Src` links. By clicking on the `Src` link, you will find a list of translation strings on the left-hand side and the language translation on the right-hand side.
![Spanish translation](https://i.imgur.com/B5jv7kW.png)

Of course, for the English language many of the translation strings are blank on the right-hand side since they are already in English and will default to the original. However, the `No results 2` string is important, which is discussed below.

![No results 2 string](https://i.imgur.com/we1xkpy.png)

When an end-user searches but receives no matching results, the `No results found` string is displayed as well as whatever the `No results 2` string is set to. This can be demonstrated using the image above and below:

![No results 2 demo](https://i.imgur.com/btwcGnm.png)

This allows employees to easily update in real-time the support phone number (or remove it entirely) without needing to bother with changing the underlying HTML.

***
## Process Information
This section of the `README` briefly concerns some of the ways we adhered to good software engineering processes while delivering this project.

Our team is utilizing Github both as our version control and for project management. We broke up our deliverables into 5 key [milestones](https://github.com/teddyliang/Meta-Mesh-Help-Desk/milestones). Each milestone has a comprehensive description that summarizes the work to be done and the use cases that are being covered.

### Testing & Continuous integration
**Testing:** We have made great strides to ensure that as much of the implemented functionality in our application is automatically tested. The repo contains the following tests:
- `test_auth.py`: Tests the login and sign-up flows
- `test_autocomplete.py`: Tests that the autocomplete works properly
- `test_internationalization.py`: Tests that switching language (English ⇔ Spanish) works correctly
- `test_keyword.py`: Tests the keywords functionality for resources
- `test_resource.py`: Tests creating and deleting resources
- `test_resource_stats.py`: Tests all three statistics for resources (appearances, thumbs-down, and clicks)
- `test_search.py`: Tests end-user search functionality for queries that both yield a result and no results, as well as searches with the category filter
- `test_urls.py`: Tests the URL resolver

These tests are great in that they are integration tests; for example, while we could have had `test_search.py` test the `WebpageSearcher` model in isolation (and fed the model some dummy resources), this test actually uses whatever resources are stored in the application/Django by making a `HTTP` call identical to ones that end-users would make (`<url>/search/?q=...`). This ensures that our tests comprehensively validate the entire end-to-end flow rather than isolating specific parts like the NLP model of the `WebpageSearcher`.

**CI:**
We run continuous integration tests for every commit and pull request. This increases our confidence in the code that we write, helps catch potential regressions and bugs, and ensures consistent style across our codebase. The CI automatically:
- Runs all tests in the `src/tests` folder
- Runs the `flake8` linter on the `helpdesk_app`, `helpdesk_proj`, and `SearchEngine` directories

*(these steps are configured in `.github/workflows/main.yml`)*

Commits that fail the CI are marked with a red ❌ and its pull requests cannot be merged.

### `Pipenv` and `.gitignore`
We are leveraging Pipenv as our packaging tool to handle dependency management. Initially, we relied upon a `requirements.txt` file but upgraded this; a list of dependencies that this project uses can be found in `Pipfile`.

To also ensure that our repo is free of autogenerated artifacts, our top-level `.gitignore` is comprehensive and ignores auto-generated Python files, virtual environments, `.DS_Store`, and much more.


### Pull Request Guidelines
As we worked on completing the open issues of this project, we followed the following guidelines:
- All commits or pull requests should follow the title convention of `[M#] X`, where `#` is the corresponding milestone number and `X` is a brief summary.
- All commits should be tied to a milestone using Github's tagging system.
- All commits should also be tied to an issue that describes the work that is being accomplished.
- Pull requests must be reviewed by at least 2 team members before being merged. Reviewers should leave comments looking out for best coding practices.
- Committed code should be devoid of dead-code, autogenerated files, print statements, etc.
- Committed code should have corresponding tests as much as possible.
- CI must be passing.

***
## Cloud Deployment Instructions
For installation & deployment guidelines to AWS, please refer to the `DEPLOYMENT.MD` file in the repo.

***
## Local Deployment Instructions
Prerequisites:
- `python3` should be installed. All other dependencies for running the web application are automatically installed using `pipenv`.

Instructions to install:
> NOTE: The `$` character indicates the start of a command and should not actually be included when running it 
- `$ git clone {ssh key}`
- `$ cd` into the `src` directory of the cloned folder
- `$ pip3 install pipenv` (if not already installed)
- `$ pipenv install`
- `$ pipenv shell`
- `$ python3 manage.py makemigrations`
- `$ python3 manage.py migrate`
- `$ python3 manage.py runserver`
- The output of the `runserver` command should contain a link to view the running application (most likely at http://127.0.0.1:8000/).

As mentioned in the User Handbook, you may create a new `superuser` account by running the command `$ python3 manage.py createsuperuser`.
