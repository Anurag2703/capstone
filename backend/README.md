1.  Come to backend folder:
        cd backend

2.  Create a Virtual Environment:
        python -m venv venv

3.  Activate it: 
        On Windows:
            venv\Scripts\activate

        On macOS / Linux:
            source venv/bin/activate

4.  To Deactivate the venv:
        deactivate

5.  Install your dependencies::
        pip install -r requirements.txt

6.  For testing (cd backend):
        python -m pytest tests




7.  To run the FastAPI server:
        uvicorn app.main:app --reload