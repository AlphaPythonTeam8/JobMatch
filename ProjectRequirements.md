
# **Job Match**

# Find best colleagues to work with

# Project Description

Professionals and companies are looking for their best new colleagues. An application that can match them would be great.

The application has two main parts:

**Employer Part** – the companies can create job ads.

**Professionals Part** – Individuals create a "company ads" - to show what they can do (qualifications) and what they want and search for.

# Functional Requirements

## Public Part

The public part must be accessible without authentication.

**Login endpoints (for both employers and professionals)** (must)– required to access the private endpoints of the application.Login requires **username** and **password**.

**Register endpoints (for both employers and professionals)** (must)–

- Requires **username** , **first name** , **last name** , and **password (professionals)**
- Requires **username, company name and password (companies)**

## Private part

Accessible only if the user is authenticated.

For **Companies:** (any of the below can be either a different endpoint, or combined)

- There must be a way to view and edit the **Company info**
- There mustbe a way to view all company's active **Job ads**
- There mustbe a way to view all company's archived (that are matched) **Job ads**
- There mustbe a way to create a **Job ad**
- There mustbe a way to view and edit details for a **Job ad**
- There mustbe a way to search in **Company ads**

For **Professionals:**

- There must be a way to view and edit the own **Professional info**.
- There mustbe a way to view all own **Company ads** (more than one are possible)
- There should be a way to set up a "main" ad.
- There must a way to create, view and edit a **Company ad**.
- There must be a way to search in **Job ads.**

### Company Info

- Description
- Location ( **city** )
- Contacts
- Picture/logo - (should)
- Currently active number of Job ads
- Number of successful matches so far

### Professional Info

- Brief summary
- Location ( **city** )
- Status
  - **Active** – the only status that allows active Company ads
  - **Busy** – all Company ads must be hidden or private
- Picture/photo – (should)
- Currently **active** number of Company ads
- List of matches (must) – could be visible or hidden (should)

### Job ads

Only companies can create Job ads.

- Salary range
- Job description
- Location (city **or** remote **or** both)
- Status
  - **Active** – visible
  - **Archived** – matched with professional and no longer active
- Set of requirements
  - Preset collection of requirements
  - **Or** ability to add requirements – should
  - **Or** ability to add requirements that need to be approved – could
  - Requirement levels – should
- List of match requests – visible to the creator only
- Functionality to **match** a request
  - The ad is Archived
  - The professional is set on Busy

### Company ads

Only professionals can create Company ads.

- Salary range
- Short motivation/description
- Location (city or full remote or both office and remote)
- Status
  - **Active** – the ad is visible in searches
  - **Hidden** – the ad is not visible for anyone but the creator
  - **Private** – the ad can be viewed by id, but do not appear in searchesshould
  - **Matched** – when is matched by a company
- Skillset
  - Preset collection of skills
  - Or ability to add skills – should
  - Or ability to add skills that need to be approved - could
  - Skill level – should
- List of match requests – visible to the creator only
- Functionality to match a request
  - The ad status is set to Matched
  - The professional is set on Busy

### Searching

Both companies and professionals can initiate search

- Companies can search for company ads (must)
- Companies can search for professionals (should)
- Companies can search for other companies (could)
- Professionals can search for job ads (must)
- Professionals can search for companies (should)
- Professionals can search for other professionals (could)
- Search threshold can be set (should) – a way to accept results that are not an exact match.
- Salary range search range (must)
  - Search threshold – percent of ads range increase (should)
- List of Skills/Requirements (must)
  - Search threshold – number of skills that may be missing from the ads (should)
- Location (must)
- Returns a result where **all conditions are met** :
- There is intersection between the salary search range and the ad range
  - Threshold application: the range of all ads is extended by the given percent symmetrically – min salary is lowered, and maximum salary is increased
    - Example: Threshold 20% - ad range 1000 – 1200 becomes 980 – 1220 for the search i.e., this ad will match search range 900 - 990
