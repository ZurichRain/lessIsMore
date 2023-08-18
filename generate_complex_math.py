from sympy import symbols, Eq, solve, latex


all_eq_lis=[]
# 定义符号
x, y = symbols('x y')

# 定义方程
eq1 = Eq(2*(x + 2)**2 + 3, 8 + 3*x)
# eq2 = Eq(5*x - 4*y, -2)


# 使用solve函数解方程组
sol = solve((eq1), (x))

print(sol)


x = symbols('x')
expr = 2*(x + 2)**2 + 3

latex_expr = latex(eq1)

print(latex_expr)
all_eq_lis.append(latex_expr)

# 定义方程
x, y = symbols('x y')
eq1 = Eq(2*x - y, 0)
eq2 = Eq(x + y, 3)

# 求解方程组
solution = solve((eq1, eq2), (x, y))
print(solution)

# 将方程组转化为 LaTeX
latex_eq1 = latex(eq1)
latex_eq2 = latex(eq2)
all_eq_lis.append(latex_eq1)
all_eq_lis.append(latex_eq2)




from jinja2 import Environment, FileSystemLoader
from pylatex import Document, Section, Math
from pylatex.utils import NoEscape
from pdf2image import convert_from_path
from PyPDF2 import PdfFileWriter, PdfFileReader,PdfReader,PdfWriter

def crop_pdf(input_pdf, output_pdf, crop_left, crop_upper, crop_right, crop_lower):
    pdf_reader = PdfReader(input_pdf)

    # Get the number of pages
    num_pages = len(pdf_reader.pages)

    pdf_writer = PdfWriter()
  
    # Iterate through all pages
    for pagenum in range(num_pages):
        page = pdf_reader.pages[pagenum]
        print(page.mediabox)

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



def generate_pdf_with_formula(formula_lis):
    # Create a new LaTeX document
    doc = Document()

    # Create a new section
    with doc.create(Section('')):
        # doc.append('An example of a simple equation is ')
        # Add the formula to the document
        for f in formula_lis:
            doc.append(Math(data=[NoEscape(f)]))

    # Generate the PDF
    doc.generate_pdf('output', clean_tex=False)


# LaTeX 公式
# latex_formula = "ax^2 + bx + c = 0"
# 生成 PDF
generate_pdf_with_formula(all_eq_lis)

# Run the function
crop_pdf('output.pdf', 'output1.pdf', 200, -45, 200, 545)

images = convert_from_path('/data/lessIsMore/generate_data/formulaMath/output.pdf')

# 然后你可以保存这些图像或者进行其它操作
for i, image in enumerate(images):
    image.save('output_page'+ str(i) +'.jpg', 'JPEG')


# 从PDF文件路径转换为图片
images = convert_from_path('/data/lessIsMore/generate_data/formulaMath/output1.pdf')

# 然后你可以保存这些图像或者进行其它操作
for i, image in enumerate(images):
    image.save('output1_page'+ str(i) +'.jpg', 'JPEG')
