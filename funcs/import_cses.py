import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import autopep8
succ =0
def extract_solution_code(solution_href,driver):
    
    driver.get(solution_href)
    time.sleep(.25)
    solution_html = driver.page_source
    soup = BeautifulSoup(solution_html, 'html.parser')
    code = '\n'.join(code.text for code in soup.find('div', class_='linenums').find_all('div'))
    
    # If <code> tag is found, extract its text content
    if code:

        lexer = get_lexer_by_name("cpp")

        formatted_code=autopep8.fix_code(code)
        highlighted_code = highlight(formatted_code.strip(), lexer, HtmlFormatter(style='colorful'))

        # Return the highlighted code
        return highlighted_code
    else:
        return None

def extract_problem_info(problem_href):
    response = requests.get(problem_href)
    soup = BeautifulSoup(response.content, 'html.parser')
    cells = soup.find('div',class_='md').find_all('p')
    


    statement_text = cells[0].text
    if not statement_text:
        statement_text = None

    input_text = cells[1].text
    if not input_text:
        input_text = None
    
    
    output_text = cells[2].text
    if not output_text:
        output_text = None
    constraints1 = '<br>'.join([constraint.text.strip() for constraint in soup.find('div',class_='md').find('ul').find_all('li')])
    constraints_elements = soup.find('ul', class_='task-constraints').find_all('li')
    constraints = '<br>'.join([constraint.text.strip() for constraint in constraints_elements])
    return statement_text, input_text, output_text, (constraints+"<br>"+constraints1).replace(r'\e', '&leq;')

def generate_html(solution_href, problem_href, problem_title, lang, driver):
    solution_code = extract_solution_code(solution_href,driver)
    statement_text, input_text, output_text, constraints = extract_problem_info(problem_href)
    statement_text = statement_text.replace(r'\rightarrow', '&rarr;')
    x = [statement_text, input_text, output_text, constraints, solution_code]
    for e in x:
        if e is None:
            print(f"Unsuccesfully while trying save {problem_title} to /solutions/eolymp/{problem_title}.html\nBecouse of ")
            return
        
    html_content = f"""
    <!DOCTYPE html>
    <html>
        <head>
		<title> Eolymp | {problem_title} </title>

		<meta charset= "UTF-8" />
		<meta name= "description" content= "Detailed solution and explanation for the CSES Apartments problem" />
		<meta name= "keywords" content= "apartments, cses apartments solution, cses ,cses solutions, cses problem set solutions, algorithm visualization" />
		<meta name= "author" content= "japl" />
		<meta name= "viewport" content= "width=device-width, initial-scale=1.0" />
		<script type="text/javascript" async
  		src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
		</script>
		<link rel="icon" href="../../favicon.ico" />
		
		
		
		<!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-FJRKSBQ1BY"></script>
	


		<link rel="stylesheet" href="../solution.css">
	</head>
        <body>
            <div id="navbar">
                <nav>
                    <ul>
                        <li><a class="active" href="../../index.html"> ↳ Back</a></li>
                    </ul>
                </nav>
            </div>

            <div id="conteudo">
                <h1>{problem_title}</h1>

                <p style="font-family: Arial, Helvetica, sans-serif; color      : #A65E4E; font-size:30px;">Statement:</p>
                <p style="font-size:25px ;  text-align: justify"> ( The original statement can be found <a href="{problem_href}" target="_blank">here</a> ) <br>{statement_text}</p>
                <p style="font-family: Arial, Helvetica, sans-serif; color      : #A65E4E; font-size:30px;">Input:</p>
                <p style="font-size:25px ;  text-align: justify">{input_text}</p>
                <p style="font-family: Arial, Helvetica, sans-serif; color      : #A65E4E; font-size:30px;">Output:</p>
                <p style="font-size:25px ;  text-align: justify">{output_text}</p>
                <p style="font-family: Arial, Helvetica, sans-serif; color      : #A65E4E; font-size:30px;">Constraints:</p>
                <p style="font-size:25px ;  text-align: justify">{constraints}</p>
                <p style="font-family: Arial, Helvetica, sans-serif; color      : #A65E4E; font-size:30px;">Solution:</p>
                <pre style="color:#D9C0A3;background:#323840ff; border-radius:15px;font-size:0.9vw;">{solution_code}</pre>
                </iframe>
            </div>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/default.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
        <!-- and it's easy to individually load additional languages -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/go.min.js"></script>
        </body>
    </html>
    """
    global succ
    with open(f"../solutions/cses/{problem_title}.html", "w") as html_file:
        html_file.write(html_content)
    succ+=1
    print(f"Succesfully saved {problem_title} to ../solutions/cses/{problem_title}.html")

# Load JSON data
with open('./data/cses.json') as json_file:
    data = json.load(json_file)


# Using Selenium to scrape dynamic content
options = webdriver.FirefoxOptions()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.get("https://www.cses.fi/login")
time.sleep(5)

# Process each entry in the JSON data
for entry in data:
    generate_html(entry['solution_href'], entry['problem_href'], entry['problem_title'], entry['lang'], driver)
driver.quit()
print(f"Succesfully added {succ} of {len(data)} problem to /cses/")