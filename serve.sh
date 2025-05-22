git pull

cd frontend
npm run build
pm2 restart all

cd ..

cd backend

kill -9 `sudo lsof -t -i:8000`

conda run -n gsw pip install -r requirements.txt

conda run -n gsw uvicorn app.main:app --reload

cd ..
