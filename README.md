<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->


<!-- PROJECT LOGO -->
<br />
<div align="center">


<h3 align="center">News QA</h3>
  <p align="center">
    A news question-answering app powered by Open AI GPT.
  </p>
  <p align="center">
    The news QA app is live at <a href="https://newsq.knightlab.com">https://newsq.knightlab.com</a>
  </p>
  <img width="600" alt="image" src="https://github.com/cindyhu2023/news-q-and-a/assets/57238301/34f3c087-ce6e-412f-8d2a-7b056e5c0da0">
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
    </li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
https://github.com/cindyhu2023/news-q-and-a/assets/57238301/eb4bccd3-9ff5-4dcf-8821-fb130d483713

This is a news question-answering app with CNN news articles as references. Currently, the database only includes articles published during January 2022 - March 2022, so questions about news outside of that time period might not be answerable. ([CNN news dataset source](https://www.kaggle.com/datasets/hadasu92/cnn-articles-after-basic-cleaning))

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With

* [![React][React.js]][React-url]
* [![Flask][Flask.py]][Flask-url]
* [![OpenSearch][Opensearch]][Opensearch-url]
* [![OpenAI GPT][OpenAI]][OpenAI-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started
This app has two parts: client (`/web`) and server (`/api`)

Here's how to set up if you want to run the repo locally:

### Server

* pip install (you may want to create a virtual env with python first)
  ```sh
  cd /api
  pip install -r requirements.txt
  ```
* Create a `.env` file in `/api` and include your keys for OpenSearch and Open AI
```
OPEN_AI_KEY = 
OPENSEARCH_URL = 
OPENSEARCH_USERNAME = 
OPENSEARCH_PASSWORD = 
```

* initialize document store with news article data (you can swap with your own data)
```
cd /util
python docStoreInit_cnn.py
```

* start the server
```
cd ..
flask run
```

### Client
* install packages
  ```
  cd /web
  npm i
  ```
* start the app client
  ```
  npm run start
  ```


<p align="right">(<a href="#readme-top">back to top</a>)</p>





<!-- CONTACT -->
## Contact

Cindy - cindyhu2023@u.northwestern.edu

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Flask.py]: https://img.shields.io/badge/Flask-20232A?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]:https://flask.palletsprojects.com/en/3.0.x/
[Opensearch]:https://img.shields.io/badge/OpenSearch-20232A?style=for-the-badge&logo=opensearch&logoColor=005EB8
[Opensearch-url]: https://opensearch.org
[OpenAI]: https://img.shields.io/badge/OpenAI-20232A?style=for-the-badge&logo=openai&logoColor=412991
[OpenAI-url]:https://openai.com
