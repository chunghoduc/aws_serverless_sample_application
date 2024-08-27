
# Serverless Image Management Application

This project is a serverless image management application built using AWS Lambda, AWS API Gateway, and AWS S3. It provides endpoints to list images, automatically generate thumbnails for uploaded images, and rename images and their thumbnails.

## Table of Contents

- [Project Overview](#project-overview)
- [Installation Guide](#installation-guide)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This serverless application includes the following features:
1. **List Images and Thumbnails:** Retrieve a list of all images and their corresponding thumbnails from an S3 bucket.
2. **Generate Thumbnail:** Automatically generate a thumbnail for an image uploaded to the S3 bucket.
3. **Rename Image:** Rename an image and its corresponding thumbnail in the S3 bucket.

## Installation Guide

### Prerequisites

- **AWS CLI:** [Install AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
- **AWS SAM CLI:** [Install AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- **Python 3.9** (or later)
- **Git**

### Clone the Repository

```bash
git clone https://github.com/your-username/serverless-image-management.git
cd serverless-image-management
```

### Install Dependencies

Make sure you have Python 3.9 or later installed. Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Configure AWS CLI

Ensure your AWS CLI is configured with the appropriate credentials and default region:

```bash
aws configure
```

## API Endpoints

### 1. List Images and Thumbnails

- **Method:** `GET`
- **Endpoint:** `/images`
- **Description:** Retrieves a list of all images and their corresponding thumbnails from the S3 bucket.

**Example Request:**
```http
GET /images
```

**Response Example:**
```json
[
    {
        "image": "s3://your-image-bucket/image1.jpg",
        "thumbnail": "s3://your-image-bucket/thumbnails/image1.jpg"
    },
    {
        "image": "s3://your-image-bucket/image2.jpg",
        "thumbnail": "s3://your-image-bucket/thumbnails/image2.jpg"
    }
]
```

### 2. Generate Thumbnail

- **Method:** `POST` (Triggered by S3 event)
- **Endpoint:** N/A
- **Description:** This Lambda function generates a thumbnail automatically when an image is uploaded to the S3 bucket. This function is triggered by S3 events.

**Workflow:**
1. Upload an image to the S3 bucket (e.g., `your-image-bucket/image1.jpg`).
2. The Lambda function will automatically create a thumbnail for the uploaded image.

### 3. Rename Image

- **Method:** `POST`
- **Endpoint:** `/images/rename`
- **Description:** Allows users to rename an image and its corresponding thumbnail in the S3 bucket.

**Request Body:**
```json
{
    "old_name": "image1.jpg",
    "new_name": "new_image1.jpg"
}
```

**Example Request:**
```http
POST /images/rename
Content-Type: application/json

{
    "old_name": "image1.jpg",
    "new_name": "new_image1.jpg"
}
```

**Response Example:**
```json
{
    "message": "Renamed image1.jpg to new_image1.jpg and corresponding thumbnail."
}
```

## Deployment

### Deploy Using AWS SAM

1. **Package and Deploy:**

   Ensure you have set up an S3 bucket to store deployment artifacts and that you have updated your GitHub secrets with the S3 bucket name.

   ```bash
   sam build
   sam package --s3-bucket your-s3-bucket-name --output-template-file packaged.yaml
   sam deploy --template-file packaged.yaml --stack-name your-stack-name --capabilities CAPABILITY_IAM --no-fail-on-empty-changeset
   ```

### Automate Deployment with GitHub Actions

1. **Configure GitHub Secrets:**
   - Go to your GitHub repository settings.
   - Add `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` as secrets.

2. **Push Code:**
   - Push your code changes to the `main` branch.
   - The GitHub Actions workflow will automatically build, package, and deploy your serverless application.

## Contributing

We welcome contributions! Please follow the standard fork-and-pull request workflow. For detailed contribution guidelines, refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to modify the README file as needed to fit your project's specifics and requirements.

