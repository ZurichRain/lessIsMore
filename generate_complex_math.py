import os

from sympy import symbols, Eq, solve, latex, solveset, S, sympify
from jinja2 import Environment, FileSystemLoader
from pylatex import Document, Section, Math, Center
from pylatex.utils import NoEscape
from pdf2image import convert_from_path
from PyPDF2 import PdfFileWriter, PdfFileReader,PdfReader,PdfWriter
import random
import numpy as np
import json


def generate_poly(degree,x):
    # x = symbols('x')
    coeffs = [np.random.randint(-100, 100) for _ in range(degree + 1)]
    poly = sum(c*x**i for i, c in enumerate(reversed(coeffs)))

    return poly

class Generate_Math:

    def __init__(self, outPath) -> None:
        
        self.outPath = outPath

    def generate_pdf_with_formula(self, formula_lis):
        # Create a new LaTeX document

        doc_prompt_lis = ['','We used following equation:']

        doc_prompt = random.choice(doc_prompt_lis)       
        
        doc = Document()

        # Create a new section
        with doc.create(Section('')):
            with doc.create(Center()) as centered:
                doc.append(doc_prompt)
                # Add the formula to the document
                for f in formula_lis:
                    doc.append(Math(data=[NoEscape(f)]))

        # Generate the PDF
        doc.generate_pdf('overalpdf', clean_tex=False)

    def crop_pdf(self, input_pdf, output_pdf, crop_left, crop_upper, crop_right, crop_lower):
        pdf_reader = PdfReader(input_pdf)

        # Get the number of pages
        num_pages = len(pdf_reader.pages)

        pdf_writer = PdfWriter()
    
        # Iterate through all pages
        for pagenum in range(num_pages):
            page = pdf_reader.pages[pagenum]

            # The coordinates are in point = 1/72 inch
            page.mediabox.upper_right = (
                page.mediabox.right - crop_right,
                page.mediabox.right - crop_upper
            )
            page.mediabox.lower_left = (
                page.mediabox.left + crop_left,
                page.mediabox.left + crop_lower
            )

            pdf_writer.add_page(page)

        with open(output_pdf, 'wb') as out:
            pdf_writer.write(out)

    def saveImg(self, all_eq_lis, img_id):
        # 生成 PDF
        self.generate_pdf_with_formula(all_eq_lis)

        # Run the function
        self.crop_pdf('overalpdf.pdf', 'croppdf.pdf', 200, -45, 200, 545)

        images = convert_from_path('croppdf.pdf')

        # 然后你可以保存这些图像或者进行其它操作
        for i, image in enumerate(images):
            output_PATH = self.outPath + 'img_{}_'.format(img_id)+ str(i) +'.jpg'
            image.save(output_PATH, 'JPEG')


def get_Linear_Equation_Math_Image(outpath):

    symbols_lis = ['x y','a b','c d','X Y']
    # 定义符号
    x, y = symbols(random.choice(symbols_lis))
    
    gen_eq_lis = []
    
    img_id = 0
    while(img_id < 10):
        all_eq_lis=[]
        # 定义方程
        # eq1 = Eq(2*(x + 2)**2 + 3, 8 + 3*x)
        # eq2 = Eq(5*x - 4*y, -2)
        ceq1 = generate_poly(2,x)
        ceq2 = generate_poly(2,x)
        eq1 = Eq(ceq1,ceq2)

        # 使用solve函数解方程组
        sol = solve((eq1), (x))
        print(sol)

        tag = False
        for s in sol:
            if( not sympify(s).is_integer):
                tag = True
                break
        
        if tag:
            continue
        img_id+=1

        latex_expr = latex(eq1)

        print(latex_expr)

        all_eq_lis.append(latex_expr)

        genor = Generate_Math(outpath)

        genor.saveImg(all_eq_lis,img_id)

        if len(sol)>1:
        
            gpt4_prompt = '''Here's a LaTeX formatted equation, {}. The answer to which is {} and {}. Please generate the related QA according to the example.'''.format(latex_expr,str(sol[0]),str(sol[1]))
        
        elif len(sol)==1:

            gpt4_prompt = '''Here's a LaTeX formatted equation, {}. The answer to which is {}. Please generate the related QA according to the example.'''.format(latex_expr,str(sol[0]))

        json_data = {
            'img':'img_{}_0.jpg'.format(img_id),
            'prompt_for_gpt4': gpt4_prompt
        }
        gen_eq_lis.append(json_data)

    with open('./gen_math_data.json', 'w') as f:

        f.write(json.dumps(str(gen_eq_lis)))
    




if __name__ == '__main__':

    get_Linear_Equation_Math_Image('./output_imgs/')
    # symbols_lis = ['x y','a b','c d','X Y']
    # x, y = symbols(random.choice(symbols_lis))
    # ceq1 = generate_poly(1,x)
    # ceq2 = generate_poly(0,x)
    # eq1 = Eq(ceq1,ceq2)
    # # eq2 = Eq(5*x - 4*y, -2)

    # # 使用solve函数解方程组
    # sol = solve((eq1), (x))
    # print(sympify(sol[0]).is_integer)
    # print(type(sol))
    # print(type(sol[0]))
    # print(sol[0])

    # print()

    # # sol = solve((eq1), (x))
    # # print(sol)

    # latex_expr = latex(eq1)

    # print(latex_expr)
    # all_eq_lis=[]
    # all_eq_lis.append(latex_expr)
    # for eqs in sol:
    #     # all_eq_lis.append(list(sol)[0])
    #     all_eq_lis.append(eqs)

    # genor = Generate_Math('./')

    # genor.saveImg(all_eq_lis)

# all_eq_lis=[]







# x = symbols('x')
# expr = 2*(x + 2)**2 + 3




# # 定义方程
# x, y = symbols('x y')
# eq1 = Eq(2*x - y, 0)
# eq2 = Eq(x + y, 3)

# # 求解方程组
# solution = solve((eq1, eq2), (x, y))
# print(solution)

# # 将方程组转化为 LaTeX
# latex_eq1 = latex(eq1)
# latex_eq2 = latex(eq2)
# all_eq_lis.append(latex_eq1)
# all_eq_lis.append(latex_eq2)









# LaTeX 公式
# latex_formula = "ax^2 + bx + c = 0"



# # 从PDF文件路径转换为图片
# images = convert_from_path('/data/lessIsMore/generate_data/formulaMath/output1.pdf')

# # 然后你可以保存这些图像或者进行其它操作
# for i, image in enumerate(images):
#     image.save('output1_page'+ str(i) +'.jpg', 'JPEG')
