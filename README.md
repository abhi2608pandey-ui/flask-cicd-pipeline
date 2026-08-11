Absolutely. Below is a complete README-ready step-by-step guide based on everything you actually built. You can copy this directly into README.md.

# Flask Student Registration — CI/CD Pipeline

A Flask-based Student Registration application with a complete CI/CD pipeline using:

- Python / Flask
- Pytest
- Docker
- GitHub
- GitHub Actions
- AWS ECR
- AWS EC2
- IAM
- SSH
- Automated deployment and health checks

---

## Architecture

```text
Developer
    |
    | git push
    v
GitHub Repository
    |
    v
GitHub Actions
    |
    +----> Run Pytest
    |
    +----> Build Docker Image
    |
    +----> Push Image to Amazon ECR
    |
    +----> SSH into EC2
               |
               +----> Login to ECR
               +----> Pull latest image
               +----> Stop old container
               +----> Start new container
               +----> Health Check
                       |
                       v
                 Flask Application
                       |
                    Port 5000
1. Project Structure
CICD Pipeline Project/
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── templates/
│   ├── add_student.html
│   ├── base.html
│   ├── index.html
│   └── update_student.html
│
├── tests/
│   └── test_app.py
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── app.py
├── pytest.ini
├── requirements.txt
└── README.md
2. Create the Flask Application

Create the Flask application in:

app.py

The application provides the Student Registration functionality and includes a health endpoint:

/health

The health endpoint returns:

{
  "service": "student-registration",
  "status": "healthy"
}
3. Create Python Requirements

Create:

requirements.txt

Include the required Flask, MongoDB and testing dependencies.

Install dependencies locally:

pip install -r requirements.txt
4. Create Automated Tests

Tests are stored in:

tests/test_app.py

Configure pytest using:

pytest.ini

Run the tests:

pytest

Expected result:

7 passed

The tests were successfully verified locally before creating the CI/CD pipeline.

5. Create Dockerfile

Create a Dockerfile to containerize the Flask application.

The container runs:

python app.py

The application listens on:

5000
6. Build Docker Image Locally

Build the Docker image:

docker build -t student-registration:test .

Verify the image:

docker images
7. Run Docker Container Locally

Run:

docker run -d --name student-registration-test -p 5000:5000 student-registration:test

Verify:

docker ps

Test the health endpoint:

curl http://localhost:5000/health

Expected:

{
  "service": "student-registration",
  "status": "healthy"
}

Stop the test container:

docker stop student-registration-test
8. Initialize Git Repository

Initialize Git:

git init

Check the repository:

git status

Add project files:

git add .

Create the first commit:

git commit -m "Initial Flask CI/CD project"
9. Create GitHub Repository

Create a GitHub repository for the project.

Add the remote:

git remote add origin https://github.com/<USERNAME>/flask-cicd-pipeline.git

Rename the branch:

git branch -M main

Push the project:

git push -u origin main
10. Create GitHub Actions Workflow

Create:

.github/workflows/ci-cd.yml

The initial workflow performs:

Checkout source code
Set up Python
Install dependencies
Run pytest
Build Docker image

Commit the workflow:

git add .github/workflows/ci-cd.yml
git commit -m "Add GitHub Actions test pipeline"
git push

Verify the workflow under:

GitHub → Actions

The workflow should show green/successful execution.

11. Create AWS ECR Repository

Create an Amazon ECR repository:

student-registration

Region used:

us-east-1

The ECR repository stores the Docker images created by GitHub Actions.

12. Create AWS IAM User for GitHub Actions

Create an IAM user specifically for GitHub Actions.

The user needs permission to:

Authenticate to ECR
Push Docker images
Upload image layers
Manage ECR image metadata

The required ECR permissions include:

ecr:GetAuthorizationToken
ecr:BatchCheckLayerAvailability
ecr:CompleteLayerUpload
ecr:InitiateLayerUpload
ecr:PutImage
ecr:UploadLayerPart

Store the AWS credentials securely in GitHub Secrets.

13. Add GitHub Repository Secrets

Go to:

GitHub Repository
→ Settings
→ Secrets and variables
→ Actions
→ New repository secret

Create:

AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION

Example:

AWS_REGION=us-east-1

Never put AWS credentials directly into the workflow file.

14. Add ECR Build and Push Stage

Update:

.github/workflows/ci-cd.yml

The workflow logs into ECR, builds the Docker image and pushes it.

The image is tagged using:

${{ github.sha }}

This gives every Git commit its own Docker image tag.

Example:

232c34598d2271cd30ffa8ab2a9971f6691835f0

The image is pushed to:

845041271182.dkr.ecr.us-east-1.amazonaws.com/student-registration

Commit and push:

git add .github/workflows/ci-cd.yml
git commit -m "Add ECR image push stage"
git push

Verify the GitHub Actions workflow is green.

15. Create Amazon EC2 Instance

Create an EC2 instance using:

Amazon Linux 2023

Connect to the instance using SSH.

Verify the operating system:

cat /etc/os-release
16. Install and Start Docker on EC2

Install Docker if required.

Verify Docker:

docker --version

Start Docker:

sudo systemctl start docker

Enable Docker:

sudo systemctl enable docker

Verify:

sudo systemctl status docker --no-pager

Add the EC2 user to the Docker group if required:

sudo usermod -aG docker ec2-user

Reconnect to the EC2 instance after changing group membership.

Verify:

docker ps
17. Create EC2 IAM Role

Create an IAM role for the EC2 instance:

student-registration-ec2-ecr-role

Attach ECR read permissions to this role.

The role allows EC2 to:

Authenticate to ECR
Pull Docker images

Attach the role to the EC2 instance.

18. Verify EC2 IAM Role

On EC2:

aws sts get-caller-identity

Expected output contains:

assumed-role/student-registration-ec2-ecr-role

This confirms EC2 is using the IAM role.

19. Authenticate EC2 with ECR

On EC2:

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 845041271182.dkr.ecr.us-east-1.amazonaws.com

Expected:

Login Succeeded
20. Verify ECR Images

Check available images:

aws ecr describe-images \
  --repository-name student-registration \
  --region us-east-1

The output shows the Docker image tag generated from the Git commit SHA.

21. Manually Pull ECR Image on EC2

Example:

docker pull 845041271182.dkr.ecr.us-east-1.amazonaws.com/student-registration:<IMAGE_TAG>

Verify:

docker images
22. Run Application Container on EC2

Run:

docker run -d \
  --name student-registration \
  -p 5000:5000 \
  845041271182.dkr.ecr.us-east-1.amazonaws.com/student-registration:<IMAGE_TAG>

Verify:

docker ps

Expected:

0.0.0.0:5000->5000/tcp
23. Test Application Inside EC2

Run:

curl http://localhost:5000/health

Expected:

{
  "service": "student-registration",
  "status": "healthy"
}
24. Configure EC2 Security Group

Allow inbound traffic for the application port:

TCP 5000

For production environments, restrict the source IP/range appropriately instead of allowing unrestricted access.

25. Test Application Publicly

Find the EC2 public IPv4 address.

Example:

http://<EC2_PUBLIC_IP>:5000/health

Test from Windows:

curl http://<EC2_PUBLIC_IP>:5000/health

Expected HTTP status:

200 OK

Expected response:

{
  "service": "student-registration",
  "status": "healthy"
}
26. Create Dedicated SSH Deployment Key

Generate an Ed25519 key pair locally:

ssh-keygen -t ed25519 -C "github-actions-deploy"

Created files:

github-actions-deploy
github-actions-deploy.pub

Important:

github-actions-deploy
        ↓
PRIVATE KEY — KEEP SECRET

github-actions-deploy.pub
        ↓
PUBLIC KEY
27. Add Public SSH Key to EC2

On EC2:

mkdir -p ~/.ssh
nano ~/.ssh/authorized_keys

Add the contents of:

github-actions-deploy.pub

Do not delete existing authorized keys.

Set permissions:

chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
28. Test SSH Deployment Key

From Windows:

ssh -i "D:\CICD Pipeline Project\github-actions-deploy" ec2-user@<EC2_PUBLIC_IP>

Successful login confirms the deployment key works.

29. Protect SSH Keys with .gitignore

Add:

github-actions-deploy
github-actions-deploy.pub

to:

.gitignore

Verify:

git status

The SSH key files must not appear as untracked files.

30. Add EC2 Deployment Secrets to GitHub

Go to:

GitHub
→ Settings
→ Secrets and variables
→ Actions

Add:

EC2_SSH_PRIVATE_KEY
EC2_HOST
EC2_USER

Values:

EC2_SSH_PRIVATE_KEY = contents of github-actions-deploy
EC2_HOST = EC2 public IP
EC2_USER = ec2-user

Never commit the private key to Git.

31. Add Automated EC2 Deployment to GitHub Actions

Add the deployment stage after the ECR push:

- name: Deploy to EC2
  uses: appleboy/ssh-action@v1.2.2
  with:
    host: ${{ secrets.EC2_HOST }}
    username: ${{ secrets.EC2_USER }}
    key: ${{ secrets.EC2_SSH_PRIVATE_KEY }}
    script: |
      aws ecr get-login-password --region ${{ secrets.AWS_REGION }} | docker login --username AWS --password-stdin ${{ steps.login-ecr.outputs.registry }}

      docker pull ${{ steps.login-ecr.outputs.registry }}/${{ env.ECR_REPOSITORY }}:${{ github.sha }}

      docker stop student-registration || true
      docker rm student-registration || true

      docker run -d \
        --name student-registration \
        -p 5000:5000 \
        ${{ steps.login-ecr.outputs.registry }}/${{ env.ECR_REPOSITORY }}:${{ github.sha }}

      sleep 5

      curl --fail http://localhost:5000/health
32. Validate Workflow YAML

Install PyYAML if required:

pip install pyyaml

Validate the workflow:

python -c "import yaml; yaml.safe_load(open('.github/workflows/ci-cd.yml')); print('YAML syntax OK')"

Expected:

YAML syntax OK
33. Commit EC2 Deployment Workflow
git add .github/workflows/ci-cd.yml
git commit -m "Add EC2 deployment stage"

Then protect the SSH keys:

git add .gitignore
git commit -m "Ignore deployment SSH keys"

Push:

git push
34. Verify GitHub Actions

Go to:

GitHub → Actions

The workflow should execute:

Tests
   ↓
Docker Build
   ↓
ECR Push
   ↓
EC2 Deployment
   ↓
Health Check

All stages should be green.

35. Verify Deployment on EC2

On EC2:

docker ps

Verify the container:

student-registration

Verify the port:

0.0.0.0:5000->5000/tcp

Then:

curl http://localhost:5000/health

Expected:

{
  "service": "student-registration",
  "status": "healthy"
}
36. Final End-to-End Test

Make a small application change.

Then:

git add .
git commit -m "Update application version"
git push

GitHub Actions automatically:

Runs tests
     ↓
Builds Docker image
     ↓
Pushes image to ECR
     ↓
Connects to EC2
     ↓
Pulls new image
     ↓
Stops old container
     ↓
Starts new container
     ↓
Runs health check

If GitHub Actions is green and the EC2 health check succeeds, the automated deployment is working.

37. Final Result

The completed CI/CD pipeline provides:

Component	Purpose
Flask	Web application
Pytest	Automated testing
Docker	Application containerization
GitHub	Source code management
GitHub Actions	CI/CD automation
AWS IAM	Secure permissions
Amazon ECR	Docker image registry
Amazon EC2	Application hosting
SSH	Automated EC2 deployment
Health Check	Deployment verification
Deployment Flow
Code Change
    ↓
git push
    ↓
GitHub
    ↓
GitHub Actions
    ↓
pytest
    ↓
Docker Build
    ↓
Amazon ECR
    ↓
SSH
    ↓
Amazon EC2
    ↓
Docker Container
    ↓
Health Check
    ↓
Application Live
Security Notes
Never commit AWS access keys.
Never commit the EC2 private SSH key.
Store credentials in GitHub Actions Secrets.
Use an EC2 IAM role for ECR access instead of AWS credentials on the server.
Keep SSH private keys in .gitignore.
Restrict EC2 Security Group access appropriately for production.
Use HTTPS/TLS and a reverse proxy such as Nginx for a production deployment.
Project Status

CI/CD Pipeline: COMPLETE ✅

Automated testing ✅
Automated Docker build ✅
Automated ECR push ✅
Automated EC2 deployment ✅
Automated health check ✅
End-to-end deployment verified ✅

 Use placeholders such as `<AWS_ACCOUNT_ID>` and `<EC2_PUBLIC_IP>` so the README can safely be public.
