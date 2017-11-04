# Pyramid Learning Journal

**Author**: Michael Shinners

**Version**: 1.0.3

## Overview
Blog created with Pyramid for recording a Learning Journal of Code 401: Python

Deployed on Heroku: http://michaels-learning-journal.herokuapp.com/

## Tests
6 unit tests
4 functional tests
All tests pass, with 100% coverage in Python 2 & 3. 

## Architecture
Written in Python, with pytest for testing. Uses the web framework Pyramid with a scaffold built with the Cookiecutter pyramid-cookiecutter-alchemy. Deployed with Heroku.

## Contributors
[Megan Flood](https://github.com/musflood) - Help building out the site using Pyramid

## Change Log
10-31-2017 10:25pm - All pages are static, but successfully deployed to Heroku. 
11-1-2017 8:00pm - App is successfully deployed on Heroku and has minor interconnectivity. Step 1 is complete.
11-2-2017 9:05pm - App appearance and functionality has been upgraded with the addition of bootstrap for the front end appearance and UX. Added all post detail and full (per spec) interconnectivity between pages. All requirements met, step 2 complete.
11-3-2017 10:25pm - Created the database and connected all views to it. Updated views to reflect this.
11-4-2017 3:02pm - Completed all tests, including a massive amount of @pytest fixtures to get all out tests operational. 