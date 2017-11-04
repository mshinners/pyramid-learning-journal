"""List of all learning journal entries."""

from datetime import datetime

FTM = '%Y-%m-%d%Z%H:%M:%S.%f'


ENTRIES = [
    {
    'title': "...day the 13th",
    'id': 13,
    'body': "<p>today was a interesting. I learned about yet another new data structure, but really didn't have any time to devote to learn much about it, as most of lab time was trying to get the past 2 day's stuff working and then spending a lot of time on the Pyramid stuff. Getting the Learning Journal set-up is quite the challenging task.</p>",
    'creation_date': datetime.strptime("2017-11-02UTC05:44:51.401346", FTM)
    },
    {
    'title': "The Twelfth Night",
    'id': 12,
    'body': "<p>Another long, but productive day. A lot of learning took place. I learned about Heap today. The latest data structure, and boy is it confusing. I also learned more about configuring our app better using pythonic structure. We finished the night by getting our learning journals published which was a feat. I learned a good deal more about Gluon, of which will be my topic for my Lightning Talk.</p>",
    'creation_date': datetime.strptime("2017-11-01UTC03:47:23.438358", FTM)
    },
    {
    'title': 'Heroku broken - Day 11',
    'id': 11,
    'body': "<p>Today was a very full day of learning. Last night I read more about Big-O notation, and have a better grasp on its meaning and purpose. While I still don't really comprehend the math behind it (especially when it comes to the (log n) notation, I understand the concepts, ad am usually able to recognize the right levels. I also read up on Jinja2, and trust that putting it into practice to day will help me to understand it a little better. I learned a great deal about Pyramid, and while I felt quite overwhelmed with it during lecture yesterday, I expect it will get clearer with practice as well. I also learned the latest data structure of Deque.</p>",
    'creation_date': datetime.strptime("2017-10-31UTC07:27:12.453147", FTM)
    },
    {
    'title': "Day of the Tenth",
    'id': 10,
    'body': "<p>Today I learned to trust myself. During the whiteboard challenge, I first thought up the beginnings of the answer, having two separate variables, one looking at the next, and one looking at the next.next. But I didn't finish that thought to have it go faster vs slower and felt that it was NOT the right direction and my partner and I spent a lot more time trying to find a different approach that never happened came. When we learned the answer and that I was on the right track from the begining, it gave me a sense that I do have enough knowledge to figure out problems, I just need to have the faith in myself that I may have an idea of a solution. I'm tired, I'm rambling again, so I think I'm done.</p>",
    'creation_date': datetime.strptime("2017-10-28UTC15:10:44.841504", FTM)
    },
    {
    'title': "Ninth day",
    'id': 9,
    'body': "<p>Today i learned I need sleep! I stayed too late last night and paid for it dearly, even more so than my usual deprivation. I am exhausted. I learned about the Aprenti program today, and will keep that as a possible choice. I learned about Doubly-Listed Lists and Queues. I learned how to better implement HTTP error codes and have a good idea about handling exceptions. I learned the importance of bytes-strings and unicode strings, as we had quite a difficult getting the right one in the right place and at the right time.</p>",
    'creation_date': datetime.strptime("2017-10-27UTC03:14:41.677228", FTM)
    },
    {
    'title': "8th Day",
    'id': 8,
    'body': "<p>Had to switch up the title, it was getting a bit monotonous. Today was a good day of actually understanding what I was doing. There were, of course, things that completely baffled me. But today, there were other things that may have previously baffled me completely that today I felt were just out of my grasp of understanding. (I'm really tired right now at 10:20 as I'm riding the long bus home so I'm pretty sure these sentences aren't making much sense, but Ill continue to try my best.) But take the whiteboard challenge today. Last week, I may have just kinda frozen up. But today I had some sort of an idea of what to do. Where previously I may have been blocked as to where to start, I has some sort of idea. Now, my thoughts were often wrong and ill-written, but I did something that had the essence of an idea. And I was able to work through the code and see why it wouldn't work and could start over with a fresh tactic. That felt good! Then again, working with my partners on our assignments, I didn't feel nearly as lost as I may have thought I might be. One one project I felt much more like a contributor than I was previously able to do. And on the other, I feel I was a near-equal partner. This has been a positive growth day, nay, week! Thus ends my weary ramblings, goodnight!</p>",
    'creation_date': datetime.strptime("2017-10-26UTC04:50:06.432421", FTM)
    },
    {
    'title': "Day 7",
    'id': 7,
    'body': "<p>Today I learned a great deal about the server-client connection process. I feel that I competently understand every step of process and continue to grow in my understanding of the testing process. Today's code review where we built the linked list was wonderful. I could visualize what a linked list was finally adn it all made sense how to build it and test it.</p>",
    'creation_date': datetime.strptime("2017-10-25UTC14:34:50.219260", FTM)
    },
    {
    'title': "Day 6",
    'id': 6,
    'body': "<p>Today, I learned about Sockets. NOt just sockets, but socket.sockets, (*sockets), sockets sockets, everywhere. I learned how to set up a client and server to talk to each other using python. I started to lean about linked lists but have a LONG way to go before I would feel remotely comfortable with them. I went to a meet-up tonight and learned more about time complexity (Big O) and memory complexity. I learned things like durable store, any(), and depth1st vs. breadth1st, and much more.</p>",
    'creation_date': datetime.strptime("2017-10-24UTC02:53:56.364779", FTM)
    },
    {
    'title': "Day 5",
    'id': 5,
    'body': "<p>DAY OF CODE! Wow! that kicked my but all day! But I learned a lot. The testing part, though agonizing, helped me learn. I am too tired to sit in front of this screen any further tonight, but knocking out my LJ!</p>",
    'creation_date': datetime.strptime("2017-10-22UTC06:56:04.123134", FTM)
    },
    {
    'title': "Day 4",
    'id': 4,
    'body': "<p>Today was a challenging day. The code challenge was a stressful activity. Even though it was not graded, it showed me just how much I didn't what I was doing. I already knew that, but this made it shine. I did surprise myself just a little bit, however. I felt I was able to complete more code than I thought I could. Even though it didn't work, I was able to get more code written in roughly better order than I thought I might at first. I learned quite a bit more while working with my partner today. He is quite gifted in the art of coding and he has taught my some thing in my observation of him writing, and in his navigating of my driving. I can better put together functions, and working together, we figured out how to write some tests. In lecture time, I learned more about lists and and how to manipulate them. Tuples and dicts, too. We learned a bit about error handling, but frankly we went through that so fast, that I didn't really retain much about that. And we learned new ways of testing, using Tox, which allows for for testing in multiple versions, namely the 2 we use, 2.7 &amp; 3.6.</p>",
    'creation_date': datetime.strptime("2017-10-21UTC05:40:12.574438", FTM)
    },
    {
    'title': "Day 3",
    'id': 3,
    'body': "<p>Today I learned more about basic Python structure. I learned how to work with lists, tuples, bust mostly dictionaries. Understanding that they are searched by keys, instead of values, is a key difference, I feel, to what would be expected. </p> <p>I also learned about loops and how to navigate them. The various methods used to store, sort, pull and analyze the data held within is immense, but will prove very beneficial in the future as I learn how best to take advantage of the commands.</p>",
    'creation_date': datetime.strptime("2017-10-20UTC14:38:41.770755", FTM)
    },
    {
    'title': "Day 2",
    'id': 2,
    'body': "<p>Today I learned about our first tests. That was an interesting component about programming to which I had never given much thought. That was a concept that was easy enough to understand, but a bit more difficult to implement. I also learned more about how to run code in the terminal, specifically using ipython. I learned about the if <strong>name</strong> == '<strong>main</strong>': code block. This concept took me quite a while to wrap my head around, but I think I finally understood it by the time I left. There was so much I learned in lecture that I shant list it all, but all basic python code that wasn't covered as well (or often not at all) in the codecademy tutorials. I will be reviewing the daily class summaries during our bonus time tomorrow, that'll be for certain.</p>",
    'creation_date': datetime.strptime("2017-10-18UTC01:11:26.031863", FTM)
    },
    {
    'title': "Today I learned.....",
    'id': 1,
    'body': "<p>that there is a whole bunch to learning a whole new language. That all the tools used to work with Python itself have their own learning curves. I learned about sublime, about some of the many plug-ins available. I learned about environments and (kinda) how to navigate them. I learned that I do not yet know to what level this course is going to tear me(us) down. I learned about selling myself, being my own marketer, pitchman, and cheer squad.</p>",
    'creation_date': datetime.strptime("2017-10-16UTC23:38:15.391577", FTM)
    }
]
