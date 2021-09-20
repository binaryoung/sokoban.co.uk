# sokoban.co.uk

This is the source of the [sokoban.co.uk](https://sokoban.co.uk)

## Tech Stacks 
* Flask
* Vue.js
* Tailwind CSS

## Deploy

### Build Frontend

```bash
cd frontend
npm i
npm run build
cp -r dist/* ../static/
```

### Run server
Start the flask app using Gunicorn or other WSGI servers