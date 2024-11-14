# QuickPNR 🚅 - A Django API for Indian Railway PNR Status

QuickPNR is a robust Django REST Framework (DRF) API that delivers real-time Indian Railway PNR (Passenger Name Record) information. By leveraging the power of Selenium for web scraping, it extracts data directly from the official Indian Railways website and presents it in a structured, developer-friendly JSON format.

## Key Features ✨

* **PNR Status Retrieval:**  Effortlessly fetch comprehensive PNR details, including:
  * Train information (number, name)
  * Passenger details
  * Booking and charting status
  * Journey details (boarding/destination stations, date, class)
  * Fare information
  * Real-time train status
* **Automated Captcha Handling:**  Seamlessly bypass captcha challenges during the scraping process, ensuring uninterrupted data retrieval.
* **JSON Output:**  Receive data in a clean and organized JSON format, simplifying integration with your applications or services.
* **Email Notifications (Optional):**  Configure the API to send email notifications to users with their PNR details.
* **User Authentication:** Secure your API with JWT-based authentication, including:
  * **Registration:** Allow users to create accounts.
  * **Login:** Enable users to access protected resources.
  * **Google Login:** Provide a streamlined login experience with Google authentication.
  * **Password Management:** Implement features for updating passwords and handling forgotten passwords.

## API Endpoints

**Base URL:** `/api/v1/`

### PNR Endpoints

* **GET /pnr/fetch/?pnr=<pnr_number>:**
  * Retrieves PNR details and sends an email notification to the authenticated user.
  * Requires a valid JWT token for authentication.
  * **Query Parameters:**
    * `pnr`: The 10-digit PNR number.
  * **Example Request:**

        ```bash
        curl -H "Authorization: Bearer <your_jwt_token>" "/pnr/fetch/?pnr=1234567890"
        ```

* **POST /pnr/fetch:**
  * Creates a new PNR record in the database if it doesn't already exist.
  * Scrapes PNR details from the Indian Railways website.
  * Requires a valid JWT token for authentication.
  * **Request Body:**

        ```json
        {
            "pnr": "1234567890" // The 10-digit PNR number
        }
        ```

  * **Example Request:**

        ```bash
        curl -X POST -H "Authorization: Bearer <your_jwt_token>" -H "Content-Type: application/json" \
             -d '{"pnr": "1234567890"}' /pnr/fetch
        ```

* **PATCH /pnr/fetch/:**
  * Updates an existing PNR record in the database with the latest scraped information.
  * Requires a valid JWT token for authentication.
  * **Example Request:**

        ```bash
        curl -X PATCH -d '{"pnr": "1234567890"}' -H "Authorization: Bearer <your_jwt_token>" /pnr/fetch/
        ```

### User Authentication Endpoints

* **POST /register/:**
  * Registers a new user account.
  * **Request Body:**

        ```json
        {
            "username": "johndoe",
            "email": "john.doe@example.com",
            "password": "securepassword"
        }
        ```

* **POST /login/:**
  * Logs in a user with their username and password.
  * Returns a JWT token upon successful authentication.
  * **Request Body:**

        ```json
        {
            "username": "johndoe",
            "password": "securepassword"
        }
        ```

* **POST /googleLogin/:**
  * Allows users to log in using their Google accounts.
  * Requires handling Google authentication on the frontend and sending the Google authentication token to this endpoint.
  * **Request Body:**

        ```json
        {
            "google_token": "<google_auth_token>"
        }
        ```

* **POST /updatePassword/:**
  * Updates the password for the authenticated user.
  * Requires a valid JWT token for authentication.
  * **Request Body:**

        ```json
        {
            "old_password": "oldpassword",
            "new_password": "newpassword"
        }
        ```

* **POST /forgotPassword/:**
  * Initiates the password reset process.
  * Typically sends a password reset email to the user's registered email address.
  * **Request Body:**

        ```json
        {
            "email": "john.doe@example.com"
        }
        ```

## Technologies Used 📦

* **Backend:** Django, Django REST Framework (DRF)
* **Web Scraping:** Selenium
* **Image Processing (for Captcha):** Pillow (PIL), pytesseract
* **Authentication:** JWT (JSON Web Token)
* **Task Queue (Optional):** Celery (for email notifications)
* **Message Broker (Optional):** Redis (for Celery)

## Getting Started 🚀

* **Clone the repository:**

```bash
git clone https://github.com/your-username/quickpnr.git
cd quickpnr
```

* **Install dependencies:**

```bash
pip install -r requirements.txt
```

* **Set up environment variables: Create a .env file based on the provided template.**

* **Apply database migrations:**

```bash
python manage.py migrate
# Start the development server:
python manage.py runserver
```

## Contributing 🤝

We welcome contributions to QuickPNR! Please feel free to open issues for bug reports, feature requests, or suggestions. If you'd like to contribute code, fork the repository and submit a pull request.

## License 📄

This project is licensed under the MIT License.
