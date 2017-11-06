TEST_PLAN.md

# Pyramid Learning Journal

#Test Plan

**Author**: Michael Shinners

## Overview
My plan to tackle all my testing is to build upon the current tests, using the pytest decorators, and Tox.

Deployed on Heroku: http://michaels-learning-journal.herokuapp.com/

## The Plan

1. Test that all views display as planned.
    A. Home view
    B. Detail view
    C. Create view
    D. Update view

2. Test all functionality
    A. Home button takes to home page
    B. Create button takes to create page
    C. A submitted entry posts to the list.
    D. A sumitted post posts to teh top of the list.
    E. A new post has valid text in title.
    F  A new post has valid text in the body.
    G. A new post has valid timestamp on it.

3. Test error handling
    A. Requested entry not found.
    B. Page not found.
    C. 
