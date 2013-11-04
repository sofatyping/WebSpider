WebSpider
=========

The spider tool is a tool that analyze the content(HTML) of a website. So the spider tool needs to go through all the web pages so that it have scan the structure of the whole website, knows the relations among all the web pages. The secondary task of a spider tool is to scan the content of the web pages and look for problems in the pages.
 
We are going to built the spider tool with Django framework in Python. Django framework is the MVC model for Python. It is easy to use. Since we are processing strings in spider tool. Python is a strong tool to process strings. Also, we are going to use beautifulsoup, which is a extra package for Python. Beautifulsoup is a tool that it can locate the tags in HTML content. In addition, we need to communicate with MySQL. We are using MySQL to build three tables for unvisited links, visiting links and visited links. Last but not the less, we will use bootstrap to make to page looks better.

The main functions of spider tool we are going to build is followed:
1) Scan the website and build a tree structure of the web pages based on the links in the website
2) Scan all the HTML codes and look for if the codes fit w3c standards
3) Give statements about how to fix the coding problems according to w3c standards
4) Scan the structure of HTML codes and give some recommendations on SEO

The spider tool contains four pages. The first page is a google-like homepage so that user can enter the url address they want to analyze. The second page is a tree structure which will display the structure of the website. It will also provide all the links in the website. The third page will display the coding flaws the tool finds, the number of lines of the flaw and how to fix it. The fourth page will show the suggestions on how to revise the structure of a webpage so that makes it fit the SEO better.

The workflow of the spider tool analysis is that a user enter a url address. The server receive the post request and read the content from the url. After this, it is going to find all the links in DFS method. Meanwhile, the content of the web pages in analyzing in backend to find out the flaws and improvements. Finally, all the result will send back to browser to display to users.
