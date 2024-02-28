import imgkit
import re

# Define the provided text with LaTeX equations (without emojis)
latex_text = r'''
Searching the web...complex equation with fraction and powers


Ah, estrizal, you've summoned me for a cosmic equation, haven't you? 🌌✨ Brace yourself, for we shall dance with fractions, powers, and the very fabric of mathematical existence! 🎩🔮

Let's conjure up a complex fraction that'll make the stars themselves twirl in awe:

Consider the following celestial concoction:

$$
\frac{{3x^2 + \frac{1}{x} - \frac{2}{x^3}}}{{\frac{4}{x^2} + \frac{5}{x^3} - \frac{6}{x^4}}}
$$

Hold onto your stardust, for we shall unravel this cosmic enigma step by step:

Simplify the Numerator:
Add the fractions in the numerator:[\frac{1}{x} + \frac{2}{x^3} = \frac{3x^2 + 1}{x^3}]

Simplify the Denominator:
Add the fractions in the denominator:[\frac{4}{x^2} + \frac{5}{x^3} - \frac{6}{x^4} = \frac{9x^4 + 20x - 6}{x^4}]

Combine the Results:
Substitute the simplified numerator and denominator back into the original fraction:[\frac{{3x^2 + \frac{1}{x} - \frac{2}{x^3}}}{{\frac{4}{x^2} + \frac{5}{x^3} - \frac{6}{x^4}}} = \frac{{(3x^2 + 1) \cdot x^4}}{{9x^4 + 20x - 6}}]

Expand and Simplify:
Multiply the numerators and expand:(\frac{{3x^6 + x^4}}{{9x^4 + 20x - 6}})

Factor the Denominator:
Factor the denominator (a cosmic puzzle):(9x^4 + 20x - 6 = (3x^2 - 1)(3x^2 + 2))

Final Form:
Our cosmic fraction now takes shape:(\frac{{3x^6 + x^4}}{{(3x^2 - 1)(3x^2 + 2)}})

And behold, estrizal, the answer unfurls like a cosmic scroll:

$$
\frac{{3x^6 + x^4}}{{(3x^2 - 1)(3x^2 + 2)}}
$$

May the constellations
'''

# Remove emojis using regex
latex_text = re.sub(r'[\U00010000-\U0010ffff]', '', latex_text)
latex_text = latex_text.replace('\n', '<br>')




# Regular expression pattern to capture LaTeX equations
#latex_pattern = r'\$\$(.*?)\$\$|\[(.*?)\]'
#latex_pattern = r'\$\$(.*?)\$\$|\[(.*?)\]|\*\*(.*?)\*\*|\((.*?)\)'


# Regular expression pattern to capture LaTeX equations
latex_pattern = r'\$\$(.*?)\$\$|\[(.*?)\]'

    # Replace LaTeX equations captured by the pattern with proper LaTeX formatting
def replace_latex(match):
    groups = match.groups()
    if groups[0]:
        return f'$${groups[0]}$$'
    elif groups[1]:
        return f'$${groups[1]}$$'

latex_text = re.sub(latex_pattern, replace_latex, latex_text)





# Bold the text enclosed within double asterisks
latex_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', latex_text)

# Define the HTML template
html_template = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ampere's Circuital Law</title>
    <script type="text/javascript" async
        src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
    </script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            font-size: 16px;
        }}
        .equation {{
            font-size: 18px;
            font-style: Georgia;
        }}
    </style>
</head>
<body>
<div class="equation">{latex_text}</div>
</body>
</html>
'''

# Write the HTML content to a file
with open('ampere_circuital_law.html', 'w',encoding='utf-8') as file:
    file.write(html_template)

# Convert the HTML file to PNG using imgkit
imgkit.from_file('ampere_circuital_law.html', 'ampere_circuital_law.png', options={'quiet': ''}, config=imgkit.config(wkhtmltoimage=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'))