- All skills from the search list are in the list of skills/requirements in the ads
  - Any combination of (n – t) skills in the search is present in the ad, where **n** is the number of skills in the search and **t** is the threshold
- Location matches the city and all full remote ads

### Matching

Both companies and professionals can initiate match request.

- Companies can match more than one company ads (must)
- Professionals can match a job ad (must)

## Administration

Optionally, create application administration functionality (could)

- Admins approve companies' and professionals' registration
- Admins can block/unblock companies and professionals
- Admins can delete application data (profiles, ads etc.)
- Admins can add/delete or approve skills/requirements

## Third-Party Service

- Integrate with [https://dev.mailjet.com/email/guides/send-api-v31/](https://dev.mailjet.com/email/guides/send-api-v31/) for email notifications (should)
  - Notification for a matching request (should)
  - Notification for ads (could)
- Integrate with [Twitter API Documentation | Docs | Twitter Developer Platform](https://developer.twitter.com/en/docs/twitter-api) for sending tweets on ad creation (do not use personal account!) (should)
- Mock third-party service for salary ranges or new skills/requirements – your app will make requests to the mock service to acquire information and then use it to make range suggestions or update the skill pool with new (trending) entries. (could)
  - [Create mock APIs in seconds with Mockoon](https://mockoon.com/)
  - [Setting up mock servers | Postman Learning Center](https://learning.postman.com/docs/designing-and-developing-your-api/mocking-data/setting-up-mock/)

## REST API

Provide a RESTful API that supports the full functionality of the system. (must)

# Technical Requirements

## General

- Follow [KISS](https://en.wikipedia.org/wiki/KISS_principle), [SOLID](https://en.wikipedia.org/wiki/SOLID), [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) principles when coding
- Follow REST API design [best practices](https://blog.florimondmanca.com/restful-api-design-13-best-practices-to-make-your-users-happy) when designing the REST API (see Appendix)
- Use tiered project structure (separate the application in layers)
- The service layer (i.e., "business" functionality) must be unit tested
- You should implement proper exception handling and propagation
- Try to think ahead. When developing something, think – "How hard would it be to change/modify this later?"

## Database

The data of the application must be stored in a relational database. You need to identify the core domain objects and model their relationships accordingly. Database structure should avoid data duplication and empty data (normalize your database).

Your repository must include two scripts – one to create the database and one to fill it with data.

## Git

Commits in the GitLab repository should give a good overview of how the project was developed, which features were created first and the people who contributed. Contributions from all team members must be evident through the git commit history! The repository must contain the complete application source code and any scripts (database scripts, for example).

Provide a link to a GitLab repository with the following information in the README.md file:

  - Project description
  - Link to the Swagger documentation (must)
  - Link to the hosted project (if hosted online)
  - Instructions on how to set up and run the project locally
  - Images of the database relations (must)

## Optional Requirements

Besides all requirements marked as should and could, here are some more _optional_ requirements:

- Integrate your project with a Continuous Integration server (e.g., GitLab's own) and configure your unit tests to run on each commit to your master branch
- Host your application's backend in a public hosting provider of your choice (e.g., AWS, Azure)
- Use branches while working with Git

# Teamwork Guidelines

Please see the Teamwork Guidelines document.

# Appendix

  - [Guidelines for designing good REST API](https://blog.florimondmanca.com/restful-api-design-13-best-practices-to-make-your-users-happy)
  - [Guidelines for URL encoding](http://www.talisman.org/~erlkonig/misc/lunatech%5Ewhat-every-webdev-must-know-about-url-encoding/)
  - [Git commits - an effective style guide](https://dev.to/pavlosisaris/git-commits-an-effective-style-guide-2kkn)

# Legend

- Must– Implement these first.
- Should – if you have time left, try to implement these.
- Could – only if you are ready with everything else give these a go.