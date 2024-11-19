# **Email Campaign Manager**

This is an **Email Campaign Manager** built with Django, Django REST Framework, Celery, and Redis. The app enables users to manage email campaigns efficiently, including scheduling newsletters, managing subscribers, and sending bulk emails with HTML content.

---

## **Features**

- **User Management**
  - User registration and authentication with JWT tokens.
- **Email Management**
  - Add and manage email addresses.
  - Mark invalid or failed emails as inactive.
- **Newsletter Management**
  - Create and manage newsletters with HTML content.
  - View all newsletters created by the user.
- **Subscription Management**
  - Subscribe emails to newsletters.
  - Allow anonymous email subscriptions.
- **Email Scheduling**
  - Schedule newsletters for all subscribers.
  - Send custom emails to selected recipients.
  - Automatically process scheduled tasks at specified times.
- **Custom Email Templates**
  - Send newsletters using HTML templates.

---

## **Technologies Used**

- **Backend:**
  - Django
  - Django REST Framework
- **Task Queue:**
  - Celery
- **Broker and Result Backend:**
  - Redis
- **Email:**
  - Django's EmailMultiAlternatives

---
## **Run With Docker**
```bash
docker compose up
```
### **or Dont**
## **Installation**

### **Prerequisites**

1. Python 3.8+
2. Redis installed and running

### **Setup**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/kaustubha-chaturvedi/email-campaign.git
   cd email-campaign
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   . venv/Scripts/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup the Database**
   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Redis Server**
   Ensure Redis is running locally. If not, start it with:
   ```bash
   redis-server
   ```

7. **Run Celery Worker**
   Open a new terminal and navigate to the project directory:
   ```bash
   celery -A campaign worker --loglevel=info
   ```

8. **Run Celery Beat (Optional)**
   To process periodic tasks:
   ```bash
   celery -A campaign beat --loglevel=info
   ```

9. **Run the Server**
   ```bash
   python manage.py runserver
   ```

10. **Access the App**
    Visit `http://127.0.0.1:8000/api/` to view the API.

---


## **Future Improvements**

- Add analytics for email open rates and click tracking.
- Integrate a frontend interface.

---

## **Contributing**

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit changes: `git commit -m "Add feature"`.
4. Push to the branch: `git push origin feature-name`.
5. Create a pull request.

---

## **License**

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
