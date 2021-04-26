## Andrew McMillan's ePortfolio

## Professional Self-Assessment

  The capstone course provided the opportunity to review and reexamine material from previous courses and to enhance select projects from those courses. This ePortfolio contains that enhanced work and highlights my strengths as a developer in both an individual and collaborative context. The creation process has reinforced my computer science education as a whole and prepared me to work in a variety of modern team environments and project management methodologies. I am comfortable using different tools and strategies that facilitate development and collaboration in the software development life cycle. Working on physical science data applications such as this would be ideal for me as a professional in the computer science field.  
  
  The course simulated the software development life cycle and emphasized team collaboration and transparency with stakeholders. I created an early narrative that identified potential use cases for various artifact enhancements. I believe my ultimate choice of application design is a positive indicator of my practicality, and that the application concept has market appeal. I supported a collaborative environment by creating the narratives, code review, and milestone deliverables, incorporating feedback from those, and by providing periodic progress updates to my instructor. One of the best quality control methods is code review. The code review video identifies inefficiencies and security flaws with the original artifacts and envisions specific design, algorithmic, and database solutions. Video communication and presentation software skills are in demand in these times of distributed teams and remote work. They are excellent tools for information sharing and communicating with stakeholders. Competence with version control tools and techniques is critical for individuals and collaborators. I used the GitHub repository and my local machine for effective version control that maintains the history of enhancements and demonstrates the ability to use branching and merging to safely develop new features.
  
  Enhancements were required in each of the three categories: design and architecture, data structures and algorithms, and database. Security was also a heavily emphasized requirement. The temperature and humidity artifact that the overall design is based on was heavily altered and enhanced. The original program was basically a temperature and humidity sensor reader with simple conditional lighting variations. I converted it into a weather station plus historical data application that reads temperature and humidity data, and through numerous processes and manipulation, converts it into daily and monthly statistical records and displays them. I believe it showcases my ability as a developer to take limited input and create much more. The algorithmic/data structure enhancement centers around a self-balancing AVL tree but includes more additional functions and structures. There are numerous feature additions that show an ability to adapt the artifact to the specific programming task. The database enhancement involves heavy use of aggregate functions. These are very important in data analytics which is of growing importance in nearly every field.
  
  Secure coding is a critical practice. It tends to be less of an issue with Python, and the program takes no input and has no external data file dependencies, but there are potential crash points. The sensor data must be numbers because the tree functions require data type consistency for Boolean comparisons, and that same data goes through mathematical operations in lists that must have consistent numerical data types. Certain operations cannot be performed on empty lists, which do occur frequently when the tree range searches return nothing. Those conditions are checked to prevent crashes. The data can become corrupted if data structures are not emptied after each cycle. The entire tree and all the lists need to be emptied so it doesn’t append to previous day’s data and corrupt the data or cause overflows. Accessing the database also has risks. I made sure the connection was made and handled the exception, otherwise. 
  
  The biggest challenge was the transformation of three separate and unrelated artifacts into one. That meant altering each artifact in a way that would make them compatible. That takes a lot of planning and structured development, and that’s why project management and development frameworks are important. The weather station is designed to run continuously. It requires timing mechanisms that regulate the number of sensor readings, schedule function calls to perform CRUD operations on the data, and schedule record inserts at the end of the day and month. All three components are regulated by timer mechanisms. The data from the sensor is read with the sensor function every few minutes. At the very end of the day, that data is inserted into the tree node structures, sorted by temperature. Multiple functions calls read the tree data and write to data structures. Non-tree functions then extract the data and perform a few calculations to generate statistic value variables that become the column values of one daily record. After daily record insertion, the date is checked. If it is the first of the month, all the records are aggregated, and a new monthly record is generated for the monthly table.    
  
## The Weather Station and Historical Data App

```python



```
```python
# Here is some in python
def foo():
  print 'foo'
```  


You can use the [editor on GitHub](https://github.com/AndrewMcMillan1/AndrewMcMillan1/edit/gh-pages/index.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for


Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/AndrewMcMillan1/AndrewMcMillan1/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.
