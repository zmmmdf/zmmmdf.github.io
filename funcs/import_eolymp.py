import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from tqdm import tqdm  # Import tqdm for the progress bar

succ = 0
def extract_solution_code(solution_href,driver):
    
    driver.get(solution_href)
    solution_html = driver.page_source
    time.sleep(.25)
    soup = BeautifulSoup(solution_html, 'html.parser')
    code_cpp = soup.find('code', class_='hljs cpp')
    code_py = soup.find('code', class_='hljs stylus')
    code_tag = None
    if code_cpp:
        code_tag=code_cpp
        code_type = 'cpp'
    elif code_py:
        code_tag=code_py
        code_type = 'py'
    if code_tag:
        code = code_tag.get_text()
        lexer = get_lexer_by_name(code_type)
        highlighted_code = highlight(code.strip(), lexer, HtmlFormatter(style='colorful'))
        return highlighted_code
    else:
        return None

def extract_problem_info(problem_href):
    response = requests.get(problem_href)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    statement_text = ""
    statement_div =  soup.select('div.tw-content > p > span')
    
    if statement_div:
        for i, stat in enumerate(statement_div):
            statement_text += stat.text.strip()
            
            if i < len(statement_div) - 1:
                statement_text += "\n"
    else:
        statement_text = None

    input_div = soup.find('div', class_='eo-problem-input')
    if input_div:
        input_text = input_div.find('div').text.strip()
    else:
        input_text = None
    
    output_p = soup.find('p', class_='tw-paragraph tw-block')
    if output_p:
        output_text = output_p.text.strip()
    else:
        output_text = None
        
    constraints_elements = soup.find_all('span', class_='eo-message__text')
    constraints = '<br>'.join([constraint.text.strip() for constraint in constraints_elements])
    return statement_text, input_text, output_text, constraints

def generate_html(solution_href, problem_href, problem_title, lang, driver):
    solution_code = extract_solution_code(solution_href,driver)
    statement_text, input_text, output_text, constraints = extract_problem_info(problem_href)
    x = [statement_text, input_text, output_text, constraints, solution_code]
    y = ['statement_text', 'input_text', 'output_text', 'constraints', 'solution_code']
    for e in x :
        if e is None:
            # print(f"Unsuccesfully while trying save {problem_title} to ../solutions/eolymp/{problem_title}.html\nBecouse of {y[x.index(e)]}")
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
                <p style="font-size:25px ;  text-align: justify"> ( The original statement can be found <a href="{problem_href}" target="_blank">here</a> ){statement_text}</p>
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
    with open(f"./solutions/eolymp/{problem_title}.html", "w") as html_file:
        html_file.write(html_content)
    global succ
    succ+=1



with open('./data/eolymp.json') as json_file:
    data = json.load(json_file)



options = webdriver.FirefoxOptions()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.get("https://www.eolymp.com/en/login")
time.sleep(10)

for entry in tqdm(data, desc="Processing", unit="problem"):
    generate_html(entry['solution_href'], entry['problem_href'], entry['problem_title'], entry['lang'], driver)
driver.quit()

print(f"Succesfully added {succ} of {len(data)} problem to ../eolymp/")
