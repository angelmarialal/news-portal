# Cloud-Based News Portal Using AWS & DevOps

A cloud-based news portal developed using Flask, MySQL, Docker, GitHub, bcrypt, and AWS EC2. The application allows users to register, log in, add news posts, edit/delete posts, and search news articles.


## Features

- User Registration and Login
- Secure Password Hashing using bcrypt
- Add News Posts
- Edit News Posts
- Delete News Posts
- Search Functionality
- MySQL Database Integration
- AWS EC2 Deployment
- Docker Support
- GitHub Version Control


## Technologies Used

- Python
- Flask
- HTML
- CSS
- MySQL
- Docker
- GitHub
- AWS EC2
- bcrypt


## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/news-portal.git
```

### Move to Project Folder

```bash
cd news-portal
```

### Install Required Packages

```bash
pip install -r requirements.txt
```

### Run Flask Application

```bash
python3 app.py
```

## Docker Configuration

### Build Docker Image

```bash
docker build -t newsportal .
```

### Run Docker Container

```bash
docker run -p 5000:5000 newsportal
```


## AWS EC2 Deployment

The application is deployed on AWS EC2 Ubuntu server.

### Run Application in Background

```bash
nohup python3 app.py &
```

## Live Website

http://3.111.217.73:5000


## GitHub Repository

https://github.com/angelmarialal/news-portal.git


## Database

Database Name:

```sql
news_portal


## Workflow

Homepage → Register → Login → Add Post → Edit/Delete Post → Logout


## Security Features

- Password hashing using bcrypt
- Session management
- Input validation
- SQL Injection Prevention

## Author

ANGEL MARIYA LAL
Marian College Kuttikkanam Autonomous
