# Fullstack project React.js + FastAPI + MongoDB

Demo vending machine web application

UI designed for mobile and tablet screen size but also work as well on every screen sizes.


### Structure project
```
    app |  //contains Frontend using React.js + Redux
        |- nginx //contains nginx file
        |- public //contains static files from react
        |- src //contains files those work with react
    
    server| //contains Backend using FastAPI
           |- database //database connection
           |- routers //api routes
           |- schema //database schema
           |- spec //contains test files
                |- data //mock or init data
           |- utils //utility functions
```

### Installation
1. clone project
```
git clone git@github.com:nattapong-c/reactjs-fastapi.git
```

2. go to project path where docker-compose.yml is. Run docker compose
```
cd /path/to/project
docker-compose up --build
```

3. Go to [http://localhost:3000](http://localhost:3000) for web application and [http://localhost:3003/docs](http://localhost:3003/docs) for API documentation

### Init data money
1. Go to API documentation [http://localhost:3003/docs](http://localhost:3003/docs)
2. Go to Money section and open API "POST /money/init"
3. Click "Try it out"
4. Click "Execute" to init money data

### Init data product
1. Go to API documentation [http://localhost:3003/docs](http://localhost:3003/docs)
2. Go to Product section and open API "POST /product/init"
3. Click "Try it out"
4. Click "Execute" to init product data

*NOTE: You can see init data in /server/spec/data
