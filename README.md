# TeamProject2022_36
# frontend
## Project setup
```
cd frontend
npm install
```
### Compiles and hot-reloads for development
```
npm run serve
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

# backend
## Project setup
```
cd backend
pip install -r requirements.txt
```
Create `.env` file in root of backend and set contents to.
```
SQLALCHEMY_DATABASE_URI=sqlite:///sqlite.db
TEST_DATABASE_URI=sqlite:///testing.db
SQLALCHEMY_TRACK_MODIFICATIONS=False
SECRET_KEY=34ab221b66e000c3f405e14c54b43104f0281ab3ef242a64280d151232436f28
FLASK_PORT=5000
DEBUG=True
```
## Run backend
```
python app.py
```