LLM APP Deployment Guide (CMD):

Before deploying the application on your system, enter your own API keys in the views.py file 

1. Download Python Version 3.13.0 or later and test if it is installed in CMD by writing: python --version

2. Create Virtual Environment in CMD by writing: python -m venv myenv

3. Activate the Virtual Environment in CMD by writing: myenv\Scripts\activate

4. Download required packages if not intalled by writing in CMD: pip install Django==4.1.4 openai==0.28.0 together==1.3.3

5. Navigate to directory of appplicaiton by writing in CMD: cd path\to\the\app

6. Run the application by writing in CMD: python manage.py runserver 8080

7. Access application in browser by opening: http://127.0.0.1:8080
