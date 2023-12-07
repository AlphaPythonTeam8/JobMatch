# JobMatch

## Table of Contents
- [Introduction](#introduction)
- [The Team Behind JobMatch](#the-team-behind-jobmatch)
- [Getting Started](#getting-started)
- [Installation & Setup](#installation--setup)
- [Environment Configuration](#environment-configuration)
- [Email Service Configuration with MailTrap](#email-service-configuration-with-mailtrap)
- [Admin Account Creation with Special Registration Code](#admin-account-creation-with-special-registration-code)
- [Functionality](#functionality)
- [Database Structure Overview](#database-structure-overview)
- [Security First](#security-first)
- [Room for Growth](#room-for-growth)
- [Technologies](#technologies)

## Introduction
JobMatch is a platform that connects you instantly to a world of opportunities, tailored to your skills and ambitions. It's where your professional journey accelerates, powered by technology that understands your potential and pairs it with the market's demands.

## The Team Behind JobMatch
Our core trio of tech enthusiasts includes:
- **Alex Dimova** 
- **Angel Marinov** 
- **Mario Stanoychev** 

## Getting Started
This guide will walk you through the basic steps to get JobMatch up and running on your local machine for development and testing purposes.

## Installation & Setup

Follow these steps to set up JobMatch on your local machine:

1. **Clone the Project Repository:**

```
git clone https://github.com/AlphaPythonTeam8/JobMatch.git
```
2. **Install Required Packages:**
Navigate to the cloned directory and run:

```
pip install -r requirements. txt
```



3. **💾 Environment Configuration**

To run JobMatch, you will need to set up your environment variables. These are crucial for connecting to the database, securing your application, and setting authentication parameters. Below is a breakdown of the `.env` file contents:

- `JOB_MATCH_DB_HOST`: The address of your database server. For Azure-hosted MariaDB, it might look like `jobmatchserver.mariadb.database.azure.com`.

- `JOB_MATCH_DB_NAME`: The name of your specific database in MariaDB, such as `jobmatch`.

- `JOB_MATCH_DB_USER`: Your database username with necessary permissions, something like `alphateam8@jobmatchserver`.

- `JOB_MATCH_DB_PASSWORD`: The password for your database user. It should be unique and not publicly disclosed.

- `JWT_SECRET_KEY`: The key used to sign and verify JWT tokens. This must be a long, random, and unique string.

- `MAILTRAP_USERNAME`: Your MailTrap username for email testing and sandboxing.

- `MAILTRAP_PASSWORD`: The corresponding password for your MailTrap account.

- `API_KEY`: Specific API key provided by MailTrap or other services that require it.

- `ADMIN_REGISTRATION_CODE`: A secure code used during the admin registration process. This code should be kept confidential.

##  Email Service Configuration with MailTrap
<img src="https://mailtrap.io/wp-content/uploads/2023/04/email-api-hero.svg" alt="MailTrap Logo" width="300"/>


JobMatch uses MailTrap to simulate email sending in a safe and sandboxed environment, which is particularly useful during the development and testing phases. With MailTrap, we can ensure that the email verification process is fully operational before deploying to production.

### Setting Up MailTrap for Email Verification

1. Go to [MailTrap](https://mailtrap.io/) and sign up for an account.
2. Navigate to your inbox settings after registration.
3. Copy the API Key, Username, and Password from the SMTP settings section.
4. Use these credentials in your `.env` file to configure the email service in JobMatch.

### How MailTrap is Used for Email Verification

When a new user registers on JobMatch, they are required to verify their email address to activate their account. Here's how the process works:

- A unique verification token is generated for the user and stored in the database.
- JobMatch constructs a verification email containing a link with the token as a parameter.
- The email is sent through MailTrap's fake SMTP server to the user's email address, but instead of reaching an actual mailbox, it's caught within MailTrap's testing environment.
- The user clicks on the verification link, which leads them back to JobMatch, where we check the token's validity.
- If the token matches, we mark the user's email as verified in the database.

This process ensures that our user verification flow works correctly without sending actual emails to real users' inboxes.


## Features

### Public Section
🌐 The public section of the application is accessible without authentication.
- Users must register, verify their email, and log in to access private endpoints.

### Private Section
🔒 The private section is accessible only to authenticated users. JobMatch caters to three user types: company, professional, and admin.

#### Company Features
- 🏢 **View and Update Information:** Companies can manage their profiles.
- 📋 **Ad Management:** Create, edit, and delete job ads.
- 📊 **Ad Listings:** View a comprehensive list of all ads.
- 🔍 **Search for Professionals:** Find professionals by username.
- 🌐 **Company Ad Search:** Search for ads with filters like location.
- 🤝 **Match Requests:** Send and process requests to professionals or company ads.

#### Professional Features
- 🙍‍♂️ **Profile Management:** Professionals can edit and update their profiles.
- 📝 **Ad Creation and Editing:** Manage company ads.
- 📈 **Ad Interaction:** View specific ads and their match requests.
- 🔎 **Job Search:** Find companies by username and search for job ads with salary range filters.
- 💌 **Match Requests:** Send and manage match requests to companies or job ads.
- 📬 **Request Overview:** View all sent or received match requests.

#### Admin Features
- 🚫 **User Management:** Block or unblock company or professional profiles.
- 🗑️ **Content Control:** Delete job or company ads as needed.

## 🔐 Admin Account Creation with Special Registration Code

Creating an admin account on JobMatch is a secure process that requires a special registration code, ensuring that only authorized individuals can gain administrative access. Here's how it works:

### Admin Registration Process

1. An admin initiates the registration process by providing a `username`, `password`, and the `ADMIN_REGISTRATION_CODE`.
2. The backend service verifies that the provided registration code matches the one stored in the environment variables, which is known only to existing administrators or the system installer.
3. If the registration code is valid, the password is hashed using reliable cryptographic hashing algorithms for secure storage in the database.
4. A new admin record is created with the hashed password and stored in the `Admin` table of the JobMatch database.

## ⚒️ Functionality
JobMatch's functionality is just the tip of the iceberg. We have designed a system with the potential to expand, envisioning features like live notifications and real-time updates that could redefine professional networking.

## 🗺️ Database Structure Overview

JobMatch's database is a carefully architected warehouse of data tables designed to ensure robust and seamless interactions between different elements of the platform. Here's a glimpse into our structure:

![JobMatch Database Schema](https://github.com/AlphaPythonTeam8/JobMatch/blob/main/schema.png?raw=true)

| Table Name    | Description |
|---------------|-------------|
| **Admin**     | Stores data related to the platform's administrators, including credentials and permissions for overseeing the JobMatch ecosystem. |
| **Professional** | Captures professional details, qualifications, and status, pivotal in the matching process. |
| **Company**   | Holds information about companies seeking talent, including company details, contact info, and verification status. |
| **JobAd**     | Contains job advertisements created by companies, with details like salary ranges, job descriptions, and ad status. |
| **CompanyAd** | Similar to JobAd, but tailored for internal postings within companies. |
| **Skill & CompanyAdSkill** | Maintain a list of skills essential for matching professionals with suitable job ads, forming the backbone of the matching algorithm. |
| **MatchRequests** | Logs interactions where professionals express interest in job ads or companies show interest in professionals. |
| **Notification** | Manages notifications for various actions and updates on the platform, keeping users informed. (to be further implemented) |
| **JobAdSkill & JobAdInteraction** | Facilitate the many-to-many relationships between job ads and required skills, including professional interactions with these ads. |
| **AuditLog** | Tracks actions taken by users to maintain the integrity and security of the platform, providing a transparent audit trail. (to be further implemented) |

Our database schema is designed with scalability in mind, allowing us to introduce additional features such as live notifications, real-time updates, and more complex matching algorithms as we grow. We've built a foundation that's not only secure and comprehensive but also adaptable to the ever-changing landscape of the job market.


---

As we continue to evolve, our database will expand to support new features that will make JobMatch even more powerful. We're excited about the future, and we invite you to join us on this journey.


## 🔐 Security First
We take security seriously. That's why we've built JobMatch on a foundation of JWT tokens for authentication. Each token is a promise of a secure session, with SQLAlchemy as our gatekeeper, ensuring that every database transaction is performed with the utmost integrity.

## 🔬 Room for Growth
We are excited about the room we've built into JobMatch for new features. Our codebase is a canvas, ready for innovations like live notifications, which could bring an immediacy and dynamism to the job matching experience.

### FastAPI

JobMatch leverages the power of [FastAPI](https://fastapi.tiangolo.com/), a modern, fast (high-performance) web framework for building APIs with Python. FastAPI provides automatic interactive API documentation, easy serialization, and asynchronous request handling, making it an ideal choice for our backend architecture.

For more information on how FastAPI powers JobMatch, check out the [official FastAPI documentation](https://fastapi.tiangolo.com/).

  
### Technologies
<div align="left">
	<code><img width="30" src="https://user-images.githubusercontent.com/25181517/183423507-c056a6f9-1ba8-4312-a350-19bcbc5a8697.png" alt="Python" title="Python"/></code>
    <code><img width="30" src="https://user-images.githubusercontent.com/25181517/192107854-765620d7-f909-4953-a6da-36e1ef69eea6.png" alt="HTTP" title="HTTP"/></code>
	<code><img width="30" src="https://user-images.githubusercontent.com/25181517/192158954-f88b5814-d510-4564-b285-dff7d6400dad.png" alt="HTML" title="HTML"/></code>
	<code><img width="30" src="https://user-images.githubusercontent.com/25181517/183898674-75a4a1b1-f960-4ea9-abcb-637170a00a75.png" alt="CSS" title="CSS"/></code>
	<code><img width="30" src="https://user-images.githubusercontent.com/25181517/117447155-6a868a00-af3d-11eb-9cfe-245df15c9f3f.png" alt="JavaScript" title="JavaScript"/></code>
	<code><img width="30" src="https://github.com/marwin1991/profile-technology-icons/assets/136815194/3c698a4f-84e4-4849-a900-476b14311634" alt="MariaDB" title="MariaDB"/></code>
	<code><img width="30" src="https://pbs.twimg.com/profile_images/476392134489014273/q5uAkmy7_400x400.png" title="SQLAlchemy"/></code>
  	<code><img width="30" src="https://cdn.worldvectorlogo.com/logos/fastapi.svg" title="FastAPI"/></code>
</div>



⭐ Star us on GitHub — it helps!

[JobMatch Footer](#) | © 2023 JobMatch Team